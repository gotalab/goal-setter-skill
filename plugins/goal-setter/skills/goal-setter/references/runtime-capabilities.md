# Runtime Capabilities Reference

Read this before drafting or activating a Goal that depends on subagents, service agents, MCP tools, network access, browser/computer use, app-backed actions, approvals, enterprise-managed policy, or broad multi-item orchestration.

## Capability Posture

Use available capabilities when they materially improve end-to-end completion. Do not treat service agents, MCP tools, network access, browser/computer use, app-backed actions, or approvals as forbidden extras.

Treat these as governed capabilities:

- subagents
- service agents
- MCP tools
- network access
- browser/computer use
- app-backed actions
- approval flows
- managed enterprise policy

If a required capability is blocked, do not mark the Goal done by substituting weaker evidence. Ask for approval or stop under On block with the smallest needed capability.

## Subagents and Context Separation

Subagents are allowed for separable investigation, source-backed research, review, and validation planning.

When subagents are intended, encode that in the Goal text as explicit authorization for bounded subagent/delegation use. Runtime policy may still restrict actual spawning, but the Goal should not leave intended delegation implicit. This clause should survive Goal compression; make it short, not absent.

On Codex, name the tool concretely — abstract phrasing does not fire. "Fresh-context verification" and "independent review" are read as in-context self-work, not as launching a separate context (verified: Codex frequently does not interpret "fresh context" as an explicit subagent launch). Read-only separate contexts — review, research, final/adversarial verification — are **subagents** (`spawn_agent`, lightweight, no worktree). To get one, write an imperative directive: "spawn a read-only subagent to review/research/verify <X>; do not self-review." Write parallelism uses `create_thread` (own worktree) only when an established project exists; otherwise it too uses partitioned subagents (see Parallel Fan-out). This rides the user-sent `/goal`: both `spawn_agent` and `create_thread` are gated to an explicit user request, so they fire when the human sends the `/goal` line and do not fire from a goal the skill auto-sets via `create_goal`. Where a separate context genuinely cannot be guaranteed, "or an equivalent independent pass" is the honest fallback — but say plainly it is an in-context pass, not a fresh context.

Prefer read-only subagents for:

- repo reconnaissance
- external research
- spec-gap review
- validation discovery
- test-failure triage
- strategy review when progress stalls
- final diff/review checks

Merge concise, actionable findings into `execution-notes.md` when notes are used. Do not create separate run-management report files unless the user explicitly asks or a bulky evidence artifact is genuinely needed.

Research should resolve a concrete decision, validate an assumption, compare an implementation option, or understand a required external interface. When research uses external or fast-moving information, require source links, dates where relevant, and a short note on how the finding affects the Goal.

Do not let research expand scope unless the Goal constraints explicitly allow it.

## External Actions

External side-effecting actions may be part of the Goal when end-to-end completion requires them.

Examples:

- PR creation
- issue comments
- deployments
- CRM updates
- document edits
- emails
- calendar changes
- source-system writes

Let the runtime's approval and managed-policy system decide whether they can proceed. If approval is denied or unavailable, preserve completed internal work and report the exact remaining external action.

Do not stop merely because an external action needs approval and the runtime can request it.

## Enterprise and Sandbox Assumptions

For enterprise portability, assume filesystem writes, shell execution, network access, MCP servers, app actions, browser/computer use, and subagents may be controlled by managed policy.

Use them when available and useful, but do not silently weaken the Goal if they are blocked.

Continue with the best in-sandbox path only when the Done condition can still be honestly satisfied. Otherwise report the smallest approval, capability, or location needed.

In sandboxed environments:

- Prefer inline goals when sidecar storage is not clearly writable.
- Prefer sidecars in an already-writable plan/spec directory.
- Use explicit `--run-root` only when the user or environment provides a writable location.
- Do not assume repo-external user-state paths are writable.
- Do not require `python3` or shell helper execution when direct file creation or inline goals are simpler.

## Pipeline-Shaped Execution

For separable multi-item work, prefer item-by-item progress: act on and verify each discovered item as soon as it is ready.

Wait for the full set only when all prior results are needed for:

- deduplication
- cross-item comparison
- zero-result early exit
- a prompt that explicitly depends on the full set

Do not request large fan-out, dynamic workflows, or many agents unless the user or Goal explicitly opts into that scale. When opting in, state the bounded surface, ownership split or routing rule, merge/review evidence, and any cap on parallel agents or retries.

## Parallel Fan-out

Spawning many agents because more feels faster is not the default; for most Goals it duplicates work and creates merge conflicts that quietly erode the Done evidence. Fan-out earns its cost only when the work splits into independent, separately verifiable units that share no state — and it pays off most on otherwise serial work. It covers more than implementation: parallel read-only research, multi-aspect review, and adversarial verification fan out the same way — split into independent units, run in parallel, synthesize.

Fan out only when all three hold:

- the units do not touch the same files or interlocking state
- each unit carries its own evidence or deliverable, checkable on its own
- a parent integration/synthesis step confirms the merged result, not just the units

**Structure (always in the Goal, runtime-agnostic).** Write a discovery rule for finding the independent units (state the rule, do not enumerate units you cannot yet name), an owned surface and its own evidence/deliverable per unit, item-by-item progress, a cap on parallel count and retries, and a parent integration/synthesis gate. This works on both runtimes and even when units are discovered at runtime; it gives the contract value even with no parallelism.

**Tool by work type.** On Codex the everyday parallel primitive is the **subagent** (`spawn_agent`) — always available, no worktree. Use it for read-only work (research, multi-aspect review, adversarial/final verification) and for write units whose file ownership is cleanly partitioned so they never touch the same files. **`create_thread`** adds a real git worktree per unit, but it requires a resolvable `projectId`, so it is only available in an established project — not on an empty or freshly-created workspace (verified in a real run: the executor reported "create_thread needs a projectId" and could not cut one there). Reserve `create_thread` for write units that genuinely must touch shared files, and only when a project workspace exists; otherwise partition the files and fan out with subagents. On Claude Code the dynamic workflow handles this on its own judgment — subagents for read-only stages, worktree isolation for write stages.

**Phased pipeline.** Large work often stages cleanly: (1) parallel read-only research to clarify scope and open questions, (2) parallel write implementation, (3) integrate, (4) parallel adversarial/final verification. This is a common shape, not a mandate — use the phases that fit, and keep each phase's units independent with their own evidence.

**How it runs, per runtime:**

- **Claude Code**: the model fans out on its own judgment, so the Goal just describes the structure and phases. The natural form is a dynamic workflow — discover the work-list, dispatch scoped units in parallel (subagents for read-only stages, worktree-isolated for write stages), and synthesize; the active run owns orchestration end to end. No extra trigger needed.
- **Codex**: both `spawn_agent` and `create_thread` fire only from a `/goal` line the *human sends*, not from a goal the skill auto-sets via `create_goal` (verified: the directive fired when the human typed `/goal`, was declined when tool-set). So for fan-out work, **do not auto-set — emit the `/goal …` line for the user to send**; that one send authorizes the cascade. Name the tools concretely and imperatively — abstract phrasing ("fresh-context verification", "use subagents") and hedges ("when useful", "only when separable") launch nothing (verified). Two rules keep the run from silently falling back to serial:
  - **Bootstrap first (phase 0).** Parallel write units need a shared committed baseline; an empty or non-git workspace cannot cut a worktree at all, and fanning out before the skeleton is committed makes every thread reinvent or collide on it. So the first phase is a main-thread step — git init, build/test scaffold, committed cross-module interface contracts — before any write fan-out.
  - **Name the tool, not its arguments; don't over-promise `create_thread`.** Write `spawn_agent`/`create_thread` and "own worktree", but never `projectId`/`target.type`/schema fields — tool-call-shaped text overfits the schema and stalls the executor. Because `create_thread` needs a resolvable `projectId`, it is unavailable on a fresh workspace (verified: the executor reported it "needs a projectId" and could not cut one), so default write fan-out to `spawn_agent` over strictly partitioned files, and use `create_thread` only when an established project exists and units must share files. Tell Codex to work in the current project/workspace and let the runtime resolve the location.

When the three conditions do not all hold — interlocking refactors, a single-cause bug or flaky-test investigation, a metric tuned by one serial loop — do not fan out the writes: parallel writes against shared state make "independent" a lie and break the merge. A read-only investigation can still fan out with subagents; keep one write contract.

## Coverage and Completeness

For broad review, audit, research, migration, or bug-finding Goals, state the intended coverage bound.

If scope is sampled, capped, skipped, retried only a fixed number of times, or narrowed during execution, record the limit and why it is acceptable in `execution-notes.md` when notes are used and in the final response.

When completeness matters, continue discovery until the explicit coverage bound is met or until fresh findings dry up under the chosen method. Do not turn this into an unbounded search; if the dry-up rule is not appropriate, use the smallest explicit coverage rule that makes the final claim honest.

"Do everything" should mean every item in the bounded requested surface, not every theoretically related item. Define the bounded surface from the spec, touched interfaces, evidence surface, affected docs/help/tests, source maps, or discoverable stale-surface scans. If discovery reveals a materially adjacent surface, include it when it is required for honest end-to-end completion; otherwise record it as out-of-scope or follow-up instead of expanding indefinitely.

Before claiming Done on high-confidence completion, verify the evidence with a fresh-context check — an independent read-only subagent or equivalent — not self-review; add completeness criticism when coverage claims are broad.
