# 本期焦點

## React 與現代前端框架的發展歷程

### 引言

在過去十年間，前端開發經歷了翻天覆地的變化。從早期的 jQuery 操作 DOM，到 AngularJS 的雙向綁定，再到 React 的虛擬 DOM 和元件化架構，前端框架不斷推動著 Web 開發的邊界。

本期雜誌將深度探討 React 這個改變前端世界的重要框架，從核心概念到實戰技巧，從基礎的元件化思想到前沿的工具鏈，為讀者呈現一幅完整的現代前端開發圖景。

---

## 大綱

* [程式：React 模擬實作](focus_code.md)
   - Virtual DOM 實作
   - State 與 Hooks 模擬
   - 元件渲染機制
   - Diff 演算法
* [程式碼下載](_code/)

1. [前端框架演進](focus1.md)
   - 靜態網頁時代
   - jQuery 與 DOM 操作
   - MVC/MVVM 的興起
   - React 的誕生
   - 現代多元生態

2. [React 核心概念：元件與 JSX](focus2.md)
   - 元件化思想
   - JSX 語法基礎
   - 宣告式 UI
   - 單向資料流

3. [狀態管理：useState](focus3.md)
   - React 的狀態哲學
   - useState 的使用
   - 狀態的非同步更新
   - 不可變性原則

4. [副作用與 useEffect](focus4.md)
   - 什麼是副作用
   - useEffect 的生命週期
   - 依賴陣列機制
   - 清理函式

5. [元件間通訊：props 與 context](focus5.md)
   - Props 的單向資料流
   - Props drilling 問題
   - Context API 解決方案
   - 組合 vs 繼承

6. [React Router 與 SPA](focus6.md)
   - SPA 的概念
   - React Router 基礎
   - 巢狀路由
   - 路由守衛

7. [現代前端工具鏈](focus7.md)
   - Vite vs Webpack
   - TypeScript 整合
   - Linting 與格式化
   - 測試框架

---

## 濃縮回顧

### 前端框架的演進

前端開發的歷史是一部從混亂走向秩序的演進史。2006 年 jQuery 的出現簡化了 DOM 操作，2010 年 Backbone.js 引入了 MVC 模式，2013 年 React 的誕生徹底改變了遊戲規則。

React 的創新在於提出了「虛擬 DOM」和「宣告式 UI」的概念。開發者不再需要手動操作 DOM，而是聲明元件在不同狀態下應該呈現什麼樣子，React 負責將 UI 與狀態同步。

### React 的核心思想

React 的核心哲學可以歸納為以下幾點：

- **元件化**：將 UI 拆解為獨立、可復用的小部件
- **宣告式**：描述 UI 應該是什麼樣子，而非如何達到
- **單向資料流**：資料從父元件流向子元件
- **不可變性**：狀態不直接修改，而是取代

### 從 class 到 function

2018 年 React 16.8 引入 Hooks，從此函式元件取代類別元件成為主流。useState、useEffect 等 Hooks 讓函式元件也能擁有狀態和副作用處理能力，程式碼變得更加簡潔和可測試。

### 現代前端生態

如今的前端生態豐富多元。React 仍是市場佔有率最高的框架，Vue 和 Angular 各有擁護者，而 Svelte 和 Solid.js 等新秀正在挑戰既有的設計理念。

---

## 結論與展望

React 自 2013 年誕生至今，已成為前端開發領域不可忽視的力量。從 React 19 的 Server Components 到各種新興框架的競爭，前端開發的未來將更加多元和精彩。

---

## 延伸閱讀

- [前端框架演進](focus1.md)
- [React 核心概念](focus2.md)
- [useState 狀態管理](focus3.md)
- [useEffect 副作用](focus4.md)
- [元件通訊](focus5.md)
- [React Router](focus6.md)
- [工具鏈](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
