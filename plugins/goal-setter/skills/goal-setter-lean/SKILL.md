---
name: goal-setter-lean
description: Compact single-file version of goal-setter. Turns a rough request into a short, evidence-backed /goal completion contract — same core gates (intended-outcome image, clarification, binary evidence-bounded Done, fresh-context verification) and the verified Codex/Claude Code parallel mechanics, inline with no reference files. Use for long-running implementation, migration, refactor, debugging, research, or review work when you want the essentials without the full reference set. For durable sidecar audit/resume and the full readiness rubric, use the goal-setter skill instead. Not for one-turn edits, ordinary Q&A, or subjective work with no rubric.
---

# Goal Setter (Lean)

Turn a rough request into a compact `/goal` completion contract — the shortest condition that still pins the requested outcome. This is the single-file version of `goal-setter`; for sidecar audit/resume and the full reference set, use that skill.

A Goal is a completion contract for the user's requested outcome, not an implementation recipe. Never shrink or reinterpret the outcome; minimize only the surrounding prompt. Default to an inline condition. Set the goal through the runtime's native mechanism, or emit the exact `/goal …` line; never claim it was set unless it was.

## When to use

A Goal fits when the task has one durable objective, may take many iterations, and Done can be verified by commands, artifacts, diffs, screenshots, benchmarks, sourced evidence, or a written rubric. Bad fits: one small edit, "make it better" with no rubric, subjective output with no evidence, high-risk changes with no approval boundary — say so and suggest a normal prompt or a planning pass. If the only blocker is a missing verification surface, offer a preliminary Goal that builds it first (rubric, eval + baseline, checklist, or reproduction), with the main Goal to follow.

## Before drafting: the image

Reconstruct what the user is trying to create and why, in 2-4 sentences. This is the highest-leverage step — a wrong starting image is amplified across the whole autonomous run. The image fixes what and why; objective, evidence, constraints, and Done all follow from it. When the prompt is rough, mirror the image back compactly, bundling any critical questions, for one-pass correction before the long run begins.

Resolve ambiguity by risk:

- Ask first only when missing information could change the objective, evidence surface, Done, validation, scope, or a high-risk boundary (auth, security, billing, data handling, public contract, external side effects). Bundle the questions into one round trip.
- Encode low-risk, reversible ambiguity as a stated assumption and continue.
- Explore briefly — read anchors, search — when the evidence surface, validation, baseline, or blockers are discoverable rather than guessable. Do not start implementation during exploration.

## The contract

Write it in the task's own terms as plain prose, no labeled fields. Open with one line — what the outcome serves and for whom. Then cover, dropping any clause that would not change this run:

- **Objective** — one sentence naming the final, verifiable state. Not "improve X"; "X does Y, verified by Z."
- **Evidence / verification** — where Done is checked (running app, test output, benchmark, screenshot, sourced comparison, reviewable artifact). If none exists, require building the smallest practical one, or stop if that needs unavailable credentials or services.
- **Read first** — one or two mandatory anchors plus "discover adjacent docs/tests as needed." A path earns a place only if it is the scope boundary or evidence surface, or is genuinely not discoverable; the executor can find files, and enumerated paths go stale.
- **Constraints** — a scope rule (the simplest thing that meets the objective; no refactors, features, or abstractions beyond it), the 1-3 hard boundaries this task could actually break (named concretely), the catch-all "do not alter other externally visible contracts or cross destructive boundaries unless the objective requires it," and — when metrics, tests, or coverage are involved — anti-gaming: do not satisfy checks by deleting, weakening, bypassing, or narrowing required behavior, tests, or data.
- **Validation** — the real commands or artifact checks, with concrete targets by domain:
  - bugs: reproduce first; Done is the failing case passing with no related regressions
  - performance: metric, threshold, method, and runs (e.g. p95 < 250 ms over 3 runs)
  - tests/CI: the exact command and its pass condition
  - migration/batch: counts verified by query or grep, with the coverage bound stated
  - research: the decision it must enable, the sources in scope, the evidence standard
  - quality: an observable bar — lint/types/tests green, N reviewed examples, or a user-approved artifact
  - Where outcomes have distinct classes (success / failure / timeout), require evidence that each relevant class fired; a check that could not have failed proves nothing.
- **Done** — binary and evidence-bounded; requires the whole requested outcome, not every related improvement. Verified by a fresh-context check — an independent read-only subagent or equivalent, not self-review — before Done is claimed. State who decides findings: those touching correctness, safety, or Done block until fixed; the rest are the executor's call (fix, or keep with the reason recorded).
- **Run rules** (long or high-risk runs only) — report progress only against tool results, never claim unverified work as done; act on sufficient information and never end a turn on a plan or a promise; pivot within constraints when approaches stall; do not silently change the objective, Done, evidence, or scope (that is an amendment — stop and ask).
- **Block** — stop instead of thrashing when required behavior cannot be safely inferred, validation fails the same way after ~3 distinct approaches, a needed capability/credential/approval is blocked with no honest substitute, or a decision would touch schema/auth/billing/production without permission. Report state, evidence, attempts, the exact blocker, and the smallest decision needed.
- **Final report** — outcome first, plain words, the user's language, written for a reader who watched none of the run; name any decision the Goal left undefined that you settled by judgment.

**Length.** Shorter is better — a long Goal crowds out the model's own judgment. Most land around 800-1,800 characters; 2,500 is the ordinary ceiling, 4,000 the hard cap (Codex counts Unicode codepoints, Claude Code counts UTF-16 code units). If too long, cut examples, file lists, and optional operations before weakening objective, evidence, constraints, validation, or Done. Validate length once; if it fails, restructure rather than trim in loops.

## Parallel (decomposable work)

When the outcome splits into independent, separately verifiable units that share no state, put the structure in the Goal: a discovery rule for the units, a per-unit owned surface with its own evidence, item-by-item progress, and a parent integration check. Large work often stages as a phased pipeline: bootstrap → parallel research → parallel implementation → integrate → parallel adversarial/final verification.

- **Claude Code** fans out on its own judgment — a dynamic workflow, subagents for read-only stages and worktree isolation for write stages. No extra trigger.
- **Codex** — both parallel tools fire only from a `/goal` line the *user sends*, not from an auto-set goal, so deliver decomposable goals as a `/goal …` line for the user to send. Four rules keep it from silently running serial: subagents (`spawn_agent`) are the default worker (read-only work, and write units with cleanly partitioned files); `create_thread` (own worktree) only when an established project exists, since it needs a resolvable `projectId`; name the tool, not its arguments (no `projectId`/`target.type` — a non-visible id stalls it into serial); on an empty or non-git workspace, bootstrap (git init, build/test scaffold, committed interface contracts) before any write fan-out. Write directives flat — hedges like "when useful" make Codex run serially.

When those conditions do not hold — an interlocking refactor, a single-cause bug, a serially tuned metric — do not fan out writes; keep one write contract. A read-only investigation can still use subagents.

## Activate

Use the runtime's native goal tool when visible (Codex `create_goal`; check `get_goal` first and reuse a matching active goal instead of duplicating). Otherwise emit the exact `/goal …` line. **Exception:** for decomposable Codex work, do not auto-set — emit the `/goal …` line for the user to send (an auto-set goal does not parallelize). Never claim the goal was set unless it was.

## Readiness check (before activating)

Confirm, dropping n/a items: the intended-outcome image is formed (mirrored back when the prompt was minimal); one binary, evidence-bounded Done; evidence surface and validation are explicit or have a discovery rule; constraints are the 1-3 real boundaries plus anti-gaming, not a boilerplate denylist; fresh-context verification is required before Done; progress-against-tool-results and persistence rules are present on long runs; decomposable work carries the structure plus a runtime-sized launch directive (Codex: a user-sent `/goal` line); length checked once. If anything essential is missing or a critical decision is unresolved, fix it or ask before activating.
