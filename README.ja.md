# goal-setter

**長めの依頼を、終わり方がはっきりした Codex の `/goal` に整える。**

goal-setter は Codex 用のスキルです。一回で終わらない作業について、「何ができたら完了か」「何で確かめるか」「何を変えてはいけないか」「どこで止まるか」を短くまとめます。細かい作り方までは固定せず、実行する側がコードを読んで判断できる余地を残します。

細かい手順を詰めるより、何を証拠で確認するかを固定する考え方です。手順は固定しすぎません。

**Codex** 向けに作っています。**Claude Code** でも使えます。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter のアイコン: ばらばらの依頼がチェック済みの goal へ収束するイメージ" width="180">
</p>

## いつ使うか

すべての依頼を Goal にする必要はありません。修正、説明、一度だけの確認なら、普通の依頼で十分です。何度か確かめながら進める作業や、証拠で完了を判断したい作業に使います。

| 作業 | 向いている形 |
| --- | --- |
| 一回で終わる修正、説明、確認 | 普通の依頼 |
| 数回の試行があり得る狭い作業 | 一文または短い段落の Goal |
| 移行、性能改善、広い不具合修正、証拠つき調査 | 通常の Goal |
| 長い調査や高リスクな変更 | Goal と、必要最小限の計画・チェック表・評価資料 |

## 何をするか

- 依頼の完成像を先に整理する。
- 結果、確認方法、作業範囲、危険度、停止判断を変える内容だけを入れる。
- 曖昧すぎて正直な Goal を作れない時はヒアリングに入り、前の回答で次が変わる質問は一つずつ、互いに独立した不足事項はまとめて聞く。
- Goal の受付は親のコンテキストで行い、実行中のフィードバックループ、並行探索、コンテキスト分離、独立検証が完了判断を改善する時は、Goal に具体的な subagent 実行指示を入れる。別タスクはユーザーが明示した時だけ作る。

詳しい動きは [docs/RUNTIME.ja.md](docs/RUNTIME.ja.md) にあります。例は
[docs/EXAMPLES.ja.md](docs/EXAMPLES.ja.md) にあります。

## インストール

どれか1つを選びます。

| 使う環境 | 入れ方 | 呼び出し方 |
| --- | --- | --- |
| Codex App の `/plugins` | Codex App Plugin | `$goal-setter:goal-setter ...` |
| Codex の local skills | Codex Skill | `$goal-setter ...` |
| Claude Code | Claude Code marketplace | `/goal-setter:goal-setter ...` |
| Skills CLI 対応の別ツール | Skills CLI | そのツールの呼び出し方 |

Codex App を使うなら、基本は **Codex App Plugin** だけで十分です。

### Codex App Plugin

Codex で `/plugins` を開き、**Add plugin marketplace** に次を入れます。

```text
Source: gotalab/goal-setter-skill
Git ref: main
Sparse paths: plugins/goal-setter
```

その後、Plugins 画面から **Goal Setter** をインストールします。

### Codex Skill

Codex chat で実行します。

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Codex を再起動し、`$goal-setter` で呼び出します。

### Claude Code

```text
/plugin marketplace add gotalab/goal-setter-skill
/plugin install goal-setter@goal-setter
```

明示的に呼ぶ場合は `/goal-setter:goal-setter` を使います。

### Skills CLI

```bash
npx skills add gotalab/goal-setter-skill
```

## 使い方

発動せずに下書きする:

```text
$goal-setter APIクライアントのv2移行のgoalを下書きして
```

整えて発動する:

```text
$goal-setter goalを設定して: リファクタ後にcheckoutテストが全部通ること
```

Goal は Codex の Goal 機能でそのまま設定します。フィードバックループ、並行探索、コンテキスト分離、独立検証が完了判断を改善する場合は、実行中の Codex が対象の作業で subagent を起動し、証拠を待ち、統合してから判断するという具体的な指示を Goal に入れます。Goal の受付自体は、依頼の理解に大きな独立調査が必要な場合を除き、親のコンテキストで行います。順序や役割を固定した流れにはせず、親がその時点の証拠とコストから次の使い方を決めます。`create_thread` は別タスクを作る機能なので、ユーザーが別タスク化を明示した場合だけ使います。

## 資料

- [例](docs/EXAMPLES.ja.md)
- [実行時の動き](docs/RUNTIME.ja.md)
- [変更履歴](CHANGELOG.md)

## リポジトリ

```text
skills/goal-setter/SKILL.md          # スキル本体
skills/goal-setter/scripts/          # goal の長さ確認
scripts/                             # 配布前の確認
plugins/goal-setter/                 # Codex plugin 用の一式
.claude-plugin/                      # Claude Code 用の情報
```

## License

[MIT](LICENSE)
