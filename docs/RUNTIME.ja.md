# Runtime Behavior

goal-setter は goal text を書くスキルです。新しい scheduler を実装しているわけではなく、各 runtime に既にある goal / 並列化の仕組みを使います。

## Activation

| Runtime | 動き |
| --- | --- |
| Codex、通常タスク | native goal tool で goal を set できる |
| Codex、分解可能な並列タスク | ユーザーが送る `/goal ...` 行を返す |
| Claude Code | ユーザーが送る `/goal ...` 行を返す |

Codex の並列ケースだけは特別です。`spawn_agent` と `create_thread` は明示的なユーザー依頼から発火するため、分解可能な作業では、goal-setter が `/goal ...` の一行を渡し、ユーザーがそれを送ることで並列カスケードを authorize します。

## 並列作業

成果が独立して個別検証できる単位に割れる場合、goal には次を入れます。

- 単位を発見するルール
- 単位ごとの担当範囲と証拠
- item-by-item の進捗
- 親 thread の統合チェック
- Done 前の独立検証

分割可否は、ファイル配置より先に、挙動の結合度、共有状態、統合リスクで判断します。ファイルパスは repo を読んだ後の手がかりであって、最初の境界ではありません。ユーザーが数を指定していない限り、subagent 数は固定しません。親 agent が独立性、リスク、コスト、統合できる証拠量を見て数と波を決め、各波を統合してから追加するか判断します。

## Codex

既存の Codex project で git HEAD が使える場合、非自明な write unit は `create_thread` worktree fan-out を必須にします。

- write unit ごとに1つの thread
- child thread ごとに1つの担当範囲
- 単位ごとの証拠と統合ルール
- 編集前の unit-scoped goal
- すべての証拠が揃った後の main thread 統合

`spawn_agent` は読み取り系に使います。調査、レビュー、最終検証、ログ解析、既存挙動の把握など、main thread の context を汚しやすい作業に向いています。subagent は証拠、反証、不確実性、抜け、読み取り結果を返し、親 agent が統合、書き込み判断、最終判断を持ちます。

`create_thread` が使えない、workspace が worktree に向いていない、または単位が小さすぎる場合は、goal 内で fallback 理由を明示します。`or` で曖昧に逃がすと、Codex が serial に進める可能性があります。

## Claude Code

Claude Code では、同じ分解構造を dynamic workflow として実行できます。goal は構造と「並列で fan-out せよ」という意図を書きますが、機構の細部は run に委ねます。読み取り段階は subagent、書き込み段階は worktree isolation になることがあります。

## Goal がカバーするもの

非自明な作業では、goal-setter は次を考慮します。

- 目的と、その成果がなぜ必要か
- objective と Done 条件
- 証跡と検証方法
- read-first anchors
- hard boundaries と、必要なチェックを弱めないルール
- 長い run の進捗ルール
- stop conditions
- independent verification
- final report
- 不確実な調査では、棄却条件と停止条件を含む問いと仮説のループ

短いタスクには短い goal を書きます。結果に影響しない条項は入れません。
