# 4. BERT 的預訓練任務

## Masked Language Model

MLM 是 BERT 的主要預訓練任務，佔據了約 95% 的預訓練計算資源。具體做法：

1. **遮蓋策略**：隨機選擇 15% 的輸入 token
2. **替換方式**：80% 換成 [MASK]，10% 換成隨機詞，10% 保持不變
3. **預測目標**：模型預測被遮蓋位置的原詞

這種混合策略是為了緩解微調時 [MASK] token 不存在的問題。若僅使用 [MASK]，模型可能學習到依賴這個特殊標記的行為。

## Next Sentence Prediction

NSP 是輔助預訓練任務，幫助模型理解句子間關係：

1. **訓練資料**：50% 是實際相連的相鄰句子對
2. **負樣本**：50% 來自不同文檔的句子對
3. **標籤**：IsNext 表示連續，NotNext 表示不連續

NSP 任務讓 BERT 學習句子級的關係，這對於問答、自然語言推理等需要理解句子間關係的任務非常重要。

## 預訓練語料

BERT 使用了兩個大規模語料：
- **BooksCorpus**：包含超過 11,000 本英語書籍
- **English Wikipedia**：包含約 25 億單詞

這兩個語料的組合提供了豐富的文本類型，包括小說、新聞、百科等，有助於模型學習多樣的語言表示。

## 訓練細節

- **模型規模**：Base 版本 12 層、768 隱藏維度、12 注意力頭、1.1 億參數
- **Large 版本**：24 層、1024 隱藏維度、16 注意力頭、3.4 億參數
- **訓練時間**：Base 在 16 個 TPU 上訓練 4 天
- **批次大小**：256 sequences（Base）/ 256 sequences（Large）
- **學習率**：1e-4（Base）/ 1e-5（Large）
- **訓練步數**：1,000,000 步

## 兩個任務的貢獻

消融實驗顯示，MLM 帶來了主要的效能提升，NSP 在某些任務（如QNLI、SST-2）上有顯著幫助。兩者結合讓 BERT 在各種 NLP 任務上都能取得優異表現。

## 參考資源

- https://www.google.com/search?q=BERT+pre-training+tasks+MLM+NSP+Masked+Language+Model+Next+Sentence+Prediction
- https://www.google.com/search?q=BERT+pre-training+data+BooksCorpus+Wikipedia+corpus+size
- https://www.google.com/search?q=BERT+training+hyperparameters+TPU+batch+size+learning+rate+steps