# 2. Transformer 架構解析

## 注意力機制核心

Transformer 的核心是自注意力（Self-Attention）機制。對於輸入序列中的每個位置，模型可以同時計算與所有其他位置的關聯性，捕捉長距離依賴關係。自注意力的計算過程如下：

1. 輸入向量透過三個線性變換生成 Query、Key、Value
2. 計算 Query 與所有 Key 的點積，得到注意力權重
3. 注意力權重經過 Softmax 正規化
4. 加權平均所有 Value 得到輸出

這個過程可以矩陣化操作，充分利用 GPU 的平行運算能力。

## 多頭注意力

Transformer 使用「多頭注意力」（Multi-Head Attention），將注意力計算分解為多個獨立的「頭」。每個頭學習不同的注意力模式，有的關注語法關係，有的關注語義關聯。多頭的輸出會被拼接並線性變換，形成最終的表示。

這種設計讓模型能夠同時捕捉多種不同類型的關聯資訊，顯著提升模型的表達能力。

## 位置編碼

Transformer 本身不考慮序列順序資訊，為了解決這個問題，論文中引入了位置編碼（Positional Encoding）。位置編碼使用正弦和餘弦函數，為每個位置生成獨特的編碼向量，並加入到輸入嵌入中。

BERT 採用的是改進後的位置編碼，支援更長的序列並改善了相對位置表示。

## Encoder 與 Decoder

原始 Transformer 包含 Encoder 與 Decoder 兩部分：
- **Encoder**：處理輸入序列，生成語境化的表示
- **Decoder**：在Encoder輸出的基礎上，自回歸地生成輸出序列

BERT 只使用 Encoder 部分，透過雙向處理輸入序列學習語言表示。這種設計非常適合理解任務，如分類、問答、命名實體識別等。

## Layer Normalization 與残差連接

每個 Transformer 層都包含：
1. 自注意力子層 + 残差連接 + Layer Normalization
2. 前饋網路子層 + 残差連接 + Layer Normalization

這些設計確保了深度網路的穩定訓練，讓數百層的 Transformer 能夠有效學習。

## 參考資源

- https://www.google.com/search?q=Transformer+architecture+self-attention+multi-head+positional+encoding+explained
- https://www.google.com/search?q=Transformer+encoder+decoder+Layer+Normalization+residual+connection+explainer
- https://www.google.com/search?q=attention+mechanism+Query+Key+Value+self-attention+calculation+step+by+step