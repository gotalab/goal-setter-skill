# Changelog

## 0.1.0 — 2026-06-10

Initial release.

- **Skill**: image-first goal intake for long autonomous runs
  - Intended Outcome Image gate: reconstruct what/why before drafting; mirror back for one-pass correction on minimal prompts
  - Clarification and bounded exploration gates
  - Compact contract output (target ≤2,500 chars): objective, evidence surface, validation, anti-gaming constraints, subagent authorization, progress/pivot rules, binary Done, block conditions
  - Goal readiness audit (0/1/2 scoring) before activation
  - Sidecar mode (`GOAL.md` + `execution-notes.md`) for day-scale runs with durable audit/resume
  - Checkpoint reporting in the user's language
- **Runtimes**: Codex (native `set_goal` activation) and Claude Code (emits exact `/goal` line) from a single skill
- **Plugin**: Claude Code plugin packaging with `/goal-setter` command and single-plugin marketplace
