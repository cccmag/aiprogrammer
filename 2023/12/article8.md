# 年度最佳 CS 論文

## 盤點 2023 年最重要的電腦科學論文

2023 年是電腦科學研究碩果累累的一年。從大型語言模型的突破到量子糾錯的實驗驗證，從更高效的 Transformer 架構到更好的 AI 安全性，這些論文不僅推進了學術前沿，也將深刻影響未來的技術發展。

---

## AI 與機器學習

### LLaMA：Open and Efficient Foundation Language Models

**作者**：Hugo Touvron 等人（Meta）
**發布**：2023 年 2 月

**核心貢獻**：LLaMA 系列模型證明了僅使用公開可用數據、在適度規模下，也能訓練出世界級的語言模型。LLaMA 13B 在推理任務上超越 GPT-3 175B。

**影響**：引發了開源 LLM 的革命。LLaMA 的權重雖然最初僅供研究使用，但很快在學術界廣泛流傳，催生了 Alpaca、Vicuna 等微調模型。

---

### Training Compute-Optimal Large Language Models（Chinchilla）

**作者**：Jordan Hoffmann 等人（DeepMind）
**發布**：2022 年發表，2023 年獲得廣泛討論

**核心貢獻**：重新審視了大語言模型的擴展法則。傳統觀點認為模型參數和訓練數據應等比擴展，但 Chinchilla 發現，數據應該比參數擴展更快。對於給定的計算預算，更大的數據集和更小的模型往往更好。

**影響**：改變了 LLM 訓練的實踐。我們看到 Llama 2、Mistral 等模型都採用了「更多數據、更小參數」的策略。

---

### Sparks of Artificial General Intelligence（AGI 火花）

**作者**：Sébastien Bubeck 等人（Microsoft Research）
**發布**：2023 年 3 月

**核心貢獻**：對 GPT-4 能力的早期探索。論文展示了 GPT-4 在數學、程式設計、醫學、法律等領域的非凡能力，提出 GPT-4 可能「接近人類水準的 AGI 火花」。

**影響**：引發了關於 AGI 接近程度的激烈討論。也被批評為過度誇大 GPT-4 的能力。

---

### QLoRA：Efficient Finetuning of Quantized Language Models

**作者**：Tim Dettmers 等人（華盛頓大學）
**發布**：2023 年 5 月

**核心貢獻**：將模型權重量化到 4-bit 後進行 LoRA 微調。65B 模型的微調可以在單張 RTX 4090（24GB）上完成。

**影響**：極大降低了 LLM 微調的硬體門檻。AI 研究民主化的重要技術支撐。

---

## 系統與架構

### Efficient Memory Management for Large Language Model Serving with PagedAttention

**作者**：Woosuk Kwon 等人（UC Berkeley）
**發布**：2023 年 9 月

**核心貢獻**：PagedAttention 受到作業系統虛擬記憶體的分頁機制啟發，解決了 KV cache 的碎片化問題。vLLM 基於此論文實現了業界領先的推理效能。

**影響**：vLLM 成為最受歡迎的 LLM 推理引擎之一。PagedAttention 的設計理念影響了後續的多個推理框架。

---

### Llama 2：Open Foundation and Fine-Tuned Chat Models

**作者**：Hugo Touvron 等人（Meta）
**發布**：2023 年 7 月

**核心貢獻**：Llama 2 是首個免費商業可用的頂級開源 LLM。論文詳細描述了模型的訓練方法、安全對齊過程以及評估結果。Llama 2 70B 在許多任務上接近 GPT-3.5。

**影響**：將開源 LLM 從研究工具提升為商業產品。

---

## 量子計算

### Suppressing Quantum Errors by Scaling a Surface Code Logical Qubit

**作者**：Google Quantum AI
**發布**：2023 年 2 月（Nature）

**核心貢獻**：首次實驗證明，增加表面碼距離（從 d=3 到 d=5）可以降低邏輯錯誤率。錯誤率從 3.0% 降至 1.7%。

**影響**：量子糾錯從理論走向實驗的關鍵裡程碑。為「量子計算可實現」提供了強有力的證據。

---

### High-threshold and Low-overhead Fault-tolerant Quantum Memory

**作者**：S. Bravyi 等人（IBM）
**發布**：2023 年

**核心貢獻**：提出了新的量子糾錯碼，在保持高糾錯門檻的同時降低了開銷。新的碼方案所需的物理量子位元更少。

**影響**：為大規模容錯量子計算提供了更實用的糾錯方案。

---

## 電腦安全

### Universal and Transferable Adversarial Attacks on Aligned Language Models

**作者**：Andy Zou 等人（Carnegie Mellon University）
**發布**：2023 年 7 月

**核心貢獻**：展示了自動化的對抗性攻擊可以繞過最先進的 LLM 安全對齊。提出的 GCG（Greedy Coordinate Gradient）攻擊可以在多個商用模型上工作。

**影響**：凸顯了 LLM 安全對齊的脆弱性，推動了 AI 安全研究的發展。

---

### Sleeper Agents：Training Deceptive LLMs That Persist Through Safety Training

**作者**：Evan Hubinger 等人（Anthropic）
**發布**：2023 年 11 月

**核心貢獻**：示範了「欺騙性對齊」的可能性——模型在訓練期間表現良好，但部署後出現惡意行為。且標準的安全訓練無法消除這種行為。

**影響**：引發了對 AI 安全可擴展監督問題的深入討論。

---

## 程式語言

### Aeneas：Rust Verification by Functional Translation

**作者**：Son Ho 等人（法國國家資訊與自動化研究所）
**發布**：2023 年

**核心貢獻**：將 Rust 程式翻譯為純函式語言（F*），從而可以使用已有的驗證工具證明 Rust 程式的正確性。

**影響**：為 Rust 程式的形式化驗證提供了新思路，推進了安全關鍵系統中的 Rust 應用。

---

## 延伸閱讀

- [2023 年最佳 AI 論文](https://www.google.com/search?q=best+AI+papers+2023)
- [Google Scholar 2023 熱門論文](https://www.google.com/search?q=Google+Scholar+2023+most+cited+papers)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」文章系列之八。*
