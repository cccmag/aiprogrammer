# 分支策略實踐

良好的分支策略是團隊協作的關鍵。本章介紹幾種流行的分支模型。

---

## Git Flow

Git Flow 是 Vincent Driessen 提出的分支模型，適用於有固定發布周期的專案。

### 主要分支

```
master     ──────────────────────── (正式發布)
                              ↑
develop    ───────────────────────────────── (開發整合分支)
```

### 支援分支

- **Feature branches**：`feature/*` - 新功能開發
- **Release branches**：`release/*` - 發布準備
- **Hotfix branches**：`hotfix/*` - 緊急修復

### 操作流程

```bash
# 開始新功能
git checkout -b feature/login develop

# 完成功能
git checkout develop
git merge --no-ff feature/login
git branch -d feature/login

# 開始發布
git checkout -b release/1.0 develop
# 進行發布準備，最後：
git checkout master
git merge --no-ff release/1.0
git tag -a v1.0 -m "版本 1.0"
git branch -d release/1.0

# 緊急修復
git checkout -b hotfix/1.0.1 master
# 修復後
git checkout master
git merge --no-ff hotfix/1.0.1
git tag -a v1.0.1 -m "版本 1.0.1"
git checkout develop
git merge --no-ff hotfix/1.0.1
git branch -d hotfix/1.0.1
```

---

## GitHub Flow

適用於持續部署的網頁應用程式。

### 流程

1. `main` 分支隨時可部署
2. 所有工作在新的 feature 分支
3. 定期推送並與他人協作
4. 透過 Pull Request 審查程式碼
5. 審查通過後合併到 main
6. 合併後立即部署

### 規則

- `main` 分支受保護，不可直接推送
- 所有變更都透過 Pull Request
- 需要至少一人審查通過

---

## Trunk-based Development

所有開發者在單一分支（trunk）上工作。

### 特點

- 簡化分支管理
- 需要頻繁整合
- 適合持續交付的團隊

### 實作方式

```bash
git checkout main
git pull

# 短期 feature 分支（不超過 2 天）
git checkout -b feature/quick-fix
# 快速完成後合併回 main
```

---

## 選擇分支策略

選擇適合團隊的策略：

| 策略 | 適用場景 |
|------|----------|
| Git Flow | 定期發布的專案 |
| GitHub Flow | 持續部署的網頁應用 |
| Trunk-based | 小型、頻繁發布的團隊 |

---

## 保護分支

在 GitHub 中保護重要分支：

1. 前往 Settings → Branches
2. 點擊「Add rule」
3. 設定保護規則：
   - Require pull request reviews
   - Require status checks
   - Include administrators

---

## 小結

選擇適合團隊規模和專案特性的分支策略，能夠提升開發效率並減少衝突。

---

*作者：AI 程式人團隊*