#!/usr/bin/env python3
"""Build references/pbidea_sources.txt.gz from the PbIdea exported source.

The PbIdea framework keeps its complete API in exported PowerBuilder source
files (code/): every user object, DataWindow, window, function and structure
is a text file whose prototypes block doubles as the API reference. This script
scans that folder and packs every object's full text (plus a one-line
description extracted from the source comments) into one gzip archive that the
skill's search/get/list scripts read directly — no database, no index, no
third-party packages.

Usage:
    python scripts/build_archive.py --source <path/to/PbIdea/code>
    python scripts/build_archive.py --source <path/to/PbIdea/code> \
        --out references/pbidea_sources.txt.gz
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
    """Best-effort one-line description of an object.

    Priority: the bilingual `//cn:`/`//en:` comment inside the `type variables`
    block (uo_httpclient.sru literally documents itself as "基于winhttp的http
    client" there); then the same tags anywhere in the file; finally the first
    plain comment line that does not read like commented-out code — the old
    fallback grabbed lines such as "//MessageBox(...)" verbatim.
    """
    m = re.search(r"type variables\s*(.*?)\s*end variables", text, re.S)
    block = m.group(1) if m else ""
    for cm in re.finditer(r"//(?:cn|en):\s*(.+)", block, re.I):
        desc = cm.group(1).strip()
        if desc:
            return desc
    for cm in re.finditer(r"//(?:cn|en):\s*(.+)", text, re.I):
        desc = cm.group(1).strip()
        if desc:
            return desc
    for cm in re.finditer(r"^\s*//\s*(.+)$", text, re.MULTILINE):
        desc = cm.group(1).strip()
        if desc and not _looks_like_code(desc):
            return desc
    return ""


def _looks_like_code(desc):
    """True when a // line is commented-out code, not prose description.

    Heuristic on the line right after "//": starts with an identifier followed
    by "(" (a call like "MessageBox(...)"), or contains an assignment or ends
    with ";" (e.g. "BorderColor = RGB(200,120,60)").
    """
    return bool(re.search(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*\s*\(|\s*=\s*|;$", desc))


def main():
    parser = argparse.ArgumentParser(description="Build pbidea_sources.txt.gz from exported PB source")
    parser.add_argument("--source", required=True, help="path to the exported code/ folder")
    parser.add_argument("--out", default=os.path.join("references", "pbidea_sources.txt.gz"),
                        help="output archive path (default references/pbidea_sources.txt.gz)")
    args = parser.parse_args()

    source = os.path.abspath(args.source)
    if not os.path.isdir(source):
        raise SystemExit(f"source not found: {source}")

    # Every subfolder of code/ is one PBL (pbjson.pbl, websuite.pbl, ...).
    pbl_dirs = sorted(d for d in os.listdir(source)
                      if os.path.isdir(os.path.join(source, d)))
    if not pbl_dirs:
        raise SystemExit(f"no PBL subfolders under {source}")

    out_path = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    total = 0
    enc_counts = {}
    type_counts = {}
    with gzip.open(out_path, "wt", encoding="utf-8", compresslevel=9, newline="\n") as f:
        for pbl in pbl_dirs:
            pbl_dir = os.path.join(source, pbl)
            # Store the library name without the ".pbl" suffix (websuite.pbl -> websuite)
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
                desc = extract_description(text)

                assert "\x1e" not in text and "\x1f" not in text
                assert "\x1f" not in desc
                f.write("\x1e" + f"{pbl_name}\x1f{obj}\x1f{kind}\x1f{desc}" + "\n")
                f.write(text + "\n")
                total += 1

    print(f"packed {total} objects into {out_path}")
    print("encodings:", enc_counts)
    print("types:", type_counts)
    print("pbls:", ", ".join(pbl_dirs))


if __name__ == "__main__":
    main()
