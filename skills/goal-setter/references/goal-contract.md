# Goal Contract Reference

Read this before drafting, activating, or auditing any non-trivial Goal. This file is the detailed contract surface; keep `SKILL.md` focused on routing and mode selection.

## Core Shape

A Goal is a completion contract for the user's requested outcome, not a detailed implementation recipe. It should name one final, verifiable state and leave bounded execution judgment to the agent.

The contract should demand end-to-end completion of the requested outcome while keeping Done evidence-bounded. Avoid open-ended perfection claims or exhaustive-world wording.

The first sentence must carry the main objective by itself. If the reader cannot tell what Done means from the objective, evidence surface, and Done clause without parsing operational instructions, the Goal is too diffuse.

Use context-minimalist wording. Do not shrink or reinterpret the user's requested outcome; minimize only the surrounding prompt. Include context and instructions only when they materially affect evidence, constraints, validation, autonomy, progress visibility, or stop conditions. Prefer discovery rules over long preloaded context when the repo, spec, tests, or evidence surface can reveal the details during execution.

Every inline Goal or `GOAL.md` must cover:

- one objective
- evidence surface / verification environment
- context to read first
- constraints and anti-gaming rule
- validation or validation discovery rule
- subagent/context-separation policy
- visible progress / checkpoint reporting rule
- progress/pivot rule
- done condition
- block condition

Every non-trivial Goal should explicitly allow available governed subagents for separable investigation, source-backed research, validation discovery, test-failure triage, strategy review when progress stalls, and final review. Prefer read-only subagents unless an external side effect is required, allowed by policy, and part of end-to-end completion. Do not rely on implicit agent autonomy or generic "use tools" wording for this permission; keep the authorization short but present.

Use measurable targets where they are meaningful. Use observable evidence when strict measurement would be brittle or would distort the work.

Before setting a Goal, resolve ambiguity that could produce the wrong outcome. Ask the necessary focused questions together when missing decisions affect the objective, evidence surface, Done condition, scope, safety, public contract, auth, security, billing, data handling, production dependencies, or another high-risk boundary. For low-risk implementation details, prefer autonomous progress when a safe, reversible assumption or observable evidence rule can be inferred from the spec, evidence surface, tests, docs, or nearby product behavior.

## Intended Outcome Image

Before clarifying, exploring, or drafting, reconstruct a short intended outcome image: what the user is actually trying to create or achieve, and why it matters, in 2-4 sentences. Derive the rest of the contract from it in order: the image fixes what the finished state looks like and why; the evaluation criteria follow from the image; the constraints follow from the criteria; the objective, evidence surface, and Done clause express them. You cannot write honest criteria, constraints, or Done for an outcome you cannot yet picture, so resolve the image first.

The image fixes what and why; it does not fix how. Leave implementation method, sequencing, and tactics to the agent. Capture the intended outcome of this task only, not the user's general values, preferences, or working style.

Because a Goal runs autonomously and long, a wrong starting image is amplified across the whole run, so an honest image is a precondition for an honest contract and the cheapest place to correct course. Reach a trustworthy image dynamically: infer from the request, repo, tests, docs, and nearby behavior; run bounded exploration when reality is unknown but discoverable; ask only the highest-leverage questions when intent is user-owned. When the prompt is minimal or rough, mirror the reconstructed image back compactly so the user can correct it in one pass before the long run begins; bundle any critical clarification questions into that same message so the user answers in one round trip. Keep the image out of the Goal text itself; let it shape the objective, evidence, validation, constraints, and Done. A single intent or north-star line may survive into the Goal only when it changes the agent's judgment at forks.

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

Default to an inline goal condition.

Length budget:

- Target <= 2,500 characters for ordinary inline goals.
- Target <= 3,500 characters for portable Codex/Claude Code goals.
- Hard cap <= 4,000 characters.
- If too long, compress examples, context lists, and optional operations before weakening objective, evidence, constraints, validation, subagent policy, progress/pivot, done, or block conditions.
- If still too long, ask whether to use sidecar files plus a compact launcher objective for durable audit/resume or plan/spec ownership, or split/narrow the Goal.

Do not hide essential completion criteria only in sidecar files when targeting runtimes or evaluators that may not reliably inspect sidecar files. The condition and transcript evidence must still let the evaluator judge completion.

Keep optional operational patterns such as checkpoint commits, draft PRs, or external notifications out of the core condition unless the user asks or the run is expected to last hours, span many files, or leave experimental artifacts.

Before activation, run a bloat pass:

- Delete examples, repeated synonyms, explanatory rationale, and implementation sequencing that do not change Done.
- Replace long file lists with mandatory anchors plus a discovery rule unless every listed file is part of the evidence surface.
- Replace step-by-step implementation instructions with constraints, validation, and pivot rules. Preserve "what must be true", not "how to build it", unless the user explicitly requires a specific method.
- Keep optional operations such as commits, PRs, sidecars, broad fan-out, notifications, or external writes out unless they are requested or required for honest Done evidence.
- Keep subagent/delegation authorization explicit for non-trivial Goals even when compressing; omission changes runtime behavior.
- If the Goal still reads like a project plan, produce an inline objective plus optional sidecar content instead of stuffing the plan into the native Goal text.

Preserve execution freedom:

- Do not encode routine implementation order, architecture choices, tool order, file edit order, or debugging steps when the repo can determine them.
- Allow small reversible assumptions and better discovered validation/evidence methods when they preserve the same user outcome.
- Specify hard boundaries for public API, schema, auth, security, billing, data retention, production dependencies, approval boundaries, and coverage claims; leave low-risk implementation tactics to the agent.

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

Prefer mandatory anchor files and evidence surfaces over long exhaustive file lists. For implementation Goals, list the spec, core contract docs, key entrypoints, and key tests, then say to discover adjacent implementation/docs/tests as needed. Exhaustive file lists are appropriate only when those exact files are the evidence surface or required scope.

If unknown, include:

- `AGENTS.md` if present
- the provided spec/issue/request
- relevant tests and docs discovered in the project

## Evidence Surface / Verification Environment

State where the final result can be checked. This can be a running app, browser screenshot, test output, benchmark, source-backed comparison table, decision memo, spreadsheet, CRM-ready list, customer-facing draft, or other reviewable artifact.

If the evidence surface is missing or unrealistic, require the agent to create the smallest practical verification surface or stop if that requires unavailable credentials, services, devices, data, or user approval.

## Constraints

Common constraints:

- Keep changes scoped to the requested feature and directly related tests/docs.
- Do not make unrelated cleanup changes.
- Do not change public API, schema, auth behavior, billing behavior, security behavior, data retention behavior, or production dependencies unless the spec explicitly requires it.
- Prefer the smallest reversible assumption when the spec is incomplete.
- Do not satisfy metrics by deleting, weakening, bypassing, or narrowing required behavior, tests, data, sources, or review criteria unless explicitly approved.

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
- final diff review confirms no public API, schema, auth, billing, security, data retention, or unrelated dependency changes

If validation is unknown, require the agent to discover relevant validation commands from repo docs, scripts, package metadata, nearby CI config, or the evidence surface, then record what was run when notes are used.

For visual Goals, convert references into checklist or design-system criteria where possible. Do not chase pixel-perfect asset recreation unless the user explicitly requires it.

## Progress and Pivot

Start with a concise checklist for reaching Done. Track each item as not started, in progress, complete, or blocked. At meaningful checkpoints, update the checklist and report in the user's language (match the language of the request):

- progress made
- evidence confirmed
- remaining work
- next step

Do not update so often that reporting displaces execution. If a design judgment is needed, record the adopted option and reason instead of leaving ambiguity hidden. If commits are explicitly in scope, summarize implemented changes, validation, and next actions before and after committing.

Compare progress against the Done condition using evidence, not effort spent.

If two distinct approaches fail to improve the evidence surface, use read-only strategy review when available: diagnose why progress is stalled, and recommend whether to continue, narrow, change approach, improve validation, or stop.

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
- high-confidence completion includes final read-only review or completeness criticism when useful
- notes are current and reviewable when sidecars are used
- final diff is scoped to intended code/tests/docs plus any run files
- final response summarizes implementation, evidence, and user-review-needed decisions

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

Before activation, score each item 0, 1, or 2:

- One objective
- Intended outcome image formed; objective, evidence, and Done derived from it; image mirrored back for one-pass correction when the prompt was minimal
- Clarification gate passed, or unresolved questions were asked before activation
- Bounded exploration gate passed when discoverable project/data/tool/validation facts were needed
- Binary Done when
- Done is evidence-bounded, not an unbounded "perfect everything" condition
- Measurable targets used where meaningful
- Subjective criteria converted to observable evidence where measurement is not appropriate
- Evidence surface / verification environment is explicit or has a discovery rule
- Concrete validation surface or a discovery rule for validation
- Anti-gaming constraint included when metrics, tests, coverage, rankings, or visual criteria are involved
- Inline condition length checked: ordinary target <= 2,500 characters, portable target <= 3,500 characters, hard cap <= 4,000 characters
- Bloat pass completed: no repeated rationale, long examples, avoidable file lists, or optional operations that weaken the main objective
- Execution freedom preserved: the Goal states outcome, evidence, constraints, validation, pivot, Done, and block rules without unnecessary implementation sequencing
- Autonomous continuation path covers investigation, implementation, validation, and review
- Visible progress rule covers checklist status and checkpoint reporting without forcing excessive updates
- Progress/pivot path covers stalled approaches without changing the Goal itself
- Goal-amendment boundary prevents silent changes to objective, Done, evidence, constraints, approval boundaries, or final coverage claims
- Explicit constraints
- Explicit context to read first
- Subagents/context-separation policy included
- Broad claims have an explicit coverage bound or an honest discovery/omission reporting rule
- On block rules included
- High-risk changes are blocked or explicitly allowed

If sidecars are used, also check:

- Run ID is ordered and searchable
- Exactly two run files are created
- Execution notes are required
- Compact launcher objective points to `GOAL.md` and avoids restating the sidecar plan in full

If any score is 0, revise before activation. If safe revision is impossible because required decisions are missing, ask the smallest complete set of focused questions needed to make the Goal safe and correct.
