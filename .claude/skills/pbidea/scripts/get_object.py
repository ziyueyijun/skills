#!/usr/bin/env python3
"""Fetch the complete exported source of one or more PbIdea objects.

search_db.py finds which object a keyword lives in; this script retrieves the
whole object source (external function prototypes, Chinese comments, constants,
event scripts) so you can answer from the full API surface without re-opening
any file.

Usage:
    python scripts/get_object.py <name> [pbl]

- name : object name, substring match (e.g. "uo_json", "uo_datawindowex")
- pbl  : optional library filter if several libraries contain the name

Run from the skill directory. The scripts switch stdout/stderr to UTF-8
themselves, so no PYTHONIOENCODING is needed on Windows.
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

HERE = os.path.dirname(os.path.abspath(__file__))
ARCHIVE = os.path.normpath(os.path.join(HERE, "..", "references", "pbidea_sources.txt.gz"))

# Map the Chinese kind stored in the index back to the PB export extension
# (用户对象 -> sru) so headers read like real file names.
EXT = {"用户对象": "sru", "数据窗口": "srd", "窗口": "srw", "全局函数": "srf",
       "结构": "srs", "菜单": "srm", "工程": "srj", "应用": "sra"}

# DataWindow exports carry painter attributes (coordinates, fonts, colors)
# that are useless for API answers; strip them when printing. The index and
# search matching are untouched.
_LAYOUT_ATTR = re.compile(
    r'\s(?:x|y|width|height|font\.[a-z.]+|color|background\.[a-z.]+|'
    r'border)="(?:[^"]|"")*"')


def strip_layout(text, kind):
    if kind != "数据窗口":
        return text
    return _LAYOUT_ATTR.sub("", text)


def load_records():
    if not os.path.isfile(ARCHIVE):
        sys.exit(f"Index not found: {ARCHIVE} — 技能包缺少 references/pbidea_sources.txt.gz")
    with gzip.open(ARCHIVE, "rt", encoding="utf-8") as f:
        raw = f.read()
    recs = []
    for blk in raw.split("\x1e")[1:]:
        head, _, text = blk.partition("\n")
        fields = head.split("\x1f", 3) + [""]
        recs.append({"pbl": fields[0], "filename": fields[1], "type": fields[2], "text": text})
    return recs


def main():
    parser = argparse.ArgumentParser(description="Print one or more PbIdea object sources")
    parser.add_argument("name", help="object name substring, e.g. uo_json")
    parser.add_argument("pbl", nargs="?", help="restrict to this library when names collide")
    args = parser.parse_args()

    recs = load_records()
    wanted = args.name.casefold()
    rows = [r for r in recs if wanted in r["filename"].casefold()]
    if args.pbl:
        rows = [r for r in rows if r["pbl"].casefold() == args.pbl.casefold()]

    if not rows:
        sys.exit(f"未找到对象名含「{args.name}」的源码（可用 search_db.py 按关键词检索，或 list_objects.py 浏览清单）")
    for r in rows:
        ext = EXT.get(r["type"], r["type"])
        print(f"===== {r['pbl']} / {r['filename']}.{ext} =====")
        print(strip_layout(r["text"], r["type"]))
        print()


if __name__ == "__main__":
    main()
