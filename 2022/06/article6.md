# Transformer 訓練穩定性

## 訓練 Transformer 的挑戰

深層 Transformer 的訓練比想像中困難。即使架構設計精巧，訓練過程中仍可能遇到梯度不穩定、收斂緩慢、數值溢出等問題。這些問題隨著模型深度和寬度的增加而急劇惡化。特別是在注意力層中，不當的初始化會導致 softmax 飽和或梯度消失，使模型無法有效學習。

## 初始化策略

Transformer 對參數初始化非常敏感。Xavier/Glorot 初始化適合 tanh 激活函數，Kaiming/He 初始化適合 ReLU 激活函數。T5 採用特殊的初始化策略，先將所有參數初始化為零，再按層的深度的平方根進行縮放。此外原始 Transformer 對線性層的權重使用正態分布 N(0, 0.02) 初始化，對偏置使用零初始化。選擇合適的初始化對訓練成功至關重要。

## 學習率排程

Transformer 原論文使用 Noam 學習率排程。在前 warmup_steps 步（通常 4000 或 8000 步），學習率從零線性升溫到最大值。這個升溫階段讓模型在訓練初期保持穩定的參數更新，避免注意力分布在大梯度下崩潰。之後學習率按步數的平方根衰減，允許模型在訓練後期進行精細調整。

## Adam Optimizer

Transformer 使用 Adam 優化器，配置為 β1=0.9、β2=0.98、ε=1e-9。相比標準 Adam 的 β2=0.999，0.98 的值讓優化器更重視近期梯度，有助於在 Transformer 訓練動態中保持穩定。搭配 Noam 排程使用效果最佳。

## 標籤平滑

原始 Transformer 使用 ε=0.1 的標籤平滑（label smoothing），將 one-hot 的目標分布與均勻分布混合。這種正則化方法防止模型過度自信於訓練標籤，顯著提升泛化能力，在翻譯等任務上通常能帶來 0.5 到 1 個 BLEU 分的提升。

## 梯度裁剪

大規模 Transformer 模型需使用梯度裁剪，通常 max_norm=1.0 或 5.0。梯度裁剪防止梯度爆炸導致參數更新過大，破壞模型的收斂穩定性。

## Pre-Norm 與 Post-Norm

原始 Transformer 使用 Post-Norm，即在殘差連接之後進行層正則化。後續研究發現 Post-Norm 在深層模型中訓練不穩定。Pre-Norm 將 Layer Norm 移到子層之前，即 x + Sublayer(LayerNorm(x))。Pre-Norm 大幅提升了深層訓練的穩定性，幾乎所有現代 Transformer 皆採用此設計。

## 其他正則化

原始 Transformer 對每個子層輸出應用 dropout rate=0.1，並對嵌入層和位置編碼應用 dropout。在某些實作中，還會對注意力權重應用 dropout（attention dropout）防止過擬合。

## 參考資源

- Noam 學習率排程：https://www.google.com/search?q=Noam+learning+rate+schedule+transformer
- 標籤平滑：https://www.google.com/search?q=label+smoothing+regularization
- Pre-Norm vs Post-Norm：https://www.google.com/search?q=pre+norm+post+norm+transformer
