# 本月新知

## 2026 年 4 月程式與 AI 技術動態

### 資料科學工具更新

**Pandas 3.0 正式發布**

Pandas 團隊於本月發布 Pandas 3.0 正式版本。這是繼 Pandas 2.0 多年後最重要的更新，引入了全新的「惰性 DataFrame」概念，允許使用者建構一個運算圖，最後再統一執行。新版本也強化了對 Apache Arrow 的原生支援，記憶體效率大幅提升。此外，`groupby` 操作在底層使用了多執行緒進行最佳化，大規模資料集上的效能提升高達 5 倍。

**NumPy 2.1 推出**

NumPy 團隊發布 2.1 版本，著重於改善陣列運算的效能與彈性。新版本引入了實驗性的「可變長度陣列」支援，以及在 Intel CPU 上自動啟用 AVX-512 指令集加速。`np.linalg` 模組中的矩陣運算也經過最佳化，大型矩陣乘法速度提升約 30%。

**Matplotlib 4.0 進入 Beta**

Matplotlib 4.0 進入公測階段，帶來全新的預設主題和對 GPU 加速的實驗性支援。新預設主題改善了色彩對比度與可讀性，特別是在暗色模式下。`plt.subplots` 的 API 也變得更加直覺，支援巢狀佈局（nested layout）的聲明式語法。

### AI 與機器學習

**Scikit-learn 2.0 發布**

Scikit-learn 2.0 正式發布，這是該專案自 2007 年以來的最大版本更新。新版本原生整合了 GPU 加速（透過 CuPy 後端），支援大規模資料集的隨機森林和 SVM 訓練。此外，新加入了自動化特徵工程模組 `sklearn.feature_engineering`，提供自動特徵生成、選擇與交叉驗證的管線整合。

**JupyterLab 5.0 登場**

JupyterLab 5.0 帶來了全新的「即時協作」功能，類似於 Google Docs 的多人即時編輯體驗。新版本也整合了 AI 輔助程式碼生成功能，使用者在 Notebook 中可以直接透過快捷鍵呼出 AI 助手，無需離開編輯環境。

**Deepnote 推出免費方案**

雲端資料科學平台 Deepnote 宣布推出功能豐富的免費方案，支援 GPU 執行個體、協作編輯和自動化排程。這為個人開發者和學生提供了強大的雲端資料科學環境。

### 資料庫與資料工程

**DuckDB 2.0 發布**

嵌入式 OLAP 資料庫 DuckDB 發布 2.0 版本，重點強化了與 Pandas 的整合。使用者可以直接將 Pandas DataFrame 傳遞給 DuckDB 執行 SQL 查詢，利用 DuckDB 的 MPP 架構加速複雜的聚合運算。效能測試顯示，對 1 億筆資料進行 groupby 操作時，DuckDB 比原生 Pandas 快 10 倍以上。

**Apache Arrow 20.0 發布**

Apache Arrow 20.0 引入了「零拷貝序列化」的重大改進，使得不同程式語言（Python、R、Java、C++）之間的資料交換幾乎無開銷。這對多語言資料管線開發具有里程碑意義。

**Delta Lake 4.0 新增即時串流支援**

Delta Lake 4.0 加入了原生的即時串流支援，讓使用者可以在同一個資料湖上同時執行批次和串流工作負載。

### 業界動態

- **Gradio 5.0 發布**：機器學習演示框架 Gradio 發布第 5 版，支援更複雜的多步驟互動式應用
- **Streamlit 2.0 進入測試**：資料應用框架 Streamlit 大改版，支援多頁面應用的聲明式路由
- **Hugging Face Datasets 3.0**：整合 Arrow 後端，資料加載速度提升 5 倍
- **Google 發布 BigQuery Studio**：統一資料分析與機器學習開發環境
- **Databricks 收購 MosaicML**：強化開源 LLM 微調平台與資料湖倉生態整合

### 標準與規範

- **OpenTelemetry 資料管線追蹤規範發布**：為資料工程提供標準化觀測能力
- **W3C 發布 WebDataset 標準草案**：定義瀏覽器中處理大規模資料集的 API
