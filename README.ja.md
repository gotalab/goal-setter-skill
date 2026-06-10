# goal-setter

**長い自律実行が始まる前に、数語の指示を完成した `/goal` 条件に変換する。**

**Codex** のために作られ、**Claude Code** でも動く。1つのスキルで両ランタイム。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-concept.png" alt="ばらばらの作業が1つのgoal契約へ収束するイメージ" width="50%">
</p>

---

## なぜ必要か

goal は、完了条件が満たされるまでエージェントを働かせ続ける仕組みだ（[Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex)）。その条件をきちんと書くには手間がかかる。成果は何か、何で確認するか、何を変えてはいけないか、いつ止まるか。どれかを省くと実行は狙いからずれていく。goal は無人で走るので、出発点の粗さはそのまま何時間ぶんにも膨らむ。

goal-setter が生まれた理由は単純で、その条件を書く作業こそ、まさに人が省略する部分だからだ。完成像はすでに頭の中にある。実際に打つのは短い一行だけ。このスキルはその一行から完成像を復元し、成果を変えうる曖昧さがなくなるまで確認してから、goal の発動まで持っていく。質問はまとめて送るので、たいてい1往復で済む。

## 何をするか

- **まず完成像を復元する。** 何かを書き始める前に、作ろうとしているものとその理由を数文で再構成する。指示が最小限のときは、復元した像を見せて直してもらう。重要な質問は同じメッセージに束ねるので、往復は最小限で済む。曖昧さが残れば解消するまで確認する。成功基準・制約・Done 条件はすべてこの像から導く
- **成果を左右する質問だけ聞く。** スコープ、確認方法、安全の境界。リポジトリから分かることは探索で済ませ、リスクの低い細部は仮定として明記する
- **コンパクトな条件を書く。** goal テキストは「何を・なぜ」を固定し、「どうやるか」はエージェントに任せる。手順書にはしない
- **停止と正直さのルールを組み込む。** チェックを弱めて通すことの禁止。行き詰まったら戦略を見直し、それでもだめなら停止。目標や Done 条件の無断書き換えの禁止。進捗はツールの実行結果と照合できるものだけ報告する
- **サブエージェントの使用を明示的に許可する。** Codex は goal 本文に許可がないと実行中にサブエージェントを使わないため、必ず書き込む
- **発動前に監査する。** すべての goal を契約チェックリストと突き合わせ、欠けがあれば直してから発動する
- **日単位の作業にはサイドカー。** 永続的な記録と再開用に `GOAL.md` + `execution-notes.md` を作る

## インストール

### Codex（推奨）

Codex 内で同梱の `$skill-installer` を使う。`$CODEX_HOME/skills`
（既定では `~/.codex/skills`）に入り、通常の Codex チャットで
`$goal-setter` を使えるようにする一番単純な方法：

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

インストール後に Codex を再起動し、`$goal-setter` で呼ぶか、依頼文から自動で発動させる。

手動の場合も同じ skill フォルダを置く：

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" "${CODEX_HOME:-$HOME/.codex}/skills/goal-setter"
```

### Codex（プラグイン marketplace）

スキル単体ではなく Codex の plugin カードから入れたい場合は、この repo を
marketplace として追加し、Codex 内の `/plugins` から **Goal Setter** をインストールする：

```bash
codex plugin marketplace add gotalab/goal-setter-skill
```

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

### 任意のエージェント（skills CLI）

エージェント横断の skills CLI（Codex、Claude Code、Cursor ほか約70エージェント対応）からも、このリポジトリを直接入れられる：

```bash
npx skills add gotalab/goal-setter-skill
```

リポジトリから `skills/goal-setter/` を発見し、各エージェントのスキルディレクトリにリンクする。

## 使い方

**Draft** — 発動せずに条件をレビューする：

> APIクライアントのv2移行のgoalをドラフトして

**Activate** — 整形と発動を一気にやる：

> goalをセットして: リファクタ後にcheckoutテストが全部通ること

goal-setter は完成像を復元し、必要なことだけ聞き、条件を書いて監査し、ランタイム自身の goal 機構で発動する（下表参照）。依頼が小さすぎる、または曖昧すぎてまともな goal にならない場合は、そう言って通常のプロンプトを提案する。

## 実例

小さなリポジトリ（`src/api` 配下の3モジュールが `@acme/api-client` v1 を使用、テストと `docs/v2-migration.md` あり）でスキルを実際に走らせた出力をそのまま載せる。

入力：

> set a goal: migrate src/api to the v2 client

goal-setter はリポジトリを探索し、復元した完成像を見せる。移行ドキュメントから「v2 では retry のデフォルトが変わる」という罠を自力で拾っている点に注目：

> Here's what I understand you want: migrate everything under src/api off the deprecated @acme/api-client (v1) onto @acme/sdk (v2, already in your dependencies at ^2.3.0), following docs/v2-migration.md — `createClient(opts)` instead of `new ApiClient(opts)`, `auth: { token | tokenProvider }` instead of the `authToken` callback, `retry: { attempts }` instead of `retries`, and `SdkError` instead of `ApiError` — with no behavior change for the code that calls these modules. I plan to: keep retries at 3 by passing `retry: { attempts: 3 }` explicitly (the v2 default changed from 0 to 2); keep the exported signatures of getUser, listUsers, createOrder, and makeScopedClient stable, except makeScopedClient's return type moves to the v2 client type; and remove @acme/api-client from package.json once nothing references it. Done means no v1 references remain in src/ or tests/ and `npm test`, `npm run build`, and `npm run lint` all pass. Correct me if any of that is off — otherwise I'll set the goal.

発動されるもの（2,450字）：

```text
/goal Context: this serves the shop-backend team by getting src/api off
the deprecated @acme/api-client v1 and onto the supported @acme/sdk v2
(already in dependencies) with no behavior change for callers. Migrate
all code under src/api from @acme/api-client to @acme/sdk per
docs/v2-migration.md, leaving zero v1 references and unchanged
caller-facing behavior. Verify through npm test, npm run build, and npm
run lint passing, plus a grep showing no @acme/api-client, ApiClient, or
ApiError references left in src/ or tests/. Read docs/v2-migration.md,
src/api/client.ts, and src/api/orders.ts first; discover adjacent tests
under tests/api as needed. Keep changes scoped to the migration and do
the simplest thing that meets it. Hard boundaries: preserve current retry
behavior by passing retry: { attempts: 3 } explicitly (the v2 default
changed from 0 to 2); keep the exported signatures and behavior of
getUser, listUsers, createOrder, and makeScopedClient stable for callers,
except makeScopedClient's return type moves to the v2 client type; map
ApiError handling to SdkError without changing .status semantics. Do not
alter other externally visible contracts, and do not make checks pass by
deleting, weakening, or skipping tests. Remove @acme/api-client from
package.json once no code references remain. Use available governed
read-only subagents when materially useful for separable triage,
validation discovery, or strategy review; before claiming Done, verify
the evidence with a fresh-context check (independent subagent or
equivalent), not self-review. Maintain a concise checklist with
checkpoint updates; before reporting progress, audit each claim against a
tool result from this run - unverified work is reported as unverified,
never as done. When you have enough information to act, act; never end a
turn on a plan or a promise. Done when src/ and tests/ contain no
@acme/api-client references, the v1 dependency is removed from
package.json, and npm test, npm run build, and npm run lint all pass. If
two approaches fail to improve the evidence, review strategy and pivot
within constraints; do not silently change the objective, Done condition,
evidence, or constraints. Stop only if @acme/sdk lacks a documented
equivalent for required behavior or validation stays blocked by the same
failure after 3 distinct attempts. The final report is for a reader who
watched none of the run: outcome first, plain words, in the user's
language.
```

打ったのは一行だけ。上のファイルパス・コマンド・境界はすべて、リポジトリと移行ドキュメントの探索から導かれたものだ。

## 発動の仕組み

goal-setter はランタイム自身の goal 機構だけを使う。発動のために子セッションやサイドプロセスを起動することはない。

| ランタイム | 経路 |
|---|---|
| Codex | ネイティブの `set_goal` ツールで自分で発動する |
| Claude Code | そのまま送信できる `/goal …` の一行を渡す |

差がある理由：Claude Code（v2.1.170 時点）には、現行セッションに goal をセットするためにモデルが呼べるツールがない — `/goal` はユーザーコマンドだ。そのため Claude Code ではスキルがすべてを準備し、あなたはその一行を送るだけでいい。

## goal がカバーするもの

すべての非自明な goal は次を含む：その成果が誰の何のためかを示す1行 · 1つの目標 · 何で成功を確認するか · 最初に読むもの · このタスクが壊しうる数個の境界と、チェックを弱めて通すことの禁止 · 検証コマンド（または見つけ方） · サブエージェントの許可と Done 前の独立チェック · ツール結果と照合した進捗報告（依頼した言語で） · 約束でターンを終えず動き続けるルール · 行き詰まったときの方針転換ルール · 二値の Done 条件 · 明示的な停止条件 · 実行を見ていなかった人にも分かる最終レポート。

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
