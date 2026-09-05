#!/usr/bin/env python3
"""Browse the PbIdea object inventory (catalog table in references/pbidea.db).

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
import os
import sqlite3


def main():
    parser = argparse.ArgumentParser(description="Browse the pbidea.db object catalog")
    parser.add_argument("pbl", nargs="?", default=None,
                        help="only list objects in this library folder (e.g. websuite)")
    parser.add_argument("--type", default=None, help="object kind filter, e.g. 数据窗口 / 窗口 / 用户对象")
    parser.add_argument("--name", default=None, help="substring filter on object name")
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.normpath(os.path.join(here, "..", "references", "pbidea.db"))
    conn = sqlite3.connect(db_path)

    sql = "SELECT name, pbl, type, description FROM catalog"
    conds, params = [], []
    if args.pbl:
        conds.append("pbl = ?")
        params.append(args.pbl)
    if args.type:
        conds.append("type = ?")
        params.append(args.type)
    if args.name:
        conds.append("name LIKE ?")
        params.append(f"%{args.name}%")
    if conds:
        sql += " WHERE " + " AND ".join(conds)
    sql += " ORDER BY pbl, name"

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        print("没有匹配的对象。")
        return

    current_pbl = None
    for name, pbl, kind, desc in rows:
        if pbl != current_pbl:
            current_pbl = pbl
            print(f"\n== {pbl} ==")
        line = f"  {name}  ({kind})"
        if desc:
            line += f"  — {desc}"
        print(line)
    print()


if __name__ == "__main__":
    main()