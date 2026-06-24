# 梯度檢查點

## 什麼是梯度檢查點

梯度檢查點（Gradient Checkpointing）是一種以時間換取空間的記憶體最佳化技術。在反向傳播時，標準做法會儲存所有中間活化值（activations）以供梯度計算。梯度檢查點則選擇性地捨棄部分中間結果，在需要時重新計算。

## 運作原理

前向傳播時，模型會選取某些層作為檢查點（checkpoint）。通過檢查點時儲存輸入值，捨棄之後的中間活化值。反向傳播時，從最近的檢查點重新計算中間結果，然後計算梯度。

## 記憶體節省分析

對於一個有 N 層的網路，原始的活化值記憶體開銷為 O(N)。使用梯度檢查點後，記憶體開銷降至 O(sqrt(N)) 或 O(log N)，具體取決於檢查點的放置策略。

## 計算開銷

每個被捨棄的中間結果需要在反向傳播時重新計算一次，因此約增加一次前向傳播的計算量。實際開銷約為訓練總計算量的 20-30%。

## 應用場景

梯度檢查點特別適合：
- 視覺模型中的 U-Net、ResNet
- Transformer 模型中的長序列
- 需要加大 batch size 時
- GPU 記憶體有限但訓練時間非關鍵因素的場景

## PyTorch 實作

```python
from torch.utils.checkpoint import checkpoint
output = checkpoint(model.block, input)
```

使用 `checkpoint` 函數包裝需要檢查點的模組。支援自訂保存與捨棄哪些中間結果。

## 與其他技術的搭配

梯度檢查點可與 FSDP、ZeRO 等技術聯合使用，進一步降低記憶體需求。當 FSDP 將參數分片後，配合檢查點可訓練比單純 FSDP 更大的模型。

[搜尋梯度檢查點 PyTorch](https://www.google.com/search?q=gradient+checkpointing+PyTorch)
[搜尋 activation checkpointing 記憶體](https://www.google.com/search?q=activation+checkpointing+memory+saving)
