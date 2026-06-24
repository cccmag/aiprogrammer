# Article 4：Layer Normalization 詳解

## 與 Batch Normalization 的比較

BN 跨 batch 維度計算均值和方差，LN 跨 feature 維度計算。對於 NLP 任務，輸入序列長度各異，batch size 可能為 1，這使得 BN 不適用。LN 計算每個樣本內所有特徵的統計量，完全不受這些因素的影響。

## LN 的計算

對於輸入 x ∈ R^{B×T×D}（B=batch, T=sequence, D=feature），LN 對每個位置的 D 維特徵計算均值和方差，進行標準化。參數 γ and β 對每個特徵維度都是可學習的。LN 的計算不依賴於其他樣本，適合 RNN 和 Transformer。

## Pre-LN vs Post-LN

傳統 Transformer 使用 Post-LN：LayerNorm 放在殘差連接之後。Pre-LN 將 LayerNorm 放在殘差連接之前。實務發現 Pre-LN 更容易訓練，可以不使用 warmup。Pre-LN 的梯度在更深層更穩定，但某些研究指出可能影響表達能力。

## Layer Norm 的作用

LN 實現輸入標準化，提供以下優點：使損失地形更平滑、加速收斂、對初始化更加魯棒。與 BN 不同，LN 不需要 running statistics，在推斷時行為確定。

## 在 Transformer 中的應用

現代 Transformer 幾乎全部使用 Layer Normalization。Pre-LN 越來越流行，因訓練更穩定。個別實現會在輸出前再加一個 LayerNorm，即「Post-LN」。

## 參考資源

- Layer Normalization Paper：https://www.google.com/search?q=layer+normalization+ba+2016
- Pre-LN vs Post-LN Transformer：https://www.google.com/search?q=pre+ln+transformer+training