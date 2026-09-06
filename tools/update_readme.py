#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 README.md(英文)与 README.zh-CN.md(中文)的技能表(标记区间)。

数据源:.claude/skills/*/SKILL.md 的 frontmatter(name/description/disable-model-invocation);
中文说明:tools/skill-desc-zh.json(缺失回退英文 frontmatter);
手动触发表行序:MANUAL_ORDER(工作流顺序,非字母序),未列入的新技能自动排在末尾。

用法:python tools/update_readme.py(在仓库根目录运行)
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / ".claude" / "skills"

# 手动触发技能的行序(README 展示顺序,工作流顺序);不在列表中的新增技能自动排在末尾(按名称)
MANUAL_ORDER = [
    "ask-matt",
    "setup-matt-pocock-skills",
    "setup-ts-deep-modules",
    "wayfinder",
    "grill-me",
    "grill-with-docs",
    "to-spec",
    "to-tickets",
    "implement",
    "handoff",
    "triage",
    "improve-codebase-architecture",
]

# 技能说明中文映射;缺失时回退 frontmatter 英文描述
DESC_ZH = ROOT / "tools" / "skill-desc-zh.json"

MARK_START = "<!-- skills-table:start -->"
MARK_END = "<!-- skills-table:end -->"

# (目标文件, 语言)
TARGETS = [
    (ROOT / "README.md", "en"),
    (ROOT / "README.zh-CN.md", "zh"),
]

HEADINGS = {
    "en": (
        "### Manual-invoked (requires `/skill-name` or explicit request; no cost unless invoked)",
        "### Auto-invoked (model calls when relevant)",
    ),
    "zh": (
        "### 手动触发(需 `/技能名` 或显式点名;不主动调用即零开销)",
        "### 自动触发(模型按需调用)",
    ),
}

TABLE_HEADERS = {
    "en": "| Skill | Description |",
    "zh": "| 技能 | 说明 |",
}

SEP_LINE = "|------|------|"


# YAML 块标量指示符(`description: >-` 折叠 / `|` 字面);表格单元格只取裁剪前缀,统一以空格拼接续行
BLOCK_INDICATORS = {">", ">-", ">+", "|", "|-", "|+"}


def frontmatter_of(skill_md: pathlib.Path) -> dict:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^---\n(.*?)\n---", text, re.S | re.M)
    fm = m.group(1) if m else ""
    lines = fm.splitlines()
    result = {}
    for key in ("name", "description", "disable-model-invocation"):
        for i, line in enumerate(lines):
            km = re.match(rf"^{key}:\s*(.*)$", line)
            if not km:
                continue
            value = km.group(1).strip()
            if key == "disable-model-invocation":
                result[key] = value == "true"
            elif value in BLOCK_INDICATORS:
                parts = []
                for nxt in lines[i + 1 :]:
                    if nxt[:1] in (" ", "\t") and nxt.strip():
                        parts.append(nxt.strip())
                    elif not nxt.strip():  # 块内空行(段落分隔)跳过
                        continue
                    else:
                        break
                result[key] = " ".join(parts)
            else:
                result[key] = value.strip('"').strip("'")
            break
    return result


def clip(text: str, limit: int = 72) -> str:
    text = text.replace("|", "\\|").strip()
    if len(text) > limit:
        return text[:limit].rstrip() + "…"
    return text


def collect_rows() -> list:
    rows = []
    desc_zh = {}
    if DESC_ZH.exists():
        desc_zh = json.loads(DESC_ZH.read_text(encoding="utf-8"))
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        fm = frontmatter_of(md)
        name = fm.get("name") or skill_dir.name
        desc_en = clip(fm.get("description", ""))
        desc_zh_text = clip(desc_zh.get(name) or fm.get("description", ""))
        rows.append(
            {
                "name": name,
                "desc_en": desc_en,
                "desc_zh": desc_zh_text,
                "manual": fm.get("disable-model-invocation", False),
            }
        )
    return rows


def row_line(name: str, desc: str) -> str:
    return f"| `{name}` | {desc} |"


def render_table(rows: list, lang: str) -> str:
    lines = [TABLE_HEADERS[lang], SEP_LINE]
    lines.extend(row_line(r["name"], r[f"desc_{lang}"]) for r in rows)
    return "\n".join(lines)


def update_file(path: pathlib.Path, rows: list, lang: str) -> int:
    if not path.exists():
        print(f"未找到 {path.name}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    if MARK_START not in text or MARK_END not in text:
        print(f"{path.name} 缺少技能表标记", file=sys.stderr)
        return 1

    auto = sorted((r for r in rows if not r["manual"]), key=lambda r: r["name"])
    order_index = {name: i for i, name in enumerate(MANUAL_ORDER)}
    manual = sorted(
        (r for r in rows if r["manual"]),
        key=lambda r: (order_index.get(r["name"], len(MANUAL_ORDER)), r["name"]),
    )
    h_manual, h_auto = HEADINGS[lang]
    block = "\n\n".join(
        [
            h_manual,
            render_table(manual, lang),
            h_auto,
            render_table(auto, lang),
        ]
    )
    new_text = re.sub(
        re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
        MARK_START + "\n" + block + "\n" + MARK_END,
        text,
        flags=re.S,
    )
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.name}:自动 {len(auto)} 行 + 手动 {len(manual)} 行")
    return 0


def main() -> int:
    rows = collect_rows()
    for path, lang in TARGETS:
        if update_file(path, rows, lang) != 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
