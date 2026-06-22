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
- existing canonical artifact reuse for requested spreadsheets, reports, docs,
  dashboards, or tracking files
- read-first anchors
- hard boundaries and rules against weakening required checks
- progress rules for long runs
- stop conditions
- a risk-matched final review, including adversarial review for high-risk claims
  with a concrete target
- final report expectations
- a question-and-hypothesis loop for uncertain research, including rejection criteria and stop rules

Short tasks get short goals. Clauses that would not change the run are
dropped.
