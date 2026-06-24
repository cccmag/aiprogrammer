# 建立 React 專案

## 前言

建立現代 React 專案的方式有很多種，從官方推薦的 Vite 到 Next.js 框架等。本文將介紹最常用的幾種方式，幫助開發者選擇適合的起手式。

## Vite 建立

Vite 是目前最推薦的 React 專案起始方式，速度快、配置簡單：

```bash
npm create vite@latest my-react-app -- --template react
cd my-react-app
npm install
npm run dev
```

使用 TypeScript 模板：

```bash
npm create vite@latest my-react-app -- --template react-ts
```

建立完成後，專案結構如下：

```
my-react-app/
├── index.html
├── src/
│   ├── main.jsx
│   ├── App.jsx
│   └── App.css
├── package.json
├── vite.config.js
└── public/
```

## Create React App (CRA)

雖然 CRA 已經進入維護模式，但仍有大量既有專案使用它：

```bash
npx create-react-app my-app
cd my-app
npm start
```

CRA 預設包含 Jest 測試工具、Service Worker 等功能。但由於啟動速度較慢，新專案通常建議使用 Vite。

## Next.js

如果你的應用需要伺服器端渲染（SSR）或靜態生成（SSG），Next.js 是首選：

```bash
npx create-next-app@latest my-next-app
```

Next.js 提供了檔案系統路由、API Routes、圖片優化等開箱即用的功能。

## Remix

Remix 是另一個基於 React 的全端框架，強調 Web 標準和漸進式增強：

```bash
npx create-remix@latest my-remix-app
```

## 手動配置 Webpack

如果想要最大程度的控制權，也可以從頭配置 Webpack：

```bash
mkdir my-custom-app && cd my-custom-app
npm init -y
npm install react react-dom
npm install -D webpack webpack-cli webpack-dev-server html-webpack-plugin babel-loader @babel/core @babel/preset-env @babel/preset-react
```

建立 `webpack.config.js`：

```javascript
const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: 'babel-loader',
      },
    ],
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './public/index.html' }),
  ],
  devServer: {
    port: 3000,
    hot: true,
  },
}
```

新增 Babel 配置 `.babelrc`：

```json
{
  "presets": ["@babel/preset-env", "@babel/preset-react"]
}
```

雖然手動配置更深入理解工具鏈，但對一般開發者來說，使用 Vite 或 Next.js 是更務實的選擇。

## 專案結構建議

無論使用哪種工具，建議採用以下結構：

```
src/
├── components/    # 通用元件
├── pages/         # 頁面元件
├── hooks/         # 自訂 Hooks
├── contexts/      # React Contexts
├── services/      # API 呼叫
├── utils/         # 工具函式
├── styles/        # 全域樣式
└── types/         # TypeScript 型別
```

## 推薦開發工具

- **VS Code**：最受歡迎的編輯器
- **React Developer Tools**：Chrome/Firefox 擴充套件
- **ES7+ React/Redux/React-Native snippets**：VS Code 擴充套件
- **Prettier**：自動格式化
- **ESLint**：程式碼品質檢查

## 結語

根據專案需求選擇合適的起手式：中小型專案推薦 Vite，需要 SSR 的選擇 Next.js，既有 CRA 專案無需急著遷移。

---

## 延伸閱讀

- [Vite 快速開始](https://www.google.com/search?q=Vite+React+quick+start+guide)
- [Next.js 文件](https://www.google.com/search?q=Next.js+documentation)
- [React 專案結構建議](https://www.google.com/search?q=React+project+structure+best+practices)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」精選文章之一。*
