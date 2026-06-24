# npm 套件管理

## npm 簡介

npm（Node Package Manager）是 Node.js 的官方套件管理工具，也是世界上最大的軟體註冊中心。截至 2024 年，npm 擁有超過 200 萬個套件，每週下載量超過 300 億次。

## 基本指令

```bash
# 初始化專案
npm init -y

# 安裝套件
npm install express          # 安裝到 dependencies
npm install -D jest          # 安裝到 devDependencies
npm install -g nodemon       # 全域安裝

# 移除套件
npm uninstall express

# 更新套件
npm update
npm outdated                 # 查看可更新的套件
```

## 版本語義

npm 使用 SemVer（語義化版本）規範：`主版號.次版號.修訂號`

```json
{
  "dependencies": {
    "express": "^4.18.2",    // 相容於 4.x.x
    "lodash": "~4.17.21",   // 相容於 4.17.x
    "react": "18.2.0",      // 精確版本
    "axios": "*"            // 任何版本（不推薦）
  }
}
```

符號說明：
- `^`：允許更新次版號和修訂號
- `~`：僅允許更新修訂號
- 無符號：精確版本
- `*`：任何版本

## package-lock.json

`package-lock.json` 記錄了依賴樹的精確版本：

```json
{
  "name": "my-app",
  "lockfileVersion": 3,
  "packages": {
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-..."，
      "dependencies": {
        "accepts": "~1.3.8"
      }
    }
  }
}
```

**重要**：永遠將 `package-lock.json` 提交到版本控制中。

## npm Scripts

`package.json` 中的 `scripts` 欄位可以定義常用命令：

```json
{
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest",
    "lint": "eslint .",
    "build": "webpack --mode production"
  }
}

// 使用方式
npm start    // npm run start 的縮寫
npm run dev
npm test     // npm run test 的縮寫
```

## 常用 npm 命令進階

```bash
# 檢查過時的套件
npm outdated

# 直接更新主要版本
npm install express@latest

# 檢查安全性問題
npm audit

# 自動修復安全性問題
npm audit fix

# 列出已安裝套件
npm list --depth=0          // 僅頂層
npm list --depth=1          // 包含一層依賴

# 快取操作
npm cache clean --force
npm cache ls

# 發布套件
npm login
npm publish
npm version patch           // 自動升級版本
```

## 全域與本機套件

```bash
# 全域安裝（通常用於 CLI 工具）
npm install -g typescript
npm install -g create-react-app

# 查看全域套件
npm list -g --depth=0

# 全域安裝位置
npm root -g
```

## 私有套件與 Scope

```bash
# 使用 Scope 組織套件
npm install @mycompany/utils

# 發布私有套件
npm publish --access restricted
```

## 安全性最佳實踐

```bash
# 1. 定期執行安全性稽核
npm audit

# 2. 使用 .npmrc 設定 registry
echo "registry=https://registry.npmjs.org/" > .npmrc

# 3. 啟用 2FA
npm profile enable-2fa auth-and-writes

# 4. 檢查套件完整性
npm audit signatures
```

## 選擇套件的原則

```
考慮因素：
├── 下載量（每週）
├── GitHub Stars
├── 最後更新時間
├── 授權條款
├── 依賴數量（越少越好）
└── 維護者數量
```

## 總結

npm 不僅是套件安裝工具，更是整個 Node.js 生態的基礎設施。熟練使用 npm 的各項功能，能顯著提升開發效率和專案品質。

## 延伸閱讀

- [npm 官方文件](https://www.google.com/search?q=npm+official+documentation)
- [SemVer 語義化版本](https://www.google.com/search?q=semver+semantic+versioning)
- [npm 安全最佳實踐](https://www.google.com/search?q=npm+security+best+practices)
