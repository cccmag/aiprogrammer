# Focus 4：梯度Checkpointing詳解

## 記憶體與計算的權衡

訓練深度網路時，需要儲存 forward pass 的中間活化值用於 backward。對於大模型和中間層，這些活化值可能佔用大量記憶體。Gradient Checkpointing（又稱 activation checkpointing 或 recomputation）是一種用計算換記憶體的技術：選擇性地保存部分活化值，其餘在需要時重新計算。

## 基本原理

不做 checkpointing 時，所有活化值都保存在記憶體中。做 checkpointing 時，只保存部分的活化值（如每 N 層保存一個檢查點）。反向傳播需要中間活化值時，從最近的檢查點重新計算。這種方法將記憶體需求從 O(N) 減少到 O(sqrt(N))，代價是增加約 20-30% 的計算時間。

## 哪些層需要Checkpointing

實務中，記憶體瓶頸通常在網路的中間層。全網路都做 checkpointing 太浪費計算，只 checkpointing 少數層又不夠。我們通常對整個網路均与套用 checkpointing，或者對最深的部分做 checkpointing。

## 與模型平行的結合

在模型平行的環境中，checkpointing 的策略需要調整。每一段只應存本地層的活化值。但當 backward 需要前面段的活化值時，需要通訊。可以設計分層 checkpointing 來最小化通訊。

## 實務建議

1. 先不做 checkpointing，測量實際記憶體使用
2. 從記憶體最緊張的層開始套用
3. 注意 checkpointing 會增加計算時間
4. 某些操作（如 dropout）在重新計算時需要設置 training mode

## 參考資源

- Gradient Checkpointing：https://www.google.com/search?q=gradient+checkpointing+memory+optimization
- Activation Recomputation：https://www.google.com/search?q=activation+recomputation+deep+learning