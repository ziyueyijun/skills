# skills

An AI agent skills collection by ziyueyijun, built on the open agent skills ecosystem ([skills.sh](https://skills.sh)). Compatible with mainstream agents: Claude Code, Codex, Cursor, and more.

**中文版:** [README.zh-CN.md](README.zh-CN.md)

## Install all skills with one command

```bash
npx skills add ziyueyijun/skills
```

### Global install (available in all projects)

```bash
npx skills add ziyueyijun/skills -g
```

### Install a single skill

```bash
npx skills add ziyueyijun/skills@<skill-name>
```

## Skills

<!-- skills-table:start -->
### Manual-invoked (requires `/skill-name` or explicit request; no cost unless invoked)

| Skill | Description |
|------|------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in… |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills: set up its issue tracker… |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep… |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a sh… |
| `grill-me` | A relentless interview to sharpen a plan or design. |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates d… |
| `to-spec` | Turn the current conversation into a spec and publish it to the project… |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bul… |
| `implement` | Implement a piece of work based on a spec or set of tickets. |
| `handoff` | Compact the current conversation into a handoff document for another age… |
| `triage` | Move issues and external PRs through a state machine of triage roles, ca… |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HT… |
| `pbidea` | PbIdea 框架 API 查询技能。由 /pbidea 命令手动触发。覆盖：uo_json（JSON 解析/生成/与 DataWindow 互… |
| `powerbuilder` | PowerBuilder 官方开发文档查询技能。由 /powerbuilder 命令手动触发。覆盖：PowerScript 语言（语法/语句/事… |

### Auto-invoked (model calls when relevant)

| Skill | Description |
|------|------|
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-ba… |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the u… |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase… |
| `find-skills` | Helps users discover and install agent skills when they ask questions li… |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI… |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --… |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when th… |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the us… |
| `research` | Investigate a question against high-trust primary sources and capture th… |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking… |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill… |
| `tdd` | Test-driven development. Use when the user wants to build features or fi… |
| `wizard` | Generate an interactive bash wizard that walks a human through steps onl… |
<!-- skills-table:end -->

> The skill tables above are auto-maintained by [tools/sync-skills.sh](tools/sync-skills.sh); do not hand-edit anything between the markers.

## Repository layout

- `skills/<skill-name>/SKILL.md` — publish layout, discovered by `npx skills add ziyueyijun/skills`
- `.agents/skills/`, `.claude/skills/` — real install copies (usable immediately after clone)
- `rules/AGENTS.md` / `rules/AGENTS.zh.md` — general agent rules (English / Chinese)
- `tools/sync-skills.sh` + `tools/update_readme.py` — mirror sync & auto table regeneration (updates both READMEs)
- `skills-lock.json` — install records kept by `npx skills` (source + content hash per skill)

## General agent rules

[rules/AGENTS.md](rules/AGENTS.md) is a ready-to-use set of general agent rules (core principles: never fabricate, evidence first; includes safety bottom lines for destructive operations, conflict resolution, operating modes, etc.). Keep the Hard Rules sections as-is; trim the Preferences section as needed. The content uses no tool-specific syntax.

Note: the rules file itself is tool-agnostic, but **each tool reads a different filename** — Claude Code reads `CLAUDE.md` only, Codex reads `AGENTS.md` only (neither reads the other's filename; verified against official docs / source code). Place it per your target tool:

| Target | Location | Command |
|---|---|---|
| Claude Code (global) | `~/.claude/CLAUDE.md` | `cp rules/AGENTS.md ~/.claude/CLAUDE.md` |
| Claude Code (single project) | project-root `CLAUDE.md` | Copy the rules to project-root `AGENTS.md`, then add a line `@AGENTS.md` at the top of your CLAUDE.md (official pattern — both tools share one copy) |
| Codex (global) | `~/.codex/AGENTS.md` | `cp rules/AGENTS.md ~/.codex/AGENTS.md` |
| Codex (single project) | project-root `AGENTS.md` | Drop the file at the project root |

## License

The root MIT License covers this repository's own curated content; each skill directory keeps its upstream LICENSE file.
