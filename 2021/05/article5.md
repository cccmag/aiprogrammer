# Article 5：權重衰減與L2正則化

## 從貝葉斯說起

在貝葉斯框架下，假設參數服從先驗分佈 p(θ)。最大化後驗概率 (MAP) 等價於最小化 -log p(y|x,θ) - log p(θ)。若先驗是高斯分佈 N(0, σ²)，則 -log p(θ) ∝ ||θ||²/2σ² + const。這正是 L2 正則化。

## 權重衰減的實際效果

權重衰減直接將權重縮減：w = w * (1 - ηλ)。在 SGD 優化器中，這與 L2 正則化等價。但在 Adam 等自適應學習率優化器中，兩者並不完全等價——L2 正則化的效果被自適應學習率削弱。

## 與其他正則化的關係

L2 正則化與 Dropout、Label Smoothing 等技術有互補關係。L2 約束權重的幅度，Dropout 干預網路的資訊流動，Label Smoothing 約束目標。這些技術可以同時使用，通常能帶來額外提升。

## 實務中的權重衰減

權重衰減的超參數 λ 通常設為 0.01 到 0.0001 之間。較大的模型通常需要較小的衰減率。在微調預訓練模型時，通常使用很小的權重衰減或不使用。

## 與 Max Norm Regularization 的比較

Max norm 約束 ||w|| ≤ c，而非懲罰 ||w||²。Max norm 在 RNN 中更常用，因其能有效防止梯度爆炸。兩者可同時使用。

## 參考資源

- L2 Regularization Deep Learning：https://www.google.com/search?q=l2+regularization+neural+network+weight+decay
- Bayesian View of Regularization：https://www.google.com/search?q=bayesian+interpretation+regularization+deep+learning