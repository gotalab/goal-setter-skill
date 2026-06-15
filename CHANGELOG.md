# Changelog

## 0.6.0

- **Parallel fan-out is now tool-by-work-type and phased, on both runtimes.** Earlier versions treated `create_thread` as the single Codex parallel path; that was wrong for read-only work. The corrected model: **read-only work** (research, multi-aspect review, adversarial/final verification) fans out with **subagents** (lightweight, no worktree); **write work** (parallel implementation) uses **`create_thread`** (each unit in its own git worktree, so concurrent writes do not collide — heavyweight, reserved for genuine parallel write units). Large work is shaped as a **phased pipeline**: (1) parallel read-only research to clarify scope and open questions → (2) parallel write implementation → (3) integrate → (4) parallel adversarial/final verification. On **Claude Code** this runs as a dynamic workflow (subagents for read-only stages, worktree isolation for write stages) on the model's own judgment. On **Codex** both `spawn` and `create_thread` are gated to the user's own typed request, so for decomposable work the skill emits a `/goal …` line — naming each tool concretely and imperatively (no hedge words) — for the user to send; that one send authorizes the whole cascade. Corrected the prior "create_thread for everything" / "open a fresh read-only create_thread to verify" claims (read-only verification is a subagent) across SKILL.md, goal-contract, runtime-capabilities, GOAL.template, and README (en/ja).

## 0.5.0

- **Codex parallelism: the human sends the `/goal` line; the skill no longer auto-sets it.** The missing variable behind all the earlier flip-flopping turned out to be *who typed the directive*, not Goal-text-vs-prompt. Codex's `create_thread`/`spawn` are gated to an explicit user request: they fire when the human types `/goal <…create_thread per unit…>` (verified — this is what launched threads earlier), and are declined when goal-setter auto-sets the same goal via `create_goal` (the runtime states create_thread is "only when the user explicitly asks"). So for decomposable work on Codex, goal-setter now **emits the `/goal …` line for the user to send instead of auto-setting it** — that one human action authorizes the whole cascade: the main thread creates a thread per unit (own worktree, its own goal set by the orchestrator), uses subagents where useful, and integrates. Ordinary (non-decomposable) Codex goals still auto-set via `create_goal`. Updated SKILL.md (activation rule + Activate Mode + parallel rule), goal-contract, runtime-capabilities, and README (en/ja).

## 0.4.1

- **Forbid hedging the Codex `create_thread` directive — it was the reason parallelism still didn't fire.** A real run on 0.4.0 produced a goal that *did* contain a `create_thread` directive, but hedged: "decomposable by system only when file ownership is separable … use create_thread per independent system unit **when useful**." Codex reads "when useful" / "only when …" as an out and runs serially — the same failure as the original permissive `spawn` clause. Decomposability is now explicitly the drafter's *draft-time* judgment, not a runtime condition: once goal-setter judges the work decomposable, the goal must command the fan-out as a **flat imperative** with no "when useful" / "if appropriate" / "only when …" qualifiers. The "decompose only when …" conditions are a pre-draft checklist, not text for the goal. Enforced in SKILL.md, goal-contract, runtime-capabilities, and the readiness audit. Flexibility stays where it belongs — game/algorithm/implementation design — while the orchestration directive itself is unconditional.

## 0.4.0

- **Codex parallelism is goal-driven via `create_thread` — re-verified and corrected.** 0.3.0 concluded that Goal text cannot trigger Codex parallelism; that was tested only with a permissive `spawn`-subagent clause. Re-tested in the Codex App: an **imperative `create_thread` directive in the Goal body launches parallel threads autonomously** (no user prompt). So:
  - For decomposable work — a multi-module build, a multi-aspect review, or multi-topic research — the Goal carries the structure (discovery rule, per-unit owned surface and evidence/deliverable, integration/synthesis check) **plus** a runtime-sized launch directive.
  - **Codex default is now `create_thread`** (the analog of Claude Code's dynamic workflow): an imperative "for each unit, open a separate thread in its own worktree, set it a goal scoped to its unit, run in parallel, then integrate in the main thread, autonomously." The `spawn` subagent tool is gated by the environment to explicit user requests, so it is demoted to a user-prompt-only fallback.
  - **Claude Code** continues to fan out via a dynamic workflow on its own judgment.
  - Corrected the now-false claims (added in 0.3.0) that Goal text cannot trigger Codex parallelism — across `SKILL.md`, goal-contract, runtime-capabilities, GOAL.template, and README (en/ja).
- Added a parallel/decomposition starter example to the plugin default prompts (Codex plugin manifest and `agents/openai.yaml`).

## 0.3.0

- **Corrected the Codex parallel model from real-run verification.** Earlier versions tried to make Codex spawn parallel agents by writing the grant into the goal text (0.2.0 self-gating, 0.2.1 affirmative). Verified against the Codex App and OpenAI's docs, that does not work: a Codex goal is sequential and thread-scoped, and subagents and `create_thread` launch **only on an explicit user request in the prompt**, never from goal text. Accordingly:
  - The goal now carries decomposition **structure** only — a discovery rule for the independent units (state the rule, do not enumerate pieces unknown at draft time), an owned surface and its own Done evidence per unit, item-by-item progress, and a parent integration check over the merged result. This is runtime-agnostic and valuable even with no parallelism.
  - Parallel **execution** is a separate, runtime-specific layer: Claude Code fans out via a dynamic workflow on its own judgment; on Codex, goal-setter hands the user a short paste-line to send as their own prompt — `spawn` subagents (orchestrated workers, results collected by the main agent, no separate goals) or `create_thread` (genuinely separate threads, each with its own goal and optional worktree).
  - Removed the false claims that goal text grants or triggers Codex subagents (README, `SKILL.md`, goal-contract, runtime-capabilities, GOAL.template). The goal documents intended delegation, but on Codex the user triggers it.

## 0.2.1

- **Fix — parallel-spawn grant now actually lands in the emitted goal.** The earlier self-gating conditional ("may fan out if useful") was dropped by the bloat pass and read as optional execution advice, so goals shipped with only the read-only subagent clause and Codex never spawned parallel agents. Decomposition is now drafter-gated: when the work splits into independent, separately verifiable, share-no-state pieces, the goal carries an explicit, affirmative spawn instruction (Codex: one `create_goal` child contract per piece; Claude Code: a dynamic workflow), enforced by a readiness-audit item; non-decomposable work omits it. The read gate also widened so multi-module/multi-item/multi-target work consults the runtime guidance instead of skipping it.

## 0.2.0

Initial release.

- **Skill**: image-first goal intake for long autonomous runs
  - Intended Outcome Image gate: reconstruct what/why before drafting; mirror back for one-pass correction on minimal prompts; a one-line context note (what the outcome serves and for whom) opens every goal
  - Clarification and bounded exploration gates
  - Compact contract output (shortest that changes behavior — typically 800-1,800 chars, ceiling 2,500; governance clauses scale with run length and risk): objective, evidence surface, task-instantiated constraints (1-3 concrete boundaries, no boilerplate denylists), anti-gaming rule, validation, explicit subagent authorization with fresh-context verification before Done, evidence-audited progress reporting, persistence rule, progress/pivot rules, binary Done, block conditions, final report rule
  - Contract shape tuned for frontier models (GPT-5.5 / Claude Fable 5 prompting guides): the shape is adaptable per task, numeric triggers are tunable defaults, decision criteria over enumerations
  - Research goals: evidence budget and absence-vs-negation rules
  - Preliminary-goal pattern: when the outcome cannot be measured yet, the first goal builds the verification surface (rubric, eval + baseline, checklist, reproduction); the main goal follows it
  - Domain quantification heuristics: bugs (failing-then-passing), performance (metric/threshold/method/runs), research (decision + evidence standard), migrations (verified counts + coverage bound), operations (healthy state + rollback trigger)
  - Goal readiness audit (0/1/2 scoring, n/a allowed) before activation
  - Verification-findings disposition (blocking findings fix, the rest fix-or-record at the executor's discretion), discriminating-evidence rule (each outcome class fires; a check that could not have failed proves nothing), and final-report disclosure of decisions the goal left undefined — all framed as delegated discretion and evidence bars, not implementation constraints, from real-run feedback
  - Deterministic length validator (`scripts/validate_goal_length.py`) matching the real runtime limits — Codex counts Unicode codepoints, Claude Code counts UTF-16 code units (verified against Codex source and Claude Code 2.1.173); validate-once discipline: pass means activate, fail means restructure, never iterative trimming loops
  - Parallel decomposition (runtime-aware): goal-setter now writes goals that, on Codex, spawn separate parallel agents — each delegated agent driven by its own `create_goal` child contract; on Claude Code the same goal fans out through a dynamic workflow. Fires only when the work splits into independent, separately verifiable sub-outcomes that share no state, with owned surfaces, a parallel cap, and a parent integration gate; the grant self-gates so it stays harmless on interlocking work (refactors, single-cause bugs, serially tuned metrics)
  - Sidecar mode (`GOAL.md` + `execution-notes.md`) for day-scale runs with durable audit/resume
  - Checkpoint reporting and final report in the user's language
  - SKILL.md kept to routing, modes, and gates (88 lines); contract detail lives in gated references (progressive disclosure per skill-creator practice)
- **Runtimes**: Codex (native goal-tool activation via `create_goal`) and Claude Code (emits exact `/goal` line) from a single skill
- **Distribution**: Codex plugin marketplace metadata uses the standard `.agents/plugins/marketplace.json` -> `./plugins/goal-setter` layout, with the plugin manifest and vendored skill under `plugins/goal-setter/`; skill-only installs still use the root `skills/goal-setter/`; Claude Code plugin metadata remains in `.claude-plugin/`
- **Docs**: README hero icon added as a text-free Goal Setter app icon under `assets/`
