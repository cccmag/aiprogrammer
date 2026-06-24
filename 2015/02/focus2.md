# npm 與模組管理：套件發布、依賴管理、SemVer

## 前言

npm（Node Package Manager）是 Node.js 的套件管理工具，也是世界上最大的程式碼生態系。

## 基本命令

### 安裝與管理

```bash
# 初始化新專案
npm init -y

# 安裝套件
npm install express          # 安裝到 node_modules
npm install --save express   # 加入 dependencies
npm install --save-dev mocha # 加入 devDependencies
npm install -g nodemon       # 全域安裝

# 移除
npm uninstall express

# 更新
npm update                   # 更新所有
npm update express           # 更新特定套件
```

### package.json

```json
{
  "name": "my-app",
  "version": "1.0.0",
  "description": "我的應用",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js",
    "test": "mocha test/**/*.js"
  },
  "keywords": ["node", "express"],
  "author": "Your Name",
  "license": "MIT",
  "dependencies": {
    "express": "^4.13.0"
  },
  "devDependencies": {
    "nodemon": "^1.4.0",
    "mocha": "^2.3.0"
  }
}
```

## SemVer 版本控制

### 語法

```
major.minor.patch
   │     │    └── patch: 修正錯誤
   │     └── minor:     新功能（向後相容）
   └── major:           破壞性變更（不相容）
```

### 版本範圍

```json
{
  "exact": "1.2.3",              // 精確版本
  "range": ">=1.0.0",            // 大於等於
  "range": "<2.0.0",             // 小於
  "range": ">=1.0.0 <2.0.0",     // 範圍

  "caret": "^1.2.0",             // 相容版本（預設）
  "tilde": "~1.2.0",             // 接近版本
  "star": "*",                   // 任意版本
  "latest": "latest"             // 最新版本
}
```

```
SemVer 解釋：
─────────────
^1.2.3: >=1.2.3 <2.0.0   （相容 major 版本）
~1.2.3: >=1.2.3 <1.3.0   （相容 minor 版本）
*    : >=0.0.0            （任意版本）
```

### npm 標籤

```bash
npm install package@beta       # 安裝 beta 版
npm publish --tag beta         # 發布到 beta 標籤
npm dist-tag add pkg@1.0.0 latest # 設定 latest 標籤
```

## 發布套件

### 準備

```bash
# 登入 npm
npm adduser

# 檢查登入狀態
npm whoami
```

### 發布流程

```bash
# 更新版本
npm version patch     # 1.0.0 -> 1.0.1
npm version minor     # 1.0.0 -> 1.1.0
npm version major     # 1.0.0 -> 2.0.0

# 發布
npm publish           # 發布到 latest
npm publish --tag beta # 發布到 beta
```

### .npmignore

```
# 忽略的檔案
node_modules/
.git/
.DS_Store
*.log
test/
coverage/
```

## npm 腳本

### 生命週期鉤子

```json
{
  "scripts": {
    "preinstall": "echo before install",
    "postinstall": "echo after install",
    "prepublish": "echo before publish",
    "postpublish": "echo after publish",
    "prestart": "echo before start",
    "poststart": "echo after start",
    "prestop": "echo before stop",
    "poststop": "echo after stop"
  }
}
```

### 常見用法

```bash
npm run build          # 執行自訂腳本
npm run test           # 執行測試
npm run lint           # 執行 linter
```

## 依賴管理技巧

### 檢視依賴

```bash
npm list               # 查看依賴樹
npm list --depth=0     # 只看第一層
npm list express       # 特定套件版本
npm outdated           # 有更新的套件
npm audit              # 安全漏洞
```

### 快取管理

```bash
npm cache clean        # 清除快取
npm cache verify       # 驗證快取
```

### 離線使用

```bash
npm install --offline  # 使用本地快取
npm ci                 # 根據 lockfile 安裝
```

## 私用套件

### 組織與作用域

```bash
# 建立作用域
npm init --scope=myorg

# 發布到作用域
npm publish --access=restricted

# 安裝作用域套件
npm install @myorg/private-package
```

```json
{
  "name": "@myorg/private-package",
  "version": "1.0.0"
}
```

## 結論

npm 從簡單的套件管理器發展成為世界上最大的程式碼生態系。SemVer 版本控制讓依賴管理更加安全，npm scripts 讓專案自動化更加便捷。

---

## 延伸閱讀

- [npm 官方文檔](https://www.google.com/search?q=npm+documentation+commands)
- [SemVer 規範](https://www.google.com/search?q=SemVer+specification+version)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」歷史回顧系列之一。*