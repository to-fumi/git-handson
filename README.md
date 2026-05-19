# git-handson

Git / GitHub の基本操作を実務に近い形で学ぶハンズオンです。

---

## 目次

1. [準備](#1-準備)
2. [ローカルでの開発](#2-ローカルでの開発)
3. [ブランチの基本](#3-ブランチの基本)
4. [環境変数の設定](#4-環境変数の設定)
5. [CI の動作確認](#5-ci-の動作確認)
6. [コンフリクト](#6-コンフリクト)
7. [1人でのプロジェクト管理](#7-1人でのプロジェクト管理)

---

## 1. 準備

リポジトリをクローンして、ローカル環境を整えます。

```bash
git clone <repository_url>
cd git-handson
```

`.env.example` をコピーして `.env` を作成します。

```bash
cp .env.example .env
```

依存関係をインストールします。

```bash
pip install -r requirements.txt
```

---

## 2. ローカルでの開発

まずはローカルでテスト・静的解析・フォーマットを手動で実行します。  
この手順は後の CI 導入で自動化されます。

### テスト

```bash
pytest tests/ -v
```

**失敗させる例:** `src/core/calculator.py` の `add` の戻り値を変える

```python
def add(a: float, b: float) -> float:
    return a - b  # 本来は a + b
```

```
FAILED tests/core/test_calculator.py::test_add - AssertionError: assert 0 == 5
```

確認できたら元に戻しましょう。

### Linter

```bash
ruff check .
```

**失敗させる例:** 未使用の変数を追加する

```python
def add(a: float, b: float) -> float:
    result = a + b  # 未使用変数
    return a + b
```

```
src/core/calculator.py:2:5: F841 Local variable `result` is assigned to but never used
```

修正可能なエラーは自動で直すこともできます。※ただしルールによって自動修正できないものもあります（未使用変数の削除など）。

```bash
ruff check --fix .
```

確認できたら元に戻しましょう。

### Formatter

```bash
ruff format --check .
```

**失敗させる例:** スペースやインデントを崩す

```python
def add(a: float,b: float) -> float:  # カンマの後のスペースなし
    return a+b  # 演算子前後のスペースなし
```

```
Would reformat src/core/calculator.py
1 file would be reformatted
```

自動で修正することもできます。

```bash
ruff format .
```

確認できたら元に戻しましょう。

---

## 3. ブランチの基本

### ブランチの役割

| ブランチ | 役割 |
|---|---|
| `main` | リリース済みの安定したコード |
| `develop` | 開発中のコードを統合するブランチ |
| `feature/*` | 機能ごとの作業ブランチ |

### ブランチの作成・切り替え

自分の名前でブランチを作成します。

```bash
git switch -c feature/your-name
```

### コードの修正

`src/apps/supermarket.py` の `total_price` に `round()` を追加します。

```python
def total_price(unit_price: float, quantity: int) -> float:
    return round(multiply(unit_price, quantity), 2)
```

### コミットメッセージの規約

コミットメッセージはプレフィックスを付けて統一します。

| プレフィックス | 用途 | 例 |
|---|---|---|
| `feat:` | 新機能の追加 | `feat: checkout_total 関数を追加` |
| `fix:` | バグ修正 | `fix: divide のゼロ除算を修正` |
| `bugfix:` | バグ修正（fix と同義） | `bugfix: 割引率の上限チェックを修正` |
| `chore:` | 設定・依存関係など実装以外 | `chore: python-dotenv を追加` |
| `docs:` | ドキュメントのみの変更 | `docs: README にハンズオン手順を追加` |
| `style:` | フォーマット修正など動作に影響しない変更 | `style: ruff format を適用` |
| `refactor:` | 動作を変えないコードの整理 | `refactor: calculator を core に移動` |
| `test:` | テストの追加・修正 | `test: total_price のテストを追加` |
| `ci:` | CI 設定の変更 | `ci: typecheck ジョブに pytest を追加` |

### コミット

```bash
git add src/apps/supermarket.py
git commit -m "feat: total_price に round を追加"
```

### コミットのリセット

コミットを取り消したい場合は `reset` を使います。

**--soft: コミットだけ取り消す（変更は残る）**

```bash
git reset --soft HEAD~1
```

`git status` でファイルの変更が残っていることを確認してから、再度コミットします。

```bash
git commit -m "feat: total_price に round を追加"
```

**--hard: コミットも変更も全部取り消す**

```bash
git reset --hard HEAD~1
```

`git status` でファイルの変更も消えていることを確認します。  
消えてしまったのでコードの修正とコミットをもう一度行います。

```bash
# src/apps/supermarket.py を再度修正してから
git add src/apps/supermarket.py
git commit -m "feat: total_price に round を追加"
```

### プッシュ

```bash
git push origin feature/your-name
```

### ブランチの削除

**リモート（GitHub）**

GitHub のリポジトリページから `branches` を開き、`feature/your-name` の横のゴミ箱アイコンをクリックして削除します。

**ローカル**

```bash
git switch main
git branch -d feature/your-name
```

### Branch protection rules

`main` ブランチへの直接 push を禁止し、PR 経由のみマージできるよう設定します。

GitHub リポジトリの `Settings > Branches > Add rule` から設定します。

- Branch name pattern: `main`
- Require a pull request before merging: ON

---

## 4. 環境変数の設定

### ローカル

`.env` ファイルに環境変数を記載します。`.env` は `.gitignore` に含まれているためリポジトリには含まれません。

```
ENV=dev
TAX_RATE=0.10
DISCOUNT_RATE=0.05
```

### GitHub

GitHub Actions で使う環境変数は Repository Variables に登録します。

`Settings > Secrets and variables > Actions > Variables` から以下を登録します。

| 変数名 | 値 |
|---|---|
| `ENV` | `dev` |
| `TAX_RATE` | `0.10` |
| `DISCOUNT_RATE` | `0.05` |

---

## 5. CI の動作確認

ローカルで手動実行していたテスト・Linter・Formatter を、CI（GitHub Actions）が PR のたびに自動で実行します。

### 成功を確認する

正常なコードの状態で PR を作成し、CI が通ることを確認します。

### 失敗を確認する

以下を試して CI が落ちることを確認します。

| 失敗パターン | 方法 |
|---|---|
| Test 失敗 | 関数の戻り値を意図的に変える |
| Linter 失敗 | 未使用変数を追加する |
| Formatter 失敗 | インデントやスペースを崩す |

CI が落ちた状態を確認したら修正して再 push し、CI が復活することも確認しましょう。

---

## 6. コンフリクト

2人1組のペアで、同じ関数に異なる変更を加えてコンフリクトを発生させます。

### ペアごとの担当

| ペア | 担当関数 | Aさんの変更 | Bさんの変更 |
|---|---|---|---|
| Pair 1 | `apply_discount` | 割引率が1.0超えたら`ValueError` | 割引後に`round()`で整数化 |
| Pair 2 | `add_tax` | 税込みを`math.floor()`で切り捨て | 税込みを`round()`で四捨五入 |
| Pair 3 | `calculate_change` | お釣りが負になったら`ValueError` | お釣りを`round()`で整数化 |
| Pair 4 | `total_price` | quantityが0以下なら`ValueError` | unit_priceが負なら`ValueError` |
| Pair 5 | `unit_price` | 結果を`round(x, 2)`で小数点2桁 | total_priceが負なら`ValueError` |
| Pair 6 | 新関数 `checkout_total()` | `割引 → 税込み`の順で計算 | `税込み → 割引`の順で計算 |

### 手順

1. `develop` ブランチから各自 `feature/` ブランチを作成する
2. 担当の変更を加えてコミット・プッシュし、`develop` へ PR を作成する
3. ペアのAさんが先に PR をマージする
4. Bさんの PR でコンフリクトが発生することを確認する
5. Bさんがコンフリクトを解消して再 push する

### Pair 6 について

`checkout_total()` は適用順によって計算結果が変わります。どちらが正しいかをペアで議論してから解消しましょう。

```python
# Aさん: 割引してから税込み
total = add_tax(apply_discount(price, discount_rate), tax_rate)

# Bさん: 税込みにしてから割引
total = apply_discount(add_tax(price, tax_rate), discount_rate)
```

---

## 7. 1人でのプロジェクト管理

### Issue の作成

作業を始める前に Issue を作成して作業単位を管理します。

`Issues > New issue` から作成します。

### Issue と PR を紐付ける

PR の説明に `Close #<issue番号>` と記載すると、PR マージ時に Issue が自動でクローズされます。

```
## 概要
apply_discount に割引率の上限チェックを追加

Close #1
```

### PR のセルフレビュー・マージ

PR を作成したら自分でコードを見直してからマージします。CI が通っていることも確認しましょう。
