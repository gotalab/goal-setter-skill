# Changelog

## 0.2.2 — 2026-06-11

Codex plugin packaging.

- `.codex-plugin/plugin.json` (interface metadata, validated with the bundled plugin-creator validator) and `.agents/plugins/marketplace.json` (repo marketplace, `local` source at repo root) — same `skills/goal-setter/` serves Claude Code and Codex plugins from one layout
- `.gitignore` fixed so `.agents/plugins/` is committed while run artifacts stay ignored
- READMEs: Codex plugin install (`codex plugin marketplace add gotalab/goal-setter-skill` + `/plugins`) alongside the skill-only paths; marketplace add verified end-to-end against codex-cli 0.128.0

## 0.2.1 — 2026-06-11

Execution-freedom pass and verified distribution setup for the public release.

- **Flexibility**: the compact shape is documented as a shape, not a template — reword, reorder, and drop inapplicable clauses per task; numeric triggers (stalled-approach pivot) are tunable defaults; checklist status taxonomy is an example; readiness-audit items that don't apply score n/a instead of forcing padding
- **Subagent authorization hardened with its reason**: some runtimes (Codex) will not use subagents during a goal run unless the goal text grants it — the clause must never be compressed away
- **Codex install corrected against official docs**: `$skill-installer install <repo tree URL>` one-liner; manual path is `~/.agents/skills/` (symlinks supported; `~/.codex/skills/` deprecated); explicit invocation via `$goal-setter`
- **Claude Code plugin fixes**: removed `commands/goal-setter.md` (collided with the skill's `/goal-setter:goal-setter` invocation name; `commands/` is legacy — skills are the canonical form), added marketplace `description` and plugin `repository`; `claude plugin validate . --strict` passes

## 0.2.0 — 2026-06-11

Contract shape refined against the GPT-5.5 and Claude Fable 5 prompting guides. Goals get thicker success/evidence discipline and thinner procedure.

- **Context line**: every goal now opens with one line on what the outcome serves and for whom, compressed from the Intended Outcome Image ("give the reason, not only the request")
- **Evidence-audited progress**: progress claims must be audited against tool results before reporting; unverified work is reported as unverified — suppresses fabricated progress on long runs
- **Persistence rule**: act on sufficient information; never end a turn on a plan or promise — counters late-session early stopping
- **Task-instantiated constraints**: the generic 11-item denylist is replaced by 1-3 concrete boundaries per task plus one general externally-visible-contracts criterion ("decision criteria over enumerations")
- **Fresh-context verification before Done**: independent subagent (or equivalent) verifies the evidence instead of self-review; an independent verification harness's ready/blocked report can serve as Done evidence
- **Final report rule**: written for a reader who watched none of the run — outcome first, plain words, user's language
- **Research goals**: evidence budget (minimum sufficient evidence, cite, stop) and absence-vs-negation rule (unconfirmed ≠ no)
- Readiness audit, `GOAL.template.md`, and README examples updated to match

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
