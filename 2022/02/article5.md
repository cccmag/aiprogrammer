# 混合精度訓練 FP16

## 使用半精度浮點數加速訓練而不損失準確度

### 為什麼需要混合精度

深度學習訓練的預設資料型別是 FP32（32-bit 單精度浮點數）。但研究發現，許多神經網路可以在 FP16（16-bit 半精度）下正常收斂，同時獲得顯著的效能提升：

- **記憶體減半**：FP16 張量大小是 FP32 的一半，意味著同 GPU 記憶體可以訓練更大的模型
- **計算加速**：Tensor Core 的 FP16 吞吐量是 FP32 的 2-8 倍（取決於 GPU 架構）
- **頻寬節省**：資料傳輸量減半，減少記憶體頻寬瓶頸

### FP16 的限制

然而，直接使用 FP16 訓練並非沒有代價。FP16 有兩個主要問題：

**範圍限制**：FP16 可表示的最大值約 65504，最小正規化數約 6.1e-5。梯度值很容易超出這個範圍（特別是在訓練初期），導致 underflow 或 overflow。

**精度不足**：FP16 的有效精度約 3.3 位十進制數。在累加運算（如 loss 累加）中，小數部分容易被截斷。

### 混合精度策略

NVIDIA 提出的混合精度訓練（Mixed Precision Training）解決方案：

```
Forward pass:         FP16 （加速矩陣乘法）
  └→ 輸入和權重轉換為 FP16
  └→ 矩陣乘法在 Tensor Core 上以 FP16 執行
  └→ 累加結果以 FP32 保留

Loss 計算:            FP32 （保留精度）
  └→ loss value 始終以 FP32 儲存

Backward pass:        FP16 （加速梯度計算）
  └→ 梯度以 FP16 計算
  └→ 使用 Gradient Scaling 避免 underflow

權重更新:             FP32 （保留權重精度）
  └→ master copy of weights 始終為 FP32
  └→ FP16 梯度轉為 FP32 後更新 master weights
```

### Loss Scaling

Loss Scaling 是混合精度訓練的關鍵技術。訓練過程中，梯度值可能很小，在 FP16 中會 underflow 為 0。解決方案是在 backward 之前將 loss 放大（scale）：

```python
scaler = torch.cuda.amp.GradScaler(
    init_scale=2**16,   # 初始縮放因子 65536
    growth_factor=2.0,  # 無 overflow 時每步倍增
    backoff_factor=0.5, # 發生 overflow 時減半
    growth_interval=2000
)
```

GradScaler 的工作流程：

1. `scaler.scale(loss)`：將 loss 乘以 scale factor
2. `backward()`：計算 scaled 梯度
3. `scaler.step(optimizer)`：將梯度 unscaled 後更新權重
4. `scaler.update()`：根據是否發生 overflow 調整 scale factor

### Tensor Core 與 FP16

Tensor Core 是混合精度訓練的硬體基礎。在 A100 上：

```python
# TF32（預設模式，兼容 FP32 介面）
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True

# 使用 FP16 強制 Tensor Core
with torch.cuda.amp.autocast(dtype=torch.float16):
    output = model(input)
```

autocast 會自動選擇每個操作的最佳精度：矩陣乘法使用 FP16，歸一化和 softmax 使用 FP32。

### 實際加速效果

混合精度訓練的加速效果取決於模型和 GPU：

| 模型 | V100 FP32 | V100 AMP | A100 FP32 | A100 AMP |
|-----|-----------|----------|-----------|----------|
| ResNet-50 | 200 img/s | 320 img/s | 400 img/s | 800 img/s |
| BERT-Large | 80 seq/s | 140 seq/s | 200 seq/s | 380 seq/s |
| GPT-2 | 60K tok/s | 110K tok/s | 150K tok/s | 280K tok/s |

典型加速比為 1.5x-2x，在支援 Tensor Core 的 GPU 上更顯著。

### 注意事項

- **不是所有 GPU 支援**：需要 Volta 架構（V100）或更新
- **Batch size 可能需調整**：FP16 的精度限制可能使大 batch 訓練不穩定
- **特定層需 FP32**：BatchNorm、LayerNorm 等歸一化層建議保持 FP32
- **監控 overflow**：定期檢查是否發生梯度 overflow

### 延伸閱讀

- [Mixed Precision Training (NVIDIA)](https://www.google.com/search?q=NVIDIA+mixed+precision+training)
- [AMP: Automatic Mixed Precision](https://www.google.com/search?q=PyTorch+automatic+mixed+precision)
