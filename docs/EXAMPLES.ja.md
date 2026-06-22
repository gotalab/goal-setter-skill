# Examples

goal-setter の出力例です。実際の run では、先に repo や資料を読み、実在するファイル、検証コマンド、制約を入れ、結果に影響しない条項は落とします。

## 小さい Refactor

Before:

```text
refactor 後の checkout settings をきれいにする goal をセットして
```

After:

```text
/goal checkout settings page の挙動を変えずに、refactor で増えた
loading/error state の重複分岐を取り除く。先に settings page component、
隣接テスト、既存 settings UI pattern を読む。public props、billing copy、
Stripe/webhook behavior、pricing logic は変えない。refactor を広げない。
focused checkout settings tests と repo の type/lint check がすべて green
であることを確認し、通すためにテストを弱めたり削除したりしない。Done は重複分岐が
消え、UI state が維持され、すべての check が通ったときだけ。
```

## 長い実装

Before:

```text
invoice export を end-to-end で作る goal をセットして
```

After:

```text
/goal billing admin が既存 admin surface から invoice CSV export を実行
できるようにする。invoice calculation semantics は変えない。編集前に現在の
billing data path、permission、export convention を復元する。既存 admin
pattern に合う最小設計を選び、billing model、payment flow、無関係な admin UI
は書き換えない。permission、filter、empty export、CSV escaping、
operator-visible な success/failure path の focused tests を追加する。
意思決定と証拠は簡潔な execution-notes.md に残す。関連 tests、typecheck、
代表 CSV を download できる manual/smoke path で検証する。Done は test が
通り、CSV が documented columns と一致し、read-only subagent (`spawn_agent`) が
billing behavior drift なしと確認したときだけ。
```

## `create_thread` が必要な並列実装

Before:

```text
game の faction が events, enemies, bosses, rewards, HUD, save-load,
smoke evidence に効く goal をセットして
```

After:

```text
/goal 1 run の中で faction ecosystem を観測できる状態にする: pressure と
player history が faction power を変え、それが room events、enemy mutations、
bosses、rewards、HUD、persistence、browser smoke evidence に反映される。
faction simulation、event generation、enemy/boss mutation、rewards/relics、
HUD/smoke evidence を個別検証できる write unit として扱う。Codex では
各 unit に安定した担当範囲、個別の確認方法、理解済みの共有部分、既に使える
git/worktree があるかを先に確認する。どれか欠けるなら serial に進めるか、repo
構造を変える前に確認する。全部そろう場合だけ write unit ごとに `create_thread`
worktree を作る。各 child thread には1つの unit、担当範囲、validation evidence、
integration contract、編集前に unit-scoped goal を立てる指示を渡す。main thread
が統合し、各 unit の証拠、build、tests、browser smoke が揃った時だけ Done。
```

## ビジネスタスク

Before:

```text
散らかった QBR メモを、経営に出せる形にする goal をセットして
```

After:

```text
/goal 共有されたメモと source files から、leadership-ready な QBR brief を
作る。内容は current performance、risks、decisions needed、next actions に
整理する。先に notes、source sheets/docs、前回 QBR format を読む。
confirmed facts と assumptions を分け、数字・owner・customer quote・
commitment を捏造しない。証拠がないものは unconfirmed として残す。
すべての metric と重要 claim を named source に対応づけ、前回 format と
照合し、read-only subagent (`spawn_agent`) で unsupported claims がないか
確認する。Done は共有可能な brief ができ、open questions が明示されているときだけ。
```

## 日常タスク

Before:

```text
apartment application を出せるところまで進める goal をセットして
```

After:

```text
/goal apartment application package を submit-ready にする。ただし、送信・
署名・支払い・private information の共有は明示承認なしに行わない。必要書類を
棚卸しし、ユーザーが持っている files/notes と照合し、足りない message/checklist
items を下書きし、提出前に見ればよい packet と remaining blockers を作る。
sensitive data は local に保ち、書類や日付を捏造しない。Done はすべての
required item が ready / missing / needs user action のどれかに分類され、
最終 checklist が submission 前にユーザーが確認すべきことを明確に示したときだけ。
```
