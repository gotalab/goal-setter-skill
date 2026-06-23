# Runtime Behavior

goal-setter writes goal text. It does not implement a new scheduler. It uses the
goal and parallelism mechanisms that already exist in the runtime.

## Activation

| Runtime | Behavior |
| --- | --- |
| Codex, no worker-tool launch needed | goal-setter can set the goal with the native goal tool |
| Codex, `spawn_agent` or `create_thread` needed | goal-setter returns a `/goal ...` line for the user to send |
| Claude Code | goal-setter returns a `/goal ...` line for the user to send |

The Codex worker-tool case is different because `spawn_agent` and
`create_thread` are gated to explicit user requests. A tool-set goal can
describe the desired work, but the user-sent `/goal ...` line is what authorizes
those tools, even when `spawn_agent` is only used for final verification.

## Parallel Work

When work splits into independent, separately verifiable units and the savings
are worth the added coordination, the goal carries the decomposition structure:

- a discovery rule for the units
- an owned area and evidence requirement for each unit
- item-by-item progress expectations
- a parent integration check
- a final review level matched to risk

Separability is judged by behavioral coupling, shared state, and integration
risk before file layout. File paths are clues after reading the repo, not the
first-principles boundary. Do not fix a subagent count unless the user requested
one; the parent agent chooses the number and waves based on independence, risk,
cost, and how much evidence it can integrate. It should synthesize each wave
before launching more.

## Long Runs

For long autonomous work, the goal can require an evidence-based open-items loop.
The runner keeps the current required checks, evidence status, blockers, and
material decisions in `execution-notes.md`. After each check, it updates that
state. If Done is not met and no block condition applies, it continues to the
next highest-risk or least-certain open item instead of stopping with only "next
steps."

## Clarification

goal-setter asks before drafting only when the missing answer could change Done,
evidence, scope, risk, or stop conditions. If the user asks to be grilled or to
fully clarify a plan, it asks one material question at a time with a recommended
answer, waits for feedback, and continues only while the next answer could still
change the goal. If code, docs, or sources can answer the question, it checks
those instead of asking.

## Codex

Use `create_thread` only when all of these are true:

- at least two write units are behaviorally independent
- each unit has stable ownership and its own validation
- shared interfaces are already understood well enough to integrate
- the expected time saved exceeds thread setup, review, and merge cost
- a usable git/worktree base already exists

Never initialize git, scaffold architecture, or create shared interfaces solely
to enable parallel work. If the workspace is not already suitable, keep writes
serial or ask before changing repository structure.

Use `spawn_agent` for read-only work when a separate pass could change the Done
decision: research, multi-aspect review, adversarial review, final verification,
log analysis, existing-behavior discovery, and other noisy checks. Low-risk work
with strong automated checks does not need a subagent. Subagents return
evidence, counterevidence, uncertainty, gaps, or read-only findings; the parent
keeps synthesis, write decisions, and final judgment.

## Claude Code

Claude Code can realize the same structure as a dynamic workflow. The goal
describes the structure and the instruction to fan out in parallel, but it does
not micromanage the mechanism. Read-only stages can become subagents; write
stages can use worktree isolation when appropriate.

## What a Goal Covers

For non-trivial work, goal-setter considers:

- outcome and why it matters
- objective and Done condition
- evidence source and validation
- compression around outcome, evidence, constraints, boundaries, iteration
  policy, and blocked stop condition
- existing primary file reuse for requested spreadsheets, reports, docs,
  dashboards, or tracking files
- one-question-at-a-time clarification when requested or materially needed
- read-first anchors
- hard boundaries and rules against weakening required checks
- progress rules and open-item loops for long runs
- stop conditions
- a risk-matched final review, including adversarial review for high-risk claims
  with a concrete target
- final report expectations
- a question-and-hypothesis loop for uncertain research, including rejection criteria and stop rules

Short tasks get short goals. Clauses that would not change the run are
dropped.
