# goal-setter

**Turn one short request into a Codex-native `/goal` contract that can launch the right threads, subagents, and verification before a long autonomous run drifts.**

Built for **Codex**. Works on **Claude Code** too.

[日本語](README.ja.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter icon: loose requests converging into a checked goal contract" width="180">
</p>

---

## Why

A goal keeps the agent working until a completion condition is true (official guides: [Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) / [Claude Code](https://code.claude.com/docs/en/goal)). Writing that condition well is real work: you have to state the outcome, how success is verified, what must not change, and when to stop. For Codex, you also have to say when work should stay in the main thread, when read-only subagents should verify or research, and when separate `create_thread` worktrees should own write units. Skip any of it and the run drifts — or worse, a parallel job quietly runs serially.

goal-setter exists for a simple reason: writing the goal instruction at all is a chore. You already have the finished picture in your head; what you actually type is one short line. This skill takes that line, rebuilds the picture, and checks with you until no outcome-changing ambiguity remains; questions come bundled, so it is usually one round trip. Then it carries the goal all the way to activation.

It pays off even if you are not lazy. Most goal helpers stop at a sharper completion sentence. goal-setter goes further: it turns the intended outcome into a runtime contract for the agent that will execute it. That contract includes stop conditions, the no-weakening-tests rule, independent verification, and the evaluator's quirks — Claude Code's judge only sees the conversation; Codex parallelism has to be spelled out the right way (subagents for read-only work, mandatory `create_thread` worktrees for non-trivial write units when the project supports them, bootstrap before fan-out, tool names not tool arguments), and it fires only from a `/goal` line *you* send. Writing that by hand every time is a lot of work, and hand-written goals drift from one run to the next. The gap between this skill's output and your hand-written goal is the value.

## What it does

- **Rebuilds the intended outcome first.** Before drafting anything, it reconstructs what you are trying to build and why, in a few sentences. When your request is minimal, it shows you that reconstruction to correct, bundling any critical questions into the same message; if ambiguity remains, it keeps asking until the outcome is safe. Success criteria, constraints, and the Done condition are all derived from it.
- **Asks only what changes the outcome.** Scope, verification, safety boundaries. Everything discoverable in the repo gets explored instead of asked; low-risk details become stated assumptions.
- **Writes a compact condition without stealing the model's judgment.** The goal text fixes *what*, *why*, evidence, and safety boundaries, then leaves *how* to the agent. No step-by-step recipes unless the steps are themselves the requirement.
- **Builds in stop and honesty rules.** Checks may not be passed by weakening them; stalled approaches trigger a strategy review, then a hard stop; the objective and Done condition cannot be quietly rewritten mid-run; progress may only be reported against actual tool results.
- **Turns parallel intent into executable Codex orchestration.** If the work should split, the goal says so in the form Codex actually responds to: read-only research/review/final verification goes to `spawn_agent`; non-trivial write units become mandatory `create_thread` worktrees when the project supports them; each child thread gets exactly one unit, owned files, evidence, an integration contract, and an instruction to set its own unit-scoped goal before editing.
- **Structures splittable work for parallelism.** When the outcome breaks into independent, separately verifiable units — a multi-module build, a multi-aspect review, multi-topic research — the goal carries the decomposition structure (a discovery rule, an owned surface and its own checks per unit, an integration check) plus a runtime-sized launch directive, often staged as a phased pipeline: bootstrap → parallel research → parallel implementation → integrate → parallel adversarial/final verification. Claude Code fans this out via a dynamic workflow on its own judgment. On Codex, the skill writes a user-sent `/goal …` line because that is what authorizes `spawn_agent` and `create_thread`.
- **Audits before activating.** Every goal is checked against the contract checklist before it is set. Anything missing gets fixed first. Length is verified once with a bundled validator that counts the way each runtime actually does — Codex counts Unicode codepoints, Claude Code counts UTF-16 code units, both allow exactly 4,000 — so a passing goal activates on either; a failing one gets restructured, never trimmed in loops.
- **Lightweight notes for day-scale work.** On long autonomous runs it keeps a concise `execution-notes.md` — progress checkpoints and the mid-run decisions made and why, for resume and audit. No `GOAL.md` scaffolding; the active `/goal` is the contract.

## Why this is different

There are several good skills that make `/goal` text clearer. goal-setter is tuned for the failure mode that appears after the goal is already clear: the agent chooses the wrong execution shape.

- A task that should use five workers runs one-by-one in the main thread.
- A write-heavy unit gets sent to a lightweight subagent instead of an isolated worktree.
- A child thread starts without a unit-scoped goal, so it drifts from the parent contract.
- Final verification is done by the same agent that wrote the code.

goal-setter bakes those decisions into the goal text before the run starts. It decides whether the work is serial or decomposable, names the parallel mechanism, separates read-only subagent work from write-thread work, tells child threads to set their own goals, and makes the main thread integrate evidence before Done.

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

goal-setter rebuilds the outcome, asks anything critical, drafts and runs a readiness check on the condition, then activates it through the runtime's own goal mechanism (see below). If the request is too small or too vague to make an honest goal, it says so and suggests a normal prompt instead.

## Before / after

These examples are shortened to show the shape. In a real run, goal-setter reads the repo or source material first, fills in the actual files and checks, and drops any clause that would not change the outcome.

### Small refactor

Before:

> set a goal: clean up checkout settings after the refactor

After:

```text
/goal Keep the checkout settings page behavior unchanged while removing
the duplicated loading/error-state branch introduced by the refactor.
Read the settings page component, adjacent tests, and the existing settings
UI patterns first. Keep the public props, billing copy, Stripe/webhook
behavior, and pricing logic unchanged; do not broaden the refactor.
Validate with the focused checkout settings tests and the repo's type/lint
check, all green; do not weaken or delete tests. Before Done, spawn a
read-only subagent to verify the diff against the preserved behavior and
checks; do not self-review. Done when the duplicate branch is gone, the UI
states still render, and all checks pass.
```

### Long implementation

Before:

> set a goal: build invoice export end to end

After:

```text
/goal Build an invoice CSV export that billing admins can run from the
existing admin surface without changing invoice calculation semantics.
Reconstruct the current billing data path, permissions, and export
conventions before editing. Choose the smallest design that fits the
existing admin patterns; do not rewrite billing models, payment flows, or
unrelated admin UI. Add focused tests for permissions, filters, empty
exports, and CSV escaping, plus an operator-visible success/failure path.
Keep concise execution-notes.md checkpoints for decisions and evidence.
Validate with the relevant unit/integration tests, typecheck, and a manual
or smoke path that downloads a representative CSV. Done only when tests
pass, the CSV matches the documented columns, and independent read-only
verification finds no billing behavior drift.
```

### Parallel implementation with `create_thread`

Before:

> set a goal: make the game factions affect events, enemies, bosses, rewards, HUD, save-load, and smoke evidence

After:

```text
/goal Make the faction ecosystem observable in one run: pressure and
player history change faction power, which changes room events, enemy
mutations, bosses, rewards, HUD, persistence, and browser smoke evidence.
Treat faction simulation, event generation, enemy/boss mutation,
rewards/relics, and HUD/smoke evidence as five separately verifiable write
units. In Codex, do not implement those units serially in the main thread.
First verify the repo is an established git project with a usable HEAD; if
not, bootstrap git + scaffold + shared interfaces in the main thread. Then
create one separate thread with create_thread per write unit, each in its
own worktree. In each child thread's initial prompt, assign exactly one
unit, owned files, validation evidence, integration contract, and instruct
it to set a unit-scoped goal before editing. Run child threads in parallel,
integrate in the main thread, and gate Done on every unit's evidence plus
build, tests, browser smoke, and a read-only subagent final verification.
```

### Business task

Before:

> set a goal: turn the messy QBR notes into something leadership can use

After:

```text
/goal Produce a leadership-ready QBR brief that turns the supplied notes
and source files into a decision document: current performance, risks,
decisions needed, and next actions. Read the notes, source sheets/docs, and
prior QBR format first. Separate confirmed facts from assumptions; do not
invent numbers, owners, customer quotes, or commitments. Preserve
uncertainty as "unconfirmed" when evidence is missing. Validate by mapping
every metric and material claim back to a named source, checking the brief
against the prior format, and spawning a read-only subagent to review for
unsupported claims. Done when the brief is ready to share and all open
questions are explicitly listed.
```

### Daily task

Before:

> set a goal: help me get the apartment application done

After:

```text
/goal Get the apartment application package ready for the user to submit,
without sending, signing, paying, or sharing private information without
explicit approval. Inventory the required documents, compare them with the
user's available files or notes, draft any missing message/checklist items,
and produce a clear submit-ready packet plus remaining blockers. Keep
sensitive data local and do not fabricate documents or dates. Done when
every required item is marked ready, missing, or needs user action, and the
final checklist says exactly what the user must review before submission.
```

## Example

Actual output, from running the skill on a small repo that uses `@acme/api-client` v1 (three modules under `src/api`, tests, and a `docs/v2-migration.md`).

What you type:

> set a goal: migrate src/api to the v2 client

goal-setter explores the repo, then shows you the outcome it reconstructed — note that it caught the v2 retry-default change from the migration doc on its own:

> Here's the outcome I understand you want, so the run starts aimed right: move the API layer of shop-backend (src/api/client.ts, users.ts, orders.ts) off the legacy `@acme/api-client` v1 onto the `@acme/sdk` v2 client, following docs/v2-migration.md — `createClient` instead of `new ApiClient`, `auth.tokenProvider` instead of the `authToken` callback, and `retry: { attempts: 3 }` kept explicit since v2's default changed. The exported functions (getUser, listUsers, createOrder, makeScopedClient) keep their current signatures and request behavior, so callers and the existing vitest tests are unaffected; `makeScopedClient`'s return type moves to the v2 client type. I'll assume removing the now-unused `@acme/api-client` from package.json is in scope, and success is verified by `npm test`, `npm run build`, and `npm run lint` all green with zero v1 references left in src/ and tests/. Correct anything here before I set the goal.

What gets activated (1,343 characters — the skill judged this a short, low-risk run and left out the operating rules that would not change it, such as step-by-step progress reporting, while keeping subagent permission, the no-weakening-tests rule, independent verification, and the stop rule):

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
Use read-only subagents where useful, and before claiming Done spawn a
read-only subagent to verify the diff against the migration doc; do not
self-review.
Done when grep finds zero @acme/api-client references in src/ and tests/
and all three checks pass.
If a v1 behavior has no v2 equivalent, stop and ask rather than approximate.
Final report: outcome first, plain words, in English.
```

The one line you typed is the entire input. Every file path, command, and boundary above came from exploring the repo and the migration doc.

The shape is deliberate. The opening line states the intent — what the outcome serves and for whom; here it carries an optional `Context:` label to mark it as background rather than a requirement, but it can equally be plain prose, since the goal needs no labeled fields. Everything after it is plain prose where each contract element starts its own sentence with a fixed marker: `Read … first` (context), `Keep changes scoped` (constraints), `Validate with` (checks), `Done when` (the binary condition — on Claude Code the separate evaluator keys on this sentence), `… stop and ask` (the only legitimate exit), `Final report:`. Prose rather than labeled fields, because prose keeps the causal connections — *keep attempts explicit **since** the v2 default changed* — that a `Constraints:` list would flatten.

## How activation works

goal-setter only uses the runtime's own goal mechanism. It never spawns child sessions or side processes to activate a goal.

| Runtime | Path |
|---|---|
| Codex (ordinary) | sets the goal itself via the native goal tool (`create_goal`) |
| Codex (decomposable / parallel) | hands you the `/goal …` line to send — see below |
| Claude Code | hands you the exact `/goal …` line to send |

On Claude Code, `/goal` is a user command (no tool can set a goal on the current session as of v2.1.170), so the skill prepares everything and you send the one line. On Codex the skill normally sets the goal itself — **except for decomposable work where you want parallelism**: Codex's `create_thread`/`spawn_agent` fire only on *your* typed request, not on a tool-set goal, so the skill hands you the `/goal …` line and your sending it is what authorizes the parallel cascade.

## Running it in parallel

When the outcome splits into independent, separately verifiable units — a multi-module build, a multi-aspect review, multi-topic research — the goal carries the decomposition structure: a discovery rule, an owned surface and its own checks per unit, and an integration/synthesis check over the merged result. Large work often stages as a **phased pipeline**: (0) the main thread bootstraps a shared baseline, (1) parallel read-only research to clarify scope, (2) parallel write implementation, (3) integrate, (4) parallel adversarial/final verification. How it runs depends on the runtime:

- **Claude Code** realizes the goal's explicit fan-out invitation as a dynamic workflow on its own judgment — it discovers the units, dispatches them in parallel (subagents for read-only stages, worktree isolation for write stages), and synthesizes. The goal describes the structure and says "fan out in parallel"; it leaves the mechanism to the run.
- **Codex** has its parallel tools gated to *your* own typed request, not to a goal the skill sets behind the scenes — so for decomposable work the skill hands you a `/goal …` line, and your sending it authorizes the whole cascade. The directives encode four things real runs taught us: **subagents (`spawn_agent`) are for read-only work** (research, review, final verification); **non-trivial write units use `create_thread` as a mandatory worktree fan-out when an established project exists** — one separate thread per unit, each with owned files, evidence, and a unit-scoped goal set from the child thread's initial prompt; **bootstrap comes first** — on an empty or non-git workspace the main thread does git init + scaffold + committed interface contracts before any write fan-out; and the goal **names the tool, not its arguments** (spelling out a `projectId` the executor cannot see makes it give up and run serially). If `create_thread` is unavailable or not worth the worktree cost, the goal must say so explicitly instead of hiding it behind an "or" fallback.

This covers not just builds but multi-aspect reviews and multi-topic research — the same split-and-integrate structure.

## What a goal covers

Every non-trivial goal includes: a one-line note on what the outcome serves and for whom · one objective · how success is verified · what to read first · the few hard boundaries this task could break, plus the rule against passing checks by weakening them · validation commands (or how to discover them) · what may be delegated to subagents, with an independent check before Done · progress reported against tool results, in your language · a rule to keep acting instead of ending on a promise · pivot rules for stalled approaches · a binary Done condition · explicit stop conditions · a final report written for someone who did not watch the run.

The contract scales with the run: short low-risk tasks get short contracts, and clauses that would not change the run are dropped — a long goal crowds out the model's own judgment.

It all lives in one file: [`skills/goal-setter/SKILL.md`](skills/goal-setter/SKILL.md).

## Structure

```text
.agents/plugins/marketplace.json   # Codex marketplace; points at ./plugins/goal-setter
skills/goal-setter/
├── SKILL.md                      # the whole skill — one self-contained file
├── scripts/
│   └── validate_goal_length.py   # runtime-accurate length check (codepoints + UTF-16 units)
└── agents/openai.yaml            # Codex surface metadata
plugins/goal-setter/
├── .codex-plugin/plugin.json      # Codex plugin manifest
└── skills/goal-setter/            # vendored copy for Codex plugin installs
```

The skill is a single `SKILL.md` (plus the length helper) — no reference set, no progressive disclosure.

Codex marketplace packaging uses the standard `./plugins/goal-setter` layout.
The root `skills/goal-setter/` folder remains for skill-only installs. Claude
Code packaging lives in `.claude-plugin/`.

## License

[MIT](LICENSE)
