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

<!-- skills-table:start -->
| 技能 | 说明 | 上游来源 |
|------|------|----------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-ba… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the u… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `find-skills` | Helps users discover and install agent skills when they ask questions li… | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI… | [anthropics/skills](https://github.com/anthropics/skills) |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-me` | A relentless interview to sharpen a plan or design. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates d… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when th… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `handoff` | Compact the current conversation into a handoff document for another age… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `implement` | Implement a piece of work based on a spec or set of tickets. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HT… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the us… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `research` | Investigate a question against high-trust primary sources and capture th… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills: set up its issue tracker… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill… | [anthropics/skills](https://github.com/anthropics/skills) |
| `tdd` | Test-driven development. Use when the user wants to build features or fi… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-spec` | Turn the current conversation into a spec and publish it to the project… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bul… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `triage` | Move issues and external PRs through a state machine of triage roles, ca… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a sh… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wizard` | Generate an interactive bash wizard that walks a human through steps onl… | [mattpocock/skills](https://github.com/mattpocock/skills) |
<!-- skills-table:end -->

> 技能表由 [tools/sync-skills.sh](tools/sync-skills.sh) 自动维护,请勿手改标记区间内内容。

## 目录结构

- `skills/<技能名>/SKILL.md` — 发布布局,`npx skills add ziyueyijun/skills` 可自动发现
- `.agents/skills/`、`.claude/skills/` — 安装态真实副本(clone 后开箱即用)
- `tools/sync-skills.sh` + `tools/update_readme.py` — 镜像同步与技能表自动更新
- `skills-lock.json` — 技能来源记录(README 表格的数据源)

## 许可

根目录 MIT License 适用于本仓库自有的编排内容;各技能目录保留各自上游的 LICENSE 文件。`skills/` 下的 mattpocock 系技能来自 [mattpocock/skills](https://github.com/mattpocock/skills),Copyright (c) 2026 Matt Pocock,MIT License 发布。
