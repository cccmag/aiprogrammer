# 分支管理

## 簡介

Git 的分支功能是其最強大的特性之一。通過分支，你可以：

- 在不影響主線的情況下開發新功能
- 實驗新想法，隨時放棄或合併
- 多人並行開發不同功能

## 分支基礎

### 查看分支

```bash
git branch                  # 列出本地分支
git branch -r               # 列出遠端分支
git branch -a               # 列出所有分支
git branch -v               # 查看每個分支的最後提交
```

### 建立分支

```bash
git branch feature          # 建立新分支
git checkout -b feature     # 建立並切換到新分支
git switch -c feature       # 新語法：建立並切換
```

### 切換分支

```bash
git checkout feature         # 切換到 feature 分支
git switch feature          # 新語法：切換分支
```

### 刪除分支

```bash
git branch -d feature       # 刪除已合併的分支
git branch -D feature       # 強制刪除分支（不論是否合併）
```

## 合併分支

### git merge

將分支合併到當前分支：

```bash
# 假設目前在 master，想合併 feature 分支
git checkout master
git merge feature
```

### 合併類型

#### Fast-forward（快轉）

當前分支沒有新的提交，直接移動指標：

```
Before:          After:
master           master
  │                │
  ▼                ▼
  A ← B      A ← B ← feature
                ↑
              feature
```

#### 三路合併（3-way merge）

當有衝突時，Git 會建立新的合併提交：

```
      master
        │
        ▼
   A ← B ← C
           ↑
      feature
```

### 解決衝突

當合併時發生衝突：

```bash
# 1. 查看衝突檔案
git status

# 2. 編輯衝突檔案
# 衝突標記：
# <<<<<<< HEAD
# 你的修改
# =======
# 他們的修改
# >>>>>>> feature
```

編輯後：
```bash
git add filename.txt
git commit -m "Merge branch 'feature' into master"
```

## Rebase

### 基本用法

將当前分支的基礎重新設定到另一分支：

```bash
# 假設目前的分支結構：
# master:  A ← B ← C
# feature:      D ← E

# 在 feature 分支上執行 rebase master
git checkout feature
git rebase master

# 結果：
# master:  A ← B ← C
#                    ↑
# feature            D' ← E'
```

### 互動式 Rebase

修改、編輯、刪除提交：

```bash
git rebase -i HEAD~3  # 修改最後 3 個提交
```

選項：
- `pick` - 使用該提交
- `reword` - 修改提交訊息
- `edit` - 停下來修改
- `squash` - 合併到上一個提交
- `drop` - 刪除提交

### Rebase vs Merge

| 特性 | Rebase | Merge |
|------|--------|-------|
| 歷史 | 線性整潔 | 保留分支圖 |
| 提交歷史 | 扁平化 | 完整保留 |
| 危險性 | 較高（改變歷史） | 較低 |
| 適用場景 | 整理本地提交 | 合併已發布的提交 |

## 遠端分支

### 追蹤分支

```bash
git checkout --track origin/feature  # 建立追蹤分支
git branch -u origin/feature        # 設定上游分支
```

### 刪除遠端分支

```bash
git push origin --delete feature
```

## 分支策略

### Git Flow

```
develop ──────────────────↓
    ↑                        ↓
feature ──→ merge ──→       ↓
              ↑              ↓
hotfix ────────→ merge ───→ release ──→ master
```

- **master** - 正式發布版本
- **develop** - 開發版本
- **feature/** - 新功能
- **release/** - 發布準備
- **hotfix/** - 緊急修正

### GitHub Flow

```
         ┌─ pull request
         ↓
master ────────────→ (auto deploy)
         ↑
    feature/
```

適用於持續部署的專案。

### 簡單流程

```
master ── A ── B ── C ── D
                ↑
           feature/
```

## 練習題

1. 建立一個新分支並切換過去
2. 在新分支上開發功能並合併回 master
3. 模擬衝突並學習解決衝突
4. 練習使用 rebase 整理提交歷史