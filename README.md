# goal-setter

**Turn a few words into a complete `/goal` condition — before the long run starts.**

Built for **Codex**, and works with **Claude Code**. One skill, both runtimes.

[日本語](README.ja.md)

<img src="assets/goal-setter-concept.png" alt="Loose pieces of work converging into a single goal contract" width="33%">

---

## Why

A goal keeps the agent working until a completion condition is true ([Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)). Writing that condition well is real work: you have to state the outcome, how success is verified, what must not change, and when to stop. Skip any of it and the run drifts — a goal runs unattended, so a weak starting condition is amplified for hours.

goal-setter exists because writing that condition is exactly the part people skip. You already have the finished picture in your head; what you actually type is one short line. This skill takes that line, rebuilds the picture, checks it with you in one round trip when needed, and carries it all the way to an activated goal.

## What it does

- **Rebuilds the intended outcome first.** Before drafting anything, it reconstructs what you are trying to build and why, in a few sentences. When your request is minimal, it shows you that reconstruction for a one-pass correction instead of asking a list of questions. Success criteria, constraints, and the Done condition are all derived from it.
- **Asks only what changes the outcome.** Scope, verification, safety boundaries. Everything discoverable in the repo gets explored instead of asked; low-risk details become stated assumptions.
- **Writes a compact condition.** The goal text fixes *what* and *why* and leaves *how* to the agent. No step-by-step recipes.
- **Builds in stop and honesty rules.** Checks may not be passed by weakening them; stalled approaches trigger a strategy review, then a hard stop; the objective and Done condition cannot be quietly rewritten mid-run; progress may only be reported against actual tool results.
- **Grants subagent use explicitly.** Codex will not use subagents during a goal run unless the goal text permits it, so the permission is always written in.
- **Audits before activating.** Every goal is checked against the contract checklist before it is set. Anything missing gets fixed first.
- **Sidecar files for day-scale work.** `GOAL.md` + `execution-notes.md` when you need a durable record and resume state.

## Install

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

Or manually — Codex discovers skills in `~/.agents/skills/` (symlinks work; `~/.codex/skills/` still works but is deprecated):

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.agents/skills/goal-setter
```

Restart Codex, then invoke with `$goal-setter` or let it trigger from your request.

### Claude Code (plugin)

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

After install, the skill triggers from your request, or invoke it with `/goal-setter:goal-setter`.

Or manually:

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.claude/skills/goal-setter
```

## Usage

**Draft** — get a reviewed condition without activating it:

> draft a goal for migrating our API client to v2

**Activate** — shape and launch in one motion:

> set a goal: all checkout tests pass after the refactor

goal-setter rebuilds the outcome, asks anything critical, drafts and audits the condition, then activates it through the runtime's own goal mechanism (see below). If the request is too small or too vague to make an honest goal, it says so and suggests a normal prompt instead.

## Example

What you type:

> set a goal: migrate src/api to the v2 client

goal-setter explores the repo, then shows you the outcome it reconstructed:

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
externally visible contracts unless explicitly required. Validate with
`pnpm test tests/api` and `pnpm build`; do not satisfy them by deleting,
weakening, or skipping tests. Use available read-only subagents for
migration-doc research and validation discovery; before claiming Done,
have a fresh-context subagent verify the evidence. Maintain visible
progress with a concise checklist and checkpoint updates; audit each
progress claim against a tool result first — unverified work is reported
as unverified, never as done. When you have enough information to act,
act; never end a turn on a plan or a promise. Done when every v1
ApiClient import under src/api is gone, `pnpm test tests/api` and `pnpm
build` exit 0, and the final diff review confirms no public API or auth
changes. If two approaches fail to improve evidence, review strategy and
pivot within constraints; do not silently change the objective, Done,
evidence, or constraints. Stop only if v1/v2 behavior differences cannot
be safely inferred from docs or tests, or a required credential or
service blocks validation. Write the final report for a reader who
watched none of the run: outcome first, plain words, in the user's
language.
```

The one line you typed is the entire input. Everything else came from the repo and the reconstructed outcome.

## How activation works

goal-setter only uses the runtime's own goal mechanism. It never spawns child sessions or side processes to activate a goal.

| Runtime | Path |
|---|---|
| Codex | sets the goal itself via the native `set_goal` tool |
| Claude Code | hands you the exact `/goal …` line to send |

The difference exists because Claude Code (as of v2.1.170) has no tool a model can call to set a goal on the current session — `/goal` is a user command. So on Claude Code the skill prepares everything and activation is one keystroke by you.

## What a goal covers

Every non-trivial goal includes: a one-line note on what the outcome serves and for whom · one objective · how success is verified · what to read first · the few hard boundaries this task could break, plus the rule against passing checks by weakening them · validation commands (or how to discover them) · subagent permission, including an independent check before Done · progress reported against tool results, in your language · a rule to keep acting instead of ending on a promise · pivot rules for stalled approaches · a binary Done condition · explicit stop conditions · a final report written for someone who did not watch the run.

Full reference: [`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## Structure

```text
skills/goal-setter/
├── SKILL.md                      # routing, modes, gates
├── references/
│   ├── goal-contract.md          # the contract spec + pre-activation audit
│   ├── runtime-capabilities.md   # subagents, tools, sandbox posture
│   ├── sidecars-and-notes.md     # GOAL.md / execution-notes.md policy
│   ├── GOAL.template.md
│   └── execution-notes.template.md
├── scripts/
│   ├── init_goal_run.py          # sidecar scaffolding helper
│   └── check_python_syntax.py
└── agents/openai.yaml            # Codex surface metadata
```

Plugin packaging lives at the repo root: `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` for Codex, `.claude-plugin/` (plugin.json + marketplace.json) for Claude Code — both point at the same `skills/goal-setter/` folder.

## License

[MIT](LICENSE)
