#!/usr/bin/env python3
"""Browse the PbIdea object inventory (references/pbidea_sources.txt.gz).

Use this when you don't know what components exist yet — it lists every
exported object grouped by library (pbl), with its type and a one-line Chinese
description extracted from the source comments. Filter by pbl or object type.

Usage:
    python scripts/list_objects.py                # everything, grouped by pbl
    python scripts/list_objects.py websuite       # only one pbl
    python scripts/list_objects.py --type 数据窗口 # only DataWindows
    python scripts/list_objects.py --name uo      # only objects whose name contains "uo"
"""
import argparse
import gzip
import os
import sys

# Windows 控制台默认 GBK:让 stdout/stderr 自行切到 UTF-8,调用方无需设
# PYTHONIOENCODING
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pbidea_sources.txt.gz"))


def load_records():
    if not os.path.isfile(ARCHIVE):
        sys.exit(f"Index not found: {ARCHIVE} — 技能包缺少 references/pbidea_sources.txt.gz")
    with gzip.open(ARCHIVE, "rt", encoding="utf-8") as f:
        raw = f.read()
    recs = []
    for blk in raw.split("\x1e")[1:]:
        head, _, _text = blk.partition("\n")
        fields = head.split("\x1f", 3) + [""]
        recs.append({"pbl": fields[0], "filename": fields[1],
                     "type": fields[2], "desc": fields[3]})
    return recs


def main():
    parser = argparse.ArgumentParser(description="Browse the pbidea object catalog")
    parser.add_argument("pbl", nargs="?", default=None,
                        help="only list objects in this library folder (e.g. websuite)")
    parser.add_argument("--type", default=None, help="object kind filter, e.g. 数据窗口 / 窗口 / 用户对象")
    parser.add_argument("--name", default=None, help="substring filter on object name")
    args = parser.parse_args()

    recs = load_records()
    if args.pbl:
        recs = [r for r in recs if r["pbl"] == args.pbl]
    if args.type:
        recs = [r for r in recs if r["type"] == args.type]
    if args.name:
        recs = [r for r in recs if args.name.casefold() in r["filename"].casefold()]

    if not recs:
        print("没有匹配的对象。")
        return

    current_pbl = None
    for r in recs:
        if r["pbl"] != current_pbl:
            current_pbl = r["pbl"]
            print(f"\n== {current_pbl} ==")
        line = f"  {r['filename']}  ({r['type']})"
        if r["desc"]:
            line += f"  — {r['desc']}"
        print(line)
    print()


if __name__ == "__main__":
    main()
