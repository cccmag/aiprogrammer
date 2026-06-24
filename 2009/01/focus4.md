# npm 的起源：套件管理工具的誕生

## 前言

npm（Node Package Manager）是世界上最大的軟體註冊中心，但在 2009 年初，它還不存在。本章將回顧 npm 誕生之前，Node.js 社群如何分享和管理程式碼。

## 2009 年的模組管理困境

在 npm 出現之前，分享 Node.js 模組是一件困難的事：

```
2009 年的模組分享方式：
─────────────────────────
1. GitHub 原始碼仓库
2. 手動下載 .js 文件
3. 複製貼上程式碼
4. 論壇和郵件列表分享

問題：
─────────────────────────
- 依賴地獄：手動管理依賴關係
- 版本混亂：沒有標準化版本控制
- 安裝繁瑣：每個專案都要手動配置
- 更新困難：沒有統一的更新機制
```

## npm 的誕生

npm 是由 Isaac Z. Schlueter 在 2010 年創造的。雖然本期主題是 2009 年，但了解 npm 的起源有助於理解 Node.js 生態系的演進。

### npm 的核心設計

```javascript
// npm 的核心概念
{
  "name": "my-package",
  "version": "1.0.0",
  "description": "我的套件",
  "main": "index.js",
  "dependencies": {
    "express": "^4.0.0"
  },
  "devDependencies": {
    "mocha": "^2.0.0"
  }
}
```

### package.json 的重要性

```javascript
// package.json 定義了套件的元資料
// 讓其他開發者知道：
// 1. 套件名稱和版本
// 2. 如何使用這個套件
// 3. 這個套件依賴什麼
```

## 2009 年的替代方案

在 npm 出現之前，有幾種替代方案：

### 1. Git Submodules

```bash
# 將他人倉庫作為子模組加入
git submodule add git://github.com/user/lib.git lib
```

### 2. 手動路徑配置

```javascript
// 在程式碼中手動指定路徑
const myModule = require('./local_modules/my-module');
```

### 3. 論壇分享

開發者會在 Node.js 的 Google Group 或 GitHub 上分享程式碼，其他人需要手動下載。

## CommonJS 模組規範的影響

在 2009 年，CommonJS 規範已經為 npm 的出現奠定了基礎：

```
CommonJS 規範確定的標準：
─────────────────────────
1. require() 語法
2. module.exports 導出
3. 模組解析規則
4. package.json 約定

這些標準使得：
─────────────────────────
- 任何人都可以發布模組
- 任何人，都可以安裝模組
- 自動化工具（如 npm）可以運作
```

## 早期 Node.js 模組示例

假設在 2009 年要發布一個名為 `hello` 的簡單模組：

```javascript
// hello.js
module.exports = {
  greet: function(name) {
    return 'Hello, ' + name + '!';
  }
};
```

```javascript
// 使用方式（2009 年，需要手動複製檔案）
const hello = require('./hello');
console.log(hello.greet('World'));
```

## npm 出現後的改變

npm 在 2010 年 10 月首次發布後，Node.js 生態系開始爆發式增長：

```
npm 帶來的改變：
────────────────
之前（2009）：
  - 手動下載模組
  - 手動管理依賴
  - 安裝一個模組需要 5 分鐘

之後（2011+）：
  - npm install <package>
  - 自動處理依賴
  - 安裝一個模組只需 10 秒
```

## npm 的設計哲學

npm 的設計受到 Unix 哲學的影響：

```
npm 的設計原則：
────────────────
1. 越小越好：每個套件做一件事
2. 組合大于內建：提供基礎功能，讓開發者組合
3. 信任：每個人都可以發布
4. 去中心化：沒有中央伺服器，所有人都是貢獻者
```

## 套件生態的爆炸增長

```
npm 註冊中心統計：
───────────────────
2010 年：0 個套件
2011 年：100 個套件
2012 年：1,000 個套件
2013 年：10,000 個套件
2014 年：50,000 個套件
2015 年：150,000 個套件

現在（諧音 2026）：
  超過 2,000,000 個套件
```

## 結語

雖然 npm 在 2009 年還不存在，但了解它的起源幫助我們理解 Node.js 生態系的演進。在沒有 npm 的年代，分享和管理 Node.js 程式碼是困難的；npm 的出現徹底改變了這一切。

Node.js 社群等待一個好的套件管理工具的時間不長，這預示著這個工具將會非常重要。

---

## 延伸閱讀

- [npm 創建歷史](https://www.google.com/search?q=npm+history+creation+2010)
- [Isaac Schlueter 專訪](https://www.google.com/search?q=Isaac+Schlueter+npm+interview)
- [Node.js 早期歷史](https://www.google.com/search?q=Node.js+early+history)

---

*本篇文章為「AI 程式人雜誌 2009 年 1 月號」歷史回顧系列之一。*