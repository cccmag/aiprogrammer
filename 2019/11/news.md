# 本月新知

## 2019 年 11 月程式與 AI 技術動態

### 程式語言與框架

**Node.js 12 LTS 正式發布**

Node.js 12 於 2019 年 11 月正式進入長期支援（LTS），這是 Node.js 的重要里程碑。Node.js 12 帶來了多項改進：

- **V8 JavaScript 引擎升級至 7.6**：更快的字串操作和陣列處理
- **TLS 1.3 支援**：更安全的傳輸層加密
- **預設啟用 Worker Threads**：更好的多執行緒支援
- **診斷報告 API**：增強的除錯能力

**Deno 1.0 預覽版備受關注**

Ryan Dahl 在 2019 年 11 月發布了 Deno 1.0 的預覽版本。Deno 是 Node.js 的創造者離開 Google 後的新專案，旨在解決 Node.js 的一些設計缺陷：

- **原生支援 TypeScript**：無需額外編譯步驟
- **安全的沙箱執行**：預設不允許檔案、網路存取
- **去除了 node_modules**：使用 URL 載入依賴
- **統一的工具鏈**：內建測試、格式化、linting 工具

**React 16.13 發布**

Facebook 在 2019 年 11 月發布了 React 16.13，這是 Concurrent Mode 的進一步發展：

- **Suspense for Data Fetching**：穩定性改進
- **React.lazy 和 React.Suspense**：官方支援的程式碼分割
- **Concurrent Mode 準備**：為未來的並發渲染做準備

### AI 與機器學習

**GPT-2 完整版終於發布**

2019 年 11 月，OpenAI 正式發布了 GPT-2 的完整 1.5B 參數版本。這距離 2 月份的「部分發布」已經過去了約 9 個月。OpenAI 表示：

> 「經過仔細評估，我們認為沒有發現明顯的濫用證據，因此決定發布完整版本。」

**DeepMind 發布 AlphaFold 2 預告**

DeepMind 在 2019 年 11 月預告了 AlphaFold 2，這是蛋白質結構預測的重大突破。AlphaFold 在 CASP14 競賽中展現了前所未有的準確度。

**NVIDIA 發布 TensorFlow 2.0 優化**

NVIDIA 發布了針對 TensorFlow 2.0 的深度優化，包括：
- 混合精度訓練支援
- Multi-GPU 訓練效能提升
- Tensor Core 利用率優化

### 開發工具與雲端服務

**GitHub Actions 正式版上線**

GitHub Actions 在 2019 年 11 月正式脫離 Beta，成為 GitHub 的核心功能。開發者可以使用 YAML 定義自動化工作流程：

```yaml
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
```

**Visual Studio Online 發布**

微軟發布了 Visual Studio Online，這是一個雲端開發環境。支援多人即時協作、Git 整合和 AI 輔助程式設計。

### 業界動態

- **AWS re:Invent 2019**：亞馬遜發布多項雲端 AI 服務
- **Google Cloud Next**：Anthos 和 AI Platform 更新
- **阿里雲棧成都峰會**：中國雲端運算市場持續擴大
- **Ruby 2.7 發布**：引入 Pattern Matching

### 標準與規範

- **HTTP/3 RFC 草案**：QUIC 協定標準化接近完成
- **WebAssembly Core 規範 1.0**：正式版本即將發布
- **ES2020 提案**： BigInt 和 Dynamic Import 定稿

### 延伸閱讀

- [GPT-2+完整發布](https://www.google.com/search?q=OpenAI+GPT-2+full+release+November+2019)
- [Node.js+12+LTS](https://www.google.com/search?q=Node.js+12+LTS+November+2019)
- [Deno+1.0](https://www.google.com/search?q=Deno+1.0+preview+2019)