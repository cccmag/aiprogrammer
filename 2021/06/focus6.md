# Focus 6：張量平行與通訊優化

## 張量平行的概念

張量平行（Tensor Parallelism）是對單層進行分割的技術。以矩陣乘法為例：若 W 是大矩陣，可以將 W 分割為 [W1, W2]，在不同 GPU 上計算最後拼接。這種分割使單層的記憶體需求從 O(W) 減少到 O(W/N)。

## 矩陣乘法的分割

以線性層 Y = XA 為例。將 A 按列分割為 [A1, A2]，則 Y = [XA1, XA2]。每個 GPU 計算一部分，最終拼接結果。這種方式，每個 GPU 只需持有 A 的一部分，大幅減少記憶體。

## 通訊模式

張量平行引入了集合通訊。每個 forward pass 需要 AllGather 來組合結果，每個 backward pass 需要 ReduceScatter 來分割梯度。這些操作的通訊量與輸入大小和分割數量成正比。

## 與管線平行的比較

管線平行按層分割，張量平行按單層內部運算分割。張量平行實現更複雜，但能更高效地利用所有硬體。大模型訓練通常同時使用兩者：管線平行處理階段間的負載均衡，張量平行處理單層內的記憶體限制。

## 通訊優化策略

1. 使用 NCCL 而非 Gloo（GPU 間）
2. 融合小通訊操作為大操作
3. 使用非同步通訊隱藏延遲
4. 選擇合適的分割維度以最小化通訊

## 參考資源

- Megatron-LM：https://www.google.com/search?q=Megatron+tensor+parallelism
- Tensor Parallelism Tutorial：https://www.google.com/search?q=tensor+parallelism+deep+learning+implementation