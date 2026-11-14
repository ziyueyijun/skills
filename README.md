# skills

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

## License

[MIT](LICENSE) © 2026 ziyueyijun
