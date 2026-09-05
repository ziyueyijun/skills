#!/usr/bin/env python3
"""Search the PowerBuilder documentation SQLite index (references/pb_docs.db).

Finds pages containing the given keywords in a few milliseconds. The query is
passed straight to SQLite FTS5 MATCH syntax: multiple words are AND-ed by
default; use OR explicitly for alternatives; quote phrases for exact matches.

Usage:
    python scripts/search_db.py <query> [limit] [--pages N]

Examples:
    python scripts/search_db.py Modify
    python scripts/search_db.py "SetTransObject AND Retrieve"
    python scripts/search_db.py "DataWindow OR DataStore" 20
    python scripts/search_db.py SetTransObject 5 --pages 2

Output: one line per hit — document name, page number, and a text snippet.
Add --pages N to also print the full text of the top N hits in one call, so you
usually don't need a separate get_pages.py invocation.
"""
import argparse
import os
import sqlite3
import sys


def main():
    parser = argparse.ArgumentParser(description="Full-text search over pb_docs.db")
    parser.add_argument("query", help="FTS5 MATCH query (words AND-ed; use OR / quotes)")
    parser.add_argument("limit", nargs="?", type=int, default=10, help="max hits to list")
    parser.add_argument("--pages", type=int, default=0,
                        help="print full text of the top N hits (default 0 = snippets only)")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "references", "pb_docs.db"))
    if not os.path.isfile(db_path):
        sys.exit(f"Index not found: {db_path} — 技能包缺少 references/pb_docs.db，请检查交付是否完整")

    conn = sqlite3.connect(db_path)
    try:
        rows = conn.execute(
            "SELECT filename, page, snippet(docs, 2, '[', ']', '…', 60) "
            "FROM docs WHERE docs MATCH ? ORDER BY rank LIMIT ?",
            (args.query, args.limit)).fetchall()
    except sqlite3.OperationalError as e:
        sys.exit(f"FTS query error: {e}")

    if not rows:
        print("无命中，换个关键词试试")
        conn.close()
        return

    for filename, page, snip in rows:
        print(f"{filename}  p.{page}")
        print(f"    …{snip}…")
        print()

    if args.pages > 0:
        print(f"===== 命中前 {args.pages} 页完整文本 =====")
        for filename, page, _ in rows[:args.pages]:
            text = conn.execute(
                "SELECT text FROM pages WHERE filename=? AND page=?",
                (filename, page)).fetchone()
            if text:
                print(f"----- {filename} 第 {page} 页 -----")
                print(text[0])
                print()
    conn.close()


if __name__ == "__main__":
    main()