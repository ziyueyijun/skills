#!/usr/bin/env python3
"""Full-text search over the PbIdea framework index (references/pbidea_sources.txt.gz).

The complete exported source of all 566 PbIdea objects ships as one
gzip-compressed archive and is scanned in memory. Substring matching means
Chinese comments ("获取节点值") and English function names ("Request") both
hit — no tokenizer, no sqlite, no third-party packages, only the stdlib.

Rules that matter:
- Words are AND-ed together (narrowing the search); explicit AND is optional.
- OR between words splits alternatives: an object hits when any clause matches.
- "..." marks an exact phrase: its words must appear consecutively (any
  whitespace between them — they may even sit on different lines).
- Matching is case-insensitive and matches anywhere in an object: source text,
  plus the pbl / object name / kind fields (like the old index did).
- Short Chinese keywords work fine (plain substring), no special cases.

Usage:
    python scripts/search_db.py Request
    python scripts/search_db.py "uo_json Parse"
    python scripts/search_db.py 获取 节点
    python scripts/search_db.py "curl OR httpclient 超时"
    python scripts/search_db.py '"datawindow child"' --pages 2

Output: one line per hit — pbl/object, object type, text snippet. Add
--pages N to also print the complete source of the top N hits so you can
answer from the full object (function signatures, comments, constants) in one
call.
"""
import argparse
import gzip
import os
import re
import sys

# Windows 控制台默认 GBK:让 stdout/stderr 自行切到 UTF-8,调用方无需设
# PYTHONIOENCODING
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

WIDTH = 60

# Map the Chinese kind stored in the index back to the PB export extension so
# the --pages headers read like real file names (matches get_object.py).
EXT = {"用户对象": "sru", "数据窗口": "srd", "窗口": "srw", "全局函数": "srf",
       "结构": "srs", "菜单": "srm", "工程": "srj", "应用": "sra"}

# DataWindow exports carry painter attributes (coordinates, fonts, colors)
# that are useless for API answers; strip them when printing full objects.
# The index and search matching are untouched.
_LAYOUT_ATTR = re.compile(
    r'\s(?:x|y|width|height|font\.[a-z.]+|color|background\.[a-z.]+|'
    r'border)="(?:[^"]|"")*"')


def strip_layout(text, kind):
    if kind != "数据窗口":
        return text
    return _LAYOUT_ATTR.sub("", text)

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pbidea_sources.txt.gz"))

def load_records():
    """Return list of dicts: pbl/filename/type/text (+ folded copies)."""
    if not os.path.isfile(ARCHIVE):
        sys.exit(f"Index not found: {ARCHIVE} — 技能包缺少 references/pbidea_sources.txt.gz，请检查交付是否完整")
    with gzip.open(ARCHIVE, "rt", encoding="utf-8") as f:
        raw = f.read()
    recs = []
    for blk in raw.split("\x1e")[1:]:
        head, _, text = blk.partition("\n")
        fields = head.split("\x1f", 3) + [""]
        recs.append({"pbl": fields[0], "filename": fields[1], "type": fields[2],
                     "text": text, "rowid": len(recs)})
    for r in recs:  # match against the pbl / filename / type columns too: a
        # term like "websuite" (pbl name) must hit even if it never appears in
        # the source text
        r["head"] = f"{r['pbl']} {r['filename']} {r['type']}"
    return recs


def make_snippet(text, terms):
    """A window of raw text around the first keyword hit, with [brackets].

    The window is larger after the hit than before it; when the window does not
    start at a line boundary, it snaps forward to the next line break (within
    the budget) so snippets do not cut words in half.
    """
    low = text.lower()
    first = min((i for i in (low.find(t.lower()) for t in terms) if i != -1), default=None)
    if first is None:
        return text[: 3 * WIDTH].replace("\n", " ")
    start = max(0, first - WIDTH)
    if start > 0:
        nl = text.rfind("\n", 0, start)
        if nl != -1 and start - nl < WIDTH:
            start = nl + 1
    end = min(len(text), first + 3 * WIDTH)
    snip = text[start:end].replace("\n", " ")
    for t in sorted(terms, key=len, reverse=True):
        snip = snip.replace(t, f"[{t}]")
    return ("…" if start > 0 else "") + snip + ("…" if end < len(text) else "")


def parse_clauses(query_args):
    """Split the query into OR-separated clauses of AND-ed terms.

    Returns clauses, each a list of terms; a term is ("w", word) for a plain
    keyword or ("p", [words]) for a quoted phrase. A record matches when any
    clause matches, and a clause matches when every one of its terms does.
    """
    tokens = re.findall(r'"[^"]*"|OR|AND|\S+', " ".join(query_args))
    clauses, cur = [], None
    for tok in tokens:
        if tok.upper() == "OR":
            cur = None
        elif tok.upper() == "AND":
            continue
        elif tok.startswith('"') and len(tok) >= 2:
            words = tok[1:-1].split()
            if not words:
                continue
            if cur is None:
                clauses.append([])
                cur = clauses[-1]
            cur.append(("p", words))
        else:
            if cur is None:
                clauses.append([])
                cur = clauses[-1]
            cur.append(("w", tok))
    return [c for c in clauses if c]


def term_pattern(term):
    """Matcher for one parsed term: case-insensitive substring for a word,
    words joined by flexible whitespace for a quoted phrase."""
    kind, val = term
    if kind == "w":
        return re.compile(re.escape(val), re.I)
    return re.compile(r"\s+".join(re.escape(w) for w in val), re.I)


def main():
    parser = argparse.ArgumentParser(description="Full-text search over pbidea_sources.txt.gz")
    parser.add_argument("query", nargs="+",
                        help='keywords AND-ed; "OR" splits alternatives; "..." is an exact phrase')
    parser.add_argument("--limit", type=int, default=10, help="max hits to list (default 10, 0 = all)")
    parser.add_argument("--pages", type=int, default=0,
                        help="print full source of the top N hits (default 0 = snippets only)")
    args = parser.parse_args()

    clauses = parse_clauses(args.query)
    if not clauses:
        sys.exit("query is empty — give me keywords like: uo_json Parse")

    # Case-insensitive substring match straight on the raw text: query tokens
    # never contain whitespace, so no whitespace-folded copy is needed — and
    # str.translate over CJK text is slow (it dominated the load time).
    compiled = [[term_pattern(t) for t in clause] for clause in clauses]

    recs = load_records()
    hits = [r for r in recs if any(
        all(p.search(r["text"]) or p.search(r["head"]) for p in clause)
        for clause in compiled)]
    if not hits:
        print("无命中。换用更短或更典型的关键词再试（函数名、组件名、中文关键词，一次 1-3 个）。")
        return

    # Rank: object name matching a keyword first, then archive order.
    def name_matches(row):
        return sum(1 for clause in compiled for p in clause
                   if p.search(row["filename"]))

    hits.sort(key=lambda r: (-name_matches(r), r["rowid"]))

    # words of every clause (phrase words included) drive snippet centering
    snip_terms = [w for clause in clauses for kind, val in clause
                  for w in (val if kind == "p" else [val])]
    shown = hits if args.limit == 0 else hits[:args.limit]
    for r in shown:
        print(f"{r['pbl']} / {r['filename']}  ({r['type']})")
        print(f"    {make_snippet(r['text'], snip_terms)}")
        print()

    if args.pages > 0:
        print(f"===== 命中前 {args.pages} 个对象完整源码 =====")
        for r in shown[:args.pages]:
            ext = EXT.get(r["type"], r["type"])
            print(f"----- {r['pbl']} / {r['filename']}.{ext} -----")
            print(strip_layout(r["text"], r["type"]))
            print()


if __name__ == "__main__":
    main()
