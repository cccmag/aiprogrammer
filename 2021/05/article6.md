# Article 6：梯度消失與爆炸解決方案

## 問題的由來

在深度網路中，梯度需要從輸出層反向傳播到輸入層。根據鏈式法則，梯度是沿途各層梯度的乘積。如果每層的梯度都小於 1，則乘積迅速趨於零（梯度消失）。如果每層的梯度都大於 1，則乘積迅速趨於無窮（梯度爆炸）。

## 梯度消失的影響

梯度消失使得深層網路的淺層引數幾乎無法更新。這解釋了為何早期深度網路難以訓練：即使網路很深，靠近輸入的層幾乎學不到東西。ReLU 激活函數部分解決了這個問題——其梯度要么是 0 要么是 1。

## Xavier/He 初始化

合理的初始化可以緩解梯度問題。Xavier 初始化適用於 Sigmoid/Tanh，設為 W ~ N(0, 2/(fan_in + fan_out))。He 初始化適用於 ReLU，設為 W ~ N(0, 2/fan_in)。目的是讓向前傳播時輸入輸出方差相近，讓向後傳播時梯度方差也相近。

## Batch Normalization

BN 稳定每層輸入的分佈，減少內部協變量偏移。通過標準化，BN 確保每層的輸入分佈穩定在均值為 0、方差為 1，使梯度傳播更順暢。即使網路很深，梯度也能較好地流傳到淺層。

## 殘差連接

殘差連接提供了梯度抄近道的機會。即使主分支的梯度很小，捷徑路徑也能直接傳遞梯度。這使得極深網路的訓練成為可能。

## 梯度裁剪

在某些場景（特別是 RNN），梯度爆炸難以完全避免。這時可用梯度裁剪：當梯度的範數超過閾值時，將梯度縮放到合理範圍。這個簡單技巧對於 RNN 的穩定訓練至關重要。

## 參考資源

- Gradient Vanishing Problem：https://www.google.com/search?q=gradient+vanishing+exploding+deep+learning
- Xavier Initialization：https://www.google.com/search?q=xavier+initialization+neural+network