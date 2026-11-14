# Skill standard

Read this before creating, reviewing, or polishing a skill. It is the single source for what a skill must be and how it is tested.

## Paths

The order is the default, not a gate; the role block may be inferred from a drafted body.

- **Create:** Align here → scene and roles, name, description, trigger, body in `skill-create` → smoke test → handoff to `skill-review`.
- **Review / polish:** Align here → static scan in `skill-review` → real run here → fix here.

## What a skill is

Every produced skill opens with its role block: each role states what it is, what it decides, and what it does not do. The relationship and decision rights are the load-bearing part; every right gets a branch in the body or is cut. A metaphor ends with one line on where it stops.

A skill carries only two things:

- **Guidance** — at a fork, which way and why: priorities, trade-offs, what to prefer, when to stop, when to ask.
- **Anchors** — local facts the model would otherwise invent: paths, commands, names, schemas, thresholds, canonical sources, examples, the signal that the work is done.

A skill needs both: guidance without anchors is advice; anchors without guidance is a data dump.

Everything else is filler: motivation, history, generic methodology, restated common sense. Delete it; do not trim it. Duplicated meanings collapse into one, keeping the more decision-shaped wording. Test each line once: does it change what a capable agent does, or give it a fact it could not know? If neither, it is filler. Hard guardrails — secrets, irreversible actions, the role block's minimum — stay even when a test says they change nothing; their wording is still tested.

Procedure is guidance about order: steps only where order matters or a misstep is expensive; a checklist or template only where the work cannot be judged without one. When steps exist, each ends on a completion criterion that is clear and demanding.

The main file is a road book, not a codebase: steps first; reference inline only when every run needs it; branch-only reference and executable code live in siblings and are pointed at. Point at the environment instead of restating it; cache only what the agent cannot look up.

When writing: name a recurring judgment once with an existing word; state the target positively; keep a concept's definition, rules, and caveats together.

Defaults: one job per skill — split when two branches are different jobs, not when detail differs; verify facts and leave irreversible or preference-bound choices to the client; split a sequence only when later steps tempt the agent to rush, and only across a real handoff.

## Align

Restate the job in one sentence when the request is clear. Ask only when two readings would change the artifact; give recommended options, not open questions; stop when the client agrees on the goal, the scope, and what counts as good.

## Real run

Copy the skill (`SKILL.md` and its siblings); reread the whole copy first — grammar, terms, cross-references, contradictions; fix errors, not style.

Keep the copy, the trace, and everything else the run produces under `test/<skill name>/` at the project root (the repository root, or the session's working directory outside a repository); `<skill name>` is the skill's frontmatter `name`.

Take one real task the skill is for. Run it on that copy, and keep the trace: what it did, where it hesitated, what it got wrong. One run is the test; do not build a matrix.

Read the copy against the trace, sentence by sentence: would the agent behave differently without this line? If not, delete the sentence from the copy; the client confirms before the original changes. A disagreement is settled by running without the line, not by arguing.

The task must not mention the behavior under test; otherwise the run proves nothing. A line the run could not exercise stays in the copy; the report lists it as untested.

Finish with one run of the trimmed file on the same task; if it gets worse, restore what you cut.

## Fix what the run shows

Turn the run's problems into the smallest proposals — cut, add, reword. The client confirms; apply and run the same task once more. When two fixes are defensible, try each. Stop when the run is clean and the client accepts it.
