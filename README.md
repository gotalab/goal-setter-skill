# goal-setter

**Shape rough requests into evidence-backed `/goal` completion contracts — before the long run starts.**

Works with **Claude Code** and **Codex**. One skill, both runtimes.

[日本語](README.ja.md)

![Abstract concept of loose work converging into an evidence-backed goal contract](assets/goal-setter-concept.png)

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
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

After install, the skill triggers from your request automatically, or invoke it explicitly with `/goal-setter:goal-setter`.

Or manually:

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.claude/skills/goal-setter
```

### Codex (plugin)

```bash
codex plugin marketplace add gotalab/goal-setter-skill
```

Then open `/plugins` inside Codex and install **Goal Setter**. (Newer CLIs also support `codex plugin add goal-setter@goal-setter`.)

### Codex (skill only)

Inside Codex, use the bundled installer (works with any public GitHub repo):

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Or manually — Codex discovers skills in `~/.agents/skills/` (symlinks are supported; `~/.codex/skills/` still works but is deprecated):

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.agents/skills/goal-setter
```

Restart Codex to pick up the skill, then invoke it explicitly with `$goal-setter` or let it trigger from your request.

## Usage

**Draft** — get a reviewed contract without activating it:

> draft a goal for migrating our API client to v2

**Activate** — shape and launch in one motion:

> set a goal: all checkout tests pass after the refactor

goal-setter forms the outcome image, runs its gates, drafts the compact condition, audits it, and activates it through whatever path the runtime offers (see below). If your request is too small or too vague to be an honest goal, it says so and suggests a normal prompt instead.

## Example

What you type:

> set a goal: migrate src/api to the v2 client

What goal-setter does first — explores the repo, then mirrors the outcome image back:

> **Image:** Replace every v1 `ApiClient` usage under `src/api` with the v2 SDK so behavior is unchanged — existing integration tests stay green, no public interface or auth changes. Correct me if this is off, otherwise I'll activate.

What gets activated:

```text
/goal Context: this migration unblocks v2-only work for the API team, so
behavior parity matters more than speed. Migrate src/api from the v1
ApiClient to the v2 SDK with behavior unchanged. Verify success through
the existing integration tests in tests/api and a final diff review. Read
src/api/client.ts and docs/v2-migration.md first; discover adjacent
tests/docs as needed. Keep changes scoped to src/api and directly related
tests — the simplest change that meets the objective, no refactors beyond
it; do not change public API, auth behavior, retry semantics, or other
externally visible contracts unless explicitly required. Validate with `pnpm test tests/api` and `pnpm build`;
do not satisfy them by deleting, weakening, or skipping tests. Use
available read-only subagents for migration-doc research and validation
discovery; before claiming Done, have a fresh-context subagent verify the
evidence. Maintain visible progress with a concise checklist and
checkpoint updates; audit each progress claim against a tool result first
— unverified work is reported as unverified, never as done. When you have
enough information to act, act; never end a turn on a plan or a promise.
Done when every v1 ApiClient import under src/api is gone, `pnpm test
tests/api` and `pnpm build` exit 0, and the final diff review confirms no
public API or auth changes. If two approaches fail to improve evidence,
review strategy and pivot within constraints; do not silently change the
objective, Done, evidence, or constraints. Stop only if v1/v2 behavior
differences cannot be safely inferred from docs or tests, or a required
credential or service blocks validation. Write the final report for a
reader who watched none of the run: outcome first, plain words, in the
user's language.
```

Compare that to what most of us actually type after `/goal` — that delta is the product.

## How activation works

goal-setter only uses the runtime's **native** goal mechanism — it never spawns child sessions or side processes to activate a goal.

| Runtime | Path | Status |
|---|---|---|
| Codex | native `set_goal` tool — fully autonomous activation | ✅ |
| Claude Code | emits the exact `/goal …` line for you to send | ✅ |

Why the table looks like this: as of Claude Code v2.1.170 there is **no model-callable tool to set a goal on the current session** — `/goal` is a user command wrapping a session-scoped Stop hook. So on Claude Code, goal-setter prepares the contract and hands you the exact line; activation stays a deliberate, native, one-keystroke act.

## What a contract covers

Every non-trivial goal includes: a one-line context note (what the outcome serves and for whom) · one objective · evidence surface · context to read first · task-specific constraints + anti-gaming rule · validation (or a discovery rule for it) · subagent policy with fresh-context verification before Done · progress reporting audited against tool results (in your language) · a persistence rule (act on sufficient information; never end a turn on a promise) · progress/pivot rules · binary Done · explicit block conditions · a final report rule (outcome first, plain words, your language).

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

Plugin packaging lives at the repo root: `.claude-plugin/` (plugin.json + marketplace.json) for Claude Code, `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` for Codex — both point at the same `skills/goal-setter/` folder.

## License

[MIT](LICENSE)
