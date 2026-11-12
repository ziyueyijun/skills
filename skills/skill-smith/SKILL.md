---
name: skill-smith
description: Create or refine an agent skill. Use when writing a new SKILL.md or polishing an existing one.
---

A skill steers the agent's process on every run. Write for the agent as executor: terse, imperative, rule-shaped.

## Shape

- **One discipline per skill.** Small, atomic, composable; orchestrators stay thin and delegate to other skills by name. Shared reference lives in one place that others point to.
- **Frontmatter.** `name`: short kebab-case, ideally a phrase users already say. `description`: what it does plus the distinct branches that trigger it ("Use when the user…", including the words they will actually say); synonyms of one branch collapse into one. Where the platform distinguishes manual-only skills, strip the triggers and keep a one-line human-facing summary.
- **Open with the instruction**, not context: a sentence or two on what the agent does and what it produces. No motivation, no history.
- **End each step on a completion criterion:** "Done when…", `- [ ]` checklists, "Do not proceed until…". Strong criteria are checkable and exhaustive — demand drives thoroughness ("every modified model accounted for" beats "produce a change list").
- **Disclose branch-specific detail** into sibling files linked by relative path; the main file keeps only what every branch needs.
- **Output templates** go inline, in fenced blocks.

## Language

- Imperative, opinionated, no hedging.
- **Leading words**: bold, compact, pretrained concepts that anchor a whole behavior — *seam*, *tight loop*, *tracer bullet*, *frontier*. Repeat the token, define once; prefer an existing word to a coined one ("fast, deterministic, low-overhead" → *tight*).
- **State the target positively.** A prohibition drags the forbidden behavior into context; keep "do not" only for hard guardrails.
- **Facts are the agent's job; decisions are the user's.** Say which is which.
- **Redact secrets** wherever the skill shows commands or output.

## Polish

Test every line: does it change behavior versus the default? If not, delete the sentence — don't trim it. Settle disputes by running the skill, not by debate.

Also cut duplicated meanings (one source of truth), restatements of the environment (point at config/scripts instead), stale lines, and sprawl. When it grows, disclose reference behind pointers or split by branch or sequence — hiding later steps stops the agent rushing the current one — only when the split earns the extra load. Sharpen a pointer's wording before inlining its target.

## Verify

- A fresh agent with zero context could execute it — nothing assumed that isn't stated.
- Every step has a checkable completion criterion; every description trigger is a real branch.
- Run one real task through it; prompts are tested by execution.
