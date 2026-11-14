# skills

**简体中文** | [English](README.en.md)

一组通用的 **Agent Skills**。每个技能是一个包含 `SKILL.md` 的目录 —— 一份简短的指令文件，引导 agent 在某个具体任务上按固定流程工作。格式可跨 agent 通用，适用于支持 skill 约定的一众 coding agent（Codex、Cursor、Claude Code、OpenCode 等）。

## 已有技能

| 技能 | 用途 |
| --- | --- |
| [`skill-create`](skills/skill-create/SKILL.md) | 从需求创建新技能：对齐场景与角色、命名与描述、正文与冒烟测试，完成后交给 `skill-review` 做真实运行。 |
| [`skill-review`](skills/skill-review/SKILL.md) | 审查、诊断与打磨已有技能：静态扫描、真实运行、问题清单，以及确认后的修复。 |
| [`skill-shared`](skills/skill-shared/SKILL.md) | 前两个技能共用的编写标准（[STANDARD.md](skills/skill-shared/STANDARD.md)）：技能是什么、对齐、真实运行与修复。 |

## 安装

需要 Node.js 22.20 或更高版本。

```bash
npx skills add ziyueyijun/skills
```

默认安装到当前项目；加 `-g` 则对所有项目可用：

```bash
npx skills add ziyueyijun/skills -g
```

只安装指定的技能（`--skill` 可重复）：

```bash
npx skills add ziyueyijun/skills --skill skill-create --skill skill-shared
```

`skill-create` 与 `skill-review` 都会读取 `../skill-shared/STANDARD.md`，单独安装时请一并安装 `skill-shared`；不指定 `--skill` 则安装全部技能。

## 目录结构

```
skills/
└── <skill-name>/
    ├── SKILL.md        # 必需：frontmatter + 指令正文
    └── ...             # 可选：按分支拆分的参考文件、脚本、模板
```

`skill-shared` 除入口 `SKILL.md` 外还带有 `STANDARD.md`，供 `skill-create` 和 `skill-review` 通过相对路径引用。

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

新写技能前加载 `skill-create`，审查或打磨技能前加载 `skill-review`；两者共用的标准在 `skill-shared`。

## License

[MIT](LICENSE) © 2026 ziyueyijun
