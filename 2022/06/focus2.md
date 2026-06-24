# Focus 2：縮放點積注意力（Scaled Dot-Product Attention）

## 什麼是縮放點積注意力？

縮放點積注意力是 Transformer 的核心運算，負責計算輸入序列中每個位置對其他位置的關注程度。給定查詢矩陣 Q、鍵矩陣 K、值矩陣 V，運算流程分為四步。首先計算 Q 與 K 的點積，得到任意兩個位置之間的相似度分數。點積越大表示兩個位置越相關。然後將相似度分數除以 sqrt(d_k) 進行縮放，避免數值過大導致 softmax 飽和。接著對縮放後的分數應用 softmax 進行歸一化，使每個查詢位置的所有鍵位置權重總和為 1。最後用歸一化後的權重對 V 進行加權求和，得到注意力輸出。

## 為什麼需要縮放？

當鍵的維度 d_k 較大時，點積的數值範圍會急劇擴大。假設 Q 和 K 的元素是均值為 0、變異數為 1 的隨機變數，點積的期望變異數為 d_k。當 d_k=512 時，點積的標準差約為 22.6，遠大於 1。如此大的數值範圍會將 softmax 推入飽和區，使其梯度趨近於零。除以 sqrt(d_k) 可將變異數歸一化為 1，確保梯度處於合理範圍。

## 數學形式

公式為 Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V。Q 的形狀為 n×d_k，K 為 m×d_k，V 為 m×d_v。n 和 m 可以不同，在自注意力中 n=m，在交叉注意力中 n 來自解碼器長度，m 來自編碼器長度。

## 與 Bahdanau 注意力的比較

Bahdanau 注意力使用可學習的對齊網路計算權重，需要逐位置計算，無法利用矩陣乘法加速。點積注意力透過矩陣運算可完全並行，速度快 2 到 3 倍。此外點積注意力的數學形式更簡單，梯度的計算也更直接。

## 多頭注意力的結合

縮放點積注意力在多頭注意力中重複 h 次，每個頭在不同投影子空間上獨立計算。論文發現不同頭捕捉了不同的關係模式：某些頭關注局部上下文，某些頭關注長距離依賴。將多個頭結合後，模型能同時捕捉多種語言關係。

## 遮罩機制

在解碼器中，遮罩將上三角矩陣設為 -inf，使 softmax 後對應位置的權重為零。Padding mask 則將填充位置設為 -inf。

## 程式實作

參考 `transformer.py` 的 `scaled_dot_product_attention` 函式，使用純 NumPy 實作。

## 參考資源

- Scaled dot-product 圖解：https://www.google.com/search?q=scaled+dot+product+attention+explained
- Softmax 飽和問題：https://www.google.com/search?q=softmax+saturation+problem
