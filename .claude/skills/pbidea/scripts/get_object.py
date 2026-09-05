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

Run from the skill directory. Use PYTHONIOENCODING=utf-8 on Windows.
"""
import os
import sqlite3
import sys


# Map the Chinese kind stored in the index back to the PB export extension
# (用户对象 -> sru) so headers read like real file names.
EXT = {"用户对象": "sru", "数据窗口": "srd", "窗口": "srw", "全局函数": "srf",
       "结构": "srs", "菜单": "srm", "工程": "srj", "应用": "sra"}

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    name = sys.argv[1]
    pbl = sys.argv[2] if len(sys.argv) > 2 else None

    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "references", "pbidea.db"))
    conn = sqlite3.connect(db_path)

    if pbl:
        rows = conn.execute(
            "SELECT pbl, filename, type, text FROM object_text "
            "WHERE filename LIKE ? AND pbl = ? ORDER BY pbl, filename",
            (f"%{name}%", pbl)).fetchall()
    else:
        rows = conn.execute(
            "SELECT pbl, filename, type, text FROM object_text "
            "WHERE filename LIKE ? ORDER BY pbl, filename",
            (f"%{name}%",)).fetchall()
    conn.close()

    if not rows:
        sys.exit(f"未找到对象名含「{name}」的源码（可用 search_db.py 按关键词检索，或 list_objects.py 浏览清单）")
    for pbl_name, filename, kind, text in rows:
        ext = EXT.get(kind, kind)
        print(f"===== {pbl_name} / {filename}.{ext} =====")
        print(text)
        print()


if __name__ == "__main__":
    main()