# skills

[简体中文](README.md) | **English**

A collection of **Agent Skills** for coding agents. Each skill is a directory holding a single `SKILL.md` — a short instruction file that steers the agent through one specific task. The format is portable across agents that support the skill convention (Codex, Cursor, Claude Code, OpenCode, and others).

## Skills

| Skill | What it does |
| --- | --- |
| [`skill-smith`](skills/skill-smith/SKILL.md) | A meta-skill for writing and refining `SKILL.md` files: structure, phrasing, frontmatter, and verification criteria. |

## Install

Requires Node.js 22.20 or later.

```bash
npx skills add ziyueyijun/skills
```

Skills are installed into the current project by default. Add `-g` to make them available across all projects:

```bash
npx skills add ziyueyijun/skills -g
```

To install one skill only:

```bash
npx skills add ziyueyijun/skills --skill skill-smith
```

## Layout

```
skills/
└── <skill-name>/
    ├── SKILL.md        # required: frontmatter + instructions
    └── ...             # optional: branch-specific references, scripts, templates
```

`SKILL.md` frontmatter needs two fields:

```yaml
---
name: skill-name          # kebab-case, ideally a phrase users already say
description: what it does, plus the distinct branches that trigger it ("Use when the user…")
---
```

## Conventions

- **One discipline per skill.** Keep skills atomic and composable; orchestrators stay thin and delegate to other skills by name.
- **Open with the instruction.** No motivation, no history. End each step on a checkable completion criterion ("Done when…").
- **Disclose branch detail** into sibling files linked by relative path; the main file keeps only what every branch needs.
- **Test every line.** If it doesn't change the agent's default behavior, delete it.

Load `skill-smith` before writing or editing a skill, and follow its process.

## License

[MIT](LICENSE) © 2026 ziyueyijun
