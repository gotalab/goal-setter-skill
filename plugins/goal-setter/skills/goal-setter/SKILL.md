---
name: goal-setter
description: Clarify, lightly explore, draft, or activate a compact, outcome-first /goal completion contract for long-running implementation, migration, refactor, debugging, research, review, or validation work. Reconstructs the intended outcome first, asks only what changes it, writes a short binary-Done contract with anti-gaming and independent verification, and carries the verified Codex/Claude Code parallel mechanics (user-sent /goal line, subagents, create_thread, bootstrap-first). Use when a rough request needs Goal shaping before autonomous multi-step execution. Not for one-turn edits, ordinary Q&A, loose backlog brainstorming, or subjective work with no rubric.
---

# Goal Setter

Turn a rough request into a compact, outcome-first `/goal` completion contract — the shortest condition that still pins the requested outcome. Treat this as Goal intake: decide whether to ask, briefly explore, draft, activate, or say a normal prompt is a better fit.

A Goal is a completion contract for the user's requested outcome, not an implementation recipe. Never shrink or reinterpret the outcome; minimize only the surrounding prompt. Start from the smallest prompt that preserves the product/task contract, then add only clauses that change execution, verification, safety, or output. Default to an inline condition. Set the goal through the runtime's native mechanism, or emit the exact `/goal …` line; never claim it was set unless it was.

## When to use

A Goal fits when the task has one durable objective, may take many iterations, and Done can be verified by commands, artifacts, diffs, screenshots, benchmarks, sourced evidence, or a written rubric. Bad fits: one small edit, "make it better" with no rubric, subjective output with no evidence, high-risk changes with no approval boundary — say so and suggest a normal prompt or a planning pass. If the only blocker is a missing verification surface, offer a preliminary Goal that builds it first (rubric, eval + baseline, checklist, or reproduction), with the main Goal to follow.

## Before drafting: the image

If this intake will need tools, first send a one- or two-sentence visible preamble naming the first evidence you will check. Keep it concrete; do not write a plan that substitutes for doing the work.

Reconstruct what the user is trying to create and why, in 2-4 sentences. This is the highest-leverage step — a wrong starting image is amplified across the whole autonomous run. The image fixes what and why; objective, evidence, constraints, and Done all follow from it. When the prompt is rough, mirror the image back compactly, bundling any critical questions, for one-pass correction before the long run begins.

Resolve ambiguity by risk:

- Ask first only when missing information could change the objective, evidence surface, Done, validation, scope, or a high-risk boundary (auth, security, billing, data handling, public contract, external side effects). Bundle the questions into one round trip.
- Encode low-risk, reversible ambiguity as a stated assumption and continue.
- Explore briefly — read anchors, search — when the evidence surface, validation, baseline, or blockers are discoverable rather than guessable. Use the smallest evidence pass that can settle the goal: read one or two anchors first, repeat only when a required fact, command, boundary, or source is still missing. Do not start implementation during exploration.

## The contract

Write it in the task's own terms as plain prose, no labeled fields. Open with one line — what the outcome serves and for whom. Prefer decision rules over step sequences: describe the destination, constraints, evidence, and stop rules; leave the path open unless the exact path is part of the requirement. Use hard words like "must", "never", and "only" for true invariants (safety, destructive actions, required evidence, no weakening checks), and softer decision rules for judgment calls (when to search, ask, parallelize, retry, or pivot). Then cover, dropping any clause that would not change this run:

- **Objective** — one sentence naming the final, verifiable state. Not "improve X"; "X does Y, verified by Z."
- **Evidence / verification** — where Done is checked (running app, test output, benchmark, screenshot, sourced comparison, reviewable artifact). If none exists, require building the smallest practical one, or stop if that needs unavailable credentials or services.
- **Read first** — one or two mandatory anchors plus "discover adjacent docs/tests as needed." A path earns a place only if it is the scope boundary or evidence surface, or is genuinely not discoverable; the executor can find files, and enumerated paths go stale. This is a grounding budget, not a traversal script.
- **Constraints** — a scope rule (the simplest thing that meets the objective; no refactors, features, or abstractions beyond it), the 1-3 hard boundaries this task could actually break (named concretely), the catch-all "do not alter other externally visible contracts or cross destructive boundaries unless the objective requires it," and — when metrics, tests, or coverage are involved — anti-gaming: do not satisfy checks by deleting, weakening, bypassing, or narrowing required behavior, tests, or data.
- **Validation** — the real commands or artifact checks, with concrete targets by domain. Require the most relevant validation available, not every possible check:
  - bugs: reproduce first; Done is the failing case passing with no related regressions
  - performance: metric, threshold, method, and runs (e.g. p95 < 250 ms over 3 runs)
  - tests/CI: the exact command and its pass condition
  - migration/batch: counts verified by query or grep, with the coverage bound stated
  - research: the decision it must enable, the sources in scope, the evidence standard; report missing evidence as "unconfirmed," never as a factual "no"
  - quality: an observable bar — lint/types/tests green, N reviewed examples, or a user-approved artifact
  - if full validation is too expensive or unavailable, require the next honest check and a final report explaining the gap
  - Where outcomes have distinct classes (success / failure / timeout), require evidence that each relevant class fired; a check that could not have failed proves nothing.
- **Done** — binary and evidence-bounded; requires the whole requested outcome, not every related improvement. Verified before Done by an independent read-only pass, not self-review — on Codex write it as the imperative "spawn a read-only subagent (`spawn_agent`) to verify the evidence; do not self-review" (the words "fresh-context check" alone launch nothing there). State who decides findings: those touching correctness, safety, or Done block until fixed; the rest are the executor's call (fix, or keep with the reason recorded).
- **Run rules** (long or high-risk runs only) — report progress only against tool results, never claim unverified work as done; act on sufficient information and never end a turn on a plan or a promise; pivot within constraints when approaches stall; do not silently change the objective, Done, evidence, or scope (that is an amendment — stop and ask). On long autonomous runs, keep a concise `execution-notes.md`: append progress checkpoints and the mid-run decisions you made and why (for resume and audit), not a verbose log. `GOAL.md` is not needed — the active `/goal` is the contract.
- **Block** — stop instead of thrashing when required behavior cannot be safely inferred, validation fails the same way after ~3 distinct approaches, a needed capability/credential/approval is blocked with no honest substitute, or a decision would touch schema/auth/billing/production without permission. Report state, evidence, attempts, the exact blocker, and the smallest decision needed.
- **Final report** — outcome first, plain words, the user's language, written for a reader who watched none of the run; name any decision the Goal left undefined that you settled by judgment.

**Length.** Shorter is better — a long Goal crowds out the model's own judgment. Most land around 800-1,800 characters; 2,500 is the ordinary ceiling, 4,000 the hard cap (Codex counts Unicode codepoints; Claude Code counts UTF-16 code units). If too long, cut examples, file lists, and optional operations before weakening objective, evidence, constraints, validation, or Done. Validate length once with `python3 -B scripts/validate_goal_length.py <file>` (bundled; stdin also works); pass means activate, fail means restructure rather than trim in loops. If `python3` is unavailable, estimate once and move on.

## Parallel (decomposable work)

Subagents (`spawn_agent`) are the worker for read-only investigation, review, and verification on any goal — decomposable or not. They may handle write units only when the goal explicitly chooses subagent writes because `create_thread` is unavailable, the workspace is not an established project/worktree base, or the unit is small enough that a worktree would add more coordination than isolation. On Codex you must name subagent use explicitly and imperatively in the goal text; a goal that is silent, or grants only abstractly ("use subagents"), runs everything in-context.

When the outcome splits into independent, separately verifiable units that share no state, put the structure in the Goal: a discovery rule for the units, a per-unit owned surface with its own evidence, item-by-item progress, a parent integration check, and an explicit instruction to fan the units out in parallel and then synthesize. That parallel invitation is runtime-agnostic — a Claude Code run realizes it as a dynamic workflow, and a Codex run via the tools below — but do not leave it implicit on either runtime, or the run may go serial. Large work often stages as a phased pipeline: bootstrap → parallel research → parallel implementation → integrate → parallel adversarial/final verification.

- **Claude Code** realizes that invitation as a dynamic workflow on its own judgment — discover the units, dispatch them in parallel (subagents for read-only stages, worktree isolation for write stages), and synthesize; the active run owns orchestration. Describe the structure and the fan-out in the goal, not the mechanism.
- **Codex** — both parallel tools fire only from a `/goal` line the *user sends*, not from an auto-set goal, so deliver decomposable goals as a `/goal …` line for the user to send. The drafter must choose the write fan-out mechanism before emitting the goal; do not put `create_thread` in parentheses, behind "or", after a `spawn_agent` write alternative, or under hedges like "when useful" / "if appropriate" / "only if needed":
  - for multiple non-trivial write units with separable file ownership in an established Codex project with a usable git HEAD, make `create_thread` mandatory: create one separate thread per write unit, each in its own worktree, and run them in parallel;
  - each child thread's initial prompt must assign exactly one unit, its owned surface (and files only once known), validation evidence, integration contract, and instruct the child to set a goal scoped to that unit before editing (the human sends only the top-level `/goal`);
  - use `spawn_agent` for read-only research/review/final verification; use it for write units only when `create_thread` is unavailable, the repo is not a usable worktree base, or the chosen unit is too small for worktree isolation, and say that fallback explicitly in the goal;
  - name the tools, not their schema arguments (no `projectId`/`target.type` — a non-visible id stalls it into serial);
  - on an empty or non-git workspace, bootstrap (git init, build/test scaffold, committed interface contracts) before any write fan-out.

  So the emitted goal carries a line like: *"This work has <N> non-trivial write units: <units>. In Codex, do not implement those write units serially in the main thread. First verify the repo is an established git project with a usable HEAD; if not, bootstrap git + scaffold + interface contracts in the main thread. Then create one separate thread with `create_thread` per write unit, each in its own worktree. In each child thread's initial prompt, assign exactly one unit, owned surface (and files once discovered), validation evidence, integration contract, and instruct it to set a unit-scoped goal before editing. Run the child threads in parallel, integrate in the main thread, and gate Done on every unit's evidence plus an integration check. Use `spawn_agent` only for read-only research/review/final verification unless you explicitly report that `create_thread` is unavailable."*

When those conditions do not hold — an interlocking refactor, a single-cause bug, a serially tuned metric — do not fan out writes; keep one write contract. A read-only investigation can still use subagents.

## Activate

Use the runtime's native goal tool when visible (Codex `create_goal`; check `get_goal` first and reuse a matching active goal instead of duplicating). Otherwise emit the exact `/goal …` line. **Exception — the linchpin for Codex parallelism:** for decomposable Codex work, do not auto-set. Emit the `/goal …` line for the user to send, and tell them plainly that *their* sending it is what fires the parallel cascade — Codex's `spawn_agent`/`create_thread` start only from the user's own typed request, so an auto-set goal (or one the user never sends) runs fully serial. Never claim the goal was set unless it was.

## Readiness check (before activating)

Confirm, dropping n/a items: the intended-outcome image is formed (mirrored back when the prompt was minimal); one binary, evidence-bounded Done; evidence surface and validation are explicit or have a discovery rule; constraints are the 1-3 real boundaries plus anti-gaming, not a boilerplate denylist; independent-verification before Done is required (Codex: written as an explicit "spawn a read-only subagent to verify" imperative, not the words "fresh-context"); progress-against-tool-results and persistence rules are present on long runs; decomposable work carries the structure plus a runtime-sized launch directive (Codex: a user-sent `/goal` line); length checked once. If anything essential is missing or a critical decision is unresolved, fix it or ask before activating.
