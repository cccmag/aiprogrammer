# Article 3：梯度同步與非同步訓練

## 同步 SGD 的優缺點

同步 SGD 每個 step 都等待所有 GPU 完成並同步梯度。這保證了與單卡訓練完全一致的收斂行為——沒有 staleness 問題。但缺點是：最慢的 GPU 決定整體速度，存在 Straggler 問題。

## 非同步 SGD 的動機

非同步 SGD 允許各個 GPU 獨立更新，不等待其他 GPU。這樣每個 GPU 都能满载運行，沒有 Straggler 問題。但缺點是：梯度可能有 staleness，即用於更新的梯度不是最新的。

## Staleness 的影響

理論和實驗都表明，staleness 達到一定範圍內時，非同步 SGD 仍能收斂。但過大的 staleness 會導致收斂變慢甚至發散。實際上，非同步 SGD 通常比同步 SGD 需要更多的迭代。

## Gradient Polling

Gradient Polling 是緩解 staleness 的一種技術。只有當本地梯度完成後才去拉取最新版本，而非直接使用本地計算的梯度。雖然需要額外通訊，但能有效減少 staleness 的影響。

## PipeDream 的設計

PipeDream 使用非同步管道平行。每個階段維護自己的模型副本，用收到的輸入計算梯度並非同步更新。通過限制 staleness 在一定範圍內，可以在效率和收斂性之間取得平衡。

## 實務建議

同步 SGD 是大多數場景的首選。當訓練時間緊迫、網路頻寬有限、或存在嚴重的 Straggler 問題時，再考慮非同步方法。

## 參考資源

- Asynchronous SGD：https://www.google.com/search?q=asynchronous+sgd+deep+learning
- Gradient Staleness：https://www.google.com/search?q=gradient+staleness+distributed+training