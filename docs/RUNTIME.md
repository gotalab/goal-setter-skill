# Runtime Behavior

goal-setter writes goal text. It does not implement a new scheduler. It uses the
goal and parallelism mechanisms that already exist in the runtime.

## Activation

| Runtime | Behavior |
| --- | --- |
| Codex, activation requested | goal-setter sets the goal with the native goal tool |
| Codex, draft only requested or no native goal tool available | goal-setter returns an exact `/goal ...` line |
| Claude Code | goal-setter returns a `/goal ...` line for the user to send |

goal-setter activates the Goal normally. When parallel exploration, context
isolation, or independent verification could improve Done, it starts subagents
instead of merely mentioning that they are available. The user does not need to
resend `/goal` solely to authorize them. When the same delegation is needed in a
long-running Goal, the Goal tells Codex concretely to spawn subagents for the
named work, wait for their evidence, and synthesize it. Worker count and wave
shape remain the parent's judgment unless the user fixes them.

`create_thread` is not subagent fan-out. It creates separate user-owned Codex
tasks and is used only when the user explicitly requests separate tasks,
threads, or worktrees.

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
evidence, scope, risk, or stop conditions. If the request is too ambiguous to
define an honest pass/fail Goal, or the user asks to be grilled, it enters a real
interview instead of guessing. It asks dependent questions one at a time with a
recommended answer, and bundles independent blocking questions when their answers
do not affect one another. It stops interviewing once the Goal is safe to define.
If code, docs, or sources can answer the question, it checks those instead.

## Codex

Use `create_thread` only when the user explicitly requested a separate task,
thread, or worktree; do not infer it merely because work is decomposable. For
parallel write fan-out across multiple tasks, all of these must also be true:

- at least two write units are behaviorally independent
- each unit has stable ownership and its own validation
- shared interfaces are already understood well enough to integrate
- the expected time saved exceeds thread setup, review, and merge cost
- a usable git/worktree base already exists

Never initialize git, scaffold architecture, or create shared interfaces solely
to enable parallel work. If the workspace is not already suitable, do not
silently create tasks or fall back to serial work; report the missing condition
and the smallest decision needed. A user-requested single handoff or new thread
does not inherit the multi-task fan-out gates.

Use `spawn_agent` when a stronger feedback loop, parallel
exploration, context isolation, or a separate read-only pass could change the
Done decision. Common patterns include moving noisy research or log analysis out
of the main context, investigating independent questions in parallel, feeding
new evidence into another focused pass, and challenging actual output from a
fresh context. These are not fixed stages or roles. The parent chooses a serial,
parallel, or repeated-wave shape from current evidence, dependencies, and cost.
Low-risk work with strong automated checks does not need a subagent. Start with
the smallest useful wave, synthesize it, and launch more only when another pass
could still change Done. Review subagents stay read-only; the parent keeps
synthesis, integration, write decisions, and final judgment. This is an
execution rule: actually spawn the subagents. Do not replace it with a statement
that subagents are available or with an in-context self-review. When the same
delegation should continue across Goal turns, put the concrete spawn, wait, and
synthesize instruction in the Goal.

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
