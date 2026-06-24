# 開源社群與工具

## 2023 年開源生態系統回顧

2023 年，開源社群在 AI 浪潮中經歷了前所未有的變革。GitHub Copilot 重新定義了程式設計的方式，Hugging Face 成為 ML 的 GitHub，容器生態系統持續演進，開發者工具全面 AI 化。讓我們回顧這精彩的一年。

---

## GitHub Copilot 生態

### 從新奇到必需品

2023 年，GitHub Copilot 從一個有趣的實驗變成了開發者的標準配備：

**用戶成長**：從年初的約 100 萬付費用戶成長到年底的 180 萬用戶。超過 5 萬個企業組織使用了 Copilot for Business。

**Copilot Chat**：7 月進入公開預覽，12 月全面開放。開發者可以直接在 IDE 中與 AI 討論程式碼。

**Copilot Labs**：實驗性功能，包含語音程式設計、程式碼解釋器（結合 GPT-4）等。

### 效率提升

GitHub 發布的研究顯示：
- 使用 Copilot 的開發者完成任務的速度提高了 55%
- 開發者的工作滿意度顯著提升
- Copilot 在輔助而非取代人類開發者

### 競爭與多元

Amazon CodeWhisperer 在 4 月全面開放，對個人開發者免費。Tabnine、Replit Ghostwriter 等 AI 程式設計助手也獲得了市場份額。

---

## Hugging Face：ML 的 GitHub

### 平台成長

Hugging Face 在 2023 年經歷了爆炸性成長：

- **模型數量**：從年初的 15 萬增長到年底的 45 萬
- **資料集數量**：從 3 萬增長到 8 萬
- **估值**：在 8 月融資後達到 45 億美元

### 關鍵發布

**Hugging Chat**：開源的 ChatGPT 替代品，基於 Llama 2 和 Mistral 等模型。支援對話、Web 搜尋和網頁瀏覽。

**Transformers 4.31**：整合 Llama 2、Falcon、Mistral 等 30 多個新模型架構。

**Text Generation Inference（TGI）**：高效能 LLM 推理伺服器，支援自適應批處理、連續批處理和張量並行。

**SafeTensors**：新的模型權重格式，提供更快的載入速度和更高的安全性。

### 社群生態

Hugging Face 成為 AI 開發者的首選協作平台。Space（託管示範應用）、Hub（託管模型和資料集）和 Gradio（互動式示範）構成了一個完整的生態。

---

## Kubernetes 與雲端容器

### Kubernetes 邁入成熟期

Kubernetes 在 2023 年慶祝了其開源 9 週年，進入穩定的成熟階段：

**Kubernetes 1.27**（4 月）：冷卻/休眠狀態的 v1，更靈活的狀態集管理。

**Kubernetes 1.28**（8 月）：混合叢集的 API，更好的 sidecar 容器支援。

**Kubernetes 1.29**（12 月）：新的讀寫 API，最後的遺留元件移除。

### 容器生態演進

**Docker 爭議**：Docker 在 8 月宣布更改訂閱條款，引發了對 Docker 依賴的擔憂。Podman、Containerd 和 Finch 作為替代方案獲得關注。

**WASM 在 Kubernetes 中**：Krustlet 和 containerd-wasm-shim 讓 WebAssembly workload 可以在 Kubernetes 上執行，為邊緣運算和輕量級容器提供了新可能。

**eBPF 的崛起**：Cilium 成為主流的 Kubernetes CNI 插件，利用 eBPF 提供網路、安全和可觀測性功能。

---

## 開發者工具全面 AI 化

### 程式碼搜尋與理解

**Sourcegraph Cody**：基於 LLM 的程式碼搜尋和理解工具，支援整個程式碼庫的語意級別搜尋和問答。

**GitHub Copilot for Docs**：自動生成專案文件。

### 項目管理與協作

**Linear**：在 2023 年獲得大量關注，成為開發者偏好的專案管理工具。其整合 AI 的功能包括自動優先級分配和工單分類。

**Notion AI**：整合了寫作輔助和知識庫問答功能。

### 終端與 CLI

**Warp**：Rust 編寫的終端，內建 AI 命令搜尋功能。使用者可以用自然語言描述想要執行的操作。

**Fig**：命令列自動補全工具，整合 AI 來預測使用者意圖。

---

## 開源授權與商業模式

### 授權變化

**Redis**：在 6 月更改了授權，將模組從 BSL 改為 SSPL，引發了對資料庫開源未來的討論。

**HashiCorp**：在 8 月將 Terraform 從 MPL 更改為 BSL，導致社群分叉創立了 OpenTofu。

**Elastic**：在 5 月重新採用 AGPL 授權，結束了從開源到源可用的旅程。

### 商業模式探索

2023 年，開源公司繼續探索可持續的商業模式：
- **雲端託管**：提供託管版本
- **企業功能**：開源核心 + 付費附加功能
- **AI 服務**：基於開源模型的商業服務

---

## 延伸閱讀

- [GitHub Copilot 2023 回顧](https://www.google.com/search?q=GitHub+Copilot+2023+adoption+statistics)
- [Hugging Face 2023 年終總結](https://www.google.com/search?q=Hugging+Face+2023+year+in+review)
- [Kubernetes 1.29 發布說明](https://www.google.com/search?q=Kubernetes+1.29+release+notes+2023)
- [HashiCorp BSL 授權變更](https://www.google.com/search?q=HashiCorp+Terraform+BSL+license+change+2023)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」年度回顧系列之六。*
