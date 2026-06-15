---
name: goal-setter
description: Clarify, lightly explore, draft, or activate a compact, measurable, evidence-backed /goal completion contract for long-running implementation, migration, refactor, debugging, research, review, or validation work. Use when a rough request may need Goal shaping, clarification, bounded discovery, explicit Done evidence, validation, progress/pivot rules, subagent authorization, or block conditions before autonomous multi-step execution. Do not use for small one-turn edits, ordinary Q&A, loose backlog brainstorming, purely subjective work without a rubric, or unrelated task lists.
---

# Goal Setter

## Purpose

Turn a rough request into a compact Goal condition that can be set directly with `/goal` or a native goal tool. Treat the skill as Goal intake, not a general task router: decide whether to ask, briefly explore, draft, activate, or say a normal prompt/plan is a better fit.

A Goal is a completion contract for the user's requested outcome, not an implementation recipe. Never shrink or reinterpret the requested outcome; minimize only the surrounding prompt. Default to an inline goal condition; create sidecar files only for durable audit, resume, or plan/spec ownership.

When the user asks to run or activate a Goal, set it through the runtime's native mechanism. Codex and Claude Code both expose a `/goal` command; Codex also exposes native goal tools (`create_goal`, `get_goal`, `update_goal`). Prefer the visible native tool; if none is visible, emit the exact `/goal ...` command instead. Do not claim the goal was set unless it was actually set. **Exception — decomposable work on Codex where parallel execution is wanted: do not auto-set via `create_goal`; emit the `/goal ...` line for the user to send.** Codex's `create_thread`/`spawn` fire only on the user's own typed request, not on a tool-set goal, so the human sending the `/goal` line is what authorizes the parallel cascade (see `references/runtime-capabilities.md`).

## Reference Read Gates

Do not treat these references as optional background. Read the relevant file before doing the work named in each gate.

- Before drafting, activating, improving, or auditing any non-trivial Goal, read `references/goal-contract.md`.
- Before creating, updating, auditing, or choosing a location for `GOAL.md` / `execution-notes.md`, read `references/sidecars-and-notes.md`.
- Before writing a Goal that depends on subagents, service agents, MCP/tools, network access, browser/computer use, app-backed actions, approvals, enterprise-managed policy, broad coverage claims, or work that may split into independent parallel pieces, read `references/runtime-capabilities.md`.
- Before using the helper script or modifying its generated output, read `scripts/init_goal_run.py` and the templates it loads from `references/`.
- Before editing this skill's policy, check `SKILL.md`, relevant `references/*.md`, `references/GOAL.template.md`, `references/execution-notes.template.md`, and `scripts/init_goal_run.py` for drift.

## When to Use

Use a Goal when the task has one durable objective, may take many iterations, and the result can be verified with commands, artifacts, diffs, screenshots, benchmarks, source-backed evidence, or a written rubric. Good fits: migrations with parity checks, refactors with test validation, flaky-test or bug investigation, UI implementation against references, performance tuning with thresholds, eval-driven optimization, implementation from a spec, source-backed research with clear evidence and approval boundaries.

Bad fits: one small edit, loose unrelated backlog lists, "make this better" without evidence, subjective output with no rubric, destructive or high-risk changes without explicit approval boundaries. Say so and suggest a normal prompt or a planning pass first. One exception: when the only blocker is a missing verification surface (no rubric, eval, checklist, or baseline), offer a preliminary Goal that builds that surface first, with the main Goal to follow — see `references/goal-contract.md`.

## Intended Outcome Image

Before clarifying, exploring, or drafting, reconstruct what the user is trying to create and why, in 2-4 sentences. The image fixes what and why, not how; the rest of the contract is derived from it, and a one-line compression of it opens the Goal text. Because a wrong starting image is amplified across the whole autonomous run, this is the highest-leverage step. When the prompt is minimal or rough, mirror the image back compactly for one-pass correction, bundling any critical clarification questions into the same message. Derivation chain: `references/goal-contract.md`.

## Gates

- **Clarification**: ask focused questions first when missing information could change the objective, evidence surface, Done condition, validation, scope, external side effects, or a high-risk boundary. Encode low-risk, inferable ambiguity as stated assumptions instead of asking. In Activate Mode, ask before setting the Goal. Trigger list and question style: `references/goal-contract.md`.
- **Bounded exploration**: when an honest Goal needs discoverable facts (evidence surfaces, validation commands, baselines, blockers), explore briefly before drafting; do not start implementation. Bounds and stop conditions: `references/goal-contract.md`.

The gates are tools for resolving the image, not a strict sequence: infer, explore, or ask by risk and what is discoverable.

## Modes

### Draft Mode

Use when the user asks to create, improve, review, or draft a Goal.

1. Read `references/goal-contract.md`; read `references/runtime-capabilities.md` when external capabilities, subagents, MCP/tools, network, app actions, or sandbox handling matter.
2. Form the intended outcome image and run the gates; mirror the image back when the prompt is minimal. If critical information is missing, ask first — do not pretend the Goal is ready.
3. Draft the compact inline condition per the contract reference, then run its bloat pass and readiness audit.
4. Include sidecar content only if the user asked, an owning plan/spec directory exists, or durable audit/resume is clearly needed (read `references/sidecars-and-notes.md` first).
5. Do not activate the goal.

Output: the proposed inline `/goal` condition, the readiness assessment, and sidecar content only when warranted. When clarification is required, show the questions first and pause; do not also present a final-looking Goal unless labeled a provisional sketch.

### Activate Mode

Use when the user asks to set, run, execute, activate, or start a Goal.

1. Determine the current project root, then run Draft Mode steps 1-3 (read gates, image, gates, draft, bloat pass, readiness audit).
2. Create sidecars only when warranted: read `references/sidecars-and-notes.md`, resolve the run-file location, create exactly `GOAL.md` and `execution-notes.md`, and no extra run-management files unless the user explicitly asks.
3. If a native goal-setting tool is visible, use it. When `get_goal` is also visible, check the active goal first: reuse one that already matches the intent instead of creating a duplicate, and ask before replacing one that conflicts. **For decomposable Codex work where parallelism is wanted, do not auto-set: go to step 4 and emit the `/goal ...` line for the user to send** (a tool-set goal does not satisfy Codex's user-request gate for `create_thread`/`spawn`).
4. If no native tool is visible — or the Codex parallel exception above applies — output the exact `/goal ...` command for the user to send instead.
5. Do not claim the goal was set unless it was actually set.

## Inline Goal Condition

The contract elements, reference shape, length budget, bloat pass, and readiness audit live in `references/goal-contract.md`; the parallel/runtime mechanics live in `references/runtime-capabilities.md` (both covered by the read gates). Three things to hold onto:

- Shorter is better — a long Goal crowds out the model's own judgment. Most goals land around 800-1,800 characters; 2,500 is the ordinary ceiling, not a target.
- For decomposable work, state the decomposition structure and a runtime-sized launch directive. Claude Code fans out on its own judgment; on Codex the parallel tools fire only from a `/goal` line the user *sends*, so deliver the goal as a `/goal …` line rather than auto-setting it via `create_goal` (the subagent / `create_thread` / bootstrap rules are in `references/runtime-capabilities.md`).
- Before activating, check the final condition once with `python3 -B scripts/validate_goal_length.py <file>` (stdin also works). Pass means activate; fail means restructure per the contract reference, not iterative trimming. If `python3` or shell execution is unavailable, estimate the length once yourself and move on.

## Sidecars

Use sidecars only when they add real value for durable audit, resume, or plan/spec ownership. Read `references/sidecars-and-notes.md` first. Create exactly `GOAL.md` and `execution-notes.md` from `references/GOAL.template.md` and `references/execution-notes.template.md`; prefer an existing writable plan/spec directory when one owns the work. If the target runtime or evaluator may not reliably inspect sidecar files, do not use a sidecar-only launcher — keep the objective, evidence surface, Done, and block rules inline.

## Runtime Capabilities

Read `references/runtime-capabilities.md` before depending on subagents, service agents, MCP/tools, network, browser or app actions, approvals, broad fan-out, or enterprise/sandbox handling. If a required capability is blocked, do not weaken evidence or mark the Goal done; report the smallest approval, capability, or location needed.

## Helper Script

`scripts/init_goal_run.py` creates the two sidecar files with the right run ID format. `scripts/validate_goal_length.py` checks a final condition against the real runtime limits (it strips a code fence and the `/goal ` prefix before counting). Both are conveniences, not requirements: skip them when `python3` is unavailable, shell execution is blocked, or direct file creation is simpler. In sandboxed environments pass `--plan-dir` or `--run-root` pointing to a writable location. For syntax checks in read-only skill locations, prefer `python3 -B scripts/check_python_syntax.py <file.py>` over `py_compile` (which writes `__pycache__`).

## Output Style

After activating (or emitting the command), report: whether the goal was set or only a `/goal` command was emitted, the approximate condition character count, the compact objective, and assumptions or decisions needing user review. With sidecars, add the run ID and the paths to the two files; do not paste the full `GOAL.md` unless asked. If bounded exploration ran, summarize only the facts that changed Goal readiness.

When the work is decomposable, the Goal carries the parallel-launch directive. On Claude Code it fans out via a dynamic workflow with no extra step; on Codex, flag to the user that they must send the `/goal …` line themselves — an auto-set goal does not parallelize.
