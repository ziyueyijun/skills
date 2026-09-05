#!/usr/bin/env python3
"""Search the PowerBuilder documentation index (references/pb_pages.txt.gz).

Replacement for the old sqlite-FTS version: the complete documentation text
(6844 pages) ships as one gzip-compressed archive and is scanned in memory.
No tokenizer, no sqlite, no third-party packages — only the Python stdlib.

Matching mirrors what the old FTS5 (unicode61) index actually did:
- query words match whole tokens; underscore and punctuation split tokens, so
  'SetItem' does not hit inside 'SetItemStatus' or 'datawindow_reference';
- words and quoted phrases also match inside the document name / page number
  (the old index covered those columns too);
- CJK queries fall back to plain substring matching (superset of the old
  word-token behaviour, needed for Chinese keywords).

Query syntax (same as before):
    python scripts/search_db.py Modify
    python scripts/search_db.py "SetTransObject AND Retrieve" 20
    python scripts/search_db.py "DataWindow OR DataStore"
    python scripts/search_db.py '"datawindow reference"'        # exact phrase
Words separated by spaces (or explicit AND) are AND-ed, OR splits clauses,
quotes mark an exact phrase. Ranking: BM25 over the matched words plus an
idf-weighted phrase bonus, mirroring the previous FTS5 rank.

Output: one line per hit — document name, page number, and a text snippet.
Add --pages N to also print the full text of the top N hits in one call, so
you usually don't need a separate get_pages.py invocation.
"""
import argparse
import gzip
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pb_pages.txt.gz"))
BODY = os.path.normpath(os.path.join(HERE, "..", "references", "pb_pages.body.gz"))

K1, B = 1.2, 0.75  # BM25 parameters (same defaults as FTS5)

# one space between tokens: run of non-word chars (or underscore) collapses
_SEP = re.compile(r"[\W_]+")


def _collapse(s):
    return _SEP.sub(" ", s.casefold())


def load_records():
    """List of dicts: filename/page/text (raw, for output & snippets) plus
    'body' — a pre-tokenised lowercase copy of the text (one token per word,
    punctuation/underscore collapsed to spaces) for matching. The tokenised
    stream ships alongside the archive so loading stays fast."""
    for p in (ARCHIVE, BODY):
        if not os.path.isfile(p):
            sys.exit(f"Index not found: {p} — 技能包缺少索引文件，请检查交付是否完整")
    with gzip.open(ARCHIVE, "rt", encoding="utf-8") as f:
        raw = f.read()
    with gzip.open(BODY, "rt", encoding="utf-8") as f:
        raw_body = f.read()
    recs = []
    for blk, blk_b in zip(raw.split("\x1e")[1:], raw_body.split("\x1e")[1:]):
        head, _, text = blk.partition("\n")
        filename, _, page = head.partition("\x1f")
        _, _, body = blk_b.partition("\n")
        recs.append({"filename": filename, "page": int(page),
                     "text": text, "body": body, "rowid": len(recs)})
    for r in recs:
        r["hdr"] = _collapse(f"{r['filename']} {r['page']}")  # doc/page token stream
    return recs


def parse_clauses(query):
    """Parse the FTS-style query into AND-clauses separated by OR.

    A page matches when it matches ANY clause; a clause matches when ALL its
    words are present and its quoted phrase (if any) occurs. Each clause:
    {'words': [folded words], 'phrase': normalized phrase string|None}
    """
    tokens = re.findall(r'"[^"]*"|OR|AND|\w+', query)
    clauses = []
    for t in tokens:
        if t.upper() in ("AND", "OR"):
            continue
        if t.startswith('"'):
            phrase = " ".join(t[1:-1].split()).casefold()
            if not clauses or clauses[-1]["phrase"] is not None:
                clauses.append({"words": [], "phrase": None})
            clauses[-1]["phrase"] = phrase
        else:
            word = t.casefold()
            if not clauses:
                clauses.append({"words": [], "phrase": None})
            clauses[-1]["words"].append(word)
    return [c for c in clauses if c["words"] or c["phrase"]]


def word_pattern(word):
    """Matcher for a query word. ASCII identifier words match as whole tokens
    (like the old unicode61 tokenizer); CJK/mixed words are plain substrings."""
    esc = re.escape(word)
    if re.fullmatch(r"[0-9A-Za-z_]+", word):
        return re.compile(r"(?<![0-9A-Za-z])" + esc + r"(?![0-9A-Za-z])")
    return re.compile(esc)


def phrase_pattern(phrase):
    """Regex for a quoted phrase on the collapsed token space: the words must
    appear as consecutive tokens with single spaces between them."""
    words = re.findall(r"\w+", phrase)
    esc = [re.escape(w) for w in words]
    return re.compile(r"(?<![0-9A-Za-z])" + " ".join(esc) + r"(?![0-9A-Za-z])")


def make_snippet(text, terms, width=60):
    """Window of raw text around the first keyword hit, brackets around
    matched words. Matching is case-insensitive, whole-word for ASCII
    identifiers (so positions point at real words in the raw text)."""
    cand = []
    for t in terms:
        pat = _case_pat(t)
        cand.extend(m.start() for m in pat.finditer(text))
    if not cand:
        cand = [text.lower().find(t) for t in terms]
        cand = [p for p in cand if p != -1]
    first = min(cand) if cand else 0
    start = max(0, first - width)
    end = min(len(text), first + 3 * width)
    snip = text[start:end].replace("\n", " ")
    for t in sorted(set(terms), key=len, reverse=True):
        snip = _case_pat(t).sub(lambda m: "[" + m.group(0) + "]", snip)
    return ("…" if start > 0 else "") + snip + ("…" if end < len(text) else "")


def _case_pat(term):
    """Case-insensitive matcher of a term against raw text: whole-word for
    ASCII identifiers, plain substring otherwise."""
    if re.fullmatch(r"[0-9A-Za-z_]+", term):
        return re.compile(r"(?<![0-9A-Za-z])" + re.escape(term) + r"(?![0-9A-Za-z])",
                          re.IGNORECASE)
    return re.compile(re.escape(term), re.IGNORECASE)


def main():
    parser = argparse.ArgumentParser(description="Full-text search over pb_pages.txt.gz")
    parser.add_argument("query", help="words AND-ed; use OR / quotes for alternatives or exact phrases")
    parser.add_argument("limit", nargs="?", type=int, default=10,
                        help="max hits to list (default 10, 0 = all)")
    parser.add_argument("--pages", type=int, default=0,
                        help="print full text of the top N hits (default 0 = snippets only)")
    args = parser.parse_args()

    clauses = parse_clauses(args.query)
    if not clauses:
        sys.exit("query is empty — give me keywords like: SetTransObject AND Retrieve")

    recs = load_records()
    n_docs = len(recs)

    # ---- idf: document frequency of every word/phrase over the corpus ------
    words = sorted({w for c in clauses for w in c["words"]})
    pat = {w: word_pattern(w) for w in words}
    ph_pat = {c["phrase"]: phrase_pattern(c["phrase"])
              for c in clauses if c["phrase"]}

    if words:
        body_df = {w: sum(1 for r in recs if pat[w].search(r["body"]))
                   for w in words}
        hdr_df = {w: sum(1 for r in recs if pat[w].search(r["hdr"]))
                  for w in words}
        docfreq = {w: min(n_docs, body_df[w] + hdr_df[w]) for w in words}
    else:
        docfreq = {}
    idf = {w: math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
           for w, df in docfreq.items()}

    # phrase counts live on the collapsed body/header token streams
    def phrase_count(r, ph):
        return len(ph_pat[ph].findall(r["body"])) + (
            1 if ph in r["hdr"] else 0)

    if ph_pat:
        df_phrase = {ph: sum(1 for r in recs if phrase_count(r, ph) > 0)
                     for ph in ph_pat}
        idf_phrase = {ph: math.log(1 + (n_docs - df + 0.5) / (df + 0.5))
                      for ph, df in df_phrase.items()}
    else:
        df_phrase, idf_phrase = {}, {}
    avgdl = sum(len(r["body"]) for r in recs) / n_docs

    # ---- scan: BM25 over matched clauses -----------------------------------
    scored = []  # (score, rowid)
    for r in recs:
        body, hdr = r["body"], r["hdr"]
        score = 0.0
        matched = False
        for c in clauses:
            tf = []
            ok = True
            for w in c["words"]:
                n = len(pat[w].findall(body)) + len(pat[w].findall(hdr))
                if n == 0:
                    ok = False
                    break
                tf.append(n)
            if not ok:
                continue
            pn = phrase_count(r, c["phrase"]) if c["phrase"] is not None else 0
            if c["phrase"] is not None and pn == 0:
                continue
            matched = True
            denom = len(body)
            for w, t in zip(c["words"], tf):
                score += t * (K1 + 1) / (t + K1 * (1 - B + B * denom / avgdl)) * idf[w]
            if pn:
                score += (pn * (K1 + 1) / (pn + K1 * (1 - B + B * denom / avgdl))
                          * idf_phrase[c["phrase"]])
        if matched:
            scored.append((-score, r["rowid"]))
    scored.sort()
    ranked = [recs[i] for _, i in scored]

    if not ranked:
        print("无命中，换个关键词试试")
        return

    # ---- print -------------------------------------------------------------
    shown = ranked if args.limit == 0 else ranked[:args.limit]
    terms = [w for c in clauses for w in c["words"]]
    terms += [w for c in clauses if c["phrase"] for w in re.findall(r"\w+", c["phrase"])]
    for r in shown:
        print(f"{r['filename']}  p.{r['page']}")
        print(f"    {make_snippet(r['text'], terms)}")
        print()

    if args.pages > 0:
        print(f"===== 命中前 {args.pages} 页完整文本 =====")
        for r in shown[:args.pages]:
            print(f"----- {r['filename']} 第 {r['page']} 页 -----")
            print(r["text"])
            print()


if __name__ == "__main__":
    main()
