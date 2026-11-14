---
name: skill-create
description: Create a new agent skill (SKILL.md) from a request. Use when the user asks to make, write, draft, or scaffold a skill or SKILL.md. Not for reviewing or fixing an existing skill — use skill-review.
---

## Roles

- **Author** — you: gather evidence, draft, run the smoke test. You decide how to write and when the evidence is enough; you do not decide what the client wants.
- **Client** — the user: owns the problem, scope, risk, and go/no-go. They decide what is worth doing; they do not write the text.
- **Artifact** — the skill being written: carries guidance and anchors, never the author's taste, and decides nothing.

Boundary: a skill adds turns and local facts, not the ability to drive.

Read `../skill-shared/STANDARD.md` first. It is the single source for what a skill is, the align phase, the real run, and the fix pass.

## Create path

Align is in the shared standard; do it first. The order below is the default, not a gate.

- **Scene and roles.** Build one concrete run: who asks, in what state, what they expect, where a capable agent would go wrong. The roles come from that scene, and so do the decision points. Write the role block as the shared standard requires. Roles can be people, titles, objects, or forms; use what the domain would actually say. A person name in a highly specialized domain can read as unserious; there, use the domain's own register. The skill's own form belongs in the scene when it helps.
- **Name.** Short, common, the job's own word — what the client would call it, not a name borrowed from an existing skill directory. The directory and frontmatter `name` match; `name` is lowercase letters, digits, and hyphens, max 64 characters; the skill lives at `<scope>/<name>/SKILL.md` — personal `~/.claude/skills/`, or project `.claude/skills/` when the client works in a repo. A name users already say beats a clever one.
- **Description.** What it does, when to use it in the client's actual words, and what it is not for. The description is the trigger anchor, not a summary of the topic. It is always loaded: front-load the trigger word, one branch per trigger, and cut identity the body already carries. Test it: one scenario per claimed branch should fire the skill; near-misses should not.
- **Trigger.** Default automatic. Automatic skills need no `agents/openai.yaml`; add it only when the client wants Codex compatibility. Manual always gets both: Claude's `disable-model-invocation: true` and the yaml with `policy.allow_implicit_invocation: false` — even in a Claude-only deployment. The yaml carries `interface.display_name`, `interface.short_description` (25–64 chars), optional icons and `brand_color`, and `interface.default_prompt`, which names the skill as `$skill-name`. Schema: `~/.codex/skills/.system/skill-creator/references/openai_yaml.md`.
- **Body.** Draft to the shared Standard. Use the role names as subjects: "the teacher does not write the essay" beats "the agent should not". Write in the language the client will invoke it in; trigger words may be in other languages. Apply the shared Standard's rule that the main file is a road book, not a codebase: code and branch-only reference go to siblings, not the body. Create every sibling the body points at: code in `scripts/`, reference in `references/`, templates, fixtures and images in `assets/`; the smoke test runs or consumes each.

Run one smoke test: one real task, one run, on a disposable copy of the real input under `test/<skill name>/` at the project root, where `<skill name>` is the skill being created; when the client has no real input, synthesize one and mark it as synthetic; keep every smoke-test artifact there; check the output against the artifact's anchors; rereading the file is not a run. A smoke test is not the real run: no sentence-by-sentence deletion, no matrix, no embedded program. Do not run the real run or the fix pass here; hand the artifact to `skill-review` for those.
