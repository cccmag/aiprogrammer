# Focus 5：批次正規化原理與變體

## Internal Covariate Shift

Batch Normalization（BN）由 Ioffe 和 Szegedy 在 2015 年提出，解決了「內部協變量偏移」問題：訓練過程中，網路前一層輸出分佈的變化，導致後續層需要不斷適應，降低訓練效率。BN 的核心思想是對每層輸入進行標準化，使其服從均值為 0、方差為 1 的分佈。

## BN 的運作機制

BN 在訓練和推斷時行為不同。訓練時，BN 使用當前 mini-batch 的均值和方差進行標準化，並使用指數移動平均（EMA）估計全域均值和方差。推斷時，BN 使用估計的全域統計量。關鍵引數是 γ（縮放）和 β（位移），允許網路學習最優的標準化分佈。

## BN 的優點

BN 帶來多個好處：加速收斂（因輸入分佈穩定）、允許更大的學習率（因標準化作用）、對初始化不那麼敏感（因標準化輸入）、在某種程度上有正則化效果（因 mini-batch 統計量的噪聲）。

## Layer Normalization

LN 與 BN 的關鍵區別是：BN 跨 batch 維度計算統計量，LN 跨 feature 維度計算。這使得 LN 在 RNN 中更受歡迎，因為 RNN 的 batch 維度通常為 1。LN 也常用於 Transformer 架構。

## 變體比較

Instance Normalization 適用於風格遷移。Group Normalization 在通道維度分組後計算，獨立於 batch 大小，適合小 batch 場景。SyncBN 在多 GPU 同步計算 batch 統計量，解決單 GPU batch 過小的問題。

## 參考資源

- Batch Normalization Paper：https://www.google.com/search?q=batch+normalization+paper+2015
- Group Normalization：https://www.google.com/search?q=group+normalization+2018