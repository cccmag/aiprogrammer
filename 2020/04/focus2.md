# 2. 預訓練語言模型的崛起

## 從 Word2Vec 到 GPT

語言模型的發展經歷了漫長的演進。早期的語言模型如 Word2Vec 學習單詞的向量表示，但無法處理複雜的上下文關係。ELMo 使用雙向 LSTM 來學習上下文相關的詞嵌入，但模型規模受限。

2018 年，OpenAI 發布了 GPT（Generative Pre-training），首次展示了使用 Transformer 解碼器進行大規模預訓練的可能性。幾個月後，Google 發布了 BERT，使用雙向 Transformer 編碼器，在多個 NLP 任務上刷新紀錄。

## BERT 的成功

BERT 的成功源於雙向注意力機制與掩碼語言模型（Masked Language Model）訓練目標。不同於 GPT 的單向預測，BERT 能夠同時利用左右上下文資訊。預訓練時，BERT 隨機遮蓋輸入中 15% 的單詞，訓練模型預測被遮蓋的詞。

這種預訓練方法產生了強大的語言表示，在各種下游任務上只需要微調就能達到優異性能。BERT 成為 NLP 領域的遊戲改變者，催生了 RoBERTa、ALBERT、ELECTRA 等後續改進。

## GPT-2 的「更大」策略

不同於 BERT 的架構創新，GPT-2 選擇了一條看似簡單但有效的道路：將模型做得更大、資料用得更多。15 億參數的 GPT-2 在當時震驚了社群，也預示了後續「規模法則」（scaling laws）研究的興起。

OpenAI 的實驗表明，隨著模型規模與訓練資料的增加，語言模型的能力會持續提升，且這種提升具有可預測性。這為後續更大規模的實驗奠定了理論基礎。

## 預訓練 + 微調範式

預訓練語言模型的標準流程是：首先在大規模通用資料上預訓練，學習通用的語言表示；然後在特定任務的標註資料上微調，使模型適應任務需求。這種遷移學習方法大幅降低了 NLP 任務的標註成本與訓練時間。

## 參考資源

- https://www.google.com/search?q=BERT+pre-training+Transformer+bidirectional+NLP+2018
- https://www.google.com/search?q=pretrained+language+model+transfer+learning+fine-tuning+survey
- https://www.google.com/search?q=GPT+ELMo+word+embedding+language+model+evolution+history