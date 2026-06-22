# goal-setter

**Turn a rough request into a Codex `/goal` that says what success means and how to run it.**

goal-setter is a Codex skill that turns rough work into compact goals for long
agent runs: expected result, Done criteria, verification, constraints, stop
rules, and when to use subagents, `create_thread`, and worktrees.

Built for **Codex**. Works on **Claude Code** too.

[日本語](README.ja.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter icon: loose requests converging into a checked goal" width="180">
</p>

## Why

Large agent tasks rarely fail because the first prompt was not eloquent enough.
They fail because the run loses track of what counts as Done, what must not
change, what evidence matters, or when it should stop instead of trying another
guess.

A good goal is not a step-by-step recipe. It fixes the outcome and the
boundaries, then leaves implementation judgment to the model. That has become
more important as stronger models can infer design, file boundaries, and
debugging paths from the repo itself.

goal-setter also handles the part that is easy to forget in Codex: execution
shape. Read-only review and investigation should often be subagents; non-trivial
write units may need separate `create_thread` worktrees; each child thread needs
its own unit-scoped goal; the main thread should integrate evidence before Done.

## What It Writes

A generated goal usually includes:

- the intended outcome and why it matters
- pass/fail Done criteria
- validation commands or evidence to check
- a compression pass around outcome, verification surface, constraints,
  boundaries, iteration policy, and blocked stop condition
- concrete checks where possible: counts, named files, screens, cases, timings, error messages, or before/after states
- separate checks for each named item, without treating demos or substitutes as Done
- the path from the user's request to the expected result, with pass/fail checks for software or output a user will directly use
- updates to an existing canonical artifact when one already exists, instead of
  duplicating spreadsheets, reports, docs, dashboards, or tracking files
- what must be understood before execution
- a question-and-hypothesis loop for uncertain research: central question, competing hypotheses, rejection criteria, evidence updates, and review that tries to disprove weak conclusions
- the first files or sources to read, without over-enumerating paths
- constraints, including a rule that checks must not pass by weakening tests
- compatibility and quality rules that preserve only real boundaries while
  favoring readable, changeable, low-complexity results
- stop conditions for blocked, unsafe, or looping runs
- independent verification before Done, including adversarial checks for high-risk
  claims when there is a concrete result to attack
- parallelization rules for subagents, `create_thread`, worktrees, and child goals
- parent-chosen subagent waves for read-only investigation, multi-aspect review,
  adversarial review, debugging, and verification instead of fixed counts

The goal stays short by default. Hard imperatives are reserved for real
invariants; implementation order, internal design, and exact file boundaries stay
open unless they are part of the requirement.

## What Is Different

Most prompt helpers make a clearer instruction. goal-setter tries to make the
run choose the right Codex execution structure.

- It reconstructs the intended outcome before drafting.
- It asks only for ambiguity that changes the outcome, evidence, scope, or risk.
- It separates read-only subagent work from write-thread work.
- It leaves subagent count and waves to the parent agent, based on independence, risk, cost, and how much evidence it can integrate.
- It names `spawn_agent` for read-only multi-aspect and adversarial review, but
  leaves ordinary command parallelism to the executor.
- It only emits full `create_thread` write fan-out when there are multiple
  non-trivial, independently verifiable write units.
- It tells child threads to set their own unit-scoped goals before editing.
- It uses behavioral coupling, shared state, and integration risk before file
  layout when deciding whether work can split.

## Install

Pick one install path:

| If you use | Install | Invoke with |
| --- | --- | --- |
| Codex App `/plugins` | Codex App Plugin | `$goal-setter:goal-setter ...` |
| Codex local skills | Codex Skill | `$goal-setter ...` |
| Claude Code | Claude Code marketplace | `/goal-setter:goal-setter ...` |
| Another agent with Skills CLI support | Skills CLI | the agent's skill invocation syntax |

Most Codex App users should use **Codex App Plugin**. You do not need to install
both the Codex Skill and the Codex App Plugin.

### Codex Skill

In Codex chat:

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Restart Codex, then invoke with `$goal-setter` or let it trigger from the
request.

Manual install:

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" "${CODEX_HOME:-$HOME/.codex}/skills/goal-setter"
```

### Codex App Plugin

In Codex, open `/plugins`, choose **Add plugin marketplace**, and enter:

```text
Source: gotalab/goal-setter-skill
Git ref: main
Sparse paths: plugins/goal-setter
```

Then install **Goal Setter** from the Plugins screen.

Invoke with `$goal-setter:goal-setter`, or select **Goal Setter** from the skill
picker.

### Claude Code

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

This GitHub shorthand tracks the repository default branch. To pin a branch or
tag, append `@ref` to the marketplace source.

Invoke with `/goal-setter:goal-setter`, or let the skill trigger from the
request.

### Any Agent With the Skills CLI

```bash
npx skills add gotalab/goal-setter-skill
```

## Usage

Draft a goal without activating it:

```text
$goal-setter draft a goal for migrating our API client to v2
```

Shape and activate when the runtime can set the goal directly:

```text
$goal-setter set a goal: all checkout tests pass after the refactor
```

For decomposable Codex work, goal-setter gives you an exact `/goal ...` line to
send yourself. That user-sent line is what authorizes Codex parallelism such as
`spawn_agent` and `create_thread`.

## Example

Input:

```text
set a goal: make the game factions affect events, enemies, bosses, rewards,
HUD, save-load, and smoke evidence
```

Output shape:

```text
/goal Make the faction ecosystem observable in one run: pressure and player
history change faction power, which changes room events, enemy mutations,
bosses, rewards, HUD, persistence, and browser smoke evidence.

Treat faction simulation, event generation, enemy/boss mutation, rewards/relics,
and HUD/smoke evidence as separately verifiable write units. In Codex, do not
implement those units serially in the main thread. Create one separate
create_thread worktree per write unit when the repo supports it; each child
thread gets one owned area, evidence requirements, an integration rule,
and a unit-scoped goal before editing. The main thread integrates and gates Done
on each unit's evidence, build/tests/smoke, and final verification by a read-only
subagent (`spawn_agent`).
```

More examples: [docs/EXAMPLES.md](docs/EXAMPLES.md)

## Runtime Notes

- Codex ordinary goals can be set through the native goal tool.
- Codex parallel goals are handed back as a user-sent `/goal ...` line because
  Codex parallel tools fire from explicit user requests.
- Claude Code receives the exact `/goal ...` line and can realize the same
  decomposition as a dynamic workflow.

Details: [docs/RUNTIME.md](docs/RUNTIME.md)

## Repository

```text
skills/goal-setter/SKILL.md          # the skill
skills/goal-setter/scripts/          # goal length validator
plugins/goal-setter/                 # Codex plugin bundle
.claude-plugin/                      # Claude Code plugin metadata
```

## License

[MIT](LICENSE)
