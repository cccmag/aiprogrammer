# 開發環境：VS Code + Node.js

## 為什麼選擇 VS Code

Visual Studio Code 是當今最受歡迎的程式碼編輯器，由 Microsoft 開發並開源。它輕量、可擴展，內建對 JavaScript、TypeScript 和 Node.js 的優秀支援。

### 安裝 VS Code

前往 [code.visualstudio.com](https://code.visualstudio.com/) 下載並安裝對應作業系統的版本。安裝完成後，建議立即安裝以下擴展：

- **ESLint**：程式碼風格檢查
- **Prettier**：自動格式化
- **JavaScript (ES6) code snippets**：程式碼片段
- **Node.js Modules Intellisense**：模組自動補全
- **GitLens**：Git 整合增強

## 安裝 Node.js

### 使用 nvm 管理版本

建議使用 nvm（Node Version Manager）管理 Node.js 版本：

```bash
# 安裝 nvm（macOS/Linux）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# 安裝最新 LTS 版本
nvm install --lts

# 設定預設版本
nvm alias default 'lts/*'

# 驗證安裝
node --version
npm --version
```

Windows 使用者可以使用 nvm-windows 或直接從 [nodejs.org](https://nodejs.org/) 下載安裝。

### npm 套件管理器

npm 是 Node.js 內建的套件管理器：

```bash
# 初始化專案
mkdir my-project
cd my-project
npm init -y

# 安裝套件
npm install express
npm install --save-dev nodemon

# 執行腳本
node index.js
npx nodemon index.js
```

## VS Code 設定

### 專屬設定檔

建立 `.vscode/settings.json` 來統一團隊設定：

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "files.eol": "\n",
  "javascript.validate.enable": true,
  "javascript.format.enable": false,
  "typescript.validate.enable": true
}
```

### 除錯設定

建立 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "node",
      "request": "launch",
      "name": "執行目前檔案",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "type": "node",
      "request": "launch",
      "name": "啟動應用",
      "program": "${workspaceFolder}/index.js",
      "env": { "NODE_ENV": "development" }
    }
  ]
}
```

## Hello World 範例

建立 `index.js`：

```javascript
const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
  res.end('Hello, World!\n');
});

server.listen(port, hostname, () => {
  console.log(`伺服器運行於 http://${hostname}:${port}/`);
});
```

執行 `node index.js` 並開啟瀏覽器訪問 http://127.0.0.1:3000/。

## Playground 測試

對於簡單的語法測試，可以使用以下方式：

```bash
# 直接執行 JS 檔案
node -e "console.log('Hello')"

# 使用 REPL（互動式環境）
node

# 瀏覽器 Console
# 按 F12 開啟開發者工具 → Console 分頁
```

在 VS Code 中，也可以安裝 Code Runner 擴展，選取程式碼片段後右鍵選擇「Run Code」快速執行。

## 結語

一個好的開發環境能大幅提升學習和開發效率。VS Code 搭配 Node.js 是學習 JavaScript 的最佳入門組合。熟悉編輯器快捷鍵、除錯工具和終端機操作後，就可以專注在程式邏輯上了。

---

**延伸閱讀**

- [VS Code 官方文件](https://www.google.com/search?q=VS+Code+documentation)
- [Node.js 入門指南](https://www.google.com/search?q=Node.js+getting+started)
- [nvm 使用教學](https://www.google.com/search?q=nvm+Node+Version+Manager)
