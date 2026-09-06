# skills

An AI agent skills collection by ziyueyijun. This repository's own skills are published through the open agent skills ecosystem ([skills.sh](https://skills.sh)) and installable with one command; in the repository itself they live in `.claude/skills/` and load automatically when Claude Code runs here.

**中文版:** [README.zh-CN.md](README.zh-CN.md)

## Install skills with npx

Installs this repo's own skills (currently `pbidea`, `powerbuilder` — skills tracked in [skills-lock.json](skills-lock.json) come from their respective upstreams and are not re-published here):

```bash
npx skills add ziyueyijun/skills
```

- List what is available without installing: `npx skills add ziyueyijun/skills -l`
- Install a single skill: `npx skills add ziyueyijun/skills -s pbidea`
- Global install (available in all projects): `npx skills add ziyueyijun/skills -g`

The CLI writes the skill into the project's `.agents/skills/` and symlinks it for Claude Code and the other agents it supports.

## Updating skills

- Already installed a skill and want the latest version? Run `npx skills update` in that project (or `npx skills update -g` for a global install); `npx skills update <skill>` updates just one.
- When this repository releases a new version of an original skill, re-run `npx skills add ziyueyijun/skills` (or `npx skills update`) to pull it.

## Using skills in this repository

- Open Claude Code here: every skill in `.claude/skills/` loads automatically (manual-invoked ones — `disable-model-invocation` — start with `/skill-name`).
- In another project without npx: copy `.claude/skills/<name>` into that project's `.claude/skills/`, or into `~/.claude/skills/` to make it available in every project. Skills are self-contained (stdlib-only Python scripts, no network), so a directory copy is all you need.

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
| `pbidea` | PbIdea framework API lookup skill, triggered manually via /pbidea. Cover… |
| `powerbuilder` | PowerBuilder official documentation lookup skill, triggered manually via… |
| `search` | Manual fact-checking companion to research, triggered only by explicit `… |

### Auto-invoked (model calls when relevant)

| Skill | Description |
|------|------|
| `code-review` | Review the changes since a fixed point (commit, branch, tag, or merge-ba… |
| `codebase-design` | Shared vocabulary for designing deep modules. Use when the user wants to… |
| `diagnosing-bugs` | Diagnosis loop for hard bugs and performance regressions. Use when the u… |
| `domain-modeling` | Build and sharpen a project's domain model. Use when discussing codebase… |
| `find-skills` | Helps users discover and install agent skills when they ask questions li… |
| `git-guardrails-claude-code` | Set up Claude Code hooks to block dangerous git commands (push, reset --… |
| `grilling` | Grill the user relentlessly about a plan, decision, or idea. Use when th… |
| `playwright-best-practices` | Use when writing Playwright tests, fixing flaky tests, debugging failure… |
| `prototype` | Build a throwaway prototype to answer a design question. Use when the us… |
| `research` | Investigate a question against high-trust primary sources and capture th… |
| `resolving-merge-conflicts` | Use when you need to resolve an in-progress git merge/rebase conflict. |
| `setup-pre-commit` | Set up Husky pre-commit hooks with lint-staged (Prettier), type checking… |
| `skill-creator` | Create new skills, modify and improve existing skills, and measure skill… |
| `tdd` | Test-driven development. Use when the user wants to build features or fi… |
| `wizard` | Generate an interactive bash wizard that walks a human through steps onl… |
<!-- skills-table:end -->

> The skill tables above are auto-maintained by [tools/update_readme.py](tools/update_readme.py); do not hand-edit anything between the markers.

## Repository layout

- `.claude/skills/<skill-name>/SKILL.md` — the one and only skills directory; Claude Code loads skills from it when running in this repo
- `.mcp.json` — MCP servers used when developing in this repo (github / context7); credentials are `${VAR}` placeholders only, never plaintext — see below
- `tools/update_readme.py` + `tools/skill-desc-zh.json` — skill-table regeneration (Chinese descriptions)
- `rules/AGENTS.md` / `rules/AGENTS.zh.md` — general agent rules (English / Chinese)
- `skills-lock.json` — install records kept by `npx skills` (source + content hash per skill)
- `settings.json` — reference copy of the author's Claude Code user config (not loaded by Claude Code; see below)

## Claude Code settings reference

[settings.json](settings.json) at the repository root is the author's own Claude Code user configuration, kept here as a reference copy for readers who want to see how permissions, deny rules and env overrides can be set up. **Claude Code does not read a `settings.json` at the repository root** — it loads settings only from `~/.claude/settings.json` (user-wide, applies to every project) and `<project>/.claude/settings.json` (project-wide; must live inside the project's `.claude/` directory). The `env` section is machine-specific (a local proxy endpoint and model remapping) and will not work as-is on another machine — copy selectively.

## MCP configuration

[.mcp.json](.mcp.json) wires up two MCP servers for development in this repo: github (GitHub operations) and context7 (third-party library docs). **Credentials are never committed in plaintext** — the file holds only `${VAR}` placeholders, expanded by Claude Code from the process environment at startup.

Setup steps:

1. Have an `.mcp.json` in the project — this repo ships a placeholder version that is safe to commit (it contains no secrets).
2. Obtain a token from each service: a GitHub fine-grained or classic PAT, and a Context7 API key.
3. Put the real values in the `env` block of `~/.claude/settings.json` (user-level settings — never in committed files), e.g.:

   ```json
   {
     "env": {
       "GITHUB_PAT": "github_pat_your-token",
       "CONTEXT7_API_KEY": "ctx7sk_your-key"
     }
   }
   ```

   Claude Code injects the `env` block into the process environment at startup — equivalent to OS environment variables (it overrides shell exports and is visible only to Claude Code and its subprocesses); `${VAR}` in `.mcp.json` expands from there. A default-value form is also supported: `${VAR:-default}`.
4. Restart Claude Code for the variables to take effect (they are read when a session starts); `claude mcp list` shows server status and missing-variable warnings.

Notes:

- **No `.env` file needed** — Claude Code does not auto-load one from the project root; variables must come from the process environment (a shell export or a settings `env` block).
- A missing variable does not block loading: you get a startup warning and requests carry the literal `${VAR}` (authentication fails loudly rather than silently misbehaving).
- The reference [settings.json](settings.json) copy at the repo root contains no tokens; real values live only in your user-level `~/.claude/settings.json`.
- If a token was ever exposed (committed by accident, pasted into a chat in plaintext, …), rotate it at the service and update the settings.

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
