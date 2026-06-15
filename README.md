# goal-setter

**Turn one short request into a `/goal` condition you can trust with a long autonomous run.**

Built for **Codex**. Works on **Claude Code** too.

[日本語](README.ja.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter icon: loose requests converging into a checked goal contract" width="180">
</p>

---

## Why

A goal keeps the agent working until a completion condition is true (official guides: [Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) / [Claude Code](https://code.claude.com/docs/en/goal)). Writing that condition well is real work: you have to state the outcome, how success is verified, what must not change, and when to stop. Skip any of it and the run drifts — a goal runs unattended, so a weak starting condition is amplified for hours.

goal-setter exists for a simple reason: writing the goal instruction at all is a chore. You already have the finished picture in your head; what you actually type is one short line. This skill takes that line, rebuilds the picture, and checks with you until no outcome-changing ambiguity remains; questions come bundled, so it is usually one round trip. Then it carries the goal all the way to activation.

It pays off even if you are not lazy. Folding in the stop conditions, the no-weakening-tests rule, and the evaluator's quirks — Claude Code's judge only sees the conversation; Codex parallelism has to be spelled out (an imperative `create_thread` directive in the goal, or `spawn` subagents from your prompt) — by hand, every time, is a lot of work, and hand-written goals drift from one run to the next. The gap between this skill's output and your hand-written goal is the value.

## What it does

- **Rebuilds the intended outcome first.** Before drafting anything, it reconstructs what you are trying to build and why, in a few sentences. When your request is minimal, it shows you that reconstruction to correct, bundling any critical questions into the same message; if ambiguity remains, it keeps asking until the outcome is safe. Success criteria, constraints, and the Done condition are all derived from it.
- **Asks only what changes the outcome.** Scope, verification, safety boundaries. Everything discoverable in the repo gets explored instead of asked; low-risk details become stated assumptions.
- **Writes a compact condition.** The goal text fixes *what* and *why* and leaves *how* to the agent. No step-by-step recipes.
- **Builds in stop and honesty rules.** Checks may not be passed by weakening them; stalled approaches trigger a strategy review, then a hard stop; the objective and Done condition cannot be quietly rewritten mid-run; progress may only be reported against actual tool results.
- **States delegation and independent verification.** The goal names what may be delegated and requires a fresh-context check (an independent subagent or equivalent) before Done. Claude Code fans out on its own judgment; on Codex the `spawn` subagent tool waits for your explicit prompt, while `create_thread` parallelism is written into the goal itself.
- **Structures splittable work for parallelism.** When the outcome breaks into independent, separately verifiable units — a multi-module build, a multi-aspect review, multi-topic research — the goal carries the decomposition structure (a discovery rule, an owned surface and its own checks per unit, an integration check) plus a runtime-sized launch directive: Claude Code fans out via a dynamic workflow, and on Codex the goal spells out an imperative `create_thread` orchestration — a separate thread per unit, each in its own worktree with its own goal — that runs autonomously.
- **Audits before activating.** Every goal is checked against the contract checklist before it is set. Anything missing gets fixed first. Length is verified once with a bundled validator that counts the way each runtime actually does — Codex counts Unicode codepoints, Claude Code counts UTF-16 code units, both allow exactly 4,000 — so a passing goal activates on either; a failing one gets restructured, never trimmed in loops.
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

> Here's the outcome I understand you want, so the run starts aimed right: move the API layer of shop-backend (src/api/client.ts, users.ts, orders.ts) off the legacy `@acme/api-client` v1 onto the `@acme/sdk` v2 client, following docs/v2-migration.md — `createClient` instead of `new ApiClient`, `auth.tokenProvider` instead of the `authToken` callback, and `retry: { attempts: 3 }` kept explicit since v2's default changed. The exported functions (getUser, listUsers, createOrder, makeScopedClient) keep their current signatures and request behavior, so callers and the existing vitest tests are unaffected; `makeScopedClient`'s return type moves to the v2 client type. I'll assume removing the now-unused `@acme/api-client` from package.json is in scope, and success is verified by `npm test`, `npm run build`, and `npm run lint` all green with zero v1 references left in src/ and tests/. Correct anything here before I set the goal.

What gets activated (1,352 characters — the skill judged this a short, low-risk run and left out the operating rules that would not change it, such as step-by-step progress reporting, while keeping subagent permission, the no-weakening-tests rule, independent verification, and the stop rule):

```text
/goal Context: this keeps shop-backend on the supported @acme/sdk v2 client
so the API layer stays current and maintainable.
Migrate src/api (client.ts, users.ts, orders.ts) from @acme/api-client v1
to @acme/sdk v2 per docs/v2-migration.md: createClient replaces new
ApiClient, the authToken callback becomes auth.tokenProvider, and
retries: 3 becomes retry: { attempts: 3 } — keep attempts explicit since
the v2 default changed. Update the exported makeScopedClient return type
to the v2 client type, switch any ApiError handling to SdkError, and
remove @acme/api-client from package.json once unused.
Read docs/v2-migration.md first.
Keep changes scoped to the migration: the functions exported from src/api
keep their current signatures and request behavior (paths, query shapes,
retry count); no refactors or features beyond it.
Validate with npm test, npm run build, and npm run lint, all green; do
not weaken, skip, or delete tests to make them pass.
Use read-only subagents where useful, and before claiming Done have a
fresh-context check (independent subagent or equivalent) confirm the diff
against the migration doc.
Done when grep finds zero @acme/api-client references in src/ and tests/
and all three checks pass.
If a v1 behavior has no v2 equivalent, stop and ask rather than approximate.
Final report: outcome first, plain words, in English.
```

The one line you typed is the entire input. Every file path, command, and boundary above came from exploring the repo and the migration doc.

The shape is deliberate. `Context:` is the only label — it marks the opening line as background, not a requirement to verify. Everything after it is plain prose where each contract element starts its own sentence with a fixed marker: `Read … first` (context), `Keep changes scoped` (constraints), `Validate with` (checks), `Done when` (the binary condition — on Claude Code the separate evaluator keys on this sentence), `… stop and ask` (the only legitimate exit), `Final report:`. Prose rather than labeled fields, because prose keeps the causal connections — *keep attempts explicit **since** the v2 default changed* — that a `Constraints:` list would flatten.

## How activation works

goal-setter only uses the runtime's own goal mechanism. It never spawns child sessions or side processes to activate a goal.

| Runtime | Path |
|---|---|
| Codex (ordinary) | sets the goal itself via the native goal tool (`create_goal`) |
| Codex (decomposable / parallel) | hands you the `/goal …` line to send — see below |
| Claude Code | hands you the exact `/goal …` line to send |

On Claude Code, `/goal` is a user command (no tool can set a goal on the current session as of v2.1.170), so the skill prepares everything and you send the one line. On Codex the skill normally sets the goal itself — **except for decomposable work where you want parallelism**: Codex's `create_thread`/`spawn` fire only on *your* typed request, not on a tool-set goal, so the skill hands you the `/goal …` line and your sending it is what authorizes the parallel cascade.

## Running it in parallel

When the outcome splits into independent, separately verifiable units — a multi-module build, a multi-aspect review, multi-topic research — the goal carries the decomposition structure: a discovery rule, an owned surface and its own checks per unit, and an integration/synthesis check over the merged result. How it runs in parallel depends on the runtime:

- **Claude Code** fans out on its own judgment — typically a dynamic workflow that discovers the units, dispatches them in parallel, and synthesizes the results. No extra instruction needed.
- **Codex** uses `create_thread` as the default. Its `create_thread`/`spawn` tools fire only on *your* own typed request, not on a goal the skill sets behind the scenes — so for decomposable work the skill hands you a `/goal …` line carrying an imperative directive (open a separate thread per unit, each in its own worktree with its own goal, run them in parallel, then integrate in the main thread, autonomously). You send that one line; that single action authorizes the whole cascade — threads, their per-unit goals, and subagents. `spawn` subagents are the lighter alternative (`Spawn one agent per <unit> and run them in parallel`).

This covers not just builds but multi-aspect reviews and multi-topic research — the same split-and-integrate structure.

## What a goal covers

Every non-trivial goal includes: a one-line note on what the outcome serves and for whom · one objective · how success is verified · what to read first · the few hard boundaries this task could break, plus the rule against passing checks by weakening them · validation commands (or how to discover them) · what may be delegated to subagents, with an independent check before Done · progress reported against tool results, in your language · a rule to keep acting instead of ending on a promise · pivot rules for stalled approaches · a binary Done condition · explicit stop conditions · a final report written for someone who did not watch the run.

The contract scales with the run: short low-risk tasks get short contracts, and clauses that would not change the run are dropped — a long goal crowds out the model's own judgment.

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
│   ├── validate_goal_length.py   # runtime-accurate length check (codepoints + UTF-16 units)
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
