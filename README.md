# skills

**简体中文** | [English](README.en.md)

一组通用的 **Agent Skills**。每个技能是一个只含 `SKILL.md` 的目录 —— 一份简短的指令文件，引导 agent 在某个具体任务上按固定流程工作。格式可跨 agent 通用，适用于支持 skill 约定的一众 coding agent（Codex、Cursor、Claude Code、OpenCode 等）。

## 已有技能

| 技能 | 用途 |
| --- | --- |
| [`skill-smith`](skills/skill-smith/SKILL.md) | 编写与打磨 `SKILL.md` 的元技能：结构、措辞、frontmatter 与验证标准。 |

## 安装

需要 Node.js 22.20 或更高版本。

```bash
npx skills add ziyueyijun/skills
```

默认安装到当前项目；加 `-g` 则对所有项目可用：

```bash
npx skills add ziyueyijun/skills -g
```

只安装某一个技能：

```bash
npx skills add ziyueyijun/skills --skill skill-smith
```

## 目录结构

```
skills/
└── <skill-name>/
    ├── SKILL.md        # 必需：frontmatter + 指令正文
    └── ...             # 可选：按分支拆分的参考文件、脚本、模板
```

`SKILL.md` 的 frontmatter 只需两个字段：

```yaml
---
name: skill-name          # kebab-case，尽量用用户日常会说的短语
description: 做什么 + 哪些不同场景会触发它（"Use when the user…"）
---
```

## 编写约定

- **一个技能只负责一件事。** 保持原子、可组合；编排型技能保持轻薄，按名字委派给其他技能。
- **开头直接给指令。** 不写动机和历史；每一步以可检查的完成标准收尾（"Done when…"）。
- **分支细节下沉** 到同级文件，用相对路径链接；主文件只保留每个分支都需要的部分。
- **测每一行。** 这行没有改变 agent 的默认行为，就删掉。

新写或修改技能前，先加载 `skill-smith` 并按其流程执行。

## License

[MIT](LICENSE) © 2026 ziyueyijun
