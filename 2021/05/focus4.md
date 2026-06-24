# Focus 4：正則化技術全景

## 正則化的必要性

神經網路有極强的表示能力，幾乎可以擬合任何訓練資料。但這也意味著容易過擬合——在訓練資料上表現優秀，泛化能力卻不理想。正則化的目標是約束網路的複雜度，使其在未见過的資料上也有好表現。

## L2 正則化

L2 正則化（又稱權重衰減）是將引數的 L2 範數加入損失函數：L_total = L_original + λ||w||²/2。梯度下降時，這相當於每步都將權重縮減一個因子 (1-ηλ)。L2 正則化使得權重趨向較小的值，類似的效果也可以通過直接限制權重的最大範數實現。

## Dropout

Dropout 由 Hinton 等人在 2012 年提出。訓練時，每個神經元以機率 p 隨機「關閉」。這可以理解為訓練了一個集成模型——多個子網路的集合。推斷時使用完整網路，但輸出乘以 (1-p)。Dropout 有效防止了神經網路對特定神經元的依賴。

## Data Augmentation

資料增強是另一种正则化策略——不改变模型结构，而是让训练数据更具多样性。通过对输入数据进行变换（旋转、裁剪、颜色调整等），模型能够学习到更鲁棒的特征。Test-time augmentation（TTA）则是在推理时对样本进行多次增强并平均结果。

## Label Smoothing

Label smoothing 将硬标签转换为软标签：如果有 K 个类别，真实标签从 one-hot (0, 1, 0) 变为 (ε/K, 1-ε+ε/K, ε/K)。这防止模型对训练数据过度自信，改善了泛化能力。

## 參考資源

- Dropout Original Paper：https://www.google.com/search?q=dropout+hinton+2012
- Regularization in Deep Learning：https://www.google.com/search?q=regularization+deep+learning+techniques