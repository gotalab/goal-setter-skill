# goal-setter

**数語の指示を、完成した `/goal` 条件に変換する — 長い自律走行が始まる前に。**

**Codex** のために作られ、**Claude Code** でも動く。1つのスキルで両ランタイム。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-concept.png" alt="ばらばらの作業が1つのgoal契約へ収束するイメージ" width="50%">
</p>

---

## なぜ必要か

goal は、完了条件が真になるまでエージェントを働かせ続ける仕組みだ（[Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)）。その条件をきちんと書くのは本物の作業になる。成果は何か、何で確認するか、何を変えてはいけないか、いつ止まるか。どれかを省くと走行はずれていく。goal は無人で走るので、弱いスタート条件は数時間ぶん増幅される。

goal-setter が生まれた理由は単純で、その条件を書く作業こそ、まさに人が省略する部分だからだ。完成像はすでに頭の中にある。実際に打つのは短い一行だけ。このスキルはその一行から完成像を復元し、曖昧さが成果を変えうる限り確認してから、goal の発動まで運ぶ。質問はまとめて送るので、たいてい1往復で済む。

## 何をするか

- **まず完成像を復元する。** 何かを書き始める前に、作ろうとしているものとその理由を数文で再構成する。指示が最小限のときは、復元した像を見せて直してもらう。重要な質問は同じメッセージに束ねるので、往復は最小限で済む。曖昧さが残れば解消するまで確認する。成功基準・制約・Done 条件はすべてこの像から導く
- **成果を左右する質問だけ聞く。** スコープ、確認方法、安全の境界。リポジトリから分かることは探索で済ませ、リスクの低い細部は仮定として明記する
- **コンパクトな条件を書く。** goal テキストは「何を・なぜ」を固定し、「どうやるか」はエージェントに任せる。手順書にはしない
- **停止と正直さのルールを組み込む。** チェックを弱めて通すことの禁止。行き詰まったら戦略を見直し、それでもだめなら停止。目標や Done 条件の無断書き換えの禁止。進捗はツールの実行結果と照合できるものだけ報告する
- **サブエージェントの使用を明示的に許可する。** Codex は goal 本文に許可がないと走行中にサブエージェントを使わないため、必ず書き込む
- **発動前に監査する。** すべての goal を契約チェックリストと突き合わせ、欠けがあれば直してから発動する
- **日単位の作業にはサイドカー。** 永続的な記録と再開用に `GOAL.md` + `execution-notes.md` を作る

## インストール

### Codex（プラグイン）

```bash
codex plugin marketplace add gotalab/goal-setter-skill
```

その後 Codex 内で `/plugins` を開いて **Goal Setter** をインストールする（新しめの CLI なら `codex plugin add goal-setter@goal-setter` も使える）。

### Codex（スキル単体）

Codex 内で同梱インストーラを使う（public な GitHub リポなら何でも入る）：

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

手動の場合 — Codex は `~/.agents/skills/` からスキルを発見する（symlink 可。`~/.codex/skills/` も動くが非推奨パス）：

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.agents/skills/goal-setter
```

Codex を再起動し、`$goal-setter` で呼ぶか、依頼文から自動で発動させる。

### Claude Code（プラグイン）

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

インストール後は依頼文からスキルが発動する。明示的に呼ぶ場合は `/goal-setter:goal-setter`。

または手動で：

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.claude/skills/goal-setter
```

## 使い方

**Draft** — 発動せずに条件をレビューする：

> APIクライアントのv2移行のgoalをドラフトして

**Activate** — 整形と発動を一気にやる：

> goalをセットして: リファクタ後にcheckoutテストが全部通ること

goal-setter は完成像を復元し、必要なことだけ聞き、条件を起草・監査して、ランタイム自身の goal 機構で発動する（下表参照）。依頼が小さすぎる・曖昧すぎて誠実な goal にならない場合は、そう言って通常のプロンプトを提案する。

## 実例

入力：

> goalをセットして: src/api をv2クライアントに移行

goal-setter はリポジトリを探索し、復元した完成像を見せる：

> **イメージ:** `src/api` 配下の v1 `ApiClient` の使用箇所をすべて v2 SDK に置き換える。挙動は不変 — 既存の統合テストはグリーンのまま、公開インターフェースと認証は変更しない。違っていれば直してください。OKなら発動します。

発動されるもの：

```text
/goal Context: this migration unblocks v2-only work for the API team, so
behavior parity matters more than speed. Migrate src/api from the v1
ApiClient to the v2 SDK with behavior unchanged. Verify success through
the existing integration tests in tests/api and a final diff review. Read
src/api/client.ts and docs/v2-migration.md first; discover adjacent
tests/docs as needed. Keep changes scoped to src/api and directly related
tests — the simplest change that meets the objective, no refactors beyond
it; do not change public API, auth behavior, retry semantics, or other
externally visible contracts unless explicitly required. Validate with
`pnpm test tests/api` and `pnpm build`; do not satisfy them by deleting,
weakening, or skipping tests. Use available read-only subagents for
migration-doc research and validation discovery; before claiming Done,
have a fresh-context subagent verify the evidence. Maintain visible
progress with a concise checklist and checkpoint updates; audit each
progress claim against a tool result first — unverified work is reported
as unverified, never as done. When you have enough information to act,
act; never end a turn on a plan or a promise. Done when every v1
ApiClient import under src/api is gone, `pnpm test tests/api` and `pnpm
build` exit 0, and the final diff review confirms no public API or auth
changes. If two approaches fail to improve evidence, review strategy and
pivot within constraints; do not silently change the objective, Done,
evidence, or constraints. Stop only if v1/v2 behavior differences cannot
be safely inferred from docs or tests, or a required credential or
service blocks validation. Write the final report for a reader who
watched none of the run: outcome first, plain words, in the user's
language.
```

打ったのは一行だけ。残りはすべてリポジトリと復元された完成像から来ている。

なお、途中経過の報告は**依頼した言語**で行われる（日本語で頼めば日本語で報告が来る）。

## 発動の仕組み

goal-setter はランタイム自身の goal 機構だけを使う。発動のために子セッションやサイドプロセスを起動することはない。

| ランタイム | 経路 |
|---|---|
| Codex | ネイティブの `set_goal` ツールで自分で発動する |
| Claude Code | 送信するだけの正確な `/goal …` 行を手渡す |

差がある理由：Claude Code（v2.1.170 時点）には、現行セッションに goal をセットするためにモデルが呼べるツールがない — `/goal` はユーザーコマンドだ。そのため Claude Code ではスキルがすべてを準備し、発動はあなたの1打鍵になる。

## goal がカバーするもの

すべての非自明な goal は次を含む：その成果が誰の何に効くかの1行 · 1つの目標 · 何で成功を確認するか · 最初に読むもの · このタスクが壊しうる数個の境界と、チェックを弱めて通すことの禁止 · 検証コマンド（または見つけ方） · サブエージェントの許可と Done 前の独立チェック · ツール結果と照合した進捗報告（依頼した言語で） · 約束でターンを終えず動き続けるルール · 行き詰まったときの方針転換ルール · 二値の Done 条件 · 明示的な停止条件 · 走行を見ていなかった人向けの最終レポート。

完全なリファレンス：[`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## 構成

```text
skills/goal-setter/
├── SKILL.md                      # ルーティング、モード、ゲート
├── references/
│   ├── goal-contract.md          # 契約仕様＋発動前監査
│   ├── runtime-capabilities.md   # サブエージェント、ツール、サンドボックス方針
│   ├── sidecars-and-notes.md     # GOAL.md / execution-notes.md ポリシー
│   ├── GOAL.template.md
│   └── execution-notes.template.md
├── scripts/
│   ├── init_goal_run.py          # サイドカー生成ヘルパー
│   └── check_python_syntax.py
└── agents/openai.yaml            # Codex 向け表示メタデータ
```

プラグインのパッケージングはリポジトリ直下にある：Codex 用は `.codex-plugin/plugin.json` と `.agents/plugins/marketplace.json`、Claude Code 用は `.claude-plugin/`（plugin.json + marketplace.json）— どちらも同じ `skills/goal-setter/` を指す。

## ライセンス

[MIT](LICENSE)
