# 開放域聊天機器人

## 無邊界的對話挑戰

開放域聊天機器人的目標是能夠與人類進行任意主題的對話。與任務型系統不同，開放域系統沒有預先定義的對話目標，需要處理的對話場景是無限的。

## 從 Cleverbot 到 Meena

### Cleverbot（2006）

由 Rollo Carpenter 開發的 Cleverbot 是早期最成功的開放域聊天機器人。它使用檢索式方法，從超過 4000 萬條過往對話中選擇回覆。

### Microsoft Xiaoice（2014）

微軟的小冰是第一個大規模部署的開放域聊天機器人，特別關注情感連結和長期記憶。小冰在中國、日本、印尼等地累積了超過 6.6 億使用者。

### Google Meena（2020）

Google 在 2020 年發表了 Meena，這是一個基於 Evolved Transformer 架構的開放域聊天機器人，擁有 26 億參數。Meena 引入了 Sensibleness and Specificity Average（SSA）評估指標。

## 一致性與個性

開放域聊天機器人面臨的核心挑戰之一是保持個性的一致性。早期的系統在長期對話中經常出現前後矛盾的情況。BlenderBot（Meta, 2020）引入了人格設定機制，讓機器人在對話開始前獲得一個固定的個性描述。

## 安全與偏見

開放域系統由於生成自由度高，更容易產生有害或不當內容。解決方案包括：

- **內容過濾**：使用分類器過濾有害輸出
- **安全微調**：在安全的對話資料上進行微調
- **對齊訓練**：使用 RLHF 使模型符合人類價值觀

## 評估指標

開放域對話的評估一直是難題。主要評估方法包括：

- **自動評估**：Perplexity、BLEU、ROUGE 等
- **人工評估**：Fluency、Relevance、Engagement、Coherence
- **混合方法**：使用 GPT 等模型做自動化品質評估

## 延伸閱讀

- [Meena 技術論文](https://www.google.com/search?q=Meena+Google+open+domain+chatbot)
- [BlenderBot 個性化對話](https://www.google.com/search?q=BlenderBot+persona+based+dialogue)
- [對話安全](https://www.google.com/search?q=AI+safety+dialogue+system+open+domain)
