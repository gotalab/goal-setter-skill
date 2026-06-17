# goal-setter

**雑な依頼を、目的先行の Codex `/goal` 契約に変換する。**

goal-setter は Codex 用のスキルです。長い agent 実行に必要な、目的、Done 条件、検証、制約、停止条件、そして subagent / `create_thread` / worktree をいつ使うかまで含んだコンパクトな goal を作ります。

**Codex** 向けに作っています。**Claude Code** でも使えます。

[English](README.md)

<p align="center">
  <img src="assets/goal-setter-icon.png" alt="Goal Setter のアイコン: ばらばらの依頼がチェック済みの goal 契約へ収束するイメージ" width="180">
</p>

## なぜ

大きめの agent タスクは、最初の prompt が綺麗でないから失敗するというより、途中で「何が Done か」「何を壊してはいけないか」「何で検証するか」「どこで止まるか」が曖昧になることで崩れやすい。

良い goal は手順書ではありません。固定するのは目的と境界で、実装判断はモデルに残します。強いモデルほど、repo を読んで設計、分割、デバッグ方針を推論できるので、人間は判断の境界条件を書く方が効きます。

goal-setter は Codex 固有の実行構造も扱います。読み取り調査やレビューは subagent、非自明な書き込み単位は `create_thread` の worktree、child thread には unit-scoped goal、main thread は統合と証跡照合、という形を goal に落とします。

## 何を書くか

生成される goal はだいたい次を含みます。

- 目的と、その成果がなぜ必要か
- 二値で判定できる Done 条件
- 検証コマンドまたは証跡
- 最初に読むべき入口。ただしファイル列挙しすぎない
- 制約と、テストを弱めて通さないなどの anti-gaming ルール
- 詰まった時、危険な時、ループしている時の停止条件
- Done 前の独立検証
- subagent / `create_thread` / worktree / child goal の並列化ルール

短くするのが基本です。強い命令語は本当に不変な条件にだけ使い、実装順序、内部設計、厳密なファイル境界は要件でない限りモデルに任せます。

## 何が違うか

多くの prompt helper は指示を綺麗にします。goal-setter は、実行形を間違えないための contract を作ります。

- 完成像を復元してから goal を書く
- 結果を左右する曖昧さだけ質問する
- 読み取り subagent と書き込み thread を分ける
- child thread に unit-scoped goal を立てさせる
- 分割可否をファイル配置ではなく、挙動の結合度、共有状態、統合リスクで判断する

## インストール

### Codex Skill

```text
$skill-installer install https://github.com/gotalab/goal-setter-skill/tree/main/skills/goal-setter
```

Codex を再起動し、`$goal-setter` で呼び出します。依頼文から自動で発動することもあります。

手動インストール:

```bash
git clone https://github.com/gotalab/goal-setter-skill.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
ln -s "$(pwd)/goal-setter-skill/skills/goal-setter" "${CODEX_HOME:-$HOME/.codex}/skills/goal-setter"
```

### Codex Plugin Marketplace

```bash
codex plugin marketplace add gotalab/goal-setter-skill
```

その後、Codex の `/plugins` から **Goal Setter** をインストールします。

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

発動せずに draft する:

```text
$goal-setter APIクライアントのv2移行のgoalをドラフトして
```

runtime が直接 set できる場合に、整形して発動する:

```text
$goal-setter goalをセットして: リファクタ後にcheckoutテストが全部通ること
```

Codex で分解可能な作業の場合は、goal-setter がそのまま送れる `/goal ...` 行を返します。Codex の `spawn_agent` や `create_thread` は、ユーザー自身が送った依頼から発火するためです。

## 例

入力:

```text
game の faction が events, enemies, bosses, rewards, HUD, save-load,
smoke evidence に効く goal をセットして
```

出力の形:

```text
/goal 1 run の中で faction ecosystem を観測できる状態にする: pressure と
player history が faction power を変え、それが room events、enemy
mutations、bosses、rewards、HUD、persistence、browser smoke evidence に
反映される。

faction simulation、event generation、enemy/boss mutation、rewards/relics、
HUD/smoke evidence を個別検証できる write unit として扱う。Codex では
main thread で serial 実装しない。repo が対応していれば write unit ごとに
create_thread の worktree を作る。各 child thread には1つの担当範囲、検証証拠、
統合契約、編集前に unit-scoped goal を立てる指示を渡す。main thread が統合し、
各 unit の証拠、build/tests/smoke、read-only final verification が揃った時だけ Done。
```

詳しい例: [docs/EXAMPLES.ja.md](docs/EXAMPLES.ja.md)

## Runtime Notes

- 通常の Codex goal は native goal tool で set できます。
- Codex の並列 goal は、ユーザーが送る `/goal ...` 行として渡します。
- Claude Code には `/goal ...` 行を渡し、同じ分解構造を dynamic workflow として実行させます。

詳細: [docs/RUNTIME.ja.md](docs/RUNTIME.ja.md)

## Repository

```text
skills/goal-setter/SKILL.md          # skill 本体
skills/goal-setter/scripts/          # goal length validator
plugins/goal-setter/                 # Codex plugin bundle
.claude-plugin/                      # Claude Code plugin metadata
```

## License

[MIT](LICENSE)
