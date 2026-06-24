# Article 7：動量法的物理直覺

## 從物理的角度理解

想像一個球在損失函數曲面上滾動。沒有動量時，球根據當前位置的梯度方向移動，導致在溝谷中來回振盪。有了動量後，球累積之前的速度，即使到了溝谷邊緣仍保持向前運動的慣性，能更快地穿過溝谷。

## 數學表達

傳統動量：v_t = βv_{t-1} + η∇θ L(θ)。更新：θ = θ - v_t。這相當於「落後」於當前梯度方向，但累積了歷史速度。Nesterov 動量：v_t = βv_{t-1} + η∇θ L(θ - βv_{t-1})。先利用速度估算未來位置，再計算梯度，稱為「lookahead」。

## Nesterov 的改進

Nesterov 加速梯度在某些情況下比標準動量更快收斂。直覺上，標準動量像是「落後於」，而 Nesterov 像是在「預測」。在大多數深度學習框架中，動量參數 momentum 或 nesterov 即控制此行為。

## 與 Adam 的關係

Adam 使用了動量的概念，稱為「第一階矩估計」。但 Adam 同時使用 RMSProp 的「第二階矩估計」來自適應學習率。這使得 Adam 對梯度規模不敏感，而動量 SGD 的學習率需要仔細調整。

## 實務調參

動量參數通常設為 0.9，意味著大約累積前 10 步的歷史梯度。較大的動量參數（如 0.99）適用於非常平坦的曲面。Nesterov 動量在某些任務（如影像分類）表現稍好，但差異通常不大。

## 參考資源

- Momentum SGD：https://www.google.com/search?q=momentum+stochastic+gradient+descent
- Nesterov Accelerated Gradient：https://www.google.com/search?q=nesterov+accelerated+gradient