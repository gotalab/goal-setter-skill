# Changelog

## 0.1.0 — Unreleased

Initial release.

- **Skill**: image-first goal intake for long autonomous runs
  - Intended Outcome Image gate: reconstruct what/why before drafting; mirror back for one-pass correction on minimal prompts; a one-line context note (what the outcome serves and for whom) opens every goal
  - Clarification and bounded exploration gates
  - Compact contract output (target ≤2,500 chars): objective, evidence surface, task-instantiated constraints (1-3 concrete boundaries, no boilerplate denylists), anti-gaming rule, validation, explicit subagent authorization with fresh-context verification before Done, evidence-audited progress reporting, persistence rule, progress/pivot rules, binary Done, block conditions, final report rule
  - Contract shape tuned for frontier models (GPT-5.5 / Claude Fable 5 prompting guides): the shape is adaptable per task, numeric triggers are tunable defaults, decision criteria over enumerations
  - Research goals: evidence budget and absence-vs-negation rules
  - Goal readiness audit (0/1/2 scoring, n/a allowed) before activation
  - Sidecar mode (`GOAL.md` + `execution-notes.md`) for day-scale runs with durable audit/resume
  - Checkpoint reporting and final report in the user's language
- **Runtimes**: Codex (native goal-tool activation via `create_goal`) and Claude Code (emits exact `/goal` line) from a single skill
- **Distribution**: Codex plugin marketplace metadata uses the standard `.agents/plugins/marketplace.json` -> `./plugins/goal-setter` layout, with the plugin manifest and vendored skill under `plugins/goal-setter/`; skill-only installs still use the root `skills/goal-setter/`; Claude Code plugin metadata remains in `.claude-plugin/`
- **Docs**: README hero image added as a text-free abstract concept visual under `assets/`
