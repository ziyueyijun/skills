#!/usr/bin/env python3
"""Build the pbidea.db full-text index from the PbIdea exported source.

The PbIdea framework keeps its complete API in exported PowerBuilder source
files (code/): every user object, DataWindow, window, function and structure
is a text file whose prototypes block doubles as the API reference. This script
scans that folder and indexes every object's full text into a SQLite FTS5
database so the skill can search it in milliseconds.

The index uses the FTS5 *trigram* tokenizer, not the default unicode61 one:
unicode61 treats a contiguous run of CJK characters as a single token, so
Chinese comments ("获取节点值") can never be matched by a Chinese keyword.
Trigram indexes every 3-char substring, so both Chinese phrases and English
function names hit correctly.

Schema (mirrors the powerbuilder skill's pb_docs.db layout):
    objects      FTS5 virtual table (pbl, filename, type, text)   — searchable
    object_text  plain table (pbl, filename, type, text)          — full retrieval
    catalog      plain table (name, pbl, type, description)       — object inventory

Usage:
    python scripts/build_db.py --source <path/to/PbIdea/code>
    python scripts/build_db.py --source <path/to/PbIdea/code> --db references/pbidea.db
"""
import argparse
import os
import re
import sqlite3
import sys

# PB export files are GBK-encoded (Chinese Windows / classic PowerBuilder). Some
# may be plain ASCII or UTF-8; try in that order and fall back to latin-1.
ENCODINGS = ("utf-8", "gbk", "latin-1")

# Map PB export extension -> object kind (for the catalog / browsing).
TYPE_NAMES = {
    "sru": "用户对象",
    "srd": "数据窗口",
    "srw": "窗口",
    "srf": "全局函数",
    "srs": "结构",
    "srm": "菜单",
    "srj": "工程",
    "sra": "应用",
}

HEADER_RE = re.compile(r"^\$PBExportHeader\$.*$", re.MULTILINE)


def decode_file(path):
    """Read a PB export file and return (text, encoding_used)."""
    with open(path, "rb") as f:
        raw = f.read()
    for enc in ENCODINGS:
        try:
            return raw.decode(enc), enc
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("latin-1"), "latin-1"


def extract_description(text):
    """Best-effort one-line description of an object for the catalog.

    Priority: the bilingual `//cn:` comment inside the `type variables` block
    (uo_httpclient.sru literally documents itself as "基于winhttp的http client"
    there); otherwise the first `//` comment anywhere in the file.
    """
    m = re.search(r"type variables\s*(.*?)\s*end variables", text, re.S)
    block = m.group(1) if m else ""
    for pat in (r"//cn:\s*(.+)", r"//en:\s*(.+)"):
        cm = re.search(pat, block)
        if cm:
            return cm.group(1).strip()
    cm = re.search(r"^\s*//\s*(.+)$", text, re.MULTILINE)
    if cm:
        return cm.group(1).strip()
    return ""


def main():
    parser = argparse.ArgumentParser(description="Build pbidea.db from exported PB source")
    parser.add_argument("--source", required=True, help="path to the exported code/ folder")
    parser.add_argument("--db", default=os.path.join("references", "pbidea.db"),
                        help="output database path (default references/pbidea.db)")
    args = parser.parse_args()

    source = os.path.abspath(args.source)
    if not os.path.isdir(source):
        sys.exit(f"source not found: {source}")

    # Every subfolder of code/ is one PBL (pbjson.pbl, websuite.pbl, ...).
    pbl_dirs = sorted(d for d in os.listdir(source)
                      if os.path.isdir(os.path.join(source, d)))
    if not pbl_dirs:
        sys.exit(f"no PBL subfolders under {source}")

    db_path = os.path.abspath(args.db)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)  # rebuild from scratch so the index is always fresh

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=OFF")
    conn.execute("CREATE VIRTUAL TABLE objects USING fts5("
                 "pbl, filename, type, text, tokenize='trigram')")
    conn.execute("CREATE TABLE object_text (pbl TEXT, filename TEXT, type TEXT, text TEXT)")
    conn.execute("CREATE TABLE catalog (name TEXT, pbl TEXT, type TEXT, description TEXT)")

    total = 0
    enc_counts = {}
    type_counts = {}
    for pbl in pbl_dirs:
        pbl_dir = os.path.join(source, pbl)
        # Store the library name without the ".pbl" suffix (websuite.pbl -> websuite)
        # so filters and display read naturally.
        pbl_name = pbl[:-4] if pbl.endswith(".pbl") else pbl
        for name in sorted(os.listdir(pbl_dir)):
            path = os.path.join(pbl_dir, name)
            if not os.path.isfile(path):
                continue
            text, enc = decode_file(path)
            enc_counts[enc] = enc_counts.get(enc, 0) + 1
            # Normalize CRLF; drop the redundant $PBExportHeader$ first line.
            text = text.replace("\r\n", "\n").replace("\r", "\n")
            text = HEADER_RE.sub("", text, count=1).lstrip("\n")

            ext = name.rsplit(".", 1)[-1].lower()
            kind = TYPE_NAMES.get(ext, ext)
            type_counts[kind] = type_counts.get(kind, 0) + 1
            obj = name.rsplit(".", 1)[0]

            conn.execute("INSERT INTO objects(pbl, filename, type, text) VALUES (?,?,?,?)",
                         (pbl_name, obj, kind, text))
            conn.execute("INSERT INTO object_text(pbl, filename, type, text) VALUES (?,?,?,?)",
                         (pbl_name, obj, kind, text))
            desc = extract_description(text)
            conn.execute("INSERT INTO catalog(name, pbl, type, description) VALUES (?,?,?,?)",
                         (obj, pbl_name, kind, desc))
            total += 1

    # Human-readable object inventory for the skill to browse.
    conn.execute("CREATE INDEX idx_catalog_pbl ON catalog(pbl)")
    conn.execute("CREATE INDEX idx_catalog_name ON catalog(name)")
    conn.commit()

    print(f"indexed {total} objects into {db_path}")
    print("encodings:", enc_counts)
    print("types:", type_counts)
    print("pbls:", ", ".join(pbl_dirs))
    conn.close()


if __name__ == "__main__":
    main()