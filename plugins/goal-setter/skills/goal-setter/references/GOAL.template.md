# Goal Run: {{title}}

Run ID: `{{run_id}}`
Created: {{created_at}}

## Objective

Opening line (what this outcome serves and for whom, from the intended outcome image — plain prose; a `Context:` label is optional): ...

{{objective}}

Keep this run focused on the user's requested outcome. Do not shrink or reinterpret that outcome; minimize only the surrounding prompt. Preserve evidence, constraints, validation, explicit subagent/delegation authorization, progress visibility, Done, and On block rules; avoid adding routine implementation sequencing or optional operations that do not change Done.

## Context to read first

- `AGENTS.md` if present
- The user-provided request, spec, issue, screenshots, or failing logs
- Relevant tests and docs discovered in the project

Add concrete files here when known:

- ...

## Evidence surface / verification environment

- Where the final result can be checked: ...
- If this surface is missing or unrealistic, create the smallest practical verification surface or stop if that requires unavailable credentials, services, devices, data, or user approval.

## Constraints

- Keep changes scoped to the requested outcome and directly related tests/docs; do the simplest thing that meets the objective — no refactors, features, or abstractions beyond it, no unrelated cleanup.
- Task-specific hard boundaries (name the 1-3 this task could actually break, e.g. public API signatures, schema, auth behavior):
  - ...
- Do not alter other externally visible contracts or cross destructive boundaries unless the spec explicitly requires it.
- Prefer the smallest reversible assumption when the spec is incomplete.
- Do not satisfy metrics by deleting, weakening, bypassing, or narrowing required behavior, tests, data, sources, or review criteria unless explicitly approved.
- Record material assumptions and tradeoffs in `execution-notes.md`.

## Validation

{{validation}}

Use measurable checks when they are meaningful, and use observable evidence when a brittle metric would distort the work. When a verified behavior has distinct outcome classes (success, failure, unreachable, timeout), exercise each relevant class, constructing a case when one does not occur naturally; a check that could not have failed proves nothing.

Known required checks:

- ...

If a check cannot be run, record why in `execution-notes.md` and use the next best available check.

For visual goals, convert references into checklist or design-system criteria where possible. Do not chase pixel-perfect asset recreation unless the user explicitly requires it.

## Subagents and context separation

Use available governed subagents when they materially improve end-to-end completion. Subagents are explicitly authorized for separable investigation, source-backed research, validation discovery, test-failure triage, strategy review when progress stalls, and final review. Prefer read-only subagents unless an external side effect is required, allowed by policy, and part of this Goal. Keep this authorization explicit even when compressing the native Goal launcher.

Use research to resolve a concrete decision, validate an assumption, compare an implementation option, or understand a required external interface. When research uses external or fast-moving information, include source links, dates where relevant, and a short note on how the finding affects this Goal.

Merge concise, actionable findings into `execution-notes.md`. Do not create separate run-management report files unless the user explicitly asks or a bulky evidence artifact is genuinely needed.

Use service agents, MCP tools, network access, browser/computer use, and app-backed actions when they are available, allowed by policy, and materially improve this Goal. Treat them as governed capabilities rather than forbidden extras. If a required capability is blocked, do not mark the Goal done by substituting weaker evidence; ask for approval or stop under On block with the smallest needed capability.

External side-effecting actions such as PR creation, issue comments, deployments, CRM updates, document edits, or emails may be part of this Goal when end-to-end completion requires them. Let the runtime's approval and managed-policy system decide whether they can proceed. If approval is denied or unavailable, preserve the completed internal work and report the exact remaining external action.

For separable multi-item work, prefer item-by-item progress: act on and verify each discovered item as soon as it is ready. Wait for the full set only when all prior results are needed for deduplication, cross-item comparison, zero-result early exit, or a prompt that explicitly depends on the full set. Do not use large fan-out, dynamic workflows, or many agents unless this Goal or the user explicitly opts into that scale with a bounded surface, ownership split or routing rule, merge/review evidence, and any cap on parallel agents or retries.

This work splits into independent, separately verifiable sub-outcomes that share no state. Treat each discovered unit as a piece that owns only its files, work unit by unit, and gate Done on every unit's evidence plus an integration check over the merged result. Large work often stages as a phased pipeline: (0) the main thread bootstraps a shared baseline, (1) parallel read-only research, (2) parallel write implementation, (3) integrate, (4) parallel adversarial/final verification — use the phases that fit. On Claude Code the run may fan out through a dynamic workflow on its own judgment (subagents for read-only stages, worktree isolation for write stages). On Codex, orchestrate from this main thread: if the workspace is empty or not yet git-backed, first bootstrap it here (git init, build/test scaffold, committed interface contracts) before any write fan-out; spawn read-only subagents (`spawn_agent`) to research/review/verify without self-reviewing; fan out write units in parallel — `spawn_agent` over strictly partitioned files, or `create_thread` per unit (each in its own worktree with a goal scoped to that unit) when an established project exists; name the tool, not its arguments (no `projectId` or other schema fields — work in the current workspace and let the runtime resolve the location). Integrate and validate here, autonomously. (Drop this paragraph when the work is not decomposable — interlocking files, a single-cause investigation, or a serially tuned metric — and keep one write contract.)

For broad review, audit, research, migration, or bug-finding work, state the intended coverage bound. If scope is sampled, capped, skipped, retried only a fixed number of times, or narrowed during execution, record the limit and why it is acceptable in `execution-notes.md` and the final response.

## Progress and pivot

Keep progress visible in whatever form fits the run — a concise checklist with per-item status (e.g. not started / in progress / complete / blocked) is the usual default. At meaningful checkpoints, report in the user's language (match the language of the request): progress made, evidence confirmed, remaining work, and next step. Before reporting progress, audit each claim against a tool result from this run; unverified work is reported as unverified, never as done. Do not update so often that reporting displaces execution.

When you have enough information to act, act: do not ask permission for reversible in-scope actions, and never end a turn on a plan, a self-answerable question, or a promise about work not yet done — do that work now. On block rules define the only legitimate stops. If a design judgment is needed, record the adopted option and reason instead of leaving ambiguity hidden. If commits are explicitly in scope, summarize implemented changes, validation, and next actions before and after committing.

Compare progress against the Done condition using evidence, not effort spent. If two distinct approaches fail to improve the evidence surface, use read-only strategy review when available, preferably with a subagent; otherwise do a short self-review. Diagnose why progress is stalled, and decide whether to continue, narrow tactics without narrowing the requested outcome, change approach, improve validation, or stop under On block.

Apply the smallest bounded pivot that preserves the Goal constraints. You may change tactics, sequencing, validation discovery, implementation approach, or a reversible low-risk assumption when that makes the same Done condition more achievable. Small self-improvements are expected when they protect the real user outcome: tighten or replace a weak validation method with a better discovered one, refine an observable Done criterion, add a better evidence artifact, or clarify a low-risk assumption, as long as the objective and requested outcome are not narrowed or changed.

Do not silently change this Goal's objective, Done condition, evidence surface, safety constraints, approval boundaries, or final coverage claim. If those need to change, record the reason and proposed before/after wording in `execution-notes.md`, then stop under On block and ask for the smallest user decision unless the user already gave explicit authority for that class of change.

Safe refinements do not require a Goal amendment when they only tighten evidence, add or replace discovered validation, add newly discovered context files, improve the observable Done wording, clarify a low-risk reversible assumption, or narrow implementation tactics without narrowing the requested outcome. Record material refinements in `execution-notes.md`, but continue autonomously.

If the Goal itself appears invalid, unsafe, materially underspecified, or impossible to satisfy with honest evidence, stop under On block and ask for the smallest user decision.

When completeness matters, continue discovery until the explicit coverage bound is met or until fresh findings dry up under the chosen method. Do not turn this into an unbounded search; if the dry-up rule is not appropriate, use the smallest explicit coverage rule that makes the final claim honest.

## Done when

- The requested behavior is implemented.
- The evidence surface confirms the requested final state.
- Measurable targets are met where defined.
- Required validation passes, or any remaining failure is proven unrelated and documented with evidence.
- Broad or sampled work records the coverage bound and any omitted areas.
- Before Done is claimed, an independent read-only pass verifies the evidence — not self-review. On Codex, spawn a read-only subagent (`spawn_agent`) to do this and do not self-review (the bare phrase "fresh-context check" launches nothing there); elsewhere, an independent subagent or equivalent. Findings that touch correctness, safety, or this Done condition are fixed; other findings are either fixed or kept with the reason recorded in `execution-notes.md` — the executor's call.
- `execution-notes.md` is current and reviewable.
- The final diff is scoped to intended code/tests/docs plus this run's two files.
- The final response is written for a reader who watched none of the run — outcome first, plain words, in the user's language — and summarizes implementation, evidence, decisions needing user review, and any decisions this Goal left undefined that were settled by judgment.

## On block

Stop and report if:

- Required behavior cannot be safely inferred from the available spec/context.
- Validation fails for the same blocker after 3 distinct approaches with no improvement, with each approach and result recorded in `execution-notes.md`.
- Completing the task requires forbidden scope changes.
- A required service agent, MCP server, app action, network path, browser/computer capability, approval, or writable location is blocked and no honest in-sandbox substitute can satisfy Done.
- Missing credentials, external services, or unavailable artifacts block validation.
- A decision would affect schema, public API, auth, security, billing, data retention, or production dependencies without explicit permission.

Do not stop merely because:

- the first validation command fails
- the validation command is unknown and can be discovered from repo docs, scripts, package metadata, or nearby CI config
- a small reversible implementation choice is needed
- a separable investigation, research task, or final review can be delegated to a read-only subagent
- an external action needs approval and the runtime can request it
- notes need to be updated before continuing

When blocked, report:

- current state
- evidence collected
- attempted fixes
- exact blocker
- smallest user decision needed

## Compact goal objective

```text
Execute `{{goal_path}}` as the completion contract. Work autonomously until its Done when is satisfied by evidence, preserving its constraints, validation, progress/pivot, and On block rules. Keep `{{notes_path}}` current only at meaningful checkpoints with material decisions, evidence, coverage limits, blockers, and final review. Do not restate or expand the plan in the native Goal; stop only under `GOAL.md` On block rules.
```
