#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重生成 README.md 的技能表(skills-table 标记区间),供 tools/sync-skills.sh 调用。

数据源:skills/*/SKILL.md 的 frontmatter(name/description);
上游来源:skills-lock.json(name -> source),人工覆盖表 OVERRIDE 处理未在锁文件中的技能。
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"
LOCK = ROOT / "skills-lock.json"

# 不在 skills-lock.json 中(如插件来源/手工收录)时的来源标注
OVERRIDE = {
    "frontend-design": "anthropics/skills",
}

# 技能说明中文映射;缺失时回退 frontmatter 英文描述
DESC_ZH = ROOT / "tools" / "skill-desc-zh.json"

MARK_START = "<!-- skills-table:start -->"
MARK_END = "<!-- skills-table:end -->"


def frontmatter_of(skill_md: pathlib.Path) -> dict:
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"^---\n(.*?)\n---", text, re.S | re.M)
    fm = m.group(1) if m else ""
    result = {}
    for key in ("name", "description", "disable-model-invocation"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.M)
        if km:
            value = km.group(1).strip()
            if key == "disable-model-invocation":
                result[key] = value == "true"
            else:
                result[key] = value.strip('"').strip("'")
    return result


def load_sources() -> dict:
    sources = {}
    if LOCK.exists():
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
        for name, meta in lock.get("skills", {}).items():
            sources[name] = meta.get("source", "")
    return sources


def collect_rows() -> list:
    rows = []
    sources = load_sources()
    desc_zh = {}
    if DESC_ZH.exists():
        desc_zh = json.loads(DESC_ZH.read_text(encoding="utf-8"))
    for skill_dir in sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir()):
        md = skill_dir / "SKILL.md"
        if not md.exists():
            continue
        fm = frontmatter_of(md)
        name = fm.get("name") or skill_dir.name
        desc = desc_zh.get(name) or fm.get("description", "").replace("|", "\\|").strip()
        if len(desc) > 72:
            desc = desc[:72].rstrip() + "…"
        source = OVERRIDE.get(name) or sources.get(name, "")
        rows.append(
            (name, desc, source, fm.get("disable-model-invocation", False))
        )
    return rows


def row_line(name: str, desc: str, source: str) -> str:
    if source:
        cell = f"[{source}](https://github.com/{source})"
    else:
        cell = "本仓库自建"
    return f"| `{name}` | {desc} | {cell} |"


def render_table(rows: list) -> str:
    lines = [
        "| 技能 | 说明 | 上游来源 |",
        "|------|------|----------|",
    ]
    lines.extend(row_line(n, d, s) for n, d, s in rows)
    return "\n".join(lines)


def main() -> int:
    if not README.exists():
        print("未找到 README.md", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    if MARK_START not in text or MARK_END not in text:
        print("README.md 缺少技能表标记,请先添加", file=sys.stderr)
        return 1

    rows = collect_rows()
    auto = sorted((r for r in rows if not r[3]), key=lambda r: r[0])
    manual = sorted((r for r in rows if r[3]), key=lambda r: r[0])
    block = "\n\n".join(
        [
            "### 自动触发(模型按需调用)",
            render_table([r[:3] for r in auto]),
            "### 手动触发(需 `/技能名` 或显式点名;不主动调用即零开销)",
            render_table([r[:3] for r in manual]),
        ]
    )
    new_text = re.sub(
        re.escape(MARK_START) + r".*?" + re.escape(MARK_END),
        MARK_START + "\n" + block + "\n" + MARK_END,
        text,
        flags=re.S,
    )
    README.write_text(new_text, encoding="utf-8")
    print(f"技能表已更新:自动 {len(auto)} 行 + 手动 {len(manual)} 行")
    return 0


if __name__ == "__main__":
    sys.exit(main())
