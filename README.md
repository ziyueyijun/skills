# skills

ziyueyijun 的 AI agent 技能合集,基于开放 agent skills 生态([skills.sh](https://skills.sh)),兼容 Claude Code、Codex、Cursor 等主流 agent。

## 一条命令安装全部技能

```bash
npx skills add ziyueyijun/skills
```

### 装到全局(所有项目可用)

```bash
npx skills add ziyueyijun/skills -g
```

### 只装单个技能

```bash
npx skills add ziyueyijun/skills@<技能名>
```

## 技能列表

| 技能 | 说明 | 上游来源 |
|------|------|----------|
| `find-skills` | 从开放技能生态查找并安装技能 | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| `skill-creator` | 创建、改进技能并评测性能 | [anthropics/skills](https://github.com/anthropics/skills) |
| `frontend-design` | 前端视觉设计指导:排版、配色、避免模板化 | [anthropics/skills](https://github.com/anthropics/skills) |

## 目录结构

- `skills/<技能名>/SKILL.md` — 技能本体(发布布局,`npx skills` 可自动发现)
- `.agents/`、`.claude/`、`skills-lock.json` — 本机安装态,不入库

## 许可

根目录 MIT License 适用于本仓库自有的编排内容;各技能目录保留各自上游的 LICENSE 文件。
