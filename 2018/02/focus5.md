# Pull Request 實務

## 簡介

Pull Request（PR）是現代軟體開發中進行程式碼審查和團隊協作的核心流程。本篇介紹 PR 的最佳實踐。

## PR 的價值

### 為什麼需要 PR

1. **程式碼審查** - 團隊成員檢視變更
2. **知識分享** - 團隊成員了解彼此的改動
3. **及早發現問題** - 在合併前發現錯誤
4. **追蹤變更** - 清楚記錄每個改動的目的
5. **持續整合** - 觸發自動化測試

## 發起 PR

### 事前準備

```bash
# 1. 確保分支是最新的
git checkout develop
git pull origin develop

# 2. 建立功能分支
git checkout -b feature/new-feature

# 3. 開發與提交
git add .
git commit -m "feat: 新增功能"

# 4. 推送分支
git push -u origin feature/new-feature
```

### 撰寫 PR 描述

```markdown
## 變更摘要
<!-- 簡短描述這個 PR 的目的 -->

## 動機
<!-- 為什麼需要這個變更？ -->

## 變更內容
- 新增 `UserService` 類別
- 修改 `AuthController` 處理新流程
- 新增單元測試

## 影響範圍
- 登入模組
- 使用者管理模組

## 測試方式
1. 執行 `npm test`
2. 手動測試登入流程
3. 驗證新舊功能相容

## 相關 Issue
Closes #123
```

## Code Review

### 審查者觀點

#### 功能正確性
- 邏輯是否正確？
- 邊界條件是否處理？
- 現有功能是否被破壞？

#### 程式碼品質
- 命名是否清晰？
- 是否有重複程式碼？
- 是否有註解？

#### 效能
- 是否有效能問題？
- 資料庫查詢是否優化？

#### 安全性
- 是否有用戶輸入驗證？
- 是否有可能的安全漏洞？

### 常見審查意見

```
[blocking] - 必須修改才能合併
[optional] - 建議修改，但非必須
[nit] - 小問題，如程式碼風格
[question] - 需要澄清
```

### 審查範例

```python
# 審查者留言：
# [blocking] 這個函式沒有處理空字串的情況，請加上驗證
# [nit] 變數命名可以使用更描述性的名稱
# [question] 為什麼選擇這個演算法？
```

### 回應審查意見

```bash
# 1. 根據意見修改程式碼
git checkout feature-branch
# ... 修改程式碼 ...
git add .
git commit -m "address review comments"

# 2. 推送更新
git push origin feature-branch
```

## PR 流程

### 完整流程

```
1. 建立功能分支
      │
      ▼
2. 開發與提交
      │
      ▼
3. 推送並發起 PR ──→ 自動化測試
      │                    │
      │              測試失敗？
      │                 ╱╲
      │               是  否
      ↓               ╱   ╲
4. Code Review         ╱   ╲
      │             修復   等待
      │               ╲   ╱
      │                ╲ ╱
      ▼                 ▼
5. 修改（根據意見）──→ 4
      │
      ▼
6. 合併 PR
      │
      ▼
7. 刪除分支
```

### Squash 合併

將多個提交合併成一個：

```bash
git rebase -i HEAD~3
# 將 commit 的 pick 改為 squash
```

好處：
- 保持 master/main 分支整潔
- 每個功能只有一個提交記錄

### Merge vs Squash

| 特性 | Merge | Squash |
|------|-------|--------|
| 歷史 | 保留所有提交 | 合併為一個提交 |
| 適用 | 長期分支 | 功能分支 |
| 複雜度 | 可能複雜 | 簡潔 |

## 自動化

### Status Checks

設定 CI 檢查：

```yaml
# .github/workflows/ci.yml
name: CI
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
```

### 必備檢查

1. 單元測試通過
2. 程式碼風格檢查
3. 安全性掃描
4. 建置成功

## 練習題

1. 建立一個 PR 並練習撰寫描述
2. 為你的 PR 添加審核者
3. 根據審查意見修改並推送
4. 設定 branch protection 規則