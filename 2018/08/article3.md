# GPU 加速：CUDA 與 cuDNN

## 1. CUDA 基礎

### 什麼是 CUDA？

CUDA（Compute Unified Device Architecture）是 NVIDIA 開發的平行運算平台和 API，讓開發者能使用 NVIDIA GPU 進行通用計算。

```python
import torch

# 檢查 CUDA 是否可用
print(torch.cuda.is_available())  # True/False
print(torch.cuda.device_count())  # GPU 數量
print(torch.cuda.get_device_name(0))  # GPU 名稱
```

## 2. 張量 GPU 操作

```python
# 建立 GPU 張量
x = torch.randn(1000, 1000).cuda()
# 或
x = torch.randn(1000, 1000, device='cuda')

# 移動到 GPU
model = model.cuda()
x = x.cuda()

# 移回 CPU
x = x.cpu()
```

## 3. 多 GPU 訓練

```python
# 資料平行
model = torch.nn.DataParallel(model)
model = model.cuda()

# 手動設定
torch.cuda.set_device(0)  # 選擇 GPU
```

## 4. CUDA 記憶體管理

```python
# 檢視記憶體使用
print(torch.cuda.memory_allocated() / 1024**2)  # MB
print(torch.cuda.memory_reserved() / 1024**2)

# 清除記憶體
del x
torch.cuda.empty_cache()

# 記憶體池
torch.cuda.empty_cache()  # 釋放未使用的記憶體
```

## 5. cuDNN 加速

```python
import torch.backends.cudnn as cudnn

# 啟用 cuDNN Benchmark（輸入尺寸固定時加速）
cudnn.benchmark = True

# 啟用 cuDNN 確定性模式
cudnn.deterministic = True

# 檢查是否啟用
print(cudnn.is_acceptable(x))
```

## 6. 效能比較

```python
import time

# CPU 矩陣乘法
x = torch.randn(2000, 2000)
y = torch.randn(2000, 2000)

start = time.time()
z = torch.matmul(x, y)
print(f"CPU: {time.time() - start:.4f}s")

# GPU 矩陣乘法
x = x.cuda()
y = y.cuda()

torch.cuda.synchronize()
start = time.time()
z = torch.matmul(x, y)
torch.cuda.synchronize()
print(f"GPU: {time.time() - start:.4f}s")
```

## 7. 常見錯誤

```python
# 錯誤：張量不在同一設備
x = torch.randn(3, 4).cuda()
y = torch.randn(3, 4)  # CPU
# z = x + y  # 會錯誤！

# 解決：確保在同一設備
y = y.cuda()
z = x + y  # 正確
```

## 8. 小結

GPU 加速是深度學習的關鍵。PyTorch 提供了簡潔的 CUDA 介面，只需幾行程式碼就能利用 GPU 的平行運算能力。

---

**參考資料**
- [CUDA Documentation](https://www.google.com/search?q=CUDA+documentation+NVIDIA)
- [PyTorch GPU Tutorial](https://www.google.com/search?q=PyTorch+GPU+tutorial+CUDA)