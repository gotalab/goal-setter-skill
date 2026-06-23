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
- 不明点がある場合も、Goal の中身が変わる質問だけを一つずつ聞く。
- 小さい作業は軽く保つ。長い作業では未確認一覧を更新しながら進め、別の確認役や別スレッドは本当に必要な時だけ入れる。

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

Codex が追加の作業役を使わない場合に、整えて発動する:

```text
$goal-setter goalを設定して: リファクタ後にcheckoutテストが全部通ること
```

`spawn_agent` や `create_thread` という Codex の機能を使う必要がある場合、goal-setter はそのまま送れる `/goal ...` 行を返します。その行をユーザーが送ることで、Codex がそれらの機能を使えるようになります。

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
