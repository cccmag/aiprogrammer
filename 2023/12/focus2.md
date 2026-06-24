# 機器學習與 AI 突破

## 2023 年機器學習領域全景回顧

2023 年是機器學習領域百花齊放的一年。這一年，大型語言模型（LLM）從研究工具走向大眾應用，開源模型開始挑戰封閉巨頭，多模態和 AI Agent 開啟了新的技術方向。讓我們深入回顧這些重大突破。

---

## LLM 架構演進

### Transformer 的統治地位

2023 年，Transformer 架構繼續主導自然語言處理。主要的進展包括：

**混合專家模型（MoE）**：Mixtral 8x7B 展示了 MoE 架構的潛力，透過稀疏啟動的方式，在保持推理效率的同時大幅增加模型容量。每個 token 只啟動 2 個專家，但總體參數達到 47B。

**長上下文擴展**：從 GPT-4 的 32K，到 GPT-4 Turbo 的 128K，再到 Claude 2 的 100K token，模型能夠處理的上下文長度在一年內成長了數倍。Ring Attention、FlashAttention-2 等技術為長上下文提供了高效實現。

**對齊技術進步**：RLHF（基於人類回饋的強化學習）在 2023 年得到廣泛採用。OpenAI 提出的 InstructGPT 方法成為標準，Constitutional AI、DPO（直接偏好最佳化）等新方法也展現了潛力。

### 關鍵論文

- **LLaMA：Open and Efficient Foundation Language Models**（Meta，2 月）：展示了小模型配合高品質資料也能達到卓越效能。
- **QLoRA: Efficient Finetuning of Quantized Language Models**（華盛頓大學，5 月）：讓 65B 模型的微調可以在單張 GPU 上完成。
- **Efficient Memory Management for Large Language Model Serving with PagedAttention**（UC Berkeley，9 月）：vLLM 的核心技術，大幅提升 LLM 推理效率。

---

## 開源模型的崛起

### 從 LLaMA 到 Llama 2

**2 月**：Meta 發布 LLaMA，雖然只有研究許可，但模型權重在學術界被廣泛共享。LLaMA 7B 在推理任務上超越 GPT-3 175B，引發了開源 LLM 的熱潮。

**7 月**：Meta 發布 Llama 2，這是首個免費商業可用的大型開源模型。Llama 2 70B 在許多基準測試中接近 GPT-3.5 的水準。其商業許可引起廣泛討論，也奠定了 Llama 生態系統的基礎。

### Mistral 的驚喜

**9 月**：法國新創 Mistral AI 發布 Mistral 7B，僅 70 億參數但效能超越 Llama 2 13B。Mistral 採用 Apache 2.0 許可，完全開源。

**12 月**：Mistral 發布 Mixtral 8x7B，這是首個廣受關注的開源 MoE 模型，效能接近 GPT-3.5。

### 開源生態的繁榮

Hugging Face 上的模型數量從年初的 15 萬個成長到年底的 45 萬個。開源模型的品質提升速度令人驚嘆，到年底，開源社群已經擁有了一系列接近 GPT-3.5 水準的模型。

---

## AI Agent 的萌芽

2023 年是 AI Agent 元年的開端。雖然概念已經存在多年，但 LLM 的推理能力讓 Agent 真正變得實用。

### 重要框架

**AutoGPT**（3 月）：首個引起廣泛關注的自主 AI Agent 框架，可以將複雜任務分解為子任務並逐步執行。

**LangChain**（年初開始流行）：提供了 LLM 應用開發的模組化框架，包含鏈、記憶、工具調用等抽象。到年底成為最受歡迎的 LLM 框架。

**ChatGPT Plugins**（5 月）：OpenAI 推出的外掛系統讓 ChatGPT 能夠瀏覽網頁、執行代碼、調用第三方服務。

### 評估與挑戰

AI Agent 面臨的主要挑戰包括：
- **可靠性**：Agent 的任務完成率仍然不夠穩定
- **安全性**：自主執行可能帶來安全風險
- **成本**：長時間運行的 Agent 會消耗大量 token

---

## 多模態與基礎模型

### 從文字到多模態

2023 年見證了 AI 模型從純文字向多模態的全面轉變：

**GPT-4V**（視覺）：理解圖像內容、閱讀圖表、辨識螢幕截圖。

**DALL-E 3**（9 月）：整合 ChatGPT 的提示詞優化，生成更符合描述的圖像。

**Meta 的 ImageBind**：將六種模態（文字、圖像、影片、音頻、深度、溫度）統一到同一嵌入空間。

### 基礎模型的邊界擴展

**程式碼模型**：Code Llama、StarCoder、CodeGen 等專注於程式碼生成的模型在 2023 年大量出現。GitHub Copilot 和 Amazon CodeWhisperer 將程式碼生成能力直接整合到 IDE 中。

**科學模型**：AlphaFold 的成功激勵了更多科學領域的應用。從蛋白質到材料，從氣候到天文，基礎模型的應用範圍不斷擴展。

**影片生成**：Runway Gen-2、Pika Labs、Stable Video Diffusion 等影片生成模型在年底嶄露頭角。

---

## 訓練與推理技術

**分散式訓練**：FSDP、DeepSpeed ZeRO-3、ColossalAI 等框架大幅降低了大型模型訓練的門檻。

**推理優化**：vLLM、TensorRT-LLM、llama.cpp 等工具讓 LLM 推理變得更加高效。量化技術（GPTQ、AWQ、GGUF）讓模型可以在消費級硬體上運行。

**硬體加速**：NVIDIA H100 的全面量產、AMD MI300X 的挑戰、Apple MLX 的開源，AI 硬體市場進入多元競爭時代。

---

## 延伸閱讀

- [LLaMA 論文](https://www.google.com/search?q=LLaMA+Meta+2023+foundation+language+model)
- [Llama 2 發布](https://www.google.com/search?q=Llama+2+Meta+commercial+use+2023)
- [Mistral 7B 技術細節](https://www.google.com/search?q=Mistral+7B+2023+Apache+2)
- [GPT-4V 系統卡](https://www.google.com/search?q=GPT-4V+vision+system+card+2023)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」年度回顧系列之二。*
