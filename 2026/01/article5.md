# PyTorch GPU 驗證

## 安裝 PyTorch

前往 PyTorch 官方網站選擇對應的配置：

```bash
# CUDA 12.1 版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 使用 conda（自動匹配 CUDA 版本）
conda install pytorch torchvision torchaudio cudatoolkit=12.1 -c pytorch -c nvidia
```

## GPU 可用性檢測

```python
import torch

# 基本檢測
print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"CUDA 版本: {torch.version.cuda}")
print(f"cuDNN 版本: {torch.backends.cudnn.version()}")
print(f"cuDNN 啟用: {torch.backends.cudnn.enabled}")
```

## 多 GPU 資訊

```python
if torch.cuda.is_available():
    print(f"GPU 數量: {torch.cuda.device_count()}")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
        print(f"  記憶體: {torch.cuda.get_device_properties(i).total_memory / 1e9:.1f} GB")
```

## 實際運算驗證

建立一個簡單的張量運算，確認 GPU 上的計算結果正確：

```python
# 在 GPU 上建立張量
x = torch.randn(1000, 1000).cuda()
y = torch.randn(1000, 1000).cuda()

# 執行矩陣乘法
z = torch.matmul(x, y)

# 確認結果在 GPU 上
print(f"張量所在裝置: {z.device}")
print(f"結果形狀: {z.shape}")

# 效能比較
import time

def bench(device, size=5000):
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)
    start = time.time()
    _ = torch.matmul(a, b)
    torch.cuda.synchronize() if device.type == 'cuda' else None
    return time.time() - start

cpu_time = bench(torch.device('cpu'), 2000)
gpu_time = bench(torch.device('cuda'), 2000)
print(f"CPU 耗時: {cpu_time:.3f}s | GPU 耗時: {gpu_time:.3f}s")
```

## 參考資源

- https://www.google.com/search?q=PyTorch+GPU+verification+check+code
- https://www.google.com/search?q=PyTorch+CUDA+benchmark+matrix+multiplication
