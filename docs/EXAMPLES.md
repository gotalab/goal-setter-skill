# Examples

These examples show the shape of goal-setter output. In a real run,
goal-setter reads the repo or source material first, fills in the actual files
and checks, and drops clauses that would not change the run.

## Small Refactor

Before:

```text
set a goal: clean up checkout settings after the refactor
```

After:

```text
/goal Keep the checkout settings page behavior unchanged while removing the
duplicated loading/error-state branch introduced by the refactor. Read the
settings page component, adjacent tests, and existing settings UI patterns
first. Keep public props, billing copy, Stripe/webhook behavior, and pricing
logic unchanged; do not broaden the refactor. Validate with the focused
checkout settings tests and the repo's type/lint check, all green; do not
weaken or delete tests. Before Done, spawn a read-only subagent to verify the
diff against the preserved behavior and checks; do not self-review. Done when
the duplicate branch is gone, UI states still render, and all checks pass.
```

## Long Implementation

Before:

```text
set a goal: build invoice export end to end
```

After:

```text
/goal Build an invoice CSV export that billing admins can run from the existing
admin surface without changing invoice calculation semantics. Reconstruct the
current billing data path, permissions, and export conventions before editing.
Choose the smallest design that fits existing admin patterns; do not rewrite
billing models, payment flows, or unrelated admin UI. Add focused tests for
permissions, filters, empty exports, CSV escaping, and operator-visible
success/failure paths. Keep concise execution-notes.md checkpoints for decisions
and evidence. Validate with relevant unit/integration tests, typecheck, and a
manual or smoke path that downloads a representative CSV. Done only when tests
pass, the CSV matches the documented columns, and independent read-only
verification finds no billing behavior drift.
```

## Parallel Implementation With `create_thread`

Before:

```text
set a goal: make the game factions affect events, enemies, bosses, rewards,
HUD, save-load, and smoke evidence
```

After:

```text
/goal Make the faction ecosystem observable in one run: pressure and player
history change faction power, which changes room events, enemy mutations,
bosses, rewards, HUD, persistence, and browser smoke evidence. Treat faction
simulation, event generation, enemy/boss mutation, rewards/relics, and HUD/smoke
evidence as separately verifiable write units. In Codex, do not implement those
units serially in the main thread. First verify the repo is an established git
project with a usable HEAD; if not, bootstrap git + scaffold + shared
interfaces in the main thread. Then create one separate thread with
create_thread per write unit, each in its own worktree. In each child thread's
initial prompt, assign exactly one unit, owned area, validation evidence,
integration contract, and instruct it to set a unit-scoped goal before editing.
Run child threads in parallel, integrate in the main thread, and gate Done on
every unit's evidence plus build, tests, browser smoke, and a read-only subagent
final verification.
```

## Business Task

Before:

```text
set a goal: turn the messy QBR notes into something leadership can use
```

After:

```text
/goal Produce a leadership-ready QBR brief that turns the supplied notes and
source files into a decision document: current performance, risks, decisions
needed, and next actions. Read the notes, source sheets/docs, and prior QBR
format first. Separate confirmed facts from assumptions; do not invent numbers,
owners, customer quotes, or commitments. Preserve uncertainty as "unconfirmed"
when evidence is missing. Validate by mapping every metric and material claim
back to a named source, checking the brief against the prior format, and
spawning a read-only subagent to review for unsupported claims. Done when the
brief is ready to share and all open questions are explicitly listed.
```

## Daily Task

Before:

```text
set a goal: help me get the apartment application done
```

After:

```text
/goal Get the apartment application package ready for the user to submit,
without sending, signing, paying, or sharing private information without
explicit approval. Inventory the required documents, compare them with the
user's available files or notes, draft any missing message/checklist items, and
produce a clear submit-ready packet plus remaining blockers. Keep sensitive data
local and do not fabricate documents or dates. Done when every required item is
marked ready, missing, or needs user action, and the final checklist says
exactly what the user must review before submission.
```

## Detailed Migration Example

Input:

```text
set a goal: migrate src/api to the v2 client
```

goal-setter first reconstructs the outcome. For example:

```text
Here's the outcome I understand you want, so the run starts aimed right: move
the API layer of shop-backend (src/api/client.ts, users.ts, orders.ts) off the
legacy @acme/api-client v1 onto the @acme/sdk v2 client, following
docs/v2-migration.md. createClient replaces new ApiClient, auth.tokenProvider
replaces the authToken callback, and retry: { attempts: 3 } stays explicit
because the v2 default changed. The exported functions keep their current
signatures and request behavior. Success is verified by npm test,
npm run build, and npm run lint all green with zero v1 references left in src/
and tests/. Correct anything here before I set the goal.
```

Activated goal:

```text
/goal This keeps shop-backend on the supported @acme/sdk v2 client so the API
layer stays current and maintainable. Migrate src/api (client.ts, users.ts,
orders.ts) from @acme/api-client v1 to @acme/sdk v2 per docs/v2-migration.md:
createClient replaces new ApiClient, the authToken callback becomes
auth.tokenProvider, and retries: 3 becomes retry: { attempts: 3 } -- keep
attempts explicit since the v2 default changed. Update the exported
makeScopedClient return type to the v2 client type, switch any ApiError handling
to SdkError, and remove @acme/api-client from package.json once unused. Read
docs/v2-migration.md first. Keep changes scoped to the migration: exported
src/api functions keep their current signatures and request behavior; no
refactors or features beyond it. Validate with npm test, npm run build, and
npm run lint, all green; do not weaken, skip, or delete tests. Before claiming
Done, spawn a read-only subagent to verify the diff against the migration doc;
do not self-review. Done when grep finds zero @acme/api-client references in
src/ and tests/ and all three checks pass. If a v1 behavior has no v2
equivalent, stop and ask rather than approximate.
```
