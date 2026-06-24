# CUDA 核心優化技巧

## 記憶體對齊

確保張量記憶體對齊以提高傳輸效率：

```python
# 錯誤：可能導致記憶體不連續
x = torch.randn(3, 5).cuda()

# 正確：明確對齊
x = torch.randn(3, 4).cuda()  # 4 是 16 的倍數

# 確保連續
x = x.contiguous()
```

## 融合運算

將多個運算融合減少記憶體訪問：

```python
# 原始做法（多次記憶體訪問）
x = layer1(input)
x = relu(x)
x = layer2(x)

# 融合做法（使用 Fused）
import torch.nn.functional as F
x = F.linear(input, weight1, bias1)
x = F.relu(x)
x = F.linear(x, weight2, bias2)
```

## 避免不必要的複製

```python
# 錯誤：創建新張量
x = x.cuda()  # 可能複製

# 正確：使用 to() 方法
x = x.to(device)  # 更加明確

# 避免重複 transpose
x = x.permute(0, 2, 1).contiguous().transpose(0, 2)  # 糟糕
x = x.T  # 更好
```

## 使用就地運算

```python
# 原始做法
x = x + y

# 原地做法（可能加速）
x.add_(y)  # 注意：並非所有情況都適用
```

## 批次維度優先

GPU 運算在批次維度上更高效：

```python
# 較慢：處理多個獨立樣本
for i in range(batch_size):
    output[i] = model(input[i])

# 較快：批次處理
output = model(inputs)  # 一次處理整個批次
```

## 快取啟用

```python
# 啟用 cuDNN 基準測試
torch.backends.cudnn.benchmark = True

# 啟用 TF32（在 A100 上）
torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
```

## 記憶體池

```python
# 使用 CUDA 記憶體池
torch.cuda.empty_cache()  # 釋放快取

# 檢視記憶體使用
print(torch.cuda.memory_summary())
```

## 工具與分析

```python
# NVIDIA Nsight Systems
# 命令列分析
# nsys profile -o output python train.py

# PyTorch Profiler
with torch.profiler.profile(
    activities=[
        torch.profiler.ProfilerActivity.CPU,
        torch.profiler.ProfilerActivity.CUDA,
    ],
    record_shapes=True,
) as prof:
    model(input)

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```

## 參考資源

- https://www.google.com/search?q=CUDA+optimization+techniques+memory+access+fusion+2020
- https://www.google.com/search?q=PyTorch+performance+tuning+profiling+nsight+benchmark
- https://www.google.com/search?q=cudnn+benchmark+TF32+A100+optimization+settings