# 程式協作工作流：分支策略與程式碼審查

## 版本控制工作流

### 1. 集中式工作流

```bash
# 集中式工作流（像 SVN）
# 所有開發者在 master 分支工作

# 開發者 A
git clone server/repo
git add file.c
git commit -m "Fix bug"
git push

# 開發者 B
git pull
# 解決衝突
git push
```

### 2. 功能分支工作流

```bash
# 功能分支工作流
# 每個功能在新分支開發

# 建立功能分支
git checkout -b feature-login

# 開發、提交
git add .
git commit -m "Implement login"

# 合併回 master
git checkout master
git merge feature-login

# 刪除功能分支
git branch -d feature-login
```

### 3. Gitflow 工作流

```bash
# Gitflow 工作流
# 長期分支：master, develop
# 短期分支：feature-*, release-*, hotfix-*

# 從 develop 建立功能分支
git checkout develop
git checkout -b feature/new-feature

# 開發完成，合併回 develop
git checkout develop
git merge feature/new-feature

# 建立 release 分支
git checkout -b release/1.0
# 修復發布前問題
git checkout master
git merge release/1.0
git tag v1.0

# hotfix 流程
git checkout -b hotfix/bug master
git checkout master
git merge hotfix/bug
git tag v1.1
```

## 分支命名慣例

```bash
# 常見分支命名
feature/user-authentication
feature/payment-integration
bugfix/login-crash
bugfix/memory-leak
hotfix/security-patch
release/v1.0
release/v1.1
develop
master
```

## 程式碼審查

### 程式碼審查的好處

```
程式碼審查的價值：
─────────────────
1. 發現 Bugs
2. 分享知識
3. 確保程式碼一致性
4. 培訓新團隊成員
5. 減少技術債務
```

### 審查清單

```markdown
# Code Review Checklist
──────────────────────
功能    - 程式碼是否正確實現功能？
       - 邊界條件是否處理？
       - 錯誤處理是否完善？

設計    - 設計是否合理？
       - 是否符合團隊規範？
       - 是否過度設計？

可讀性  - 命名是否清晰？
       - 註解是否足夠？
       - 函式是否過長？

效能    - 是否有效能問題？
       - 演算法是否最優？
       - 資料庫查詢是否有效率？

安全    - 是否有安全漏洞？
       - 輸入驗證是否完善？
       - 敏感資料是否保護？
```

### 審查流程

```bash
# 典型的審查流程（2007 年的工具）
# 1. 開發者提交 commit
git commit -m "Add new feature"

# 2. 發送審查請求（email 或工具）
git request-pull origin/master

# 3. 審查者檢視變更
git diff HEAD~1 HEAD

# 4. 提供反饋
#    - 直接溝通
#    - 評論工具

# 5. 根據反饋修改
git commit --amend

# 6. 合併
git merge
```

## 持續整合

### CI 的概念

```bash
# 簡單的 CI 流程
# 每次 push 觸發建置和測試

#!/bin/bash
# .git/hooks/post-push
if [ "$1" == "origin" ]; then
    # 執行測試
    make test
    # 執行建置
    make build
    # 部署
    make deploy
fi
```

## 衝突解決

```bash
# 合併衝突解決
git merge feature-branch

# Git 會標記衝突檔案
<<<<<<< HEAD
        int x = 1;
=======
        int x = 2;
>>>>>>> feature-branch

# 手動解決
git add file.c
git commit -m "Resolve merge conflict"
```

## 結語

好的協作工作流是團隊成功的關鍵。2007 年的最佳實踐包括：
1. 使用分支隔離功能開發
2. 定期合併避免衝突累積
3. 程式碼審查提高品質
4. 自動化測試確保穩定性

這些原則至今仍是軟體開發的最佳實踐。

---

## 延伸閱讀

- [Git+workflow+branching+strategy](https://www.google.com/search?q=Git+workflow+branching+strategy)
- [code+review+best+practices+2007](https://www.google.com/search?q=code+review+best+practices+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 6 月號」本期焦點系列之一。*