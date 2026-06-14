# Changelog

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
