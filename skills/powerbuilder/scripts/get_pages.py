#!/usr/bin/env python3
"""Print full text of specific documentation pages (references/pb_pages.txt.gz).

Usage:
    python scripts/get_pages.py 08_datawindow_reference 760 765

Prints every page of that document whose number lies in [start, end],
including both ends.
"""
import argparse
import gzip
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pb_pages.txt.gz"))


def load_records():
    if not os.path.isfile(ARCHIVE):
        sys.exit(f"Index not found: {ARCHIVE} — 技能包缺少 references/pb_pages.txt.gz")
    with gzip.open(ARCHIVE, "rt", encoding="utf-8") as f:
        raw = f.read()
    recs = []
    for blk in raw.split("\x1e")[1:]:
        head, _, text = blk.partition("\n")
        filename, _, page = head.partition("\x1f")
        recs.append({"filename": filename, "page": int(page), "text": text})
    return recs


def main():
    parser = argparse.ArgumentParser(description="Print documentation pages by range")
    parser.add_argument("filename", help="document name as shown by search_db.py")
    parser.add_argument("start", type=int, help="first page number")
    parser.add_argument("end", type=int, help="last page number (inclusive)")
    args = parser.parse_args()

    recs = load_records()
    pool = [r for r in recs
            if r["filename"] == args.filename and args.start <= r["page"] <= args.end]
    if not pool:
        sys.exit(f"未找到 {args.filename} 第 {args.start}-{args.end} 页，检查文件名与页码")
    pool.sort(key=lambda r: r["page"])
    for r in pool:
        print(f"----- {r['filename']} 第 {r['page']} 页 -----")
        print(r["text"])
        print()


if __name__ == "__main__":
    main()
