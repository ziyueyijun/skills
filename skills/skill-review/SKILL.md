---
name: skill-review
description: 'Review, diagnose, or polish an agent skill (SKILL.md): static scan, real-run test, findings, and confirmed fixes. Use when the user asks to review, audit, diagnose, critique, tighten, or fix a skill ("is this any good?", "what is wrong with it?", "make it sharper"). Not for creating a new skill — use skill-create.'
---

## Roles

- **Reviewer** — you: read the skill cold, gather evidence, run the static scan and the real-run test. You decide what is defective and what to propose; you do not decide what the skill is for.
- **Client** — the user: owns the problem, scope, risk, and go/no-go. They decide which proposals to apply; they do not write the text.
- **Artifact** — the skill under review: carries its own guidance and anchors; it decides nothing.

Boundary: a review is evidence about the artifact, not a rewrite into the reviewer's taste.

Read `../skill-shared/STANDARD.md` first. It is the single source for what a skill is, the align phase, the real run, and the fix pass. This skill only reviews and polishes; creating a skill goes to `skill-create`.

## Review path

Align is in the shared standard; do it first. Then:

- **Static scan.** Every path exists, every pointer resolves, every command is runnable without side effects, the frontmatter parses with name matching the directory, the role block is complete, the description names the real branches, every decision right has a branch in the body. The scan is done when every check passes or each failure is recorded as a finding.
- **Real run (shared).** Follow the shared standard from its reread opening: reread the whole file, then try it on a real run. On a re-review, reuse the prior trace when the skill is identical to the copy last tested; rerun when it has changed.
- **Fix (shared).** Follow the shared standard. Review reports the proposals; apply only when the client asks. Polish applies the accepted proposals, then reruns the real run.

When the client names several artifacts (a directory or a list), review each in its own pass, reporting findings per artifact: skills get the real run; reference files get the static scan only — paths, pointers, and agreement with the skills that cite them (frontmatter, role block, and description are skill-only checks).

A clean review says clean and stops. A fix is the polish half of the same job, not a new skill.
