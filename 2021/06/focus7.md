# Focus 7：混合精度訓練與效能調優

## 混合精度的動機

記憶體和頻寬是訓練的兩大瓶頸。使用較低精度（如 FP16）可以：
1. 減少記憶體使用（理論上 2x，實際約 1.5x）
2. 增加運算吞吐量（現代 GPU 的 Tensor Core 對 FP16 有硬體加速）
3. 減少通訊量

混合精度訓練使用低精度計算梯度，但用 FP32 保存權重和優化器狀態，保證模型精度。

## FP16 vs BF16

FP16（半精度浮點）只有 10 位尾數，動態範圍有限。BF16（BFloat16）有 8 位尾數但 8 位指數，動態範圍與 FP32 相當。理論上 BF16 更穩定，適合大模型的混合精度訓練。2021 年，越來越多的大模型訓練採用 BF16。

## loss scaling

FP16 的動態範圍較窄，直接使用可能導致下溢。解決方案是 loss scaling：在 forward pass 放大 loss，backward pass 前縮小回來。常用策略是動態調整：當梯度出現下溢時提高 scale，正常時逐步降低。

## 實作要點

1. 使用 torch.cuda.amp 自动處理精度轉换
2. 確保某些操作（如 softmax）在 FP32 中執行以保持精度
3. 注意 BatchNorm 的統計量應在 FP32 中計算
4. 監控是否有梯度下溢（torch.cuda.amp 提供相關 API）

## 效能調優總結

1. 混合精度 + 梯度 checkpointing 通常標配
2. 使用 bucketing 和非同步通訊
3. 選擇合適的 batch size（通常 2 的冪次）
4. 使用 Profiler 找出瓶頸針對性優化

## 參考資源

- Mixed Precision Training：https://www.google.com/search?q=mixed+precision+training+pytorch
- BF16 vs FP16：https://www.google.com/search?q=BF16+FP16+deep+learning+precision