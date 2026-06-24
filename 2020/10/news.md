# 本月新知

## 2020 年 10 月程式與 AI 技術動態

### 程式語言與框架

**Python 3.9 正式發布**

Python 3.9 於 2020 年 10 月正式發布，這是 Python 語言的最新穩定版本。新版本帶來了多項重要新特性：字典合併運算子（`|`）、型別提示泛型、字串方法改進，以及效能提升。dict 合併變得前所未有的簡潔：`{**dict1, **dict2}` 現在可以寫成 `dict1 | dict2`。新增的 `str.removeprefix()` 和 `str.removesuffix()` 方法讓字串處理更直觀。Python 3.9 的 IPC（每秒鐘指令數）比 3.8 提升了約 15%。

**pip 20.2 發布：依賴解析大改進**

pip 20.2 帶來了全新的依賴解析器，這解決了長期以來 pip 在處理複雜依賴關係時的諸多問題。新解析器更嚴格、更快速，並提供了更清晰的錯誤訊息。對大型專案而言，這意味著 `pip install` 的結果更加可預測。pip 20.2  также引入了對 PEP 600 延伸架構的支援，強化了跨平台相容性。

**Django 3.1 發布**

Django 3.1 帶來了多項重要改進：非同步視圖支援（Async Views）正式進入核心、持續性連線支援、JSONField 的全面支援，以及 CSRF 保護的改进。對於需要構建即時應用的開發者來說，async views 的加入是一個重要的里程碑。現在可以直接使用 `async def` 定義視圖函數，並在 Django 中使用 asyncio。

**FastAPI 人氣急升**

FastAPI 在 2020 年的人氣持續飆升。這款現代化的 Python Web 框架結合了 Flask 的簡潔性和 Starlette 的功能集，並原生支援 Pydantic 資料驗證和自動 OpenAPI 文件生成。FastAPI 的效能接近 Node.js，顯著優於 Django 和 Flask。越來越多的 AI 應用選擇使用 FastAPI 作為 REST API 層。

### AI 與機器學習

**GPT-3 影響持續擴大**

2020 年是 GPT-3 爆發的一年。雖然 GPT-3 在 6 月就發布了，但到了 10 月，它的應用和影響正在全面展開。開發者社群開始探索 GPT-3 的各種應用場景：自動文案生成、程式碼輔助、對話系統、知識問答等。GPT-3 的 1750 億參數規模展示了超大語言模型的驚人能力，也引發了對通用人工智慧的討論。

**TensorFlow 2.3.2 穩定更新**

TensorFlow 持續快速迭代，2.3.2 是 2.3 系列的安全更新版本。TensorFlow Lite 在邊緣裝置上的部署能力持續增強，針對行動裝置和 IoT 的優化越來越成熟。TensorFlow Extended (TFX) 的 MLOps 功能也獲得了大幅改進，讓從訓練到部署的流程更加順暢。

**PyTorch 1.6 與 1.7 陸續發布**

PyTorch 在 2020 年發布了多個版本。1.6 版本引入了原生的 AMP（自動混合精度）支援，1.7 版本則帶來了更快的 RPC 基礎設施、torch.cuda.amp 改進，以及 Python 不足部分的除錯功能。PyTorch 的動態計算圖一直是研究者的最愛，而現在它的部署工具也越來越成熟。

**Hugging Face Transformers 勢不可擋**

Hugging Face 的 Transformers 庫在 2020 年成為 NLP 領域的標準工具。它提供了數千個預訓練模型，涵蓋了文字分類、命名實體識別、問答、摘要、翻譯等多種任務。BERT、GPT-2、RoBERTa、T5 等模型都可以透過一行程式碼呼叫。Transformers 庫的出現大幅降低了 NLP 應用的開發門檻。

### 開發工具與雲端服務

**GitHub CLI 1.0 正式發布**

GitHub CLI 是 GitHub 官方推出的命令列工具，2020 年 10 月發布了 1.0 正式版本。開發者可以直接在終端機中完成 PR 建立、分支管理、Issue 操作、Gist 管理等工作。GitHub CLI 大幅提升了開發者的工作效率，特別是對於習慣使用命令列的開發者而言。

**VS Code 2020 年 10 月更新**

VS Code 持續更新，10 月版本帶來了多項改進：改進的語法反白顯示、更好的 Python 偵錯支援、更快的啟動時間，以及新的「Profiles」功能。VS Code 的 Python 擴展也獲得了更新，現在可以更好地處理大型 Python 專案。

**Docker Desktop for Apple Silicon 預覽版**

隨著 Apple Silicon (M1) 晶片的發布，Docker 推出了針對 ARM 架構的預覽版本。這讓開發者可以在新的 Mac 上原生執行 Docker 容器，雖然目前還有一些相容性問題，但整體效能表現令人期待。

### 業界動態

- **Python 蟬聯 GitHub 最受歡迎語言**：根據 GitHub 的年度調查，Python 在 2020 年正式超越 JavaScript，成為 GitHub 上使用最多的語言
- **AWS 發布 Lambda 容器支援**：AWS Lambda 現在支援容器映像，這讓 Python 部署有了更多選擇
- **Google 發布 Cloud Run GA 版本**：Google Cloud Run 的正式版發布，提供了更簡單的無伺服器容器部署體驗
- **GitHub 活躍用戶突破 5000 萬**：GitHub 在 2020 年達到了另一個重要里程碑

### 標準與規範

- **PEP 604 聯合類型語法**：Python 3.10 將引入的 `int | str` 類型語法在 2020 年獲得廣泛討論
- **PEP 517/518 建構系統標準**：越來越多的 Python 專案採用 pyproject.toml 進行建構配置
- **PEP 508 依賴規範更新**：新的環境標記和依賴規範進一步改善了跨平台相容性