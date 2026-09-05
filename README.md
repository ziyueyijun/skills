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

| Skill | Description | Upstream source |
|------|------|----------|
| `ask-matt` | Ask which skill or flow fits your situation. A router over the skills in… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-me` | A relentless interview to sharpen a plan or design. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grill-with-docs` | A relentless interview to sharpen a plan or design, which also creates d… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `handoff` | Compact the current conversation into a handoff document for another age… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `implement` | Implement a piece of work based on a spec or set of tickets. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `improve-codebase-architecture` | Scan a codebase for deepening opportunities, present them as a visual HT… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-matt-pocock-skills` | Configure this repo for the engineering skills: set up its issue tracker… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-ts-deep-modules` | Wire dependency-cruiser into a TypeScript repo so each package is a deep… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-spec` | Turn the current conversation into a spec and publish it to the project… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `to-tickets` | Break a plan, spec, or the current conversation into a set of tracer-bul… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `triage` | Move issues and external PRs through a state machine of triage roles, ca… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wayfinder` | Plan a huge chunk of work (more than one agent session can hold) as a sh… | [mattpocock/skills](https://github.com/mattpocock/skills) |

### Auto-invoked (model calls when relevant)

| Skill | Description | Upstream source |
|------|------|----------|
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-ba… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the u… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `find-skills` | Helps users discover and install agent skills when they ask questions li… | [vercel-labs/skills](https://github.com/vercel-labs/skills) |
| `frontend-design` | Guidance for distinctive, intentional visual design when building new UI… | [anthropics/skills](https://github.com/anthropics/skills) |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when th… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the us… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `research` | Investigate a question against high-trust primary sources and capture th… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill… | [anthropics/skills](https://github.com/anthropics/skills) |
| `tdd` | Test-driven development. Use when the user wants to build features or fi… | [mattpocock/skills](https://github.com/mattpocock/skills) |
| `wizard` | Generate an interactive bash wizard that walks a human through steps onl… | [mattpocock/skills](https://github.com/mattpocock/skills) |
<!-- skills-table:end -->

> The skill tables above are auto-maintained by [tools/sync-skills.sh](tools/sync-skills.sh); do not hand-edit anything between the markers.

## Repository layout

- `skills/<skill-name>/SKILL.md` — publish layout, discovered by `npx skills add ziyueyijun/skills`
- `.agents/skills/`, `.claude/skills/` — real install copies (usable immediately after clone)
- `rules/AGENTS.md` / `rules/AGENTS.zh.md` — general agent rules (English / Chinese)
- `tools/sync-skills.sh` + `tools/update_readme.py` — mirror sync & auto table regeneration (updates both READMEs)
- `skills-lock.json` — upstream source records (data source for the README tables)

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

The root MIT License covers this repository's own curated content; each skill directory keeps its upstream LICENSE file. The mattpocock skills under `skills/` come from [mattpocock/skills](https://github.com/mattpocock/skills), Copyright (c) 2026 Matt Pocock, released under the MIT License.
