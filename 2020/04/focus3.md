# 3. Transformer 架構的進化

## 原始 Transformer

2017 年，Google 發表了《Attention is All You Need》論文，介紹了 Transformer 架構。Transformer 完全基於注意力機制，放棄了傳統的 RNN 和 CNN，在機器翻譯任務上達到了頂尖性能。

Transformer 的核心是自注意力（self-attention）機制。對於輸入序列中的每個位置，注意力機制計算該位置與所有其他位置之間的相關性，捕捉長距離依賴關係。這種並行的注意力計算使得 Transformer 能夠高效地處理長序列。

## GPT 系列：Transformer 解碼器

GPT-1、GPT-2 和 GPT-3 都使用 Transformer 的解碼器部分，採用單向（causal）注意力。這種設計適合生成任務，因為每個詞的表示只能依賴前面的詞。

GPT-2 的 Transformer 區塊包含：
- 多頭自注意力層
- 位置前饋網路
- 層歸一化（Layer Normalization）
- 殘差連接

## BERT 系列：Transformer 編碼器

BERT 使用完整的 Transformer 編碼器，採用雙向注意力。這使得每個詞的表示可以同時利用左右上下文。雙向注意力在理解任務（如分類、問答）上表現優異，但不適合直接用於生成。

## 改進方向

近年來，研究者提出了多種 Transformer 改進：

1. **稀疏注意力**：如 Longformer、BigBird，透過局部+全局注意力的組合處理長序列
2. **線性注意力**：如 Linformer、Performer，將注意力計算複雜度降至線性
3. **高效能和改進**：如 FLASH、Apollo 等新架構
4. **知識蒸餾**：將大型 Transformer 蒸餾為更小的版本

## 位置編碼

原始 Transformer 使用正弦/餘弦位置編碼來表達序列位置資訊。後續研究提出了相對位置編碼（如 Shaw 等人的工作）和可學習的位置編碼。GPT-2 使用了改進的位置編碼方案，增強了模型處理超長序列的能力。

## 參考資源

- https://www.google.com/search?q=Transformer+architecture+attention+mechanism+explained+2017
- https://www.google.com/search?q=GPT+BERT+decoder+encoder+differences+transformer+variants
- https://www.google.com/search?q=position+encoding+relative+absolute+transformer+improvements