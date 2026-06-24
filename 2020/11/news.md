# 本月新知

## 2020 年 11 月程式與 AI 技術動態

### 程式語言與框架

**Python 3.9.1 發布**

Python 3.9.1 於 2020 年 11 月發布，這是 3.9 系列的首個 bug 修復版本，修復了多個重要問題。新字典合併運算子（`|`）和字串方法增強讓 Python 3.9 成為迄今為止最快的 Python 版本之一。社群開始討論 Python 3.10 將引入的 match-case 語法，這是 Python 的一次重大語法擴展。

**Deno 1.6 發布**

Deno 是 Node.js 的替代品，由 Node.js 創始人 Ryan Dahl 開發。1.6 版本增加了原生編譯支援，可以將 TypeScript/JavaScript 編譯成單一的可執行檔案。這讓 Deno 應用的部署變得前所未有的簡單。

**TypeScript 4.1 發布**

TypeScript 4.1 帶來了多項重要改進：Template Literal Types 讓型別系統更加強大，Key Remapping in Mapped Types 簡化了複雜的型別操作，而 Path Mapping 不再需要 baseUrl。這些改進讓 TypeScript 繼續在型別安全領域保持領先。

### AI 與機器學習

**AlphaFold2 在 CASP14 取得突破性成功**

這是 2020 年 11 月最重要的 AI 事件。DeepMind 的 AlphaFold2 在 CASP14（蛋白質結構預測關鍵評估）競賽中達到了實驗級精度，這解決了困擾生物學家 50 年的蛋白質折疊問題。AlphaFold2 的 GDT 分數達到 92.4，超過了大多數人類專家團隊的平均水平。這一突破對藥物開發、疾病研究等領域具有深遠影響。

**OpenAI 開放 GPT-3 API**

GPT-3 於 2020 年 6 月發布後，OpenAI 終於在 2020 年 11 月開始向特定合作夥伴開放 API。開發者可以透過 API 使用 GPT-3 的強大語言能力，這開創了 AI 即服務的新商業模式。各類基於 GPT-3 的應用開始出現，包括文案生成、程式碼輔助、對話系統等。

**Hugging Face 估值超過 10 億美元**

Hugging Face 的 Transformers 庫已成為 NLP 領域的標準工具。2020 年 11 月，公司完成了新一輪融資，估值超過 10 億美元，成為 AI 領域的新獨角獸。這標誌著 AI 基礎設施公司的崛起。

**NVIDIA 發布 AI 處理器路線圖**

NVIDIA 在 2020 年底的投資者日公布了雄心勃勃的 AI 處理器路線圖。下一代 Hopper 架構預計在 2021 年推出，將提供比當前 Ampere 架構更大的效能提升。這對 AI 訓練和推理都是好消息。

### 分散式系統

**Apache Kafka 2.7 發布**

Kafka 是分散式訊息佇列的事實標準。2.7 版本增強了 KRaft（Kafka 的 Raft 共識實現），為 Kafka 擺脫對 ZooKeeper 的依賴邁出了重要一步。Kafka 的這種演進代表著分散式系統簡化的趨勢。

**TiDB 4.0 GA 版本發布**

TiDB 是 PingCAP 開發的分散式 NewSQL 資料庫。4.0 版本引入了 TiFlash（分析引擎）、更強大的分散式 SQL，以及顯著的性能提升。TiDB 正在成為大型網路公司首選的分散式資料庫解決方案。

**etcd 3.5 發布**

etcd 是 Kubernetes 的關鍵元件，儲存著叢集的所有狀態。3.5 版本帶來了效能優化和錯誤修復，增強了 Kubernetes 控制平面的穩定性。

### 開發工具與雲端服務

**GitHub 活躍用戶達到 5000 萬**

GitHub 在 2020 年達到了另一個重要里程碑——活躍用戶突破 5000 萬。這反映了開源軟體的持續繁榮和分散式開發的普及。GitHub Codespaces 也在 2020 年進入 beta 測試，讓開發者可以直接在瀏覽器中開發程式碼。

**AWS 發布新 AI 服務**

AWS 在 re:Invent 大會上發布了多項新服務，包括 Amazon SageMaker Canvas（無需程式碼的 ML 工具）和增強的 AI 服務。這些服務讓企業能夠更輕鬆地使用 AI 技術。

### 業界動態

- **雲端市場持續增長**：2020 年雲端市場規模超過 3000 億美元
- **遠距工作常態化**：DevOps 工具和 CI/CD 平台需求大增
- **開源硬體興起**：RISC-V 架構獲得更多關注
- **量子計算進展**：Google 和 IBM 在量子錯誤更正方面取得進展

### 標準與規範

- **QUIC 協議標準化進行中**：HTTP/3 的底層傳輸協議即將完成標準化
- **WebAssembly 持續演化**：WASI 標準為 WebAssembly 打開了更多應用場景
- **Async Rust 發展**：async/await 語法在 Rust 中越來越穩定