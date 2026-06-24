# AI 硬體：GPU 與深度學習

## 前言

GPU 是深度學習發展的關鍵硬體基礎，了解 GPU 對於最佳化訓練非常重要。

## CPU vs GPU

```python
# CPU: 少量強大核心
# GPU: 大量較弱核心，擅長並行計算

# 矩陣乘法對比
# CPU: O(n^3) 但單執行緒強
# GPU: O(n^3) 但並行執行
```

## CUDA 基礎

```bash
# 安裝 NVIDIA 驅動和 CUDA
nvidia-smi  # 查看 GPU 狀態
```

```python
import torch

# 檢查 GPU
print(torch.cuda.is_available())
print(torch.cuda.device_count())

# 移動到 GPU
model = model.cuda()
images = images.cuda()

# 回到 CPU
model = model.cpu()
```

## GPU 記憶體管理

```python
# 查看記憶體
print(torch.cuda.memory_allocated())
print(torch.cuda.memory_reserved())

# 清理
torch.cuda.empty_cache()
del model
torch.cuda.empty_cache()
```

## 多 GPU 訓練

```python
# 資料並行
model = nn.DataParallel(model)

# 多 GPU
model = nn.DataParallel(model, device_ids=[0, 1, 2])
```

## 選擇 GPU

| GPU | 記憶體 | 適合場景 |
|-----|--------|---------|
| RTX 2080 Ti | 11GB | 個人研究 |
| V100 | 16/32GB | 大規模訓練 |
| TITAN RTX | 24GB | 個人最高性能 |

## 延伸閱讀

- [NVIDIA 深度學習文檔](https://www.google.com/search?q=NVIDIA+deep+learning+guide)
- [CUDA 編程指南](https://www.google.com/search?q=cuda+programming+guide)