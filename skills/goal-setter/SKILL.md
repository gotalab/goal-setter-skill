---
name: goal-setter
description: Clarify, lightly explore, draft, or activate a compact, measurable, evidence-backed /goal completion contract for long-running implementation, migration, refactor, debugging, research, review, or validation work. Use when a rough request may need Goal shaping, clarification, bounded discovery, explicit Done evidence, validation, progress/pivot rules, subagent authorization, or block conditions before autonomous multi-step execution. Do not use for small one-turn edits, ordinary Q&A, loose backlog brainstorming, purely subjective work without a rubric, or unrelated task lists.
---

# Goal Setter

## Purpose

Turn a rough request into a compact Goal condition that can be set directly with `/goal` or a native goal tool. Treat the skill as Goal intake, not a general task router: decide whether to ask, briefly explore, draft, activate, or say a normal prompt/plan is a better fit.

A Goal is a completion contract for the user's requested outcome, not a detailed implementation recipe. It should let the agent continue autonomously for a long-running task, including day-scale work, while staying bounded by explicit context, evidence, constraints, validation, progress/pivot rules, Done rules, and block rules.

Use context-minimalist Goal text. Do not shrink or reinterpret the user's requested outcome. Instead, minimize the surrounding prompt: include only context and instructions that change execution safety, autonomy, evidence quality, progress visibility, or stop conditions. Do not pack routine implementation steps, explanatory rationale, long context lists, examples, or optional operations into the Goal text when constraints, validation, discovery rules, and Done evidence are enough.

Default to an inline goal condition. Create sidecar files only when they are useful for durable audit, resume, or plan/spec ownership.

Before setting a Goal, resolve ambiguity that could produce the wrong outcome. Ask the necessary focused questions together when missing decisions affect the objective, evidence surface, Done condition, scope, safety, public contract, auth, security, billing, data handling, production dependencies, or another high-risk boundary. For low-risk implementation details, make the smallest safe assumption, encode it in the Goal, and continue.

When the user asks to run or activate a Goal, set the native goal using the visible goal tool. Codex and Claude Code both expose a `/goal` command; Codex also exposes native goal tools (`create_goal`, `get_goal`, `update_goal`). Prefer the visible native goal tool/function; if none is visible, emit the exact `/goal ...` command instead. Do not claim the goal was set unless it was actually set.

## Reference Read Gates

Do not treat these references as optional background. Read the relevant file before doing the work named in each gate.

- Before drafting, activating, improving, or auditing any non-trivial Goal, read `references/goal-contract.md`.
- Before creating, updating, auditing, or choosing a location for `GOAL.md` / `execution-notes.md`, read `references/sidecars-and-notes.md`.
- Before writing a Goal that depends on subagents, service agents, MCP/tools, network access, browser/computer use, app-backed actions, approvals, enterprise-managed policy, broad fan-out, or broad coverage claims, read `references/runtime-capabilities.md`.
- Before using the helper script or modifying its generated output, read `scripts/init_goal_run.py` and the templates it loads from `references/`.
- Before editing this skill's policy, check `SKILL.md`, relevant `references/*.md`, `references/GOAL.template.md`, `references/execution-notes.template.md`, and `scripts/init_goal_run.py` for drift.

## When to Use

Use a Goal when most of these are true:

- The task may take many iterations.
- The task has one durable objective.
- Progress can be validated with commands, artifacts, diffs, screenshots, benchmarks, source-backed evidence, or a written rubric.
- The final result has a clear evidence surface or verification environment.
- The request can be converted into measurable targets or observable evidence.
- The agent can keep making bounded progress without asking for routine decisions.
- Scope boundaries and stop/block rules can be made explicit.

Good fits:

- migrations with parity checks
- refactors with test validation
- scoped quality work with reviewable before/after evidence
- flaky test investigation
- UI implementation against reference screenshots
- performance tuning with thresholds
- eval-driven prompt or artifact optimization
- implementation from a spec with reviewable notes
- source-backed research or external action workflows with clear evidence and approval boundaries

Bad fits:

- one small edit
- loose unrelated backlog lists
- "make this better" without evidence
- subjective output with no rubric
- destructive/high-risk changes without explicit approval boundaries

If the task is a bad fit, say so and suggest a normal prompt or a planning pass first.

## Intended Outcome Image

Before clarifying, exploring, or drafting, form a short intended outcome image: reconstruct what the user is actually trying to create or achieve, and why it matters, in 2-4 sentences. This image is the source from which the objective, evidence surface, validation criteria, constraints, and Done are derived. It fixes what and why, not how, so leave method and sequencing to the agent. Capture this task's intended outcome, not the user's general values or working style.

Compress the image into one context line that opens the Goal text — what the outcome serves and for whom. Models perform better on long autonomous runs when they know the reason behind the request, not only the request; the rest of the image stays out of the Goal and shapes the contract instead.

Because a Goal runs autonomously and long, a wrong starting image is amplified across the whole run, so getting it right is the highest-leverage step and a precondition for an honest contract. Reach it dynamically: infer, explore, or ask by risk and what is discoverable; the gates below are tools for resolving the image, not a strict sequence. When the prompt is minimal or rough, mirror the reconstructed image back compactly for one-pass correction before the long run starts, and bundle any critical clarification questions into that same message so the user answers in one round trip. See the image-to-criteria-to-constraints derivation in `references/goal-contract.md`.

## Clarification Gate

Before drafting or activating a Goal, decide whether the rough request is clear enough to preserve the user's intended outcome. Ask focused questions first when missing information could change the objective, evidence surface/Done condition, validation method, scope/coverage claim, external side effects/approvals, data/credential/source/runtime requirements, or any high-risk boundary (safety, public contract, auth, security, billing, data handling, production dependency, legal, financial, medical). See the full trigger list and question style in `references/goal-contract.md`.

Ask the smallest complete set of plain-language questions needed to preserve the intended outcome; do not cap the count when more are genuinely required, and add a recommended default only when it is safe and reversible. Do not ask routine implementation questions: when ambiguity is low-risk, reversible, and inferable from the request/repo/tests/docs/nearby behavior, make the smallest safe assumption, encode it in the Goal, and continue. If critical clarification is needed in Activate Mode, ask first and do not set the native Goal yet.

## Bounded Exploration Gate

If an honest Goal cannot be drafted because project, data, tool, or validation reality is unknown, but that reality can be discovered locally or from allowed sources, run a short bounded exploration before drafting or activating the Goal. Use it to identify evidence surfaces, validation commands, relevant files/docs, data/source constraints, current baselines, and likely blockers; do not start implementation. After exploration, either draft/activate the Goal, ask only the remaining user-owned questions, or say the task is not a good Goal fit. See bounds and stop conditions in `references/goal-contract.md`.

## Modes

### Draft Mode

Use when the user asks to create, improve, review, or draft a Goal.

Steps:

1. Read `references/goal-contract.md`.
2. If the Goal needs external capabilities, broad coverage, subagents, MCP/tools, network, app actions, or enterprise/sandbox handling, read `references/runtime-capabilities.md`.
3. Form the intended outcome image, then run the Clarification Gate. When the prompt is minimal or rough, mirror the image back for one-pass correction. If critical information is missing, ask the focused questions first and do not pretend the Goal is ready.
4. Run the Bounded Exploration Gate if discoverable facts are needed before an honest Goal can be written.
5. Draft the compact inline `/goal` condition first when the gates pass or when safe assumptions can be encoded.
6. Run the bloat pass from `references/goal-contract.md`: keep outcome/evidence/constraints/validation/pivot/Done/block rules, and remove routine implementation sequencing or optional operations.
7. Include a Goal readiness assessment.
8. Include optional sidecar content only if the user asked for sidecar files, supplied an owning plan/spec directory, or the task clearly needs durable audit/resume state. If sidecars are included, first read `references/sidecars-and-notes.md`.
9. Do not activate the goal.

Output:

1. Proposed inline `/goal` condition.
2. Goal readiness assessment.
3. Sidecar content only when requested or clearly useful.

### Activate Mode

Use when the user asks to set, run, execute, activate, start, or use the native goal tool.

Steps:

1. Determine the current project root.
2. Read `references/goal-contract.md`.
3. If external capabilities, broad coverage, subagents, MCP/tools, network, app actions, or enterprise/sandbox handling matter, read `references/runtime-capabilities.md`.
4. Form the intended outcome image, then run the Clarification Gate. When the prompt is minimal or rough, mirror the image back for one-pass correction. If critical information is missing, ask the focused questions and do not set the Goal yet.
5. Run the Bounded Exploration Gate if discoverable facts are needed before an honest Goal can be written.
6. Draft a compact inline goal condition first when the gates pass or when safe assumptions can be encoded.
7. Run the bloat pass from `references/goal-contract.md`; preserve execution freedom by avoiding unnecessary implementation sequencing.
8. Create sidecar files only if the user asked for files, supplied an owning plan/spec directory, or the task clearly needs durable audit/resume state.
9. If sidecars are used, read `references/sidecars-and-notes.md`, resolve the run-file location, and create exactly two run files:
   - `GOAL.md`
   - `execution-notes.md`
10. Do not create extra run-management files such as `INDEX.md`, `validation-log.md`, `subagents.md`, or subagent report files unless the user explicitly asks or a bulky evidence artifact is genuinely needed.
11. Audit the Goal using the readiness audit in `references/goal-contract.md`.
12. If a native goal-setting tool/function is visible, use it. When a goal-state tool (`get_goal`) is also visible, check the active goal first: reuse an active goal that already matches the intent instead of creating a duplicate, and ask before replacing one that conflicts.
13. If native goal setting is not visible, output the exact `/goal ...` command instead.
14. Do not claim the goal was set unless it was actually set.

## Inline Goal Requirements

The inline condition is the default output. It should include only the information needed to keep the agent aimed at the finish line:

The first group below belongs in every Goal; the governance items after it scale with run length and risk — on short low-risk goals, drop what would not change the run (see `references/goal-contract.md`).

- a one-line context note compressed from the intended outcome image (what the outcome serves and for whom)
- one objective
- evidence surface / verification environment
- important context to read first
- task-specific constraints and anti-gaming rule (instantiate the boundaries that matter for this task; do not paste a generic denylist)
- validation or validation discovery rule
- subagent/context-separation policy, including fresh-context verification before claiming Done
- optional dynamic workflow / fan-out policy when explicitly needed
- visible progress / checkpoint reporting rule, with progress claims audited against tool results
- persistence rule (act on sufficient information; never end a turn on a plan or promise)
- progress/pivot rule
- Done condition
- block condition
- final report rule (outcome first, plain words, user's language)

For non-trivial Goals, include a short authorization to use available governed subagents for separable research, validation discovery, triage, strategy review when progress stalls, and final fresh-context review. Prefer read-only subagents unless an external side effect is required, allowed by policy, and part of end-to-end completion. Keep this authorization explicit because some runtimes (Codex in particular) will not use subagents during a goal run unless the goal text grants it; never compress it away.

Length budget (canonical values and the over-budget fallback live in `references/goal-contract.md`): shorter is better — most goals should land around 800-1,800 characters, with 2,500 the ordinary ceiling (3,500 portable, 4,000 hard cap). A long Goal crowds out the model's own judgment, so every sentence must be able to change the executor's behavior; scale the governance clauses to the run and drop the ones whose absence would not change it. Compress examples, context lists, and optional operations before weakening core completion criteria.

Reference shape for activating without sidecars. It is a shape, not a fixed template: the covered elements are the contract, so reword, reorder, drop clauses that do not apply, and phrase everything in the task's own terms — a contract written for the task reads better and runs better than boilerplate. Numeric defaults in it (two stalled approaches before a pivot review) are defaults; adjust them when the task warrants.

```text
Context: this serves <who/what> by <why the outcome matters>. <objective>. Verify success through <evidence surface>. Read <minimal context> and discover adjacent tests/docs as needed. Keep changes scoped to the objective and do the simplest thing that meets it — no refactors, features, or abstractions beyond it; do not alter <the 1-3 boundaries that matter for this task> or other externally visible contracts or destructive boundaries unless the objective explicitly requires it. Validate with <known checks> or discover and run relevant checks. Use available governed subagents when materially useful for separable research, validation discovery, triage, or strategy review; before claiming Done, verify the evidence with a fresh-context check (independent subagent or equivalent), not self-review. Maintain visible progress with a concise checklist and checkpoint updates in the user's language; before reporting progress, audit each claim against a tool result from this run — unverified work is reported as unverified, never as done; do not let reporting displace execution. When you have enough information to act, act; do not ask permission for reversible in-scope actions, and never end a turn on a plan or a promise — do that work now. Done when <binary evidence-backed condition>. If two approaches fail to improve evidence, review strategy and pivot within constraints; do not silently change the objective, Done, evidence, constraints, approval boundaries, or coverage claim. Stop only if <block rules>. The final report is for a reader who watched none of the run: outcome first, plain words, in the user's language.
```

Instantiate the placeholders against this task: the context line comes from the intended outcome image, and the constraint boundaries name only what this task could actually break (e.g. public API signatures, schema, auth behavior) — replacing the long generic denylist keeps the contract inside the length budget while the new context, evidence-audit, and persistence clauses earn their characters.

## Sidecars

Use sidecars only when they add real value for durable audit, resume, or plan/spec ownership.

Before using sidecars, read `references/sidecars-and-notes.md`.

When sidecars are used:

- create exactly `GOAL.md` and `execution-notes.md`
- use `references/GOAL.template.md` and `references/execution-notes.template.md`
- prefer an existing writable plan/spec directory when one owns the work
- in sandboxed or enterprise-managed environments, do not require repo-external user-state storage
- keep notes concise, review-oriented, and bounded

The compact launcher objective for sidecars must tell the agent to execute the resolved `GOAL.md`, update `execution-notes.md` at meaningful checkpoints, and stop only under `GOAL.md` On block rules.

If the target runtime or evaluator may not reliably inspect sidecar files, do not use a sidecar-only launcher. Use an inline Goal that includes the objective, evidence surface, Done condition, and block rules, or add those essentials to the launcher while keeping it compact.

## Runtime Capabilities

Before mentioning or depending on subagents, service agents, MCP/tools, network/browser/app capabilities, approvals, broad fan-out, or enterprise/sandbox handling, read `references/runtime-capabilities.md`.

Default posture:

- Use available governed capabilities when they materially improve end-to-end completion.
- If subagents are intended, write the Goal condition as explicit user-facing authorization for bounded subagent/delegation use; runtime policy may still restrict actual spawning.
- Use dynamic workflow, broad fan-out, or many parallel agents only when the user or Goal explicitly opts into that scale, with a bounded surface, ownership split, and merge/review evidence.
- Let runtime approval and managed policy decide whether side-effecting external actions can proceed.
- If a required capability is blocked, do not weaken evidence or mark the Goal done.
- Continue in-sandbox only when Done can still be honestly satisfied.
- Report the smallest approval, capability, or location needed when blocked.

## Helper Script

This skill includes `scripts/init_goal_run.py` to create the two sidecar files with the right run ID format.

The helper is a convenience path, not a runtime requirement. It expects a local `python3` executable and a writable target location. Use it when helpful, but do not require it if `python3` is unavailable, shell execution is blocked, the target path is not writable, or direct file creation is simpler. In sandboxed environments, pass `--plan-dir` or `--run-root` pointing to an already-writable location, or skip the helper and use an inline goal.

When validating helper scripts in sandboxed or read-only skill locations, avoid `python3 -m py_compile` because it writes `__pycache__` beside the checked file. Prefer `python3 -B scripts/check_python_syntax.py <file.py>` for syntax checks and `python3 -B <script.py> ...` for helper execution.

Before using the helper, read `references/sidecars-and-notes.md`.

Example:

```bash
python3 -B <skill-path>/scripts/init_goal_run.py \
  --area checkout \
  --outcome confirmation-flow \
  --title "Checkout confirmation flow" \
  --objective "Implement the checkout confirmation flow and verify it with checkout tests."
```

## Output Style

In Draft Mode:

- if clarification is required, show the focused questions first and pause
- if bounded exploration was needed, summarize only the discovered facts that changed Goal readiness, remaining user-owned questions, and the next action
- show the proposed inline goal condition first
- show the readiness assessment
- show full sidecar content only if requested or clearly useful

When clarification is required, do not also present a final-looking Goal unless it is clearly labeled as a provisional sketch.

In Activate Mode without sidecars, after the goal is set or command is emitted, respond with:

- whether the goal was set or only a `/goal` command was emitted
- approximate inline condition character count
- the compact objective
- assumptions or user-review-needed decisions

In Activate Mode with sidecars, after files are created and the goal is set or command is emitted, respond with:

- run ID
- paths to the two files
- whether the goal was set or only a `/goal` command was emitted
- approximate launcher objective character count
- the compact objective

Do not paste the full `GOAL.md` unless the user asks.
