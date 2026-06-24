# package.json 深入解析

## package.json 的角色

`package.json` 是 Node.js 專案的核心設定檔案。它不僅記錄了專案的中繼資料，還定義了依賴、腳本、授權等關鍵資訊。

## 頂層欄位

```json
{
  "name": "my-express-app",
  "version": "1.0.0",
  "description": "An Express.js application",
  "main": "app.js",
  "license": "MIT"
}
```

### name 與 version

這兩個欄位共同構成套件的唯一識別。規則：
- name：小寫、無空格、可用連字號或底線
- version：遵循 SemVer 規範

```json
{
  "name": "@scope/package-name",
  "version": "1.2.3"
}
```

## 依賴管理

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "mongoose": "^7.6.0"
  },
  "devDependencies": {
    "jest": "^29.7.0",
    "eslint": "^8.50.0",
    "nodemon": "^3.0.1"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  },
  "optionalDependencies": {
    "bufferutil": "^4.0.7"
  }
}
```

各類型說明：
- **dependencies**：執行時期需要的套件
- **devDependencies**：僅開發時需要（測試、建置工具）
- **peerDependencies**：宿主專案必須提供的套件（通常用於插件）

## Scripts 進階用法

```json
{
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js",
    "test": "jest --coverage",
    "lint": "eslint src/",
    "lint:fix": "eslint src/ --fix",
    "build": "webpack --mode production",
    "prestart": "npm run build",
    "posttest": "npm run lint",
    "custom:deploy": "node scripts/deploy.js"
  }
}
```

使用 `pre` 和 `post` 前綴可以自動化鉤子：
- `npm run build` 執行前自動執行 `prebuild`
- `npm run build` 執行後自動執行 `postbuild`

## 專案中繼資料

```json
{
  "author": "Alice Wang <alice@example.com> (https://alice.dev)",
  "contributors": [
    { "name": "Bob Chen", "email": "bob@example.com" }
  ],
  "repository": {
    "type": "git",
    "url": "https://github.com/user/repo.git"
  },
  "bugs": {
    "url": "https://github.com/user/repo/issues"
  },
  "homepage": "https://github.com/user/repo#readme",
  "keywords": ["express", "api", "backend"]
}
```

## 發布設定

```json
{
  "private": true,
  "publishConfig": {
    "registry": "https://npm.pkg.github.com/"
  },
  "files": [
    "dist/",
    "lib/",
    "!src/"
  ],
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

- **private**: true 防止意外發布到 npm
- **files**: 指定發布時包含哪些檔案（`!` 前綴表示排除）
- **engines**: 限制 Node.js 和 npm 版本

## 專案入口與匯出

```json
{
  "main": "dist/index.js",
  "module": "dist/index.mjs",
  "types": "dist/index.d.ts",
  "exports": {
    ".": {
      "import": "./dist/index.mjs",
      "require": "./dist/index.js"
    },
    "./utils": "./dist/utils.js"
  }
}
```

`exports` 欄位是現代 Node.js 推薦的匯出方式，支援條件式匯出。

## 其他有用欄位

```json
{
  "browser": "dist/bundle.js",
  "bin": {
    "my-cli": "./bin/cli.js"
  },
  "man": "./man/doc.1",
  "workspaces": [
    "packages/*"
  ]
}
```

- **browser**：瀏覽器環境的版本
- **bin**：提供 CLI 命令
- **workspaces**：Monorepo 支援

## package.json 常見錯誤

```json
// 錯誤：版本格式不正確
"version": "1.0"

// 錯誤：name 有大寫字母
"name": "MyApp"

// 錯誤：遺漏必要的 dependencies
"dependencies": {}
```

## 自動化檢查

```bash
# 驗證 package.json 格式
npm doctor

# 檢查遺漏的依賴
npm ls

# 檢查套件完整性
npm audit
```

## 總結

`package.json` 遠不止是一個依賴清單。它定義了專案的方方面面，從執行環境到發布設定。深入理解每個欄位的用途，能夠讓專案管理更加專業和高效。

## 延伸閱讀

- [package.json 官方文件](https://www.google.com/search?q=package.json+official+documentation)
- [npm scripts 使用指南](https://www.google.com/search?q=npm+scripts+guide)
- [SemVer 計算器](https://www.google.com/search?q=semver+calculator)
