# 遮罩注意力與因果注意力

## Padding Mask

當批次中序列長度不一時，短序列需要填充（padding）到相同長度以形成批次張量。如果不使用 mask，填充 token 會參與注意力計算，引入雜訊並扭曲模型的表示。Padding mask 將填充位置的注意力權重設為零，確保模型只關注真實的序列內容。在實作中通常將填充位置對應的注意力分數設為 -inf，經 softmax 後權重自然歸零。

## 因果遮罩（Causal Mask）

在自迴歸生成任務中，解碼器只能關注當前及之前位置的 token，不能看到未來的 token，否則會造成標籤洩漏（label leakage）。例如在語言建模中，預測第 i 個詞時只能使用前 i-1 個詞作為上下文。因果遮罩是一個上三角矩陣，右上角設為 -inf，左下角設為 0。softmax 後未來位置的權重為零，確保每一步生成只依賴已產生的歷史資訊。

## Look-Ahead Mask

Look-ahead mask 與因果遮罩本質相同，在語言建模中用於遮蔽未來 token。兩者只是命名慣例不同，都服務於確保自迴歸生成因果性的同一目的。這種因果性（causality）是序列生成模型必須遵守的基本原則。

## 交叉注意力遮罩

在 Encoder-Decoder 結構中，解碼器的交叉注意力不需要遮罩未來位置，因為編碼器輸出已包含完整的輸入序列。但編碼器的輸入仍然有 padding 的情況，此時需要 padding mask 來忽略填充位置。交叉注意力的 Q 來自解碼器，K 和 V 來自編碼器，遮罩是針對 K/V 的序列維度進行的。

## Prefix Mask

T5 等模型使用 prefix mask：前綴部分使用雙向注意力（任何位置可互相關注），後綴部分使用因果注意力（只能關注自身及之前位置）。這種混合模式在 text-to-text 任務中非常常見，讓模型在編碼階段充分理解上下文，在解碼階段保持因果性。

## Sliding Window Mask

Longformer、Big Bird 等高效 Transformer 使用滑動視窗遮罩：每個 token 只關注附近 w 個 token。計算量從 O(n²) 降至 O(nw)。通常搭配全局 token 機制，讓某些位置如 [CLS] 擁有全局關注能力。

## 遮罩的組合與實作

實務中 padding mask 與 causal mask 會合併使用。方法是將兩個遮罩進行逐元素的加法或邏輯 AND 操作，形成一個統一的遮罩矩陣。

## 參考資源

- 遮罩注意力教學：https://www.google.com/search?q=transformer+mask+attention+explained
- Longformer 滑動視窗：https://www.google.com/search?q=Longformer+sliding+window+attention
