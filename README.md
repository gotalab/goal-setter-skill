# goal-setter

**Turn a few words into a complete `/goal` condition — before the long run starts.**

Built for **Codex**, and works with **Claude Code**. One skill, both runtimes.

[日本語](README.ja.md)

<p align="center">
  <img src="assets/goal-setter-concept.png" alt="Loose pieces of work converging into a single goal contract" width="50%">
</p>

---

## Why

A goal keeps the agent working until a completion condition is true ([Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)). Writing that condition well is real work: you have to state the outcome, how success is verified, what must not change, and when to stop. Skip any of it and the run drifts — a goal runs unattended, so a weak starting condition is amplified for hours.

goal-setter exists because writing that condition is exactly the part people skip. You already have the finished picture in your head; what you actually type is one short line. This skill takes that line, rebuilds the picture, keeps checking with you until no outcome-changing ambiguity remains — questions are bundled, so it is usually one round trip — and carries it all the way to an activated goal.

## What it does

- **Rebuilds the intended outcome first.** Before drafting anything, it reconstructs what you are trying to build and why, in a few sentences. When your request is minimal, it shows you that reconstruction to correct, bundling any critical questions into the same message; if ambiguity remains, it keeps asking until the outcome is safe. Success criteria, constraints, and the Done condition are all derived from it.
- **Asks only what changes the outcome.** Scope, verification, safety boundaries. Everything discoverable in the repo gets explored instead of asked; low-risk details become stated assumptions.
- **Writes a compact condition.** The goal text fixes *what* and *why* and leaves *how* to the agent. No step-by-step recipes.
- **Builds in stop and honesty rules.** Checks may not be passed by weakening them; stalled approaches trigger a strategy review, then a hard stop; the objective and Done condition cannot be quietly rewritten mid-run; progress may only be reported against actual tool results.
- **Grants subagent use explicitly.** Codex will not use subagents during a goal run unless the goal text permits it, so the permission is always written in.
- **Audits before activating.** Every goal is checked against the contract checklist before it is set. Anything missing gets fixed first.
- **Sidecar files for day-scale work.** `GOAL.md` + `execution-notes.md` when you need a durable record and resume state.

## Install

### Codex (recommended)

Inside Codex, use the bundled `$skill-installer`. It installs the skill into
`$CODEX_HOME/skills` (default: `~/.codex/skills`) and is the simplest way to
make `$goal-setter` available in normal Codex chats:

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Restart Codex after installation, then invoke with `$goal-setter` or let it
trigger from your request.

Manual install uses the same skill folder:

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" "${CODEX_HOME:-$HOME/.codex}/skills/goal-setter"
```

### Codex (plugin marketplace)

If you want the Codex plugin card instead of a skill-only install, add this repo
as a marketplace and then install **Goal Setter** from `/plugins` in Codex:

```bash
codex plugin marketplace add gotalab/goal-setter-skill
```

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

### Any agent (skills CLI)

The cross-agent skills CLI (Codex, Claude Code, Cursor, and ~70 other agents) picks this repo up directly:

```bash
npx skills add gotalab/goal-setter-skill
```

It discovers `skills/goal-setter/` from the repo and links it into each agent's skill directory.

## Usage

**Draft** — get a reviewed condition without activating it:

> draft a goal for migrating our API client to v2

**Activate** — shape and launch in one motion:

> set a goal: all checkout tests pass after the refactor

goal-setter rebuilds the outcome, asks anything critical, drafts and audits the condition, then activates it through the runtime's own goal mechanism (see below). If the request is too small or too vague to make an honest goal, it says so and suggests a normal prompt instead.

## Example

Actual output, from running the skill on a small repo that uses `@acme/api-client` v1 (three modules under `src/api`, tests, and a `docs/v2-migration.md`).

What you type:

> set a goal: migrate src/api to the v2 client

goal-setter explores the repo, then shows you the outcome it reconstructed — note that it caught the v2 retry-default change from the migration doc on its own:

> Here's what I understand you want: migrate everything under src/api off the deprecated @acme/api-client (v1) onto @acme/sdk (v2, already in your dependencies at ^2.3.0), following docs/v2-migration.md — `createClient(opts)` instead of `new ApiClient(opts)`, `auth: { token | tokenProvider }` instead of the `authToken` callback, `retry: { attempts }` instead of `retries`, and `SdkError` instead of `ApiError` — with no behavior change for the code that calls these modules. I plan to: keep retries at 3 by passing `retry: { attempts: 3 }` explicitly (the v2 default changed from 0 to 2); keep the exported signatures of getUser, listUsers, createOrder, and makeScopedClient stable, except makeScopedClient's return type moves to the v2 client type; and remove @acme/api-client from package.json once nothing references it. Done means no v1 references remain in src/ or tests/ and `npm test`, `npm run build`, and `npm run lint` all pass. Correct me if any of that is off — otherwise I'll set the goal.

What gets activated (2,450 characters):

```text
/goal Context: this serves the shop-backend team by getting src/api off
the deprecated @acme/api-client v1 and onto the supported @acme/sdk v2
(already in dependencies) with no behavior change for callers. Migrate
all code under src/api from @acme/api-client to @acme/sdk per
docs/v2-migration.md, leaving zero v1 references and unchanged
caller-facing behavior. Verify through npm test, npm run build, and npm
run lint passing, plus a grep showing no @acme/api-client, ApiClient, or
ApiError references left in src/ or tests/. Read docs/v2-migration.md,
src/api/client.ts, and src/api/orders.ts first; discover adjacent tests
under tests/api as needed. Keep changes scoped to the migration and do
the simplest thing that meets it. Hard boundaries: preserve current retry
behavior by passing retry: { attempts: 3 } explicitly (the v2 default
changed from 0 to 2); keep the exported signatures and behavior of
getUser, listUsers, createOrder, and makeScopedClient stable for callers,
except makeScopedClient's return type moves to the v2 client type; map
ApiError handling to SdkError without changing .status semantics. Do not
alter other externally visible contracts, and do not make checks pass by
deleting, weakening, or skipping tests. Remove @acme/api-client from
package.json once no code references remain. Use available governed
read-only subagents when materially useful for separable triage,
validation discovery, or strategy review; before claiming Done, verify
the evidence with a fresh-context check (independent subagent or
equivalent), not self-review. Maintain a concise checklist with
checkpoint updates; before reporting progress, audit each claim against a
tool result from this run - unverified work is reported as unverified,
never as done. When you have enough information to act, act; never end a
turn on a plan or a promise. Done when src/ and tests/ contain no
@acme/api-client references, the v1 dependency is removed from
package.json, and npm test, npm run build, and npm run lint all pass. If
two approaches fail to improve the evidence, review strategy and pivot
within constraints; do not silently change the objective, Done condition,
evidence, or constraints. Stop only if @acme/sdk lacks a documented
equivalent for required behavior or validation stays blocked by the same
failure after 3 distinct attempts. The final report is for a reader who
watched none of the run: outcome first, plain words, in the user's
language.
```

The one line you typed is the entire input. Every file path, command, and boundary above came from exploring the repo and the migration doc.

## How activation works

goal-setter only uses the runtime's own goal mechanism. It never spawns child sessions or side processes to activate a goal.

| Runtime | Path |
|---|---|
| Codex | sets the goal itself via the native goal tool (`create_goal`) |
| Claude Code | hands you the exact `/goal …` line to send |

The difference exists because Claude Code (as of v2.1.170) has no tool a model can call to set a goal on the current session — `/goal` is a user command. So on Claude Code the skill prepares everything and you activate by sending that one line.

## What a goal covers

Every non-trivial goal includes: a one-line note on what the outcome serves and for whom · one objective · how success is verified · what to read first · the few hard boundaries this task could break, plus the rule against passing checks by weakening them · validation commands (or how to discover them) · subagent permission, including an independent check before Done · progress reported against tool results, in your language · a rule to keep acting instead of ending on a promise · pivot rules for stalled approaches · a binary Done condition · explicit stop conditions · a final report written for someone who did not watch the run.

Full reference: [`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## Structure

```text
.agents/plugins/marketplace.json   # Codex marketplace; points at ./plugins/goal-setter
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
plugins/goal-setter/
├── .codex-plugin/plugin.json      # Codex plugin manifest
└── skills/goal-setter/            # vendored copy for Codex plugin installs
```

Codex marketplace packaging uses the standard `./plugins/goal-setter` layout.
The root `skills/goal-setter/` folder remains for skill-only installs. Claude
Code packaging lives in `.claude-plugin/`.

## License

[MIT](LICENSE)
