# 本月新知

## 2023 年 12 月程式與 AI 技術動態

### 年度回顧與重大發布

**Gemini 1.0 發布**

Google 於 12 月 6 日正式發布 Gemini 1.0，這是 Google 迄今為止最大、能力最強的多模態 AI 模型。Gemini 分為 Ultra、Pro 和 Nano 三個版本，分別針對複雜任務、通用場景和裝置端應用。Gemini Ultra 在多項基準測試中超越 GPT-4，特別是在 MMLU（大規模多任務語言理解）測試中達到 90.0% 的準確率。然而，發布過程中的展示影片爭議也引發了對 AI 行銷誠信的討論。

**Mistral 7B 開源引發轟動**

法國 AI 新創公司 Mistral AI 於 12 月發布 Mistral 7B，一個僅 70 億參數但效能卓越的開源模型。Mistral 7B 在各種基準測試中超越了 Llama 2 13B 和 LLaMA 1 34B，展示了小模型也能有大成就。該模型採用 Apache 2.0 授權，發布後迅速成為開源 AI 社群的焦點。

**GitHub Copilot Chat 全面開放**

GitHub 於 12 月宣布 Copilot Chat 正式全面開放，不再需要等待名單。開發者可以在 Visual Studio 和 VS Code 中直接與 AI 助手討論程式碼，進行除錯、重構和解釋，極大提升了開發效率。此舉標誌著 AI 輔助程式設計從實驗階段進入主流。

### 開發工具與平台更新

**PyTorch 2.1 穩定版發布**

PyTorch 團隊於 12 月發布 2.1 穩定版，帶來了 torch.compile 的效能改進、更好的 Transformer 支援，以及對 Apple Silicon GPU 的原生加速。這使得 PyTorch 在研究和生產環境中的適用性進一步提升。

**Amazon Q 登場**

AWS 於 12 月 re:Invent 大會上發布 Amazon Q，一個為企業打造的 AI 助手。Amazon Q 可以連接企業知識庫、程式碼倉庫和 AWS 環境，提供開發和營運支援，直接與 GitHub Copilot 和 ChatGPT Enterprise 競爭。

**Apple 發布 MLX 框架**

Apple 於 12 月開源 MLX，一個專為 Apple Silicon 設計的機器學習框架。MLX 充分利用統一記憶體架構，提供類似 NumPy 的 API，為 Mac 上的 AI 開發開啟了新可能。

### 硬體與晶片

**NVIDIA H200 發布**

NVIDIA 於 11 月宣布 H200 Tensor Core GPU，這是 H100 的升級版，配備 141GB HBM3e 記憶體，頻寬達 4.8TB/s。H200 完全相容 H100 軟體棧，成為 LLM 訓練和推理的首選硬體。

**AMD MI300X 挑戰 NVIDIA**

AMD 於 12 月發布 Instinct MI300X，配備 192GB HBM3 記憶體和 5.2TB/s 頻寬，在 LLM 推理效能上與 H100 相當。MI300X 的推出為 AI 硬體市場帶來了急需的競爭。

### 開源社群

**Linux 6.7 引入重大變更**

Linus Torvalds 於 12 月發布 Linux 6.7，引入了新的 BCachefs 檔案系統、改進的 NUMA 平衡，以及更多的 Rust 語言核心元件。Rust 進入 Linux 核心的進程持續推進。

**Docker 的 Containerd 獨立**

Containerd 專案在 12 月宣布從 Docker 完全獨立，成為 CNCF 頂級專案。這反映了容器生態系統的成熟和標準化。

### 法規與政策

**歐盟 AI 法案達成政治協議**

歐洲議會和理事會於 12 月 8 日就 AI 法案達成歷史性政治協議。這是全球首個全面的 AI 監管框架，根據風險等級對 AI 系統進行分類監管。此舉對全球 AI 治理產生了深遠影響。

**美國 AI 行政命令**

美國總統拜登於 10 月簽署 AI 行政命令，要求 AI 開發者進行安全測試、制定 AI 安全標準，並保護隱私。行政命令雖然不具立法效力，但為後續的 AI 政策奠定了基礎。

### 產業動態

- **Sam Altman 被 OpenAI 解僱又復職**：11 月的戲劇性事件震驚業界，Altman 被董事會解僱後在員工壓力下迅速復職，凸顯了 AI 治理的複雜性。
- **Microsoft 延攬 Sam Altman 未果**：Microsoft CEO Satya Nadella 在 Altman 被解僱後迅速提出聘請，但最終 Altman 回到 OpenAI。
- **Character.AI 推出角色對話模型**：Character.AI 在 12 月推出新的角色扮演對話模型，月活躍用戶突破 2000 萬。
- **Stability AI 陷入財務困境**：Stability AI 在 12 月傳出資金短缺，CEO 離職，引發對開源 AI 商業模式的反思。

### 標準與規範

- **W3C 發布 WebGPU 標準**：為 Web 高效能圖形和運算帶來新時代
- **ECMAScript 2024 草案新增 Promise.withResolvers**：簡化非同步程式設計
- **C23 標準正式發布**：C 語言時隔十年迎來重大更新
