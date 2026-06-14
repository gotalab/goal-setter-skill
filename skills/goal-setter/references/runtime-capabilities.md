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

## Parallel Decomposition

Spawning many agents because more feels faster is not the default; for most Goals it duplicates work and creates merge conflicts that quietly erode the Done evidence. Decomposition earns its cost only when the requested outcome splits into independent, separately verifiable sub-outcomes that share no state — and it pays off most on otherwise serial work.

Decompose only when all three hold:

- the pieces do not touch the same files or interlocking state
- each piece carries its own Done evidence, checkable on its own
- a parent integration check confirms the merged result, not just the pieces

The mechanism is runtime-specific. "Child goals" is the intent, not a literal command: a single `/goal` is one active completion contract and does not by itself spawn parallel autonomous goal runs. Authorize the runtime's real fan-out primitive in the Goal text, because — like subagent authorization — runtimes that need an explicit grant will not parallelize on their own:

- **Claude Code**: default to a dynamic workflow — it is the runtime's purpose-built fan-out primitive for splitting work, dispatching scoped contracts in parallel, and synthesizing results as they return, and it scales to a dynamic piece count and pipelined stages. The active goal run owns orchestration: it dispatches one scoped contract per piece, then merges and runs the integration check. Fall back to parallel subagents under git worktree isolation only for a small fixed set of independent write tasks where a full workflow is overkill.
- **Codex**: give each piece its own goal — Codex can run parallel subagents that each hold their own `create_goal` contract scoped to one owned surface. It will not delegate or parallelize unless the goal text grants it explicitly, so write the grant in. This per-child-goal form is the one to reach for on Codex when the pieces are genuinely independent.

For each piece, name the owned surface, cap the parallel count and retries, and make the parent Done depend on every piece's evidence plus the integration check. Write this grant into the Goal text by default on work that could split, phrased to self-gate ("if the work splits into independent, separately verifiable pieces that share no state...") so it stays harmless on work that does not.

When the three conditions do not all hold — interlocking refactors, single-cause bug or flaky-test investigation, a metric tuned by one serial loop — do not decompose: parallel writes against shared state make "independent" a lie and break the merge. Use read-only subagents for the separable investigation instead and keep one write contract.

## Coverage and Completeness

For broad review, audit, research, migration, or bug-finding Goals, state the intended coverage bound.

If scope is sampled, capped, skipped, retried only a fixed number of times, or narrowed during execution, record the limit and why it is acceptable in `execution-notes.md` when notes are used and in the final response.

When completeness matters, continue discovery until the explicit coverage bound is met or until fresh findings dry up under the chosen method. Do not turn this into an unbounded search; if the dry-up rule is not appropriate, use the smallest explicit coverage rule that makes the final claim honest.

"Do everything" should mean every item in the bounded requested surface, not every theoretically related item. Define the bounded surface from the spec, touched interfaces, evidence surface, affected docs/help/tests, source maps, or discoverable stale-surface scans. If discovery reveals a materially adjacent surface, include it when it is required for honest end-to-end completion; otherwise record it as out-of-scope or follow-up instead of expanding indefinitely.

Before claiming Done on high-confidence completion, verify the evidence with a fresh-context check — an independent read-only subagent or equivalent — not self-review; add completeness criticism when coverage claims are broad.
