---
name: search
description: Manual fact-checking companion to research, triggered only by explicit `/search <question>`. Verify a question against high-trust primary sources — official docs, source code, specs, first-party APIs — and answer directly in chat, citing each claim. Never writes files; use research when findings should be captured to a repo Markdown file.
disable-model-invocation: true
---

Manual counterpart of **research**. research captures findings to a repo file; **search exists for the opposite**: the user wants the answer in the conversation and nothing left on disk. Same sourcing discipline, different deliverable. Only runs when the user types `/search <question>`.

## Procedure

1. **Decide where the reading happens.** Every fetched page is paid for by whichever context reads it, so match the job to the context:
   - A small lookup — one or two official pages whose URL you know or can guess — **read it in-session**. It streams fast, costs no agent overhead, and you can narrow or stop mid-read.
   - A bigger job — several pages, multiple sources to cross-check, or long reads — **spawn a background agent** (as research does): the pages are consumed in the agent's context and only its compact findings come back, keeping this session's context lean for whatever you do next.
2. **Follow primary sources.** Official docs, source code, specs, first-party APIs — the page that owns each claim, not a secondary write-up of it. When no reachable primary source exists for a claim, say so plainly instead of filling with secondary material.
3. **Answer in chat**, shaped for scanning: the verdict up front, then the facts that back it, each tied to its source (link and, where wording matters, a short quote). Note anything you could not confirm and why.
4. **Never write files** — no Markdown, no notes, no scripts, no temp directories. If the user turns out to want the answer persisted, point them to `/research`, which does exactly that.
