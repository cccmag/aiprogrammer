# GitHub 平台使用

GitHub 是全球最大的 Git 倉庫托管平台，擁有超過 1,000 萬用戶和 2,500 萬個倉庫。本章介紹 GitHub 的基本使用方法。

---

## 建立倉庫

### 在 GitHub 上建立

1. 登入 GitHub
2. 點擊右上角「+」按鈕，選擇「New repository」
3. 填入倉庫名稱和描述
4. 選擇公開或私人倉庫
5. 初始化時可選擇加入 README、.gitignore、 license

### 推送本地倉庫

```bash
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

---

## SSH 金鑰設定

使用 SSH 方式連接 GitHub：

### 1. 產生金鑰

```bash
ssh-keygen -t rsa -b 4096 -C "your.email@example.com"
```

### 2. 複製公鑰

```bash
cat ~/.ssh/id_rsa.pub
```

### 3. 在 GitHub 設定

- 前往 Settings → SSH and GPG keys
- 點擊「New SSH key」
- 貼上公鑰內容

### 4. 測試連線

```bash
ssh -T git@github.com
```

---

## Pull Request

Pull Request (PR) 是 GitHub 協作的核心功能。

### 建立 PR

1. Fork 目標倉庫到自己的帳號
2. 克隆 Fork 的倉庫到本地
3. 建立新分支進行修改
4. 推送分支到 GitHub
5. 在 GitHub 上建立 Pull Request

### PR 審查流程

```bash
# 同步上游倉庫
git remote add upstream https://github.com/original/repo.git
git fetch upstream

# 在 PR 基礎上工作
git checkout -b feature upstream/main
```

### 程式碼審查

- 可在 PR 中新增評論
- 可要求特定人員審查
- 支援自動化測試整合（CI）

---

## GitHub Issues

Issues 用於追蹤錯誤、功能請求和任務。

```markdown
## 標題
清楚的問題描述

## 重現步驟
1. 執行...
2. 點擊...

## 預期行為
...

## 實際行為
...
```

### Labels

可使用標籤分類 Issues：
- `bug` - 錯誤
- `enhancement` - 功能增強
- `question` - 問題
- `help wanted` - 需要幫助

---

## GitHub Gist

Gist 是分享程式碼片段的服務：

```bash
# 建立公開 gist
git gist create script.py

# 建立秘密 gist
git gist create -s secret.py
```

---

## 專案管理

### Projects

GitHub Projects 提供看板式管理功能。

### Milestones

里程碑用於追蹤版本或重要目標的進度。

### Wiki

每個倉庫都有 Wiki 功能，適合存放文件。

---

## 小結

GitHub 提供了完整的程式碼托管和協作平台，從簡單的倉庫托管到複雜的程式碼審查流程，都能夠得到良好的支援。

---

*作者：AI 程式人團隊*