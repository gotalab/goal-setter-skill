# Sidecars and Notes Reference

Read this before creating, updating, auditing, or activating sidecar files. Do not load it for ordinary inline-only Draft mode unless sidecars are being considered.

## When to Use Sidecars

Create sidecar files only when they are useful for durable audit, resume, or plan/spec ownership.

Sidecars are a pressure valve for long contracts, not a default ceremony. Use them to keep the native Goal text short when the work genuinely needs durable notes, a plan/spec-owned contract, or auditable resume state. Do not create sidecars just because an inline Goal would require careful compression.

Create exactly two goal run files:

- `GOAL.md`
- `execution-notes.md`

Do not create extra run-management files such as `INDEX.md`, `validation-log.md`, `subagents.md`, or subagent report files unless the user explicitly asks or a bulky evidence artifact is genuinely needed for review.

## Storage Policy

Never create run-specific notes inside the global skill/plugin directory.

Preferred locations:

- If the user activates an existing plan directory such as `docs/plans/<plan-id>/`, create sidecars directly in that directory.
- If the user activates from a spec or plan file and sidecars are useful, prefer the directory that already owns that plan/spec when it is writable.
- If there is no existing plan/spec directory, prefer user state outside the repo for external/general use unless sandbox or enterprise policy makes repo-external writes unavailable.
- Use project-local custom roots only when the user explicitly asks for one.
- Do not create `.agents/goal-runs/` by default; `.agents` is often owned by other agent state systems.

In sandboxed or enterprise-managed environments, do not make repo-external sidecar storage a prerequisite for a good Goal. Prefer inline goals, an already-writable plan/spec directory, or an explicit writable run root. If none is available, emit the compact inline goal or ask for the smallest writable-location decision.

Plan/spec-sidecar layout:

```text
docs/plans/<plan-id>/
  GOAL.md
  execution-notes.md
```

User-state layout:

```text
$XDG_STATE_HOME/codex/goal-runs/<project-fingerprint>/<run-id>/
  GOAL.md
  execution-notes.md
```

On macOS when `$XDG_STATE_HOME` is absent:

```text
~/Library/Application Support/Codex/goal-runs/<project-fingerprint>/<run-id>/
```

Project-local custom layout, only when explicitly requested:

```text
<custom-dir>/<run-id>/
  GOAL.md
  execution-notes.md
```

## Run ID Format

Create run IDs that are ordered, readable, and searchable.

Format:

```text
<seq4>--<YYYY-MM-DD-HHMMSS>--<area-slug>--<outcome-slug>
```

Example:

```text
0007--2026-05-21-153012--checkout--confirmation-flow
```

Rules:

- For user-state or custom run roots, `<seq4>` is the next 4-digit sequence under that root.
- For plan-sidecar goals, the plan directory name can be the stable run ID when it is already ordered and searchable.
- Timestamp uses local time from the environment.
- `<area-slug>` names the module/domain.
- `<outcome-slug>` describes the desired result in searchable words.
- Use meaningful words over opaque IDs.
- Keep the run ID stable after creation.
- For Japanese or non-English requests, preserve searchable local-language keywords when useful, but prefer simple hyphen-separated terms.

## GOAL.md

Use `references/GOAL.template.md` when creating sidecar files. The generated file must include:

Before filling or auditing `GOAL.md`, read `references/goal-contract.md`. If the Goal uses subagents, service agents, MCP/tools, network access, app actions, approvals, enterprise policy, broad fan-out, or broad coverage claims, also read `references/runtime-capabilities.md` before filling `Subagents and context separation`, `Progress and pivot`, `Done when`, and `On block`.

1. `# Goal Run: <short title>`
2. `Run ID`
3. `Objective`
4. `Context to read first`
5. `Evidence surface / verification environment`
6. `Constraints`
7. `Validation`
8. `Subagents and context separation`
9. `Progress and pivot`
10. `Done when`
11. `On block`
12. `Compact set_goal objective`

## execution-notes.md

Use `references/execution-notes.template.md` for sidecar runs. The run notes file is always named `execution-notes.md`.

`execution-notes.md` is a review artifact, not a diary. It should let a reviewer answer:

- What is the current state?
- What material decisions or pivots were made, and why?
- What evidence proves progress or failure?
- What remains risky, blocked, or user-review-needed?

Standard sections:

- Summary
- Decisions
- Spec gaps / assumptions
- Changes beyond the literal spec
- Tradeoffs
- Subagent findings
- Validation
- Known risks / follow-ups
- Final review

Every material decision should record:

- what was decided
- why the decision was needed
- alternatives considered, if any
- risk
- whether user review is needed

Validation results belong in `execution-notes.md`; do not create a separate validation log unless requested or the raw output is itself a bulky evidence artifact.

Update notes only at meaningful checkpoints: material decision, phase boundary, validation result, subagent finding, blocker risk, or final review.

Bounded notes policy:

- Preserve material decisions, reasons, active assumptions, validation failures, unresolved risks, user-review-needed items, evidence pointers, coverage limits, skipped areas, sampling rules, accepted completeness tradeoffs, and accepted pivots.
- Replace stale status summaries instead of appending duplicate paragraphs.
- Keep tables to review-relevant rows.
- Roll resolved or superseded detail into `Summary`, `Known risks / follow-ups`, or `Final review` only when the reason/evidence remains clear.
- Do not paste raw command output, long research notes, screenshots, transcripts, or full subagent reports.
- If raw detail is necessary for review, save or reference it using the project's existing artifact convention. Ask before inventing a new sidecar report file.

## Helper Script

Use `scripts/init_goal_run.py` when helpful, but do not require it. The helper expects a local `python3` executable plus permission to write the chosen sidecar directory. If `python3` is unavailable, shell execution is blocked, the target path is not writable, or direct file creation is simpler, create the two files directly from the templates or use an inline goal.

In sandboxed environments, pass `--plan-dir` or `--run-root` pointing to an already-writable location, or skip the helper and use an inline goal.

When validating Python helper syntax in read-only skill locations, do not use `python3 -m py_compile`; it creates `__pycache__` beside the checked file. Use `python3 -B scripts/check_python_syntax.py <file.py>` for read-only syntax checks, and use `python3 -B <script.py> ...` for helper execution.

Example:

```bash
python3 -B <skill-path>/scripts/init_goal_run.py \
  --area checkout \
  --outcome confirmation-flow \
  --title "Checkout confirmation flow" \
  --objective "Implement the checkout confirmation flow and verify it with checkout tests."
```

After creating sidecars, set the native goal with the `Compact set_goal objective` from `GOAL.md`, or emit the exact `/goal ...` command when no native goal tool is visible.

The compact launcher objective should only point to `GOAL.md`, require updates to `execution-notes.md` at meaningful checkpoints, and preserve the On block rules. It should not restate the full sidecar plan or turn into another long Goal.

If the target runtime or evaluator may not reliably inspect sidecar files, do not rely on the compact launcher alone. Use an inline Goal with the essential objective, evidence surface, Done condition, and block rules, or add those essentials to the launcher while keeping it under the length budget.
