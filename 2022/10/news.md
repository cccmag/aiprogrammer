# 本月新知

## 2022 年 10 月 RLHF 技術動態

### ChatGPT 即將問世

2022 年 10 月，AI 領域最受矚目的事件莫過於 OpenAI 正在測試的 ChatGPT。雖然 ChatGPT 在 11 月底才正式發布，但 10 月已有消息指出 OpenAI 正在建立一個基於 GPT-3.5 系列模型的對話式 AI，並使用 RLHF（Reinforcement Learning from Human Feedback）進行微調。這項技術將徹底改變人類與 AI 的互動方式。

### InstructGPT 論文的持續影響

OpenAI 在 2022 年初發布的 InstructGPT 論文（"Training language models to follow instructions with human feedback"）繼續在學術界和工業界產生深遠影響。該論文展示了使用 RLHF 微調 GPT-3 可以讓模型更準確地遵循人類指令，同時減少有害輸出。這項工作在 10 月被 NeurIPS 2022 正式接收，進一步推動了 RLHF 的普及。

### Anthropic 的憲法 AI

Anthropic 在 2022 年 9 月發表了憲法 AI（Constitutional AI）方法，試圖解決 RLHF 中的一個根本問題：如何在不依賴大量人類標註的情況下，確保 AI 系統的行為符合人類價值觀。憲法 AI 使用一組書面原則（「憲法」）來引導模型的自我監督，減少對人類標註者的依賴。這項工作在 10 月引發了廣泛討論。

### DeepMind 的 Sparrow

DeepMind 在 2022 年 9 月發表了 Sparrow 系統，一個使用 RLHF 訓練的對話代理。Sparrow 特別強調了「有用性」和「安全性」的平衡，並引入了基於規則的獎勵模型來減少有害輸出。Sparrow 的發表標誌著 RLHF 已經從學術研究走向實用系統。

### 獎勵模型的改進

史丹佛大學和 UC Berkeley 的研究團隊在 10 月分別發表了關於獎勵模型改進的工作。史丹佛團隊提出了偏好資料的「主動學習」策略，在不增加人類標註量的情況下提高獎勵模型的準確性。UC Berkeley 則研究了獎勵模型的泛化能力，發現不同分佈下的獎勵模型表現有顯著差異。

### DPO 方法的先聲

雖然直接偏好最佳化（DPO）論文在 2023 年才正式發表，但 2022 年 10 月已有研究團隊開始探索繞過顯式獎勵模型、直接從人類偏好中最佳化策略的方法。史丹佛大學的研究者提出了基於对比學習的偏好最佳化框架，為後來的 DPO 奠定了理論基礎。

### 業界動態

- **Hugging Face** 發布了 TRL（Transformer Reinforcement Learning）函式庫的更新，使 RLHF 的實作更加便捷
- **Cohere** 宣布使用 RLHF 改進其生成模型的指令遵循能力
- **Google** 發表了 LaMDA 的 RLHF 應用案例，展示對話品質的提升
- **Meta** 開源了部分 RLHF 資料處理工具，推動了社群發展

### 會議與活動

- NeurIPS 2022 論文接收結果公布，多篇 RLHF 相關論文被接收
- EMNLP 2022 也在 10 月舉辦，包含多個關於人類反饋學習的工作坊
- AI Safety Camp 2022 討論了 RLHF 在 AI 安全中的作用

### 工具與框架

- TRL 函式庫新增了 PPOv2 訓練器，簡化了 RLHF 的實作流程
- DeepSpeed Chat 尚未發布（2023 年發布），但微軟內部已在測試相關工具
- 开源的偏好資料集（如 Anthropic HH-RLHF）持續擴大

### 展望

2022 年 10 月標誌著 RLHF 從學術研究走向工業應用的關鍵轉折點。隨著 ChatGPT 的即將問世和各大科技巨頭的投入，RLHF 將在接下來的幾年中持續主導 AI 對齊領域的發展。
