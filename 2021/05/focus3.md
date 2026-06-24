# Focus 3：學習率排程策略

## 為何需要學習率排程

學習率是最重要的超參數之一。過大導致震盪或不收斂，過小導致訓練過慢。更重要的是，學習率與訓練階段密切相關：初期需要較大學習率探索，後期需要較小學習率精調。學習率排程正是適應這種需求的機制。

## 常見排程策略

階梯衰減（Step Decay）是最簡單的策略：每當訓練進入 plateau，學習率降低一個因子（如 0.1）。指數衰減（Exponential Decay）提供更平滑的衰減曲線。餘弦退火（Cosine Annealing）模擬餘弦函數，在訓練末尾將學習率降到接近零。熱啟動餘弦衰減（Warmup + Cosine Annealing）在初期逐漸增加學習率至峰值，然后餘弦衰減，是 Transformer 訓練的標準配置。

## Warmup 的重要性

Transformer 訓練初期使用 warmup 是關鍵步驟。理論上，初期網路引數是隨機初始化的，梯度方向不穩定，此時用較小的學習率可避免不穩定。實務上，warmup 讓優化器有時間建立 Adam 的二三階矩估計，提高訓練穩定性。

## 實務建議

1. 預訓練模型通常已確定學習率排程，直接使用
2. 自定義任務，如果不知道如何設置，用 cosine annealing with warmup
3. 監控訓練曲線，適時調整
4. 較大的批量可以使用較大的學習率

## 參考資源

- Leslie Smith Warmup：https://www.google.com/search?q=learning+rate+warmup+cosine+annealing
- Attention is All You Need LR Schedule：https://www.google.com/search?q=transformer+learning+rate+schedule