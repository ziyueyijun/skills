# skills

一组给 [Claude Code](https://claude.com/claude-code) 等 agent 使用的 **Agent Skills**。每个技能是一个只含 `SKILL.md` 的目录，用一份简短的说明文件引导 agent 在特定任务上按固定流程工作。

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

## 已有技能

| 技能 | 用途 |
| --- | --- |
| [`skill-smith`](skills/skill-smith/SKILL.md) | 编写与打磨 SKILL.md 的元技能：结构、措辞、验证标准 |

## 安装

技能放在以下任一位置即可被加载：

- 个人级（所有项目可用）：`~/.claude/skills/<skill-name>/`
- 项目级（仅当前项目）：`<project>/.claude/skills/<skill-name>/`

克隆本仓库后把需要的技能目录复制或软链接过去，例如：

```bash
git clone https://github.com/ziyueyijun/skills.git
ln -s "$(pwd)/skills/skills/skill-smith" ~/.claude/skills/skill-smith   # macOS / Linux
```

Windows 下在管理员 PowerShell 中：

```powershell
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\skill-smith" -Target "D:\path\to\skills\skills\skill-smith"
```

## 编写约定

- **一个技能只负责一件事**：原子、可组合；编排型技能保持轻薄，按名字委派给其他技能。
- **开头直接给指令**，不写动机和历史；每一步以可检查的完成标准收尾（"Done when…"）。
- **分支细节下沉**：只有某个分支才需要的说明放进同级文件，用相对路径链接。
- **测每一行**：这行是否改变了 agent 的默认行为？没有就删掉。

新写或修改技能时，先加载 `skill-smith` 并按其流程执行。

## License

[MIT](LICENSE) © 2026 ziyueyijun
