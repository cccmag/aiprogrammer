# 現代前端工具鏈

## 開發環境的演進

前端開發工具鏈經歷了顯著的演進：

- **2010 年**：手動引入 CDN 腳本
- **2013 年**：Grunt、Gulp 任務自動化
- **2015 年**：Webpack 模組打包
- **2018 年**：Parcel 零配置打包
- **2020 年至今**：Vite 極速開發

## 建置工具：Vite vs Webpack

### Vite

Vite 由 Vue.js 作者尤雨溪開發，憑藉原生 ES Module 實現極速冷啟動：

```bash
npm create vite@latest my-app -- --template react
```

Vite 的開發伺服器不會打包整個應用，而是按需編譯。這意味著即使專案規模很大，冷啟動也能在瞬間完成。

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
})
```

### Webpack

Webpack 是一個功能強大的打包工具，擁有豐富的插件生態。雖然開發速度不如 Vite，但在複雜的企業級場景中仍有用武之地：

```javascript
// webpack.config.js
module.exports = {
  entry: './src/index.js',
  output: { path: 'dist', filename: 'bundle.js' },
  module: {
    rules: [
      { test: /\.jsx?$/, use: 'babel-loader' },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({ template: './index.html' })
  ]
}
```

## TypeScript 整合

TypeScript 為 JavaScript 增加了靜態型別，可以大幅減少執行時期錯誤：

```typescript
// React 元件加上型別
interface UserProps {
  id: number
  name: string
  email: string
  role: 'admin' | 'user'
}

function UserCard({ id, name, email, role }: UserProps) {
  return (
    <div className={`card role-${role}`}>
      <h3>{name}</h3>
      <p>{email}</p>
    </div>
  )
}
```

## Linting 與格式化

### ESLint

ESLint 是 JavaScript/TypeScript 的靜態分析工具，可以找出程式碼中的潛在問題：

```javascript
// eslint.config.js (Flat Config)
import js from '@eslint/js'
import reactRecommended from 'eslint-plugin-react/configs/recommended.js'

export default [
  js.configs.recommended,
  reactRecommended,
  {
    rules: {
      'react/jsx-uses-react': 'error',
      'no-unused-vars': 'warn',
      'react/prop-types': 'off',
    }
  }
]
```

ESLint 9.0 全面採用 Flat Config 格式，取代傳統的 `.eslintrc`。

### Prettier

Prettier 是一個自動化的程式碼格式化工具，確保團隊編碼風格一致：

```json
{
  "semi": false,
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100
}
```

## 測試工具鏈

現代前端測試有三層結構：

**單元測試（Vitest/Jest）**：測試個別元件或函式

```javascript
import { render, screen } from '@testing-library/react'
import { describe, it, expect } from 'vitest'
import Button from './Button'

describe('Button', () => {
  it('renders with label', () => {
    render(<Button label="Click" />)
    expect(screen.getByText('Click')).toBeDefined()
  })
})
```

**整合測試（Testing Library）**：測試元件互動

**E2E 測試（Playwright/Cypress）**：模擬使用者的完整操作流程

## 狀態管理工具

除了 React 內建的 Context API，社群提供了多種狀態管理方案：

- **Zustand**：輕量、簡潔，API 設計類似 Hooks
- **Jotai**：原子化狀態管理
- **Redux Toolkit**：Redux 的現代化封裝
- **Recoil**：Facebook 開發的實驗性方案

```javascript
import { create } from 'zustand'

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  reset: () => set({ count: 0 }),
}))
```

## CSS 解決方案

現代前端專案通常選擇以下 CSS 方案之一：

- **CSS Modules**：編譯時期自動產生的局部作用域 CSS
- **Tailwind CSS**：Utility-first CSS 框架，類別名稱即樣式
- **CSS-in-JS**：styled-components、Emotion
- **CSS Nesting**：原生 CSS 現在也支援巢狀語法

## 結語

現代前端工具鏈的核心目標是提升開發效率和程式碼品質。Vite 的極速體驗、TypeScript 的型別安全、ESLint 和 Prettier 的程式碼規範，以及完善的測試工具鏈，共同構成了專業前端開發的基礎設施。

---

## 延伸閱讀

- [Vite 官方文件](https://www.google.com/search?q=Vite+documentation)
- [TypeScript React 整合](https://www.google.com/search?q=TypeScript+React+setup)
- [現代前端工具鏈比較](https://www.google.com/search?q=modern+frontend+toolchain+comparison)

---

*本篇文章為「AI 程式人雜誌 2024 年 4 月號」焦點系列之七。*
