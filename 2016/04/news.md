# 本月新知

## 2016 年 4 月程式與 AI 技術動態

### 程式語言與框架

**Scala 2.12 開發中：全面支援 Java 8**

Typesafe 團隊在 2016 年持續推進 Scala 2.12 的開發。該版本將全面支援 Java 8 的函式式特性，包括 lambda 表達式和 Stream API。Scala 2.12 採用新的編譯器前端基於 Dotty（未來的 Scala 3.0 基礎），大幅提升編譯速度。社群對即時編譯（JIT）和垃圾回收的優化充滿期待。

**Clojure 1.8 發布：網路與效能強化**

Clojure 1.8 於 2016 年 1 月發布，持續最佳化網路程式設計能力。新增的 `clojure.core.match` 增強了模式匹配功能，`clojure.data.xml` 獲得效能改進。Clojure 在分散式系統和大資料處理領域持續保持優勢，許多金融機構採用 Clojure 建構高效能交易系統。

**Haskell 平台 7.10 邁向現代化**

Haskell Platform 7.10 帶來 GHC 7.10，提供更完善的類型類別（Type Classes）和更強大的 Template Haskell。Haskell 在形式驗證、編譯器設計和學術研究領域保持領先地位。Stack 工具鏈的成熟使得 Haskell 專案的依賴管理更加可靠。

**Rust 1.7 穩定版發布**

Rust 語言持續快速迭代，1.7 版本強化了原生 URL 解析和密碼學函式庫。Rust 的記憶體安全特性吸引越來越多系統程式設計師的注意。 Rust 核心團隊在 2016 年開始規劃 2018 年的 Edition 特性集合。

**Swift 2.2 發布：開放原始碼後的快步發展**

Apple 在 2015 年底開源 Swift 後，社群活躍度大增。Swift 2.2 加入了關鍵字抽取（Keyword Extraction）和更多平台支援。Swift 的函式式特性（map、filter、reduce）使其成為學習函式式程式設計的良好語言。

### JavaScript 與前端技術

**React 15.0 發布：Virtual DOM 持續最佳化**

Facebook 在 2016 年 4 月發布 React 15.0（實際為 2016 年 4 月的 15.0.0 版本），大幅改進伺服器端轉譯（Server-Side Rendering）。React 的元件化架構和宣告式 UI 設計深刻影響了現代前端開發。Redux 作為狀態管理方案獲得廣泛採用，函式式 Redux 結合 React 掀起前端革命。

**Angular 2 Beta 發布：全面改寫的框架**

Angular 2 在 2016 年初進入 Beta 階段，採用 TypeScript 開發，完全重寫架構。依賴注入、模組化和元件化是 Angular 2 的核心概念。 Angular 的改變顯示函式式和反應式程式設計在前端領域的影響力。

**Redux 興起：函式式狀態管理**

Redux 在 2016 年成為 React 生態中最受歡迎的狀態管理庫。Redux 採用純函式 reducer 和不可變狀態樹，完美體現函式式程式設計原則。時間旅行調試（Time Travel Debugging）和熱模組替換（Hot Module Replacement）展現了函式式架構的強大之處。

### AI 與機器學習

**Google DeepMind AlphaGo 擊敗李世乭**

2016 年 3 月，Google DeepMind 的 AlphaGo 在圍棋比賽中以 4:1 擊敗韓國九段棋手李世乭，引發全球 AI 熱潮。AlphaGo 使用深度卷積神經網路和蒙特卡羅樹搜尋，展現強化學習的驚人潛力。這場世紀對決讓 AI 從學術界走向大眾視野。

**TensorFlow 1.0 發布：機器學習框架成熟**

Google 在 2016 年 2 月發布 TensorFlow 1.0，標誌著這個開源機器學習框架的成熟。TensorFlow 的計算圖（Computation Graph）模型體現了函式式程式設計的思想。TensorFlow Serving 和 TensorBoard 等工具鏈的完善，使得大規模機器學習部署變得更加容易。

**Facebook FBLearner Flow：內部 ML 平台**

Facebook 公開其內部機器學習平台 FBLearner Flow，展示如何在實際產品中部署 ML 模型。該平台利用函式式程式設計理念，實現了高度模組化和可擴展的 ML 工作流程。

**PyTorch 興起：動態計算圖的優勢**

PyTorch 在 2016 年下半年持續發展，採用動態計算圖（Define-by-Run）設計。相較於 TensorFlow 的靜態圖，PyTorch 的命令式編程風格更符合 Python 程式設計師的習慣。PyTorch 的 autograd 系統自動計算梯度，體現了函式式微分的精神。

### 雲端與分散式系統

**Docker 1.11 發布：containerd 獨立**

Docker 在 2016 年持續進化，1.11 版本將 containerd 拆分為獨立專案。容器化技術使得函式式部署和微服務架構更加普及。AWS、Azure 和 Google Cloud 都加強了對 Kubernetes 的支援。

**Spark 2.0 開發中：DataFrame API 成熟**

Apache Spark 在 2016 年持續發展，DataFrame API 成為大資料處理的主流介面。Spark 的函式式 API（map、filter、reduce）使得分散式運算更加直覺。Spark Streaming 的出現開啟了即時大資料處理的新時代。

### 業界動態

- **蘋果收購 Turi**：強化機器學習能力
- **Google DeepMind 與 NHS 合作**：將 AI 應用於醫療領域
- **Microsoft 收購 Linkedin**：企業社交與資料整合
- **IBM Watson 商業化加速**：認知計算進入企業市場

### 標準與規範

- **ECMAScript 2016（ES7）發布**：加入指數運算子和 Array.prototype.includes
- **WebAssembly MVP 完成**：瀏覽器原生二進位格式就緒
- **HTTP/2 全面普及**：效能最佳化成為標準