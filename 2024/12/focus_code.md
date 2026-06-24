# 焦點程式碼說明

## 年度回顧資料分析程式

本期焦點文章的資料分析由 `_code/year_review_2024.js` 腳本支援。該腳本使用 Node.js（版本 22+）執行，展示以下功能：

### 功能模組

1. **資料收集**：模擬從 npm、GitHub、State of JS 等來源獲取年度數據
2. **趨勢分析**：計算技術採用率、成長率與年度變化
3. **視覺化輸出**：以表格格式呈現分析結果
4. **互動式展示**：支援命令列引數來選擇分析類別

### 使用的 JavaScript 特性

- **ESM 模組**：使用 `import/export` 語法
- **Top-level await**：非同步資料載入
- **node:test**：內建測試支援
- **Map/Set/WeakRef**：現代資料結構
- **Temporal API**（實驗性）：日期時間處理

### 執行方式

```bash
cd _code
node year_review_2024.js
```

### 輸出格式

腳本會產生以下輸出：

1. 2024 年 JavaScript 生態成長統計
2. 前端框架採用率變化
3. 年度關鍵字頻率分析
4. 技術趨勢預測模型

### 程式碼結構

```
year_review_2024.js
├── class YearReviewData    — 資料收集與儲存
├── class TrendAnalyzer     — 趨勢計算引擎
├── class Report            — 格式化報表產生
├── function demo()         — 完整展示流程
└── function main()         — CLI 入口
```

每一篇焦點文章都引用此程式的部分輸出作為數據支援。

> 參考：https://www.google.com/search?q=JavaScript+data+analysis+2024
