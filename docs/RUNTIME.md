# Runtime Behavior

goal-setter writes goal text. It does not implement a new scheduler. It uses the
goal and parallelism mechanisms that already exist in the runtime.

## Activation

| Runtime | Behavior |
| --- | --- |
| Codex, ordinary work | goal-setter can set the goal with the native goal tool |
| Codex, decomposable parallel work | goal-setter returns a `/goal ...` line for the user to send |
| Claude Code | goal-setter returns a `/goal ...` line for the user to send |

The Codex parallel case is different because `spawn_agent` and `create_thread`
are gated to explicit user requests. A tool-set goal can describe the desired
work, but the user-sent `/goal ...` line is what authorizes the parallel
cascade.

## Parallel Work

When work splits into independent, separately verifiable units, the goal carries
the decomposition structure:

- a discovery rule for the units
- an owned area and evidence requirement for each unit
- item-by-item progress expectations
- a parent integration check
- a final independent verification pass

Separability is judged by behavioral coupling, shared state, and integration
risk before file layout. File paths are clues after reading the repo, not the
first-principles boundary.

## Codex

For non-trivial write units in an established Codex project with a usable git
HEAD, the goal makes `create_thread` worktree fan-out mandatory:

- one separate thread per write unit
- one owned area per child thread
- evidence and an integration rule for each unit
- a unit-scoped goal in each child before editing
- main-thread integration after all child evidence returns

`spawn_agent` remains the default for read-only work: research, review, final
verification, log analysis, and other noisy or parallelizable checks.

If `create_thread` is unavailable, the workspace is not a usable git/worktree
base, or the write unit is too small for worktree isolation, the goal says so
explicitly instead of hiding the fallback behind an "or" clause.

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
- read-first anchors
- hard boundaries and rules against weakening required checks
- progress rules for long runs
- stop conditions
- independent verification
- final report expectations
- a question-and-hypothesis loop for uncertain research, including rejection criteria and stop rules

Short tasks get short goals. Clauses that would not change the run are
dropped.
