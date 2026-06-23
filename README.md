# goal-setter

**Turn rough long-running work into a compact Codex `/goal` with a clear finish line.**

goal-setter is a Codex skill for work that needs more than a one-off prompt. It
turns a rough request into a short goal that fixes the result, the evidence for
success, the boundaries, and the stop rules, while leaving implementation
judgment to the runner.

It favors verification targets over rule-heavy procedures: the goal should say
what must be proven, not prescribe every step.

Built for **Codex**. Works on **Claude Code** too.

[日本語](README.ja.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter icon: loose requests converging into a checked goal" width="180">
</p>

## When to Use It

Do not turn every request into a Goal. Use goal-setter when the work can keep
going across several checks and the finish line must be judged by evidence.

| Work | Better format |
| --- | --- |
| One clear edit, explanation, or review | Normal prompt |
| Narrow work that may need a few tries | One sentence or short paragraph Goal |
| Migration, performance work, broad bug fixing, or evidence-backed research | Standard Goal |
| Long research or high-risk change | Goal plus the smallest needed plan, checklist, or evaluation file |

## What It Does

- Reconstructs the intended result before drafting.
- Adds only clauses that change the result, evidence, boundary, risk, or stop
  decision.
- Asks one material question at a time only when the answer would change the
  goal.
- Keeps small work light; for long work, keeps an evidence-based open-items
  loop and adds read-only review or separate write threads only when useful.

Details live in [docs/RUNTIME.md](docs/RUNTIME.md). Examples live in
[docs/EXAMPLES.md](docs/EXAMPLES.md).

## Install

Pick one install path:

| If you use | Install | Invoke with |
| --- | --- | --- |
| Codex App `/plugins` | Codex App Plugin | `$goal-setter:goal-setter ...` |
| Codex local skills | Codex Skill | `$goal-setter ...` |
| Claude Code | Claude Code marketplace | `/goal-setter:goal-setter ...` |
| Another agent with Skills CLI support | Skills CLI | the agent's skill invocation syntax |

Most Codex App users should install only the **Codex App Plugin**.

### Codex App Plugin

In Codex, open `/plugins`, choose **Add plugin marketplace**, and enter:

```text
Source: gotalab/goal-setter-skill
Git ref: main
Sparse paths: plugins/goal-setter
```

Then install **Goal Setter** from the Plugins screen.

### Codex Skill

In Codex chat:

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Restart Codex, then invoke with `$goal-setter`.

### Claude Code

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

Invoke with `/goal-setter:goal-setter`.

### Skills CLI

```bash
npx skills add gotalab/goal-setter-skill
```

## Usage

Draft a goal without activating it:

```text
$goal-setter draft a goal for migrating our API client to v2
```

Shape and activate a goal when Codex does not need extra worker tools:

```text
$goal-setter set a goal: all checkout tests pass after the refactor
```

When the goal must launch Codex worker tools such as `spawn_agent` or
`create_thread`, goal-setter returns an exact `/goal ...` line for you to send.
That user-sent line is what authorizes those tools.

## Docs

- [Examples](docs/EXAMPLES.md)
- [Runtime behavior](docs/RUNTIME.md)
- [Changelog](CHANGELOG.md)

## Repository

```text
skills/goal-setter/SKILL.md          # the skill
skills/goal-setter/scripts/          # goal length validator
scripts/                             # packaging and release checks
plugins/goal-setter/                 # Codex plugin bundle
.claude-plugin/                      # Claude Code plugin metadata
```

## License

[MIT](LICENSE)
