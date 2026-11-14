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

## License

[MIT](LICENSE) © 2026 ziyueyijun
