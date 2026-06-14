# goal-setter

**長い自律実行を任せる前に、短い一行の依頼を `/goal` の完了条件に仕上げる。**

**Codex** 向けに作ったスキル。**Claude Code** でもそのまま使える。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter のアイコン: ばらばらの依頼がチェック済みの goal 契約へ収束するイメージ" width="180">
</p>

---

## なぜ必要か

goal を使うと、完了条件が満たされるまでエージェントが働き続ける（公式ガイド: [Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) / [Claude Code](https://code.claude.com/docs/en/goal)）。ただ、その完了条件をきちんと書くのは案外むずかしい。何ができていれば完了なのか、それを何で確認するのか、何を変えてはいけないのか、どうなったら止まるのか。どれかが抜けたまま無人で何時間も走らせると、最初の小さなずれが最後まで膨らみ続ける。

goal-setter が生まれた理由は単純で、そもそも goal の指示を書くことすらめんどくさいから。作りたいものは頭の中にあるのに、実際に打つのは短い一行だけ。goal-setter はその一行から完成像を復元し、結果を左右する曖昧さがなくなるまで確認したうえで、goal の発動まで持っていく。質問はまとめて聞くので、確認はたいてい1往復で終わる。

めんどくさがらずに書く人にも意味がある。停止条件や「テストを弱めて通さない」といった約束、評価者の癖 — Claude Code の判定役は会話ログしか見ない、Codex の並列は明示しないと動かない（goal 本文の命令形 `create_thread`、または `spawn` subagent はプロンプトから） — まで毎回手で織り込むのは大変だし、書くたびに内容がブレる。手書きの goal とこのスキルの出力を見比べたときの差分が、そのまま価値。

## 何をするか

- **まず完成像を復元する。** 何かを書き始める前に、作ろうとしているものとその理由を数文で再構成する。指示が最小限のときは、復元した完成像を見せて直してもらう。重要な質問は同じメッセージに束ねるので、往復は最小限で済む。曖昧さが残れば解消するまで確認する。成功基準・制約・Done 条件はすべてこの像から導く
- **成果を左右する質問だけ聞く。** スコープ、確認方法、安全の境界。リポジトリから分かることは探索で済ませ、リスクの低い細部は仮定として明記する
- **コンパクトな条件を書く。** goal テキストは「何を・なぜ」を固定し、「どうやるか」はエージェントに任せる。手順書にはしない
- **停止と正直さのルールを組み込む。** チェックを弱めて通すことの禁止。行き詰まったら戦略を見直し、それでもだめなら停止。目標や Done 条件の無断書き換えの禁止。進捗はツールの実行結果と照合できるものだけ報告する
- **委譲と独立検証を明記する。** goal は委譲してよい範囲と、Done 前の独立チェック（別コンテキストの検証）を明記する。Claude Code はモデルが自律的に fan-out。Codex では `spawn` subagent はユーザーの明示プロンプト待ち、`create_thread` の並列は goal 本文に書き込む
- **分割できる作業を並列向けに構造化する。** 成果が独立して個別検証できる単位に割れるとき（複数モジュールの構築・多観点レビュー・多トピックリサーチ）、goal は分解の構造（発見ルール・単位ごとの担当範囲と検証・統合チェック）＋ランタイムに応じた起動指示を持つ。Claude Code は dynamic workflow で自律 fan-out、Codex は goal 本文に命令形の `create_thread` オーケストレーション（単位ごとに別スレッド・各自 worktree・各自 goal）を書き、自律で並列実行する
- **発動前に監査する。** すべての goal を契約チェックリストと突き合わせ、欠けがあれば直してから発動する。文字数は同梱バリデータで各ランタイムの実際の数え方どおりに1回だけ検証する — Codex は Unicode コードポイント、Claude Code は UTF-16 コードユニットで数え、どちらも 4,000 ちょうどまで許可。通れば発動、超過なら少しずつ削るのではなく構成し直す
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

> Here's the outcome I understand you want, so the run starts aimed right: move the API layer of shop-backend (src/api/client.ts, users.ts, orders.ts) off the legacy `@acme/api-client` v1 onto the `@acme/sdk` v2 client, following docs/v2-migration.md — `createClient` instead of `new ApiClient`, `auth.tokenProvider` instead of the `authToken` callback, and `retry: { attempts: 3 }` kept explicit since v2's default changed. The exported functions (getUser, listUsers, createOrder, makeScopedClient) keep their current signatures and request behavior, so callers and the existing vitest tests are unaffected; `makeScopedClient`'s return type moves to the v2 client type. I'll assume removing the now-unused `@acme/api-client` from package.json is in scope, and success is verified by `npm test`, `npm run build`, and `npm run lint` all green with zero v1 references left in src/ and tests/. Correct anything here before I set the goal.

発動されるもの（1,352字 — スキルはこれを短く低リスクな実行と判断し、結果に影響しない運用ルール（逐次の進捗報告など）を省いた。サブエージェント許可・テストを弱めることの禁止・独立検証・停止ルールは残している）：

```text
/goal Context: this keeps shop-backend on the supported @acme/sdk v2 client
so the API layer stays current and maintainable.
Migrate src/api (client.ts, users.ts, orders.ts) from @acme/api-client v1
to @acme/sdk v2 per docs/v2-migration.md: createClient replaces new
ApiClient, the authToken callback becomes auth.tokenProvider, and
retries: 3 becomes retry: { attempts: 3 } — keep attempts explicit since
the v2 default changed. Update the exported makeScopedClient return type
to the v2 client type, switch any ApiError handling to SdkError, and
remove @acme/api-client from package.json once unused.
Read docs/v2-migration.md first.
Keep changes scoped to the migration: the functions exported from src/api
keep their current signatures and request behavior (paths, query shapes,
retry count); no refactors or features beyond it.
Validate with npm test, npm run build, and npm run lint, all green; do
not weaken, skip, or delete tests to make them pass.
Use read-only subagents where useful, and before claiming Done have a
fresh-context check (independent subagent or equivalent) confirm the diff
against the migration doc.
Done when grep finds zero @acme/api-client references in src/ and tests/
and all three checks pass.
If a v1 behavior has no v2 equivalent, stop and ask rather than approximate.
Final report: outcome first, plain words, in English.
```

打ったのは一行だけ。上のファイルパス・コマンド・境界はすべて、リポジトリと移行ドキュメントの探索から導かれたもの。

この形は意図的なもの。ラベルは `Context:` の1つだけ — 冒頭の行が「検証対象の要件ではなく背景」であることを示す境界線になる。それ以降は普通の散文だが、契約の各要素は決まった文頭マーカーで始まる：`Read … first`（先に読むもの）、`Keep changes scoped`（制約）、`Validate with`（検証コマンド）、`Done when`（二値の完了条件 — Claude Code では独立した評価器がこの文を手がかりに判定する）、`… stop and ask`（唯一の正当な停止）、`Final report:`。ラベル付きフィールドではなく散文にしているのは、*keep attempts explicit **since** the v2 default changed* のような因果のつながり — `Constraints:` のリストに切り刻むと消えてしまうもの — を残すため。

## 発動の仕組み

goal-setter はランタイム自身の goal 機構だけを使う。発動のために子セッションやサイドプロセスを起動することはない。

| ランタイム | 経路 |
|---|---|
| Codex | ネイティブの goal ツール（`create_goal`）で自分で発動する |
| Claude Code | そのまま送信できる `/goal …` の一行を渡す |

差がある理由：Claude Code（v2.1.170 時点）には、現行セッションに goal をセットするためにモデルが呼べるツールがない — `/goal` はユーザーコマンド。そのため Claude Code ではスキルがすべてを準備し、あなたはその一行を送るだけでいい。

## 並列で走らせる

成果が独立して個別検証できる単位に割れるとき（複数モジュールの構築・多観点レビュー・多トピックリサーチ）、goal は分解の構造（発見ルール・単位ごとの担当範囲と検証・統合チェック）を持つ。並列の動き方はランタイム次第：

- **Claude Code** はモデルが自律的に fan-out する — 通常は dynamic workflow が単位を発見し、並列に配って結果を統合する。追加の指示は不要。
- **Codex** は `create_thread` が既定で、**goal 自身が駆動する**：分解可能な作業では goal に命令形の指示（単位ごとに別スレッドを開き、各自 worktree・各自 goal、並列実行、最後に main で統合、自律で）が入る。これは goal から直接発火し、追加プロンプトは不要。軽量な `spawn` subagent は明示依頼ゲートなので、そちらを使うなら `ユニットごとに1エージェント spawn して並列で進めて` をプロンプトで送る。

これは構築だけでなく多観点レビューや多トピックリサーチにも効く — 同じ「分割して統合」の構造。

## goal がカバーするもの

すべての非自明な goal は次を含む：その成果が誰の何のためかを示す1行 · 1つの目標 · 何で成功を確認するか · 最初に読むもの · このタスクが壊しうる数個の境界と、チェックを弱めて通すことの禁止 · 検証コマンド（または見つけ方） · サブエージェントへの委譲方針と Done 前の独立チェック · ツール結果と照合した進捗報告（依頼した言語で） · 約束でターンを終えず動き続けるルール · 行き詰まったときの方針転換ルール · 二値の Done 条件 · 明示的な停止条件 · 実行を見ていなかった人にも分かる最終レポート。

契約は実行の規模に応じて縮む。短い低リスクのタスクには短い契約を書き、結果に影響しない条項は入れない。長い goal はモデル自身の判断の余地を奪うから。

完全なリファレンス：[`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## 構成

```text
.agents/plugins/marketplace.json   # Codex marketplace。./plugins/goal-setter を指す
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
│   ├── validate_goal_length.py   # ランタイム準拠の文字数チェック（コードポイント＋UTF-16）
│   └── check_python_syntax.py
└── agents/openai.yaml            # Codex 向け表示メタデータ
plugins/goal-setter/
├── .codex-plugin/plugin.json      # Codex plugin manifest
└── skills/goal-setter/            # Codex plugin install 用の vendored copy
```

Codex marketplace は標準の `./plugins/goal-setter` レイアウトを使う。
リポジトリ直下の `skills/goal-setter/` は skill 単体インストール用に残している。
Claude Code 用の packaging は `.claude-plugin/` にある。

## ライセンス

[MIT](LICENSE)
