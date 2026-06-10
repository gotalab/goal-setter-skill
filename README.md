# goal-setter

**Shape rough requests into evidence-backed `/goal` completion contracts — before the long run starts.**

Works with **Claude Code** and **Codex**. One skill, both runtimes.

---

## Why

`/goal` turns your coding agent into a long-horizon worker: it keeps going — for hours if needed — until a completion condition is met. That's also the risk. A goal runs unattended, so **a sloppy starting condition is amplified across the entire run**. Vague objective, no evidence surface, no stop rules — you come back to hours of confidently wrong work.

The prompt you type after `/goal` is doing most of the work, and the prompt you'd write yourself almost never has enough in it.

goal-setter is the missing intake step. It takes your rough, minimal ask and turns it into a **completion contract**: one objective, an evidence surface, validation rules, anti-gaming constraints, pivot rules, a binary Done condition, and explicit stop conditions. You can't build what you can't picture — so it resolves the picture first, then derives everything else from it.

## What it does

- **Intended Outcome Image** — reconstructs what you're actually trying to build and why, in 2–4 sentences, *before* drafting anything. Evaluation criteria follow from the image, constraints from the criteria, Done from both. When your prompt is minimal, it mirrors the image back for a one-pass correction instead of interrogating you.
- **Clarification & exploration gates** — asks only the questions that change the outcome (scope, evidence, safety boundaries); explores the repo for everything discoverable; assumes-and-encodes the rest.
- **Compact, contract-shaped output** — context-minimalist goal text (target ≤2,500 chars) that fixes *what* and *why* while leaving *how* to the agent. No step-by-step recipes that strangle execution freedom.
- **Anti-gaming & loop protection** — constraints against satisfying metrics by weakening tests; strategy review after 2 failed approaches; hard stop after 3; goal-amendment boundary so the agent can't silently move the goalposts.
- **Explicit subagent authorization** — non-trivial goals grant bounded delegation for research, validation discovery, triage, and final review, instead of relying on implicit autonomy.
- **Readiness audit** — every goal is scored against a 0/1/2 checklist before activation. Score a zero, revise before launch.
- **Sidecar mode** — for day-scale work: `GOAL.md` + `execution-notes.md` give you durable audit, resume state, and a reviewable decision log.

## Install

### Claude Code (plugin)

```text
/plugin marketplace add gotalab/goal-setter
/plugin install goal-setter@goal-setter
```

Or manually:

```bash
git clone https://github.com/gotalab/goal-setter.git
ln -s "$(pwd)/goal-setter/skills/goal-setter" ~/.claude/skills/goal-setter
```

### Codex

```bash
git clone https://github.com/gotalab/goal-setter.git
ln -s "$(pwd)/goal-setter/skills/goal-setter" ~/.codex/skills/goal-setter
```

## Usage

**Draft** — get a reviewed contract without activating it:

> draft a goal for migrating our API client to v2

**Activate** — shape and launch in one motion:

> set a goal: all checkout tests pass after the refactor

goal-setter forms the outcome image, runs its gates, drafts the compact condition, audits it, and activates it through whatever path the runtime offers (see below). If your request is too small or too vague to be an honest goal, it says so and suggests a normal prompt instead.

## How activation works

| Runtime | Path | Status |
|---|---|---|
| Codex | native `set_goal` tool — fully autonomous activation | ✅ works |
| Claude Code (interactive) | emits the exact `/goal …` line for you to send | ✅ works |
| Claude Code (hands-off) | **launcher pattern**: spawns `claude -p "/goal …"` as a headless child run, optionally fed by sidecar `GOAL.md` | ✅ verified |
| Claude Code (in-session, autonomous) | Stop-hook based goal armer shipped with this plugin | 🚧 roadmap |

Why the table looks like this: as of Claude Code v2.1.170 there is **no model-callable tool to set a goal on the current session** — `/goal` is a user command wrapping a session-scoped Stop hook. The launcher pattern works today because `/goal` is fully supported in headless `-p` mode: the child session sets the goal, runs the loop to completion, and exits when the evaluator confirms the condition. Sidecar files double as the context bridge into the child session.

## What a contract covers

Every non-trivial goal includes: one objective · evidence surface · context to read first · constraints + anti-gaming rule · validation (or a discovery rule for it) · subagent policy · visible progress reporting (in your language) · progress/pivot rules · binary Done · explicit block conditions.

Full reference: [`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## Structure

```text
skills/goal-setter/
├── SKILL.md                      # routing, modes, gates
├── references/
│   ├── goal-contract.md          # the contract spec + readiness audit
│   ├── runtime-capabilities.md   # subagents, tools, sandbox posture
│   ├── sidecars-and-notes.md     # GOAL.md / execution-notes.md policy
│   ├── GOAL.template.md
│   └── execution-notes.template.md
├── scripts/
│   ├── init_goal_run.py          # sidecar scaffolding helper
│   └── check_python_syntax.py
└── agents/openai.yaml            # Codex surface metadata
```

## Roadmap

- **Goal armer for Claude Code** — a plugin-shipped Stop hook + model-writable condition file that replicates `/goal` inside the current session, so the agent can arm a goal for itself without a child process.
- Marketplace listings and examples gallery.

## License

[MIT](LICENSE)
