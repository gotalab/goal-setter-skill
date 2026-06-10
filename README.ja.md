# goal-setter

**雑なお願いを、証拠で裏づけられた `/goal` 完了契約に変換する — 長い自律走行が始まる前に。**

**Claude Code** と **Codex** の両対応。1つのスキルで両ランタイム。

[English](README.md)

---

## なぜ必要か

`/goal` はコーディングエージェントを長距離ランナーに変えます。完了条件が満たされるまで、必要なら何時間でも走り続ける。それは同時にリスクでもあります。goal は無人で走るため、**雑なスタート条件は走行全体に増幅される**。曖昧な目標、証拠面の欠如、停止ルールなし — 戻ってきたら「自信満々に間違った数時間分の仕事」が待っている。

`/goal` の後に打つプロンプトが仕事の大半を決めます。そして自分で書くプロンプトには、たいてい必要なものが足りていない。

goal-setter はその欠けている「受付工程」です。最小限の雑な依頼を**完了契約**に変換します：1つの目標、証拠面、検証ルール、メトリクス偽装の禁止、ピボットルール、二値の Done 条件、明示的な停止条件。**イメージできないものは作れない** — だからまず完成像を解像し、そこからすべてを導出します。

## 何をするか

- **Intended Outcome Image（意図イメージ）** — 何かを書き始める*前に*、あなたが本当に作ろうとしているものと、その理由を 2〜4 文で復元。評価基準はイメージから、制約は基準から、Done はその両方から導出。プロンプトが最小限のときは、質問攻めにする代わりにイメージを鏡で返して 1 往復で修正
- **確認ゲート＆探索ゲート** — 成果を左右する質問（スコープ・証拠・安全境界）だけを聞き、リポジトリから発見できるものは探索し、残りは安全な仮定としてエンコード
- **コンパクトな契約形式の出力** — *何を・なぜ*を固定し、*どうやるか*はエージェントに開放する文脈最小主義の goal テキスト（目標 2,500 字以内）。実行の自由を奪う手順書にはしない
- **メトリクス偽装＆ループ防止** — テストを弱めて指標を満たすことの禁止、2 回の失敗で戦略レビュー、3 回でハードストップ、ゴールポストの無断移動を防ぐ Goal 修正境界
- **サブエージェントの明示認可** — 非自明な goal には、調査・検証発見・トリアージ・最終レビューのための委譲権限を明示的に付与。暗黙の自律性には頼らない
- **レディネス監査** — すべての goal を発動前に 0/1/2 のチェックリストで採点。0 があれば発動前に修正
- **サイドカーモード** — 日単位の作業向け：`GOAL.md` + `execution-notes.md` で永続的な監査・再開・レビュー可能な意思決定ログ

## インストール

### Claude Code（プラグイン）

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

または手動で：

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.claude/skills/goal-setter
```

### Codex

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" ~/.codex/skills/goal-setter
```

## 使い方

**Draft** — 発動せずに契約をレビュー：

> APIクライアントのv2移行のgoalをドラフトして

**Activate** — 整形と発動を一気に：

> goalをセットして: リファクタ後にcheckoutテストが全部通ること

goal-setter は成果イメージを形成し、ゲートを通し、コンパクトな条件を起草・監査して、ランタイムが提供する経路で発動します（下表参照）。依頼が小さすぎる・曖昧すぎて誠実な goal にならない場合は、そう言って通常のプロンプトを提案します。

## 実例

入力：

> goalをセットして: src/api をv2クライアントに移行

goal-setter がまずやること — リポジトリを探索し、成果イメージを鏡で返す：

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
externally visible contracts unless explicitly required. Validate with `pnpm test tests/api` and `pnpm build`;
do not satisfy them by deleting, weakening, or skipping tests. Use
available read-only subagents for migration-doc research and validation
discovery; before claiming Done, have a fresh-context subagent verify the
evidence. Maintain visible progress with a concise checklist and
checkpoint updates; audit each progress claim against a tool result first
— unverified work is reported as unverified, never as done. When you have
enough information to act, act; never end a turn on a plan or a promise.
Done when every v1 ApiClient import under src/api is gone, `pnpm test
tests/api` and `pnpm build` exit 0, and the final diff review confirms no
public API or auth changes. If two approaches fail to improve evidence,
review strategy and pivot within constraints; do not silently change the
objective, Done, evidence, or constraints. Stop only if v1/v2 behavior
differences cannot be safely inferred from docs or tests, or a required
credential or service blocks validation. Write the final report for a
reader who watched none of the run: outcome first, plain words, in the
user's language.
```

私たちが普段 `/goal` の後に打っている文章と比べてみてください — その差分がこのスキルの価値です。

なお、チェックポイント報告は**あなたの言語**で行われます（日本語で依頼すれば日本語で報告）。

## 発動の仕組み

goal-setter はランタイムの**ネイティブ** goal 機構のみを使います。発動のために子セッションやサイドプロセスを起動することはありません。

| ランタイム | 経路 | 状態 |
|---|---|---|
| Codex | ネイティブ `set_goal` ツール — 完全自律発動 | ✅ |
| Claude Code | 送信するだけの正確な `/goal …` 行を出力 | ✅ |

この表の理由：Claude Code v2.1.170 時点で、**現行セッションに goal をセットするモデル呼び出し可能なツールは存在しません** — `/goal` はセッションスコープの Stop hook をラップするユーザーコマンドです。そのため Claude Code では、goal-setter が契約を準備して正確な 1 行を手渡し、発動は意図的でネイティブな 1 打鍵として残ります。

## 契約がカバーするもの

すべての非自明な goal は次を含みます：1行のコンテキスト（その成果が誰の何に効くか） · 1つの目標 · 証拠面 · 最初に読むコンテキスト · タスク固有の制約＋メトリクス偽装の禁止 · 検証（またはその発見ルール） · サブエージェントポリシー＋Done前の新鮮コンテキスト検証 · ツール結果と照合された進捗報告（あなたの言語で） · 継続ルール（十分な情報があれば動く。約束でターンを終えない） · 進捗/ピボットルール · 二値の Done · 明示的なブロック条件 · 最終レポートのルール（結論を先に、平易な言葉で、あなたの言語で）。

完全なリファレンス：[`skills/goal-setter/references/goal-contract.md`](skills/goal-setter/references/goal-contract.md)

## 構成

```text
skills/goal-setter/
├── SKILL.md                      # ルーティング、モード、ゲート
├── references/
│   ├── goal-contract.md          # 契約仕様＋レディネス監査
│   ├── runtime-capabilities.md   # サブエージェント、ツール、サンドボックス方針
│   ├── sidecars-and-notes.md     # GOAL.md / execution-notes.md ポリシー
│   ├── GOAL.template.md
│   └── execution-notes.template.md
├── scripts/
│   ├── init_goal_run.py          # サイドカー生成ヘルパー
│   └── check_python_syntax.py
└── agents/openai.yaml            # Codex 向けメタデータ
```

## ライセンス

[MIT](LICENSE)
