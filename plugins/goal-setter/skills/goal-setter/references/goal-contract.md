# Goal Contract Reference

Read this before drafting, activating, or auditing any non-trivial Goal. This file is the detailed contract surface; keep `SKILL.md` focused on routing and mode selection.

## Core Shape

A Goal is a completion contract for the user's requested outcome, not a detailed implementation recipe. It should name one final, verifiable state and leave bounded execution judgment to the agent.

The contract should demand end-to-end completion of the requested outcome while keeping Done evidence-bounded. Avoid open-ended perfection claims or exhaustive-world wording.

The first sentence must carry the main objective by itself. If the reader cannot tell what Done means from the objective, evidence surface, and Done clause without parsing operational instructions, the Goal is too diffuse.

Use context-minimalist wording. Do not shrink or reinterpret the user's requested outcome; minimize only the surrounding prompt. Include context and instructions only when they materially affect evidence, constraints, validation, autonomy, progress visibility, or stop conditions. Prefer discovery rules over long preloaded context when the repo, spec, tests, or evidence surface can reveal the details during execution.

Every inline Goal or `GOAL.md` must cover:

- a one-line opener: what the outcome serves and for whom, compressed from the intended outcome image (plain prose; a `Context:` label is optional)
- one objective
- evidence surface / verification environment
- context to read first
- task-specific constraints and anti-gaming rule
- validation or validation discovery rule
- subagent/context-separation policy, including fresh-context verification before claiming Done
- visible progress / checkpoint reporting rule, with progress claims audited against tool results
- persistence rule
- progress/pivot rule
- done condition
- block condition
- final report rule (outcome first, plain words, user's language)

Every non-trivial Goal should explicitly allow available governed subagents for separable investigation, research, validation discovery, triage, strategy review, and final fresh-context review; prefer read-only subagents unless an external side effect is required and allowed. Keep the authorization short but present — it mainly shapes Claude Code, which fans out on its own judgment. For parallel fan-out (decomposition, multi-aspect review, multi-topic research), put the decomposition structure in the Goal (see §Inline Goal Condition) and size the launch directive to the runtime; the runtime mechanics — Claude Code's dynamic workflow, and Codex's user-sent `/goal` line with subagent/`create_thread` rules — live in `references/runtime-capabilities.md`.

Cover does not mean spell out. Objective, verification, the boundaries that matter, Done, and stop rules belong in every Goal. The governance clauses — checkpoint reporting, evidence-audited progress claims, persistence, fresh-context verification, the final report rule — earn their characters on long or high-risk autonomous runs; on short low-risk goals, drop the ones whose absence would not change the run. Current models already do much of this well by default, so write a rule only where a violation would be costly.

Use measurable targets where they are meaningful. Use observable evidence when strict measurement would be brittle or would distort the work.

Before setting a Goal, resolve ambiguity that could produce the wrong outcome. Ask the necessary focused questions together when missing decisions affect the objective, evidence surface, Done condition, scope, safety, public contract, auth, security, billing, data handling, production dependencies, or another high-risk boundary. For low-risk implementation details, prefer autonomous progress when a safe, reversible assumption or observable evidence rule can be inferred from the spec, evidence surface, tests, docs, or nearby product behavior.

## Intended Outcome Image

Before clarifying, exploring, or drafting, reconstruct a short intended outcome image: what the user is actually trying to create or achieve, and why it matters, in 2-4 sentences. Derive the rest of the contract from it in order: the image fixes what the finished state looks like and why; the evaluation criteria follow from the image; the constraints follow from the criteria; the objective, evidence surface, and Done clause express them. You cannot write honest criteria, constraints, or Done for an outcome you cannot yet picture, so resolve the image first.

The image fixes what and why; it does not fix how. Leave implementation method, sequencing, and tactics to the agent. Capture the intended outcome of this task only, not the user's general values, preferences, or working style.

Because a Goal runs autonomously and long, a wrong starting image is amplified across the whole run, so an honest image is a precondition for an honest contract and the cheapest place to correct course. Reach a trustworthy image dynamically: infer from the request, repo, tests, docs, and nearby behavior; run bounded exploration when reality is unknown but discoverable; ask only the highest-leverage questions when intent is user-owned. When the prompt is minimal or rough, mirror the reconstructed image back compactly so the user can correct it in one pass before the long run begins; bundle any critical clarification questions into that same message so the user answers in one round trip.

Compress the image into a single opening line: what the outcome serves and for whom. Knowing the reason behind the request, not only the request, lets the executor connect forks and tradeoffs to the real intent instead of guessing it. Write it as plain prose; a `Context:` label on it is optional — add it only when the opener might be misread as a requirement to verify (rare, since the evaluator keys on the Done clause). Keep the rest of the image out of the Goal; it shapes the objective, evidence, validation, constraints, and Done.

## Clarification Gate

Before drafting or activating a Goal, decide whether the request can be converted into an honest completion contract without guessing the user's real intended outcome.

Ask before setting the Goal when missing information could change:

- objective or target outcome
- evidence surface or Done condition
- validation method, metric, threshold, or comparison baseline
- scope boundary, coverage claim, or omitted areas
- external side effects, approvals, deployments, account actions, messages, purchases, writes, or public artifacts
- data, credential, source, privacy, retention, runtime, paid service, or environment requirements
- public contract, schema, auth, security, billing, legal, financial, medical, safety, or other high-risk boundary

Question style:

- Ask the smallest complete set of focused questions needed to preserve the user's intended outcome. Keep them easy to answer, but do not cap the count if more questions are genuinely required to avoid building the wrong thing.
- Phrase questions so the user can answer quickly in everyday language; translate domain jargon into concrete choices or examples when possible.
- Include a recommended default only when it is safe, reversible, and does not narrow the requested outcome.
- Do not ask routine implementation questions that the agent can safely infer from the repo, tests, docs, evidence surface, or nearby product behavior.
- If the user wants activation and the missing decision is critical, ask and wait instead of setting a vague Goal.

If the ambiguity is low-risk and reversible, encode the assumption in the Goal and continue. The Goal should make those assumptions visible through the evidence, validation, Done, or block clauses rather than hiding them in the executor's reasoning.

## Bounded Exploration Gate

Use short exploration when the missing information is discoverable by the agent and an honest Goal would otherwise guess at the evidence surface, validation, current state, or blockers.

Explore before drafting or activating when unknown discoverable facts could change:

- which files, docs, specs, tests, scripts, dashboards, datasets, or artifacts are the evidence surface
- which validation commands, benchmarks, screenshots, data checks, or review artifacts are realistic
- current baseline, failing state, data shape, model target, output format, or source freshness
- required credentials, unavailable services, sandbox limits, writable locations, or external capability blockers
- whether the request is a good Goal fit or should stay a normal prompt, plan, or research pass

Do not explore when the missing decision is user-owned. Ask instead when the decision depends on intent, acceptable tradeoff, business meaning, risk tolerance, approval boundary, target audience, desired output, or what "good enough" means.

Keep exploration bounded:

- read only the smallest useful anchors first: `AGENTS.md`, the user-provided request/spec, nearby docs/tests/scripts, package or CI metadata, and obvious evidence artifacts
- use search and lightweight inspection before broad reading
- do not start implementation, refactoring, external writes, commits, deployments, account actions, or data-changing work during exploration
- use subagents only when a separable read-only check, source-backed research pass, validation discovery, or strategy review materially improves Goal readiness
- stop exploration once the Goal can honestly state objective, evidence, validation/discovery rule, constraints, Done, and block conditions

After exploration, do exactly one of:

- draft or activate the Goal with the discovered evidence and validation surface
- ask the remaining user-owned questions in plain language
- say the task is not a good Goal fit and suggest a normal prompt or plan first

When reporting exploration, keep it short: facts found, remaining unknowns that matter, and the proposed next action. Do not paste raw inventories unless they are the evidence surface.

## Inline Goal Condition

Default to an inline goal condition. The must-cover elements are the contract, not any fixed sentence order or stock phrasing: write the condition in the task's own terms, drop clauses that genuinely do not apply, and treat numeric defaults (stalled-approach triggers, retry counts) as defaults to tune, not rules to copy.

Reference shape for a full-governance goal (adapt freely; on short low-risk runs most governance clauses drop out):

```text
This serves <who/what> by <why the outcome matters>; <objective>. Verify success through <evidence surface>. Read <minimal context> and discover adjacent tests/docs as needed. Keep changes scoped to the objective and do the simplest thing that meets it — no refactors, features, or abstractions beyond it; do not alter <the 1-3 boundaries that matter for this task> or other externally visible contracts or destructive boundaries unless the objective explicitly requires it. Validate with <known checks> or discover and run relevant checks. Use available governed subagents when materially useful for separable research, validation discovery, triage, or strategy review; <when decomposable, add the structure and a runtime-sized launch directive — e.g. "treat each independent <unit> as a separately verifiable piece owning only its <files>; fan out the units in parallel (Codex: bootstrap the baseline first if the workspace is empty, then spawn read-only subagents for research/review and fan out write units in parallel — over partitioned files, or create_thread per unit (each in its own worktree with a goal scoped to that unit) when an established project exists — and gate Done on every unit's evidence plus an integration check over the merged result">; before claiming Done, verify the evidence with a fresh-context check, not self-review — on Codex spell this concretely as "spawn a read-only subagent to verify the evidence; do not self-review" (an abstract "fresh-context check" is read as self-review there), else an equivalent independent pass; fix findings that block Done, and fix or keep-with-recorded-reason the rest. Maintain visible progress with checkpoint updates in the user's language; before reporting progress, audit each claim against a tool result from this run — unverified work is reported as unverified, never as done. When you have enough information to act, act; do not ask permission for reversible in-scope actions, and never end a turn on a plan or a promise. Done when <binary evidence-backed condition>. If approaches stop improving evidence, review strategy and pivot within constraints; do not silently change the objective, Done, evidence, constraints, or coverage claim. Stop only if <block rules>. The final report is for a reader who watched none of the run: outcome first, plain words, in the user's language, naming any decisions this Goal left undefined.
```

Instantiate every placeholder in the task's own terms: the opening line comes from the intended outcome image (mark it with an optional `Context:` label only if helpful), and the constraint boundaries name only what this task could actually break.

When the work is decomposable, write the structure into the Goal: a discovery rule for the independent units (state the rule, do not enumerate units you cannot yet name), an owned surface and its own Done evidence or deliverable per unit, item-by-item progress, and a parent integration/synthesis check. This structure is runtime-agnostic and gives the contract its value even with no parallelism. Add the launch directive that fits the runtime — Claude Code's dynamic workflow, or Codex's user-sent `/goal` line following the rules in `references/runtime-capabilities.md`. When the work is not decomposable, leave all of this out.

Length budget:

- Shorter is better. The right length is the shortest contract in which every sentence can change the executor's behavior; most goals should land around 800-1,800 characters. Treat 2,500 as the ordinary ceiling, not a target.
- A long Goal does not just cost tokens — it crowds out the model's own judgment. When the text reads like it is steering every move, cut until only outcome, verification, boundaries, and stops remain.
- <= 3,500 characters for portable Codex/Claude Code goals. Hard cap <= 4,000 — the actual runtime limit in both; exactly 4,000 passes. The runtimes count differently: Codex counts Unicode codepoints of the trimmed objective, Claude Code counts UTF-16 code units, so emoji and other astral characters count as 2 there. Japanese and other BMP text counts 1 per character in both.
- Check the final condition once with the skill's `scripts/validate_goal_length.py`; it reports both counts and enforces the stricter one. Validate once: if it passes, activate without further shortening; if it fails, restructure — cut clauses or move durable detail to sidecars — instead of looping on small trims. More than one failed validation means the draft shape failed, not the counter.
- If too long, compress examples, context lists, and optional operations before weakening objective, evidence, constraints, validation, subagent policy, progress/pivot, done, or block conditions.
- If still too long, ask whether to use sidecar files plus a compact launcher objective for durable audit/resume or plan/spec ownership, or split/narrow the Goal.

Do not hide essential completion criteria only in sidecar files when targeting runtimes or evaluators that may not reliably inspect sidecar files. The condition and transcript evidence must still let the evaluator judge completion.

Keep optional operational patterns such as checkpoint commits, draft PRs, or external notifications out of the core condition unless the user asks or the run is expected to last hours, span many files, or leave experimental artifacts.

Before activation, run a bloat pass:

- Delete examples, repeated synonyms, explanatory rationale, and implementation sequencing that do not change Done.
- Replace boilerplate constraint denylists with the 1-3 boundaries that matter for this task plus the general externally-visible-contracts criterion (see Constraints).
- Replace long file lists with mandatory anchors plus a discovery rule unless every listed file is part of the evidence surface.
- Replace step-by-step implementation instructions with constraints, validation, and pivot rules. Preserve "what must be true", not "how to build it", unless the user explicitly requires a specific method.
- Keep optional operations such as commits, PRs, sidecars, notifications, or external writes out unless they are requested or required for honest Done evidence. Keep reflexive, unbounded fan-out out; but for genuinely decomposable work keep the decomposition structure and runtime-sized launch directive — these are required, not optional (see the audit item and `references/runtime-capabilities.md`).
- Keep subagent/delegation authorization — including any parallel-decomposition grant when the work qualifies — explicit for non-trivial Goals even when compressing; omission changes runtime behavior.
- If the Goal still reads like a project plan, produce an inline objective plus optional sidecar content instead of stuffing the plan into the native Goal text.

Preserve execution freedom:

- Do not encode routine implementation order, architecture choices, tool order, file edit order, or debugging steps when the repo can determine them.
- Allow small reversible assumptions and better discovered validation/evidence methods when they preserve the same user outcome.
- Specify only the hard boundaries this task could actually break, plus the general externally-visible-contracts criterion (see Constraints); leave low-risk implementation tactics to the agent.

## Objective

Use one sentence that names the final, verifiable state.

Bad:

- Improve checkout.
- Implement the feature.
- Make this better.

Good:

- Implement the checkout confirmation flow so the user can complete payment, see confirmation, and existing checkout tests plus new confirmation-path tests pass.

## Context to Read First

List the smallest useful set of files, docs, issues, screenshots, failing logs, or tests.

A path or identifier earns a place in the Goal only when it is the scope boundary or evidence surface, or is genuinely not discoverable. The executor can find files, so pre-loading them is "how" leaking into a "what" contract, and enumerated paths go stale when files move. Otherwise name one or two mandatory anchors and a discovery rule. For implementation Goals, list the spec, core contract docs, key entrypoints, and key tests, then say to discover adjacent implementation/docs/tests as needed. Exhaustive file lists are appropriate only when those exact files are the evidence surface or required scope.

If unknown, include:

- `AGENTS.md` if present
- the provided spec/issue/request
- relevant tests and docs discovered in the project

## Evidence Surface / Verification Environment

State where the final result can be checked. This can be a running app, browser screenshot, test output, benchmark, source-backed comparison table, decision memo, spreadsheet, CRM-ready list, customer-facing draft, or other reviewable artifact.

If the evidence surface is missing or unrealistic, require the agent to create the smallest practical verification surface or stop if that requires unavailable credentials, services, devices, data, or user approval.

When the outcome itself cannot be measured yet — no rubric, no eval, no checklist, no baseline — do not draft a vague main Goal. Propose a preliminary Goal whose Done is the verification surface itself: a written rubric, an eval set with a baseline score, a checklist, or a reliable reproduction. The main Goal then starts against an honest evaluator instead of a guess. This turns "subjective output with no rubric" from a bad fit into a two-stage path; offer the pair, and activate only the preliminary Goal first.

## Constraints

Instantiate constraints per task; do not paste a generic denylist. Current frontier models follow decision criteria better than exhaustive enumerations, and boilerplate lists carried from older prompts dilute the boundaries that actually matter. Write:

- a scope rule: keep changes scoped to the objective; do the simplest thing that meets it — no refactors, features, or abstractions beyond it, no unrelated cleanup.
- the 1-3 hard boundaries this task could actually break, named concretely (e.g. "public API signatures unchanged", "auth behavior unchanged", "no schema migration"). Pick them from the intended outcome image and the evidence surface.
- one general criterion as the catch-all: do not alter externally visible contracts or cross destructive boundaries unless the objective explicitly requires it.
- the anti-gaming rule when metrics, tests, coverage, rankings, or visual criteria are involved: do not satisfy them by deleting, weakening, bypassing, or narrowing required behavior, tests, data, sources, or review criteria unless explicitly approved.
- prefer the smallest reversible assumption when the spec is incomplete.

## Validation

Prefer executable checks. Include the best available commands or artifact checks.

Examples:

- `pnpm lint`
- `pnpm test`
- `pnpm build`
- `pytest tests/<area>`
- Playwright screenshot comparison
- benchmark threshold
- eval score threshold
- coverage does not decrease for the touched module
- target latency remains below `<threshold>`
- final diff review confirms the task's named hard boundaries were not crossed

Make targets concrete by domain — numbers that represent real success, not decorative precision:

- bugs: reproduce first, fix second; success is the failing case now passing, with no related regressions
- tests/CI: the exact command and its required pass condition
- performance: metric, threshold, measurement method, and number of runs (e.g. p95 < 250 ms across 3 consecutive benchmark runs)
- quality work: an observable acceptance bar — lint/typecheck/tests green, N reviewed examples, or a user-approved artifact
- research: the decision the research must enable, the sources in scope, and the evidence standard
- migrations/batch work: counts verified by query or grep (records migrated, references removed), with the coverage bound stated
- operations: healthy state, monitoring window, failure threshold, and rollback trigger

Prefer discriminating evidence: a check that could not have failed proves nothing. When Done depends on behavior with distinct outcome classes (success, failure, unreachable, timeout), require evidence that each relevant class actually fired, constructing a case when one does not occur naturally — an unreachable URL for the failure path, a fixture for the edge case. How to construct it stays the executor's choice. Drop this clause when the behavior has only one outcome class.

If validation is unknown, require the agent to discover relevant validation commands from repo docs, scripts, package metadata, nearby CI config, or the evidence surface, then record what was run when notes are used.

For visual Goals, convert references into checklist or design-system criteria where possible. Do not chase pixel-perfect asset recreation unless the user explicitly requires it.

When an independent verification harness is available (a check-pack or verification skill that runs its own checks and reports ready/blocked), its report can serve directly as Done evidence — "Done when the verification run reports ready with zero failed critical checks" is a strong, transcript-visible criterion.

## Research Goals

For source-backed research or investigation Goals, add two rules that do not belong in implementation Goals:

- Evidence budget: use the minimum evidence sufficient to answer correctly, cite it precisely, then stop searching. Define when one broad pass suffices versus when additional lookups are required, so the run neither under-sources claims nor searches without a stopping rule.
- Absence versus negation: lack of evidence is reported as "unconfirmed", never converted into a factual "no". Preserve the distinction between missing data and confirmed negatives in the final artifact.

## Progress and Pivot

Keep progress visible in whatever form fits the run — a concise checklist with per-item status (e.g. not started / in progress / complete / blocked) is the usual default. At meaningful checkpoints, report in the user's language (match the language of the request):

- progress made
- evidence confirmed
- remaining work
- next step

Ground every progress claim: before reporting, audit each claim against a tool result from the run. Unverified work is reported as unverified, never as done. Keep this in the Goal text rather than treating it as implied.

Include a persistence rule: when the executor has enough information to act, it acts — it does not ask permission for reversible in-scope actions, and it never ends a turn on a plan, a question it can answer itself, or a promise about work not yet done. The block rules define the only legitimate stops.

Do not update so often that reporting displaces execution. If a design judgment is needed, record the adopted option and reason instead of leaving ambiguity hidden. If commits are explicitly in scope, summarize implemented changes, validation, and next actions before and after committing.

The final report addresses a reader who watched none of the run: outcome first, then supporting detail, in complete sentences and plain words in the user's language — no working shorthand, arrow chains, or labels invented mid-run. It also names any decision the Goal text left undefined and the executor settled by judgment, so contract gaps surface for the next Goal instead of staying invisible. This disclosure rule is what keeps Goals short: the executor improvises freely inside the constraints and discloses, rather than the contract trying to anticipate every gap.

Compare progress against the Done condition using evidence, not effort spent.

When distinct approaches stop improving the evidence surface (two failed approaches is the default trigger; tune it to the task's cost of iteration), use read-only strategy review when available: diagnose why progress is stalled, and recommend whether to continue, narrow, change approach, improve validation, or stop.

Apply the smallest bounded pivot that preserves the Goal constraints. The executor may change tactics, sequencing, validation discovery, implementation approach, or a reversible low-risk assumption when that makes the same Done condition more achievable. Small self-improvements are expected when they protect the real user outcome: tighten or replace a weak validation method with a better discovered one, refine an observable Done criterion, add a better evidence artifact, or clarify a low-risk assumption, as long as the objective and requested outcome are not narrowed or changed.

Do not silently change the Goal's objective, Done condition, evidence surface, safety constraints, approval boundaries, or final coverage claim. If those need to change, treat it as a Goal amendment: record the reason and proposed before/after wording when notes are used, then stop under On block and ask for the smallest user decision unless the user already gave explicit authority for that class of change.

Safe refinements do not require a Goal amendment when they only tighten evidence, add or replace discovered validation, add newly discovered context files, improve the observable Done wording, clarify a low-risk reversible assumption, or narrow implementation tactics without narrowing the requested outcome. Record material refinements in notes when notes are used, but continue autonomously.

If the Goal itself appears invalid, unsafe, materially underspecified, or impossible to satisfy with honest evidence, stop under On block and ask for the smallest user decision.

## Done When

Make completion binary and evidence-bounded. Done should require the whole requested outcome, not every theoretically related improvement. Include:

- requested behavior is implemented
- evidence surface confirms the requested final state
- measurable targets are met where defined
- required validation passes, or any remaining failure is proven unrelated and documented with evidence
- broad or sampled work records coverage bounds and omitted areas
- the evidence is verified before Done by an independent read-only subagent or equivalent, not self-review — on Codex written as the imperative "spawn a read-only subagent to verify the evidence; do not self-review" (the bare phrase "fresh-context check" launches nothing there)
- notes are current and reviewable when sidecars are used
- final diff is scoped to intended code/tests/docs plus any run files
- final response summarizes implementation, evidence, and user-review-needed decisions

When verification or review produces findings, the contract should say who decides their fate — otherwise the executor's disposition is an unauthorized improvisation, however sensible. Default: findings that touch correctness, safety, or the Done condition block Done until fixed; everything else is the executor's call — fix it, or keep it and record the reason in the final report (execution-notes when sidecars are used). This is a delegation of discretion, not a constraint; do not expand it into a severity taxonomy.

Avoid Done clauses like "all possible issues are resolved" unless there is an explicit coverage rule. Prefer "requested behavior, affected docs/skill/help/tests, stale-surface scans, and required validation are complete" or another bounded evidence statement.

## On Block

Stop instead of thrashing if:

- required behavior cannot be safely inferred
- validation fails for the same blocker after 3 distinct approaches with no improvement
- the task requires forbidden scope changes
- a required service agent, MCP server, app action, network path, browser/computer capability, approval, or writable location is blocked and no honest in-sandbox substitute can satisfy Done
- missing credentials, external services, or unavailable artifacts block validation
- a decision would affect schema, public API, auth, security, billing, data retention, or production dependencies without explicit permission

Do not stop merely because:

- the first validation command fails
- validation commands are unknown and discoverable
- completion criteria need a concrete observable evidence rule that can be safely inferred
- a small reversible implementation choice is needed
- a separable investigation, research task, or final review can be delegated
- an external action needs approval and the runtime can request it
- notes need to be updated before continuing

When blocked, report:

- current state
- evidence collected
- attempted fixes
- exact blocker
- smallest user decision needed

## Goal Readiness Audit

Before activation, score each applicable item 0, 1, or 2. Items that genuinely do not apply to this Goal (e.g. measurable targets for evidence-only work, sidecar items for inline goals) are n/a — do not pad the Goal with clauses just to satisfy the audit.

- One objective
- Intended outcome image formed; objective, evidence, and Done derived from it; image mirrored back for one-pass correction when the prompt was minimal
- Context line opens the Goal: what the outcome serves and for whom, compressed from the image
- Clarification gate passed, or unresolved questions were asked before activation
- Bounded exploration gate passed when discoverable project/data/tool/validation facts were needed
- Binary, evidence-bounded Done (not an unbounded "perfect everything" condition)
- Measurable targets used where meaningful
- Subjective criteria converted to observable evidence where measurement is not appropriate
- Evidence surface / verification environment is explicit or has a discovery rule
- Concrete validation surface or a discovery rule for validation
- Anti-gaming constraint included when metrics, tests, coverage, rankings, or visual criteria are involved
- Constraints instantiated for this task (1-3 concrete boundaries plus the general criterion), not a boilerplate denylist
- Progress claims are required to be audited against tool results; unverified work reported as unverified
- Persistence rule present: act on sufficient information, never end a turn on a plan or promise
- Fresh-context verification (independent subagent or equivalent) required before Done is claimed
- Verification-findings disposition stated: blocking findings fix, the rest fix-or-record at the executor's discretion
- Evidence is discriminating where outcome classes exist: each relevant class fires, with constructed cases when natural occurrence is luck-dependent
- Final report rule present: outcome first, plain words, user's language, written for a reader who watched none of the run, naming decisions the Goal left undefined
- Inline condition length checked once with `scripts/validate_goal_length.py` when shell is available: ordinary ceiling <= 2,500 characters, portable <= 3,500, hard cap <= 4,000
- Bloat pass completed: no repeated rationale, long examples, avoidable file lists, or optional operations that weaken the main objective
- Execution freedom preserved: the Goal states outcome, evidence, constraints, validation, pivot, Done, and block rules without unnecessary implementation sequencing
- Autonomous continuation path covers investigation, implementation, validation, and review
- Visible progress rule covers checklist status and checkpoint reporting without forcing excessive updates
- Progress/pivot path covers stalled approaches without changing the Goal itself
- Goal-amendment boundary prevents silent changes to objective, Done, evidence, constraints, approval boundaries, or final coverage claims
- Subagent/delegation policy present; for decomposable work, the decomposition structure (discovery rule, per-unit owned surface and evidence, integration check) plus a runtime-sized launch directive (Codex: flat-imperative, no hedge words, delivered as a `/goal …` line per `references/runtime-capabilities.md`). For non-decomposable work, correctly absent
- Broad claims have an explicit coverage bound or an honest discovery/omission reporting rule
- On block rules included
- High-risk changes are blocked or explicitly allowed

If sidecars are used, also check:

- Run ID is ordered and searchable
- Exactly two run files are created
- Execution notes are required
- Compact launcher objective points to `GOAL.md` and avoids restating the sidecar plan in full

If any score is 0, revise before activation. If safe revision is impossible because required decisions are missing, ask the smallest complete set of focused questions needed to make the Goal safe and correct.
