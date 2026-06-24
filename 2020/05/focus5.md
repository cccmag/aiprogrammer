# 5. NVIDIA A100 與 Ampere 架構

## A100 主要特性

2020 年 5 月發布的 NVIDIA A100 是資料中心 GPU 的旗艦產品：
- 7nm 製程（Ampere 架構）
- 312 TFLOPS (FP16, Tensor Core)
- 40GB HBM2 記憶體
- 1.6 TB/s 記憶體頻寬
- 第三代 NVLink

## Tensor Core 演進

A100 的 Tensor Core 支援更多資料格式：
- FP64 (64 位元浮點)
- FP32 (32 位元浮點)
- TF32 (Tensor Float 32)
- FP16 (16 位元浮點)
- BF16 (Brain Float 16)
- INT8, INT4

## TF32 格式

TF32 是 A100 引入的新格式：
- 指數位：8 位（與 FP32 相同）
- 尾數位：10 位（與 FP16 相同）
- 效能：比 FP32 快 8 倍，無需改變程式碼

## Multi-Instance GPU (MIG)

MIG 允許將 A100 分割為多個獨立實例：

```bash
# 查看 MIG 模式
nvidia-smi -i 0 -mig

# 啟用 MIG（需要在 DCGM 中設定）
nvidia-smi -i 0 -mig 1
```

每個實例有獨立的記憶體與運算單元，適用於多任務並行。

## NVLink 與 NVSwitch

第三代 NVLink 提供 600 GB/s 互連頻寬（每 GPU）。
多 GPU 訓練可大幅加速跨 GPU 通訊。

## A100 對深度學習的影響

| 任務 | V100 (2017) | A100 (2020) | 提升 |
|------|------------|-------------|------|
| BERT 訓練 | 8.5 ms/step | 2.2 ms/step | 3.9x |
| GPT-2 訓練 | 67 ms/step | 17 ms/step | 3.9x |
| 推理 (BERT) | 17 ms | 4 ms | 4.3x |

## 如何使用 A100

```python
import torch

# 確認 A100 是否可用
print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"Compute: {torch.cuda.get_device_capability(0)}")

# A100 自動使用 TF32
# 無需特別設定即可獲得加速
```

## 軟體支援

確保使用最新的驅動與 CUDA：
- CUDA 11.0+
- cuDNN 8.0+
- PyTorch 1.7+（建議 1.6+）

## 參考資源

- https://www.google.com/search?q=NVIDIA+A100+Ampere+architecture+specs+Tensor+Core+TF32+2020
- https://www.google.com/search?q=A100+vs+V100+performance+comparison+deep+learning+benchmark+2020
- https://www.google.com/search?q=MIG+Multi-Instance+GPU+A100+how+to+use+configuration