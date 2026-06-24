# Focus 6：層正則化與殘差連接

## 殘差連接（Residual Connection）

殘差連接是深度學習中最重要的技術之一。它讓每一層的輸出與其輸入相加，形成捷徑連接。數學形式為 output = LayerNorm(x + Sublayer(x))。這個簡單的設計讓梯度可以直接繞過子層傳播到更深的層次，有效防止了深層網路中的梯度消失問題。

## 為什麼需要殘差連接？

深度神經網路面臨兩種核心問題。第一是梯度消失，隨著網路加深，反向傳播的梯度指數級衰減，前層參數幾乎無法更新。第二是退化問題，即深層模型的訓練誤差反而高於淺層模型。這兩者的根源都在於深層網路的優化困難。殘差連接同時緩解了這兩個問題，讓 Transformer 能夠堆疊到 6、12 甚至數百層而不發生訓練失敗。

## 層正則化（Layer Normalization）

Layer Norm 對每個樣本的所有特徵維度進行歸一化。其計算公式為 LayerNorm(x) = γ * (x - μ) / sqrt(σ² + ε) + β，其中 μ 和 σ 是目前樣本的均值和標準差，γ 和 β 是可學習的縮放與平移參數。這個操作確保了每層的輸出具有穩定的數值範圍。

## Layer Norm vs Batch Norm

Batch Norm 對每個特徵跨樣本歸一化，不適合序列模型。原因在於序列長度可變，較短序列的 padding 會扭曲統計量的計算。Layer Norm 對每個樣本獨立歸一化，不受序列長度變化的影響，因此更適合 Transformer。

## Pre-Norm vs Post-Norm

原始 Transformer 使用 Post-Norm 設計（先殘差連接後正則化）。後續研究發現 Post-Norm 在深層模型中訓練不穩定，尤其當層數超過 12 層時。Pre-Norm（先正則化後殘差連接）改進了這個問題，讓訓練更加穩定。Pre-Norm 的形式為 output = x + Sublayer(LayerNorm(x))。目前幾乎所有現代 Transformer 都採用 Pre-Norm 設計。

## 實作建議

實務中 Pre-Norm 搭配 warmup 學習率排程效果最佳。許多開源實作如 Hugging Face Transformers 庫的預設配置即採用 Pre-Norm。

## 參考資源

- Layer Normalization 論文：https://www.google.com/search?q=layer+normalization+paper+2016
- Pre-Norm vs Post-Norm：https://www.google.com/search?q=pre+norm+post+norm+transformer
