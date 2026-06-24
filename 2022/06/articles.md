# 文章總覽

本期共十篇技術文章，從歷史脈絡到前沿發展，全面涵蓋 Transformer 的各個面向。

## 第一期：從 RNN 到 Transformer

回顧序列模型的演化歷程，從 RNN、LSTM、GRU 到注意力機制的誕生。分析 RNN 的並行化瓶頸與梯度消失問題，解釋 Transformer 如何以注意力機制取代遞迴。探討 BERT、GPT 等預訓練模型如何建立在 Transformer 之上。[閱讀全文](article1.md)

## 第二期：注意力權重視覺化

介紹注意力權重的視覺化方法，包括熱力圖、Sankey 圖、BertViz 工具。討論 Attention Rollout 技術以及注意力權重作為解釋工具的局限性。幫助理解模型內部的運作機制。[閱讀全文](article2.md)

## 第三期：多頭注意力的意義

深入分析多頭注意力的行為模式與功能分工。探討頭部修剪現象、不同頭對任務的重要性差異、跨語言頭部對齊等前沿研究。解釋為什麼多頭注意力比單頭更有效。[閱讀全文](article3.md)

## 第四期：位置編碼：三角函數 vs 學習式

比較 sin/cos 固定編碼與可學習編碼的優缺點。介紹 RoPE（旋轉位置編碼）與 ALiBi 等新型方法。給出短序列與長序列場景下的實務選擇建議。[閱讀全文](article4.md)

## 第五期：遮罩注意力與因果注意力

說明 padding mask、causal mask、cross-attention mask 的差異與應用。詳細解釋 sliding window mask 與 prefix mask 的使用方式。討論遮罩的組合與合併實作技巧。[閱讀全文](article5.md)

## 第六期：Transformer 訓練穩定性

介紹深層 Transformer 訓練面臨的挑戰：初始化策略、Noam 學習率排程、Adam 參數配置、標籤平滑、Pre-Norm vs Post-Norm 等關鍵技術。說明如何避免訓練過程中的常見問題。[閱讀全文](article6.md)

## 第七期：高效 Transformers：Linformer、FlashAttention

探討降低注意力 O(n²) 複雜度的各種方法。Linformer 的低秩近似、FlashAttention 的 IO 感知演算法、Reformer 的 LSH 分桶、Longformer 的滑動視窗。給出不同場景下的選型建議。[閱讀全文](article7.md)

## 第八期：Vision Transformer ViT

介紹 ViT 如何將圖片分割為 patch 並用 Transformer 處理。探討 ViT 需要大量資料的原因、Swin Transformer 的分層設計、以及 ViT 對視覺領域的深遠影響。[閱讀全文](article8.md)

## 第九期：Transformer 在語音的應用

分析 Transformer 在語音領域的應用：Speech Transformer、Whisper、AudioLM、SpeechT5。討論語音領域特有的長序列挑戰和即時處理需求。[閱讀全文](article9.md)

## 第十期：Transformer 的極限與未來

討論 Transformer 的二次複雜度限制、長上下文突破、狀態空間模型的挑戰、混合架構方向。展望 Transformer 之後的 AI 架構發展。[閱讀全文](article10.md)
