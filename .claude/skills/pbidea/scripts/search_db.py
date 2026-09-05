#!/usr/bin/env python3
"""Full-text search over the PbIdea framework index (references/pbidea.db).

Finds the exported PB objects (uo_*, d_*, w_*, nvo_*, ...) whose source
contains the given keywords. The index uses the FTS5 trigram tokenizer, which
matches substrings — so Chinese comments ("获取节点值") and English function
names ("Request") both hit, unlike the unicode61 tokenizer used for the English
PowerBuilder docs.

Rules that matter:
- Terms of 3+ characters run as a trigram MATCH (fast, indexed).
- Terms of 1-2 characters use LIKE (still served by the trigram index).
- Multiple keywords are AND-ed together (narrowing the search). Boolean
  operators (AND/OR) are NOT supported — the trigram tokenizer can't do them.
- Put the whole query in quotes if it contains spaces, or just list the words.

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
import os
import sqlite3
import sys

WIDTH = 40

# Map the Chinese kind stored in the index back to the PB export extension so
# the --pages headers read like real file names (matches get_object.py).
EXT = {"用户对象": "sru", "数据窗口": "srd", "窗口": "srw", "全局函数": "srf",
       "结构": "srs", "菜单": "srm", "工程": "srj", "应用": "sra"}


def find_term_positions(text, terms):
    """Return the byte/char offset of the first occurrence of each term."""
    low = text.lower()
    pos = []
    for t in terms:
        i = low.find(t.lower())
        pos.append(i)
    return pos


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
    parser = argparse.ArgumentParser(description="Full-text search over pbidea.db")
    parser.add_argument("query", nargs="+", help="keywords (space-separated, AND-ed)")
    parser.add_argument("--limit", type=int, default=10, help="max hits to list (default 10)")
    parser.add_argument("--pages", type=int, default=0,
                        help="print full source of the top N hits (default 0 = snippets only)")
    args = parser.parse_args()

    # nargs="+" keeps a quoted query ("uo_json Set") as ONE argv element, so
    # split every element on whitespace to get the keyword list either way.
    terms = []
    for a in args.query:
        terms.extend(a.split())
    terms = [t.strip('"') for t in terms if t.strip('"')]
    if not terms:
        sys.exit("query is empty — give me keywords like: uo_json Parse")

    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "references", "pbidea.db"))
    if not os.path.isfile(db_path):
        sys.exit(f"Index not found: {db_path} — 技能包缺少 references/pbidea.db，请先运行 build_db.py 或检查交付")

    conn = sqlite3.connect(db_path)
    try:
        # Each keyword becomes a condition; 3+ chars -> trigram MATCH, shorter
        # -> LIKE (also index-backed). Conditions are AND-ed.
        conds, params = [], []
        for t in terms:
            if len(t) >= 3:
                conds.append("objects MATCH ?")
                params.append('"' + t.replace('"', '""') + '"')
            else:
                conds.append("(filename LIKE ? OR pbl LIKE ? OR text LIKE ?)")
                params.extend([f"%{t}%"] * 3)
        sql = ("SELECT rowid, pbl, filename, type, text FROM objects WHERE "
               + " AND ".join(conds))
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError as e:
        conn.close()
        sys.exit(f"query error: {e}")

    if not rows:
        print("无命中。换用更短或更典型的关键词再试（函数名、组件名、中文关键词，一次 1-3 个）。")
        conn.close()
        return

    # Rank: object name matching a keyword first, then insertion order.
    def name_matches(row):
        return sum(1 for t in terms if t.lower() in row[2].lower())

    rows.sort(key=lambda r: (-name_matches(r), r[0]))

    for rowid, pbl, filename, kind, text in rows[:args.limit]:
        print(f"{pbl} / {filename}  ({kind})")
        print(f"    {make_snippet(text, terms)}")
        print()

    if args.pages > 0:
        print(f"===== 命中前 {args.pages} 个对象完整源码 =====")
        for rowid, pbl, filename, kind, text in rows[:args.pages]:
            ext = EXT.get(kind, kind)
            print(f"----- {pbl} / {filename}.{ext} -----")
            print(text)
            print()
    conn.close()


if __name__ == "__main__":
    main()