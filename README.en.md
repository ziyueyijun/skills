# skills

[简体中文](README.md) | **English**

A collection of **Agent Skills** for coding agents. Each skill is a directory containing a `SKILL.md` — a short instruction file that steers the agent through one specific task. The format is portable across agents that support the skill convention (Codex, Cursor, Claude Code, OpenCode, and others).

## Skills

| Skill | What it does |
| --- | --- |
| [`skill-create`](skills/skill-create/SKILL.md) | Creates a new skill from a request: align on the scene and roles, name and description, body and smoke test, then hand off to `skill-review` for the real run. |
| [`skill-review`](skills/skill-review/SKILL.md) | Reviews, diagnoses, and polishes an existing skill: static scan, real run, findings, and fixes once confirmed. |
| [`skill-shared`](skills/skill-shared/SKILL.md) | The shared standard used by the other two ([STANDARD.md](skills/skill-shared/STANDARD.md)): what a skill is, the align phase, the real run, and the fix pass. |

## Install

Requires Node.js 22.20 or later.

```bash
npx skills add ziyueyijun/skills
```

Skills are installed into the current project by default. Add `-g` to make them available across all projects:

```bash
npx skills add ziyueyijun/skills -g
```

To install specific skills (`--skill` can be repeated):

```bash
npx skills add ziyueyijun/skills --skill skill-create --skill skill-shared
```

`skill-create` and `skill-review` both read `../skill-shared/STANDARD.md`, so install `skill-shared` alongside either one. Omitting `--skill` installs every skill.

## Layout

```
skills/
└── <skill-name>/
    ├── SKILL.md        # required: frontmatter + instructions
    └── ...             # optional: branch-specific references, scripts, templates
```

Besides its entry `SKILL.md`, `skill-shared` ships `STANDARD.md`, which `skill-create` and `skill-review` reference by relative path.

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

Load `skill-create` before writing a skill and `skill-review` before reviewing or polishing one; the standard they share lives in `skill-shared`.

## License

[MIT](LICENSE) © 2026 ziyueyijun
