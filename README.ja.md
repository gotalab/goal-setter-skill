# goal-setter

**短い一行の依頼を、Codex の thread・subagent・検証まで動かせる `/goal` 契約に仕上げる。**

**Codex** 向けに作ったスキル。**Claude Code** でもそのまま使える。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter のアイコン: ばらばらの依頼がチェック済みの goal 契約へ収束するイメージ" width="180">
</p>

---

## なぜ必要か

goal を使うと、完了条件が満たされるまでエージェントが働き続ける（公式ガイド: [Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) / [Claude Code](https://code.claude.com/docs/en/goal)）。ただ、その完了条件をきちんと書くのは案外むずかしい。何ができていれば完了なのか、それを何で確認するのか、何を変えてはいけないのか、どうなったら止まるのか。Codex ではさらに、何を main thread に残し、どの読み取り作業を subagent に渡し、どの書き込み単位を `create_thread` の worktree に切るのかまで書く必要がある。どれかが抜けたまま無人で何時間も走らせると、最初の小さなずれが最後まで膨らみ続ける。並列に走るべき仕事が、静かに serial で進むこともある。

goal-setter が生まれた理由は単純で、そもそも goal の指示を書くことすらめんどくさいから。作りたいものは頭の中にあるのに、実際に打つのは短い一行だけ。goal-setter はその一行から完成像を復元し、結果を左右する曖昧さがなくなるまで確認したうえで、goal の発動まで持っていく。質問はまとめて聞くので、確認はたいてい1往復で終わる。

めんどくさがらずに書く人にも意味がある。多くの goal helper は完了条件を鋭くするところで止まる。goal-setter はもう一段進んで、その goal を実行するエージェントのためのランタイム契約にする。停止条件、「テストを弱めて通さない」といった約束、独立検証、評価者の癖 — Claude Code の判定役は会話ログしか見ない、Codex の並列は正しい書き方をしないと動かない（読み取り系は subagent、非自明な書き込み単位はプロジェクトが対応していれば `create_thread` worktree を必須指定、fan-out 前に bootstrap、ツール名は書くが引数は書かない）うえに、*あなたが送る* `/goal` の一行でしか発火しない — まで毎回手で織り込むのは大変だし、書くたびに内容がブレる。手書きの goal とこのスキルの出力を見比べたときの差分が、そのまま価値。

## 何をするか

- **まず完成像を復元する。** 何かを書き始める前に、作ろうとしているものとその理由を数文で再構成する。指示が最小限のときは、復元した完成像を見せて直してもらう。重要な質問は同じメッセージに束ねるので、往復は最小限で済む。曖昧さが残れば解消するまで確認する。成功基準・制約・Done 条件はすべてこの像から導く
- **成果を左右する質問だけ聞く。** スコープ、確認方法、安全の境界。リポジトリから分かることは探索で済ませ、リスクの低い細部は仮定として明記する
- **モデルの判断余地を奪わないコンパクトな条件を書く。** goal テキストは「何を・なぜ・何で確認するか・どこを越えてはいけないか」を固定し、「どうやるか」はエージェントに任せる。手順そのものが要件でない限り、手順書にはしない
- **停止と正直さのルールを組み込む。** チェックを弱めて通すことの禁止。行き詰まったら戦略を見直し、それでもだめなら停止。目標や Done 条件の無断書き換えの禁止。進捗はツールの実行結果と照合できるものだけ報告する
- **並列意図を Codex が実行できる指示に変える。** 分割すべき仕事なら、Codex が実際に反応する形で goal に書く。読み取り調査・レビュー・最終検証は `spawn_agent`。非自明な書き込み単位は、プロジェクトが対応していれば `create_thread` の worktree に必須 fan-out。各 child thread には1つの担当単位、担当ファイル、検証証拠、統合契約、編集前に unit-scoped goal を立てる指示まで渡す
- **分割できる作業を並列向けに構造化する。** 成果が独立して個別検証できる単位に割れるとき（複数モジュールの構築・多観点レビュー・多トピックリサーチ）、goal は分解の構造（発見ルール・単位ごとの担当範囲と検証・統合チェック）＋ランタイムに応じた起動指示を持つ。多くは段階パイプラインになる：bootstrap → 並列の調査 → 並列の実装 → 統合 → 並列の敵対的・最終検証。Claude Code は dynamic workflow で自律 fan-out。Codex では `spawn_agent` と `create_thread` を authorize するため、スキルがあなたに送ってもらう `/goal …` の一行を書く
- **発動前に監査する。** すべての goal を契約チェックリストと突き合わせ、欠けがあれば直してから発動する。文字数は同梱バリデータで各ランタイムの実際の数え方どおりに1回だけ検証する — Codex は Unicode コードポイント、Claude Code は UTF-16 コードユニットで数え、どちらも 4,000 ちょうどまで許可。通れば発動、超過なら少しずつ削るのではなく構成し直す
- **日単位の作業には軽量 notes。** 長時間自律ランでは簡潔な `execution-notes.md` を保つ — 進捗チェックポイントと途中の意思決定（何を・なぜ）を resume と監査のために。`GOAL.md` の足場は持たず、active な `/goal` が契約。

## 何が違うか

`/goal` の文章を読みやすくするスキルはいくつかある。goal-setter が狙っているのは、その先で起きる失敗：goal は明確なのに、エージェントが実行形を間違えること。

- 5 worker で分けるべき作業を main thread で一つずつ進めてしまう
- 書き込み中心の単位を、worktree ではなく軽い subagent に渡してしまう
- child thread が unit-scoped goal を持たず、親の契約から drift する
- コードを書いた本人がそのまま最終検証してしまう

goal-setter は、その判断を実行前の goal テキストに埋め込む。serial でやるか分解するかを決め、並列メカニズムを名指しし、読み取り subagent と書き込み thread を分け、child thread に自分の goal を立てさせ、main thread が証拠を統合してから Done にする。

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

goal-setter は完成像を復元し、必要なことだけ聞き、条件を書いてレディネスチェックし、ランタイム自身の goal 機構で発動する（下表参照）。依頼が小さすぎる、または曖昧すぎてまともな goal にならない場合は、そう言って通常のプロンプトを提案する。

## Before / after

ここでは形が分かるように短くしている。実際の run では、goal-setter が先にリポジトリや資料を読み、実在するファイル・チェック・制約を入れ、結果に影響しない条項は落とす。

### 小さい refactor

Before:

> refactor 後の checkout settings をきれいにする goal をセットして

After:

```text
/goal checkout settings page の挙動を変えずに、refactor で増えた
loading/error state の重複分岐を取り除く。先に settings page component、
隣接テスト、既存 settings UI pattern を読む。public props、billing
copy、Stripe/webhook behavior、pricing logic は変えない。refactor を
広げない。focused checkout settings tests と repo の type/lint check が
すべて green であることを確認し、通すためにテストを弱めたり削除したり
しない。Done 前に read-only subagent を spawn して、diff が既存挙動と
検証結果を保っていることを確認する。Done は重複分岐が消え、UI state が
維持され、すべての check が通ったときだけ。
```

### 長い実装

Before:

> invoice export を end-to-end で作る goal をセットして

After:

```text
/goal billing admin が既存 admin surface から invoice CSV export を実行
できるようにする。invoice calculation semantics は変えない。編集前に
現在の billing data path、permission、export convention を復元する。
既存 admin pattern に合う最小設計を選び、billing model、payment flow、
無関係な admin UI は書き換えない。permission、filter、empty export、
CSV escaping、operator-visible な success/failure path の focused tests を
追加する。意思決定と証拠は簡潔な execution-notes.md に残す。関連
unit/integration tests、typecheck、代表 CSV を download できる manual/smoke
path で検証する。Done は test が通り、CSV が documented columns と一致し、
read-only の独立検証で billing behavior drift がないと確認できたときだけ。
```

### `create_thread` が必要な並列実装

Before:

> game の faction が events, enemies, bosses, rewards, HUD, save-load, smoke evidence に効く goal をセットして

After:

```text
/goal 1 run の中で faction ecosystem を観測できる状態にする: pressure と
player history が faction power を変え、それが room events、enemy
mutations、bosses、rewards、HUD、persistence、browser smoke evidence に
反映される。faction simulation、event generation、enemy/boss mutation、
rewards/relics、HUD/smoke evidence を5つの個別検証できる write unit として
扱う。Codex ではこれらを main thread で serial 実装しない。まず repo が
usable HEAD を持つ established git project か確認し、そうでなければ main
thread で git + scaffold + shared interfaces を bootstrap する。その後、
write unit ごとに create_thread で別 thread を作り、それぞれ別 worktree で
走らせる。各 child thread の初期 prompt では、1つの unit、担当 files、
validation evidence、integration contract、編集前に unit-scoped goal を
立てる指示を渡す。child threads を並列で動かし、main thread が統合し、
各 unit の証拠、build、tests、browser smoke、read-only subagent の
最終検証が揃ったときだけ Done。
```

### ビジネスタスク

Before:

> 散らかった QBR メモを、経営に出せる形にする goal をセットして

After:

```text
/goal 共有されたメモと source files から、leadership-ready な QBR brief を
作る。内容は current performance、risks、decisions needed、next actions に
整理する。先に notes、source sheets/docs、前回 QBR format を読む。
confirmed facts と assumptions を分け、数字・owner・customer quote・
commitment を捏造しない。証拠がないものは unconfirmed として残す。
すべての metric と重要 claim を named source に対応づけ、前回 format と
照合し、read-only subagent で unsupported claims がないか確認する。Done は
共有可能な brief ができ、open questions が明示されているときだけ。
```

### 日常タスク

Before:

> apartment application を出せるところまで進める goal をセットして

After:

```text
/goal apartment application package を submit-ready にする。ただし、送信・
署名・支払い・private information の共有は明示承認なしに行わない。
必要書類を棚卸しし、ユーザーが持っている files/notes と照合し、足りない
message/checklist items を下書きし、提出前に見ればよい packet と remaining
blockers を作る。sensitive data は local に保ち、書類や日付を捏造しない。
Done はすべての required item が ready / missing / needs user action の
どれかに分類され、最終 checklist が submission 前にユーザーが確認すべきことを
明確に示したときだけ。
```

## 実例

小さなリポジトリ（`src/api` 配下の3モジュールが `@acme/api-client` v1 を使用、テストと `docs/v2-migration.md` あり）でスキルを実際に走らせた出力をそのまま載せる。

入力：

> set a goal: migrate src/api to the v2 client

goal-setter はリポジトリを探索し、復元した完成像を見せる。移行ドキュメントから「v2 では retry のデフォルトが変わる」という罠を自力で拾っている点に注目：

> Here's the outcome I understand you want, so the run starts aimed right: move the API layer of shop-backend (src/api/client.ts, users.ts, orders.ts) off the legacy `@acme/api-client` v1 onto the `@acme/sdk` v2 client, following docs/v2-migration.md — `createClient` instead of `new ApiClient`, `auth.tokenProvider` instead of the `authToken` callback, and `retry: { attempts: 3 }` kept explicit since v2's default changed. The exported functions (getUser, listUsers, createOrder, makeScopedClient) keep their current signatures and request behavior, so callers and the existing vitest tests are unaffected; `makeScopedClient`'s return type moves to the v2 client type. I'll assume removing the now-unused `@acme/api-client` from package.json is in scope, and success is verified by `npm test`, `npm run build`, and `npm run lint` all green with zero v1 references left in src/ and tests/. Correct anything here before I set the goal.

発動されるもの（1,343字 — スキルはこれを短く低リスクな実行と判断し、結果に影響しない運用ルール（逐次の進捗報告など）を省いた。サブエージェント許可・テストを弱めることの禁止・独立検証・停止ルールは残している）：

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
Use read-only subagents where useful, and before claiming Done spawn a
read-only subagent to verify the diff against the migration doc; do not
self-review.
Done when grep finds zero @acme/api-client references in src/ and tests/
and all three checks pass.
If a v1 behavior has no v2 equivalent, stop and ask rather than approximate.
Final report: outcome first, plain words, in English.
```

打ったのは一行だけ。上のファイルパス・コマンド・境界はすべて、リポジトリと移行ドキュメントの探索から導かれたもの。

この形は意図的なもの。冒頭の行は「その成果が誰の何のためか」という意図を述べる — ここでは任意の `Context:` ラベルを付けて「検証対象の要件ではなく背景」だと示しているが、ラベルは必須ではなく普通の散文でもよい（goal にラベル付きフィールドは要らない）。それ以降は普通の散文だが、契約の各要素は決まった文頭マーカーで始まる：`Read … first`（先に読むもの）、`Keep changes scoped`（制約）、`Validate with`（検証コマンド）、`Done when`（二値の完了条件 — Claude Code では独立した評価器がこの文を手がかりに判定する）、`… stop and ask`（唯一の正当な停止）、`Final report:`。ラベル付きフィールドではなく散文にしているのは、*keep attempts explicit **since** the v2 default changed* のような因果のつながり — `Constraints:` のリストに切り刻むと消えてしまうもの — を残すため。

## 発動の仕組み

goal-setter はランタイム自身の goal 機構だけを使う。発動のために子セッションやサイドプロセスを起動することはない。

| ランタイム | 経路 |
|---|---|
| Codex（通常） | ネイティブの goal ツール（`create_goal`）で自分で発動する |
| Codex（分解可能・並列） | `/goal …` の一行を渡す（下記参照）|
| Claude Code | そのまま送信できる `/goal …` の一行を渡す |

Claude Code（v2.1.170 時点）では `/goal` はユーザーコマンドで、モデルがセットするツールが無いため、スキルが準備してあなたが一行送る。Codex では通常はスキルが自分で goal をセットする — **ただし並列したい分解可能な作業は例外**：Codex の `create_thread`/`spawn_agent` は*あなた自身がタイプした依頼*でのみ発火し、ツールがセットした goal では発火しない。そのためスキルは `/goal …` の一行を渡し、**あなたがそれを送ること**が並列カスケードを authorize する。

## 並列で走らせる

成果が独立して個別検証できる単位に割れるとき（複数モジュールの構築・多観点レビュー・多トピックリサーチ）、goal は分解の構造（発見ルール・単位ごとの担当範囲と検証・統合チェック）を持つ。多くは**段階パイプライン**になる：(0) main thread が共有 baseline を bootstrap、(1) 範囲を明確にする並列の読み取り調査、(2) 並列の書き込み実装、(3) 統合、(4) 並列の敵対的・最終検証。並列の動き方はランタイム次第：

- **Claude Code** は goal に明示した「並列 fan-out」の指示を dynamic workflow として実現する — 単位を発見し、並列に配って（読み取り段階は subagent、書き込み段階は worktree 分離）結果を統合する。goal には構造と「並列で fan-out せよ」を書き、機構は run に委ねる（暗黙にはしない）。
- **Codex** は並列ツールが*あなた自身がタイプした依頼*でのみ発火し、スキルが裏でセットした goal では発火しない。だから分解可能な作業ではスキルが `/goal …` の一行を渡し、**あなたがそれを送る**ことでカスケード全体が authorize される。その指示には実機で分かった4つが入る：**subagent（`spawn_agent`）は読み取り系に使う** — 調査、レビュー、最終検証。**非自明な書き込み単位は、既存プロジェクトなら `create_thread` を必須の worktree fan-out として指定する** — 1単位1スレッド、各スレッドに担当ファイル・証拠・unit-scoped goal を初期プロンプトで渡す。**bootstrap が先** — 空/非 git ワークスペースでは main thread が git init＋scaffold＋interface 契約の commit を済ませてから書き込み fan-out する。そして **ツール名は書くが引数は書かない**（見えない `projectId` を書くと executor が諦めて serial に落ちる）。`create_thread` が使えない、または worktree の重さに見合わない場合は、`or` の逃げ道にせず goal 内で明示的に fallback 理由を書く。

これは構築だけでなく多観点レビューや多トピックリサーチにも効く — 同じ「分割して統合」の構造。

## goal がカバーするもの

すべての非自明な goal は次を含む：その成果が誰の何のためかを示す1行 · 1つの目標 · 何で成功を確認するか · 最初に読むもの · このタスクが壊しうる数個の境界と、チェックを弱めて通すことの禁止 · 検証コマンド（または見つけ方） · サブエージェントへの委譲方針と Done 前の独立チェック · ツール結果と照合した進捗報告（依頼した言語で） · 約束でターンを終えず動き続けるルール · 行き詰まったときの方針転換ルール · 二値の Done 条件 · 明示的な停止条件 · 実行を見ていなかった人にも分かる最終レポート。

契約は実行の規模に応じて縮む。短い低リスクのタスクには短い契約を書き、結果に影響しない条項は入れない。長い goal はモデル自身の判断の余地を奪うから。

すべて1ファイルに収まっている：[`skills/goal-setter/SKILL.md`](skills/goal-setter/SKILL.md)。

## 構成

```text
.agents/plugins/marketplace.json   # Codex marketplace。./plugins/goal-setter を指す
skills/goal-setter/
├── SKILL.md                      # スキル本体 — 自己完結の1ファイル
├── scripts/
│   └── validate_goal_length.py   # ランタイム準拠の文字数チェック（コードポイント＋UTF-16）
└── agents/openai.yaml            # Codex 向け表示メタデータ
plugins/goal-setter/
├── .codex-plugin/plugin.json      # Codex plugin manifest
└── skills/goal-setter/            # Codex plugin install 用の vendored copy
```

スキルは単一の `SKILL.md`（＋文字数ヘルパー）— reference 群も progressive disclosure も無い。

Codex marketplace は標準の `./plugins/goal-setter` レイアウトを使う。
リポジトリ直下の `skills/goal-setter/` は skill 単体インストール用に残している。
Claude Code 用の packaging は `.claude-plugin/` にある。

## ライセンス

[MIT](LICENSE)
