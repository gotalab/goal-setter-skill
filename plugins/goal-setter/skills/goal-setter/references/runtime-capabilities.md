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

On Codex, name the tool concretely — abstract phrasing does not fire. "Fresh-context verification" and "independent review" are read as in-context self-work, not as launching a separate context (verified: Codex frequently does not interpret "fresh context" as an explicit subagent launch). Read-only separate contexts — review, research, final/adversarial verification — are **subagents** (lightweight, no worktree); write work is `create_thread` (own worktree). To get a real separate read-only context, write an imperative subagent directive: "spawn a read-only subagent to review/research/verify <X>; do not self-review." This rides the user-sent `/goal`: both `spawn` and `create_thread` are gated to an explicit user request, so they fire when the human sends the `/goal` line and do not fire from a goal the skill auto-sets via `create_goal`. Where a separate context genuinely cannot be guaranteed, "or an equivalent independent pass" is the honest fallback — but say plainly it is an in-context pass, not a fresh context.

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

**Tool by work type.** Read-only work — research, multi-aspect review, adversarial/final verification — uses **subagents** (lightweight, no worktree). Write work — parallel implementation — uses **`create_thread`** (each unit in its own git worktree, so concurrent writes do not collide); worktrees are heavyweight, so reserve `create_thread` for genuine parallel write units and do not overuse it.

**Phased pipeline.** Large work often stages cleanly: (1) parallel read-only research to clarify scope and open questions, (2) parallel write implementation, (3) integrate, (4) parallel adversarial/final verification. This is a common shape, not a mandate — use the phases that fit, and keep each phase's units independent with their own evidence.

**How it runs, per runtime:**

- **Claude Code**: the model fans out on its own judgment, so the Goal just describes the structure and phases. The natural form is a dynamic workflow — discover the work-list, dispatch scoped units in parallel (subagents for read-only stages, worktree-isolated for write stages), and synthesize; the active run owns orchestration end to end. No extra trigger needed.
- **Codex**: `create_thread` and `spawn` are both gated by this environment to an **explicit user request** — what matters is that the *human sends* the directive (types the `/goal …` line or a prompt), not whether it lives in Goal-text vs prompt. A goal the skill auto-sets via `create_goal` does **not** satisfy the gate, so it runs serially (verified: the same directive fired when the human typed `/goal` and was declined when tool-set, the runtime stating these tools are "only when the user explicitly asks"). Therefore, for fan-out work on Codex, **do not auto-set — emit the full `/goal …` line for the human to send.** That one send authorizes the whole cascade: the main thread runs read-only phases with **subagents**, write phases with **`create_thread`** per unit (own worktree, its own goal scoped to the unit), and integrates. Name the tools concretely and imperatively — abstract phrasing ("fresh-context verification", "use subagents") is read as in-context self-work and launches nothing (verified). Write the directives flat and unconditional; a hedged "when useful" / "only when separable" makes Codex skip them and run serially (verified). (Whether the orchestrator's per-thread goal-set fully sticks is not 100% confirmed; instruct it anyway — the instruction drives the behavior.)

**Bootstrap before write fan-out (the real precondition).** Parallel write units in separate worktrees need a shared committed baseline first. On an empty or non-git workspace, `create_thread` worktrees cannot be cut at all; and even when git exists, fanning out before the skeleton is committed makes every thread reinvent — or collide on — the scaffold and the cross-module interfaces. So for from-scratch or empty-workspace builds, make the first phase a **main-thread** step: initialize git, stand up the build/test scaffold, and commit the **interface contracts** (the shared types and module boundaries each unit codes against) before fanning out. Only then `create_thread` per write unit. This is what phase 0 of the phased pipeline is for — scaffold-and-contracts in the main thread, then parallel implementation against a fixed baseline. State this ordering in the Goal whenever the workspace may be empty or not yet git-backed; do not ask Codex to immediately fan out write worktrees into bare ground.

**Keep the directive intent-level — name the tool, not its arguments.** Write `create_thread`, "each in its own worktree", "the main thread integrates", "spawn read-only subagents" — but do **not** spell out `projectId`, `target.type`, `environment.type`, or other tool-schema fields in the Goal. Tool-call-shaped text overfits the current schema and, worse, makes the executor stall: a `projectId` that is not visible (or is a path rather than a UUID) gets read as "I cannot create a thread", and the run silently falls back to serial work (observed — this is the parallel-avoidance failure). Instead, instruct Codex to create threads **in the current project/workspace** and let the runtime resolve the location. A project id that is not visible is **not** a reason to skip `create_thread`; the worktree fan-out should proceed on the current workspace regardless.

When the three conditions do not all hold — interlocking refactors, a single-cause bug or flaky-test investigation, a metric tuned by one serial loop — do not fan out the writes: parallel writes against shared state make "independent" a lie and break the merge. A read-only investigation can still fan out with subagents; keep one write contract.

## Coverage and Completeness

For broad review, audit, research, migration, or bug-finding Goals, state the intended coverage bound.

If scope is sampled, capped, skipped, retried only a fixed number of times, or narrowed during execution, record the limit and why it is acceptable in `execution-notes.md` when notes are used and in the final response.

When completeness matters, continue discovery until the explicit coverage bound is met or until fresh findings dry up under the chosen method. Do not turn this into an unbounded search; if the dry-up rule is not appropriate, use the smallest explicit coverage rule that makes the final claim honest.

"Do everything" should mean every item in the bounded requested surface, not every theoretically related item. Define the bounded surface from the spec, touched interfaces, evidence surface, affected docs/help/tests, source maps, or discoverable stale-surface scans. If discovery reveals a materially adjacent surface, include it when it is required for honest end-to-end completion; otherwise record it as out-of-scope or follow-up instead of expanding indefinitely.

Before claiming Done on high-confidence completion, verify the evidence with a fresh-context check — an independent read-only subagent or equivalent — not self-review; add completeness criticism when coverage claims are broad.
