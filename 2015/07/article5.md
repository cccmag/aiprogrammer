# Git 在企業中的應用

## 前言

越來越多企業採用 Git 作為主要的版本控制系統。本 文探討企業級 Git 部署的考量。

---

## 企業 Git 方案

### GitHub Enterprise

- 私有部署選項
- 企業級安全
- SAML/AD 整合

### GitLab

- 開源版本
- 企業版功能
- 完整的 CI/CD

### Bitbucket

- Atlassian 生態系
- Jira 整合
- 小型團隊友好

[搜尋 GitHub Enterprise vs GitLab comparison](https://www.google.com/search?q=GitHub+Enterprise+vs+GitLab+enterprise)

---

## 遷移考量

### 從 SVN 遷移

```bash
# 使用 git-svn
git svn clone http://svn.example.com/repo --authors-file=authors.txt

# 對應作者
# name <email>
```

### 從 CVS 遷移

需要先轉換為 SVN，再轉換為 Git。

### 遷移策略

1. **並行運行**：新舊系統同時運行一段時間
2. **分階段遷移**：按團隊逐步遷移
3. **培訓優先**：先培訓再遷移

---

## 權限管理

### 分支權限

```bash
# GitLab 保護分支設定
# Settings → Repository → Protected branches

# 設定誰可以推送/合併
main: Developers cannot force push, require approval
```

### 檔案權限

使用 Gitolite 或 Gitosis 進行細粒度控制：

```gitolite
repo myproject
    RW+     =   @developers
    R       =   @testers
    -       =   @interns
```

---

## 整合企業系統

### LDAP/Active Directory

```bash
# GitLab LDAP 設定
# /etc/gitlab/gitlab.rb
gitlab_rails['ldap_enabled'] = true
gitlab_rails['ldap_servers'] = {
  'main' => {
    'host' => 'ldap.example.com',
    'port' => 389,
    'uid' => 'uid',
    'method' => 'plain',
    'bind_dn' => 'cn=admin,dc=example,dc=com',
    'password' => 'password'
  }
}
```

### SSO 整合

```bash
# SAML 設定
# Settings → General → Security → SAML
```

---

## 備份與災難恢復

### 備份策略

```bash
# GitLab 備份
gitlab-rake gitlab:backup:create

# 自動化備份 cron
0 2 * * * /opt/gitlab/bin/gitlab-rake gitlab:backup:create
```

### 還原流程

```bash
gitlab-rake gitlab:backup:restore BACKUP=1234567890
```

---

## 效能優化

### 大型倉庫

```bash
# 启用 FSync
git config core.fsyncObjectFiles true

# 使用 shallow clone
git clone --depth 1 https://github.com/bigproject/repo.git
```

### Git LFS

處理大型二進制檔案：

```bash
# 安裝
git lfs install

# 追蹤大檔案
git lfs track "*.psd"
git lfs track "*.zip"

# .gitattributes 會自動建立
```

---

## 監控與分析

### GitStats

```bash
git clone https://github.com/hoxu/gitstats.git
./gitstats repo/ output/
```

### git-of-theseus

分析專案活躍度：

```python
pip install git-of-theseus
git-of-theseus --repo /path/to/repo
```

---

## 小結

企業級 Git 部署需要考慮安全性、整合、效能等多方面因素。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [GitHub Enterprise 文档](https://www.google.com/search?q=GitHub+Enterprise+documentation)
- [GitLab 企業版指南](https://www.google.com/search?q=GitLab+enterprise+deployment)