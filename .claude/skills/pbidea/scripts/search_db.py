#!/usr/bin/env python3
"""Full-text search over the PbIdea framework index (references/pbidea_sources.txt.gz).

The complete exported source of all 566 PbIdea objects ships as one
gzip-compressed archive and is scanned in memory. Substring matching means
Chinese comments ("获取节点值") and English function names ("Request") both
hit — no tokenizer, no sqlite, no third-party packages, only the stdlib.

Rules that matter:
- Multiple keywords are AND-ed together (narrowing the search).
- Matching is case-insensitive and matches anywhere in an object: source text,
  plus the pbl / object name / kind fields (like the old index did).
- Short Chinese keywords work fine (plain substring), no special cases.
- No boolean operators; widen or narrow by changing keywords.

Usage:
    python scripts/search_db.py Request
    python scripts/search_db.py "uo_json Parse"
    python scripts/search_db.py 获取 节点
    python scripts/search_db.py "httpclient 超时" --pages 2

Output: one line per hit — pbl/object, object type, text snippet. Add
--pages N to also print the complete source of the top N hits so you can
answer from the full object (function signatures, comments, constants) in one
call.
"""
import argparse
import gzip
import os
import sys

WIDTH = 40

# Map the Chinese kind stored in the index back to the PB export extension so
# the --pages headers read like real file names (matches get_object.py).
EXT = {"用户对象": "sru", "数据窗口": "srd", "窗口": "srw", "全局函数": "srf",
       "结构": "srs", "菜单": "srm", "工程": "srj", "应用": "sra"}

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pbidea_sources.txt.gz"))

# whitespace -> space, so snippet positions stay aligned with the original text
_WS = {ord(c): 32 for c in "\t\n\r\x0b\x0c"}


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
    for r in recs:  # folded copy keeps byte alignment with the original text
        r["folded"] = r["text"].translate(_WS).casefold()
        # the old index covered the pbl / filename / type columns too: a term
        # like "websuite" (pbl name) must hit even if it never appears in the
        # source text
        r["head"] = f"{r['pbl']} {r['filename']} {r['type']}".casefold()
    return recs


def make_snippet(text, terms):
    """A short window of text around the first keyword hit, with [brackets]."""
    low = text.lower()
    first = min((i for i in (low.find(t.lower()) for t in terms) if i != -1), default=None)
    if first is None:
        return text[: 2 * WIDTH].replace("\n", " ")
    start = max(0, first - WIDTH)
    end = min(len(text), first + WIDTH * 2)
    snip = text[start:end].replace("\n", " ")
    for t in sorted(terms, key=len, reverse=True):
        snip = snip.replace(t, f"[{t}]")
    return ("…" if start > 0 else "") + snip + ("…" if end < len(text) else "")


def main():
    parser = argparse.ArgumentParser(description="Full-text search over pbidea_sources.txt.gz")
    parser.add_argument("query", nargs="+", help="keywords (space-separated, AND-ed)")
    parser.add_argument("--limit", type=int, default=10, help="max hits to list (default 10, 0 = all)")
    parser.add_argument("--pages", type=int, default=0,
                        help="print full source of the top N hits (default 0 = snippets only)")
    args = parser.parse_args()

    terms = []
    for a in args.query:
        terms.extend(a.split())
    terms = [t.strip('"') for t in terms if t.strip('"')]
    if not terms:
        sys.exit("query is empty — give me keywords like: uo_json Parse")

    recs = load_records()
    fold_terms = [t.translate(_WS).casefold() for t in terms]

    hits = [r for r in recs
            if all(t in r["folded"] or t in r["head"] for t in fold_terms)]
    if not hits:
        print("无命中。换用更短或更典型的关键词再试（函数名、组件名、中文关键词，一次 1-3 个）。")
        return

    # Rank: object name matching a keyword first, then archive order.
    def name_matches(row):
        low_name = row["filename"].casefold()
        return sum(1 for t in fold_terms if t in low_name)

    hits.sort(key=lambda r: (-name_matches(r), r["rowid"]))

    shown = hits if args.limit == 0 else hits[:args.limit]
    for r in shown:
        print(f"{r['pbl']} / {r['filename']}  ({r['type']})")
        print(f"    {make_snippet(r['text'], terms)}")
        print()

    if args.pages > 0:
        print(f"===== 命中前 {args.pages} 个对象完整源码 =====")
        for r in shown[:args.pages]:
            ext = EXT.get(r["type"], r["type"])
            print(f"----- {r['pbl']} / {r['filename']}.{ext} -----")
            print(r["text"])
            print()


if __name__ == "__main__":
    main()
