#!/usr/bin/env python3
"""Fetch the full text of one or more pages from pb_docs.db.

search_db.py finds which document+page a keyword appears in; this script retrieves
the complete page text (function signatures, parameter lists, examples often
span several pages), so you can answer without re-opening any document.

Usage:
    python scripts/get_pages.py <filename> <start_page> [<end_page>]

- filename   : one of the document names stored in the index (e.g. "08_datawindow_reference")
- start_page : 1-based page number
- end_page   : optional; defaults to start_page

Run from the skill directory. Use PYTHONIOENCODING=utf-8 on Windows.
"""
import os
import sqlite3
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    name, start = sys.argv[1], int(sys.argv[2])
    end = int(sys.argv[3]) if len(sys.argv) > 3 else start

    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "references", "pb_docs.db"))
    conn = sqlite3.connect(db_path)

    rows = conn.execute(
        "SELECT page, text FROM pages WHERE filename = ? AND page BETWEEN ? AND ? "
        "ORDER BY page", (name, start, end)).fetchall()
    conn.close()

    if not rows:
        sys.exit(f"未找到 {name} 第 {start}-{end} 页（确认文件名和页码）")
    for page, text in rows:
        print(f"----- {name} 第 {page} 页 -----")
        print(text)
        print()


if __name__ == "__main__":
    main()