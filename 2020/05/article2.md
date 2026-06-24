# PyTorch GPU 加速驗證

## 基本檢測

```python
import torch

print(f"CUDA 可用: {torch.cuda.is_available()}")
print(f"GPU 數量: {torch.cuda.device_count()}")

if torch.cuda.is_available():
    print(f"GPU 名稱: {torch.cuda.get_device_name(0)}")
    print(f"CUDA 版本: {torch.version.cuda}")
```

## 簡單矩陣運算驗證

```python
import torch
import time

def benchmark_matmul(size=4096):
    a = torch.randn(size, size).cuda()
    b = torch.randn(size, size).cuda()
    
    # 預熱
    for _ in range(10):
        _ = torch.matmul(a, b)
    
    # 計時
    start = time.time()
    for _ in range(100):
        _ = torch.matmul(a, b)
    elapsed = time.time() - start
    
    return elapsed / 100 * 1000  # ms

if torch.cuda.is_available():
    t = benchmark_matmul()
    print(f"矩陣乘法（4096x4096）平均時間: {t:.2f} ms")
else:
    print("CUDA 不可用")
```

## 簡單類神經網路驗證

```python
import torch
import torch.nn as nn

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(784, 256)
        self.fc2 = nn.Linear(256, 10)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

model = SimpleNet().to(device)
print(f"模型位於: {next(model.parameters()).device}")

# 測試前向傳播
x = torch.randn(32, 1, 28, 28).to(device)
output = model(x)
print(f"輸入形狀: {x.shape}")
print(f"輸出形狀: {output.shape}")
```

## 記憶體狀態

```python
import torch

if torch.cuda.is_available():
    # 已分配記憶體
    allocated = torch.cuda.memory_allocated(0) / 1024**3
    # 快取記憶體
    cached = torch.cuda.memory_reserved(0) / 1024**3
    # 最大已使用
    max_used = torch.cuda.max_memory_allocated(0) / 1024**3
    
    print(f"已分配: {allocated:.2f} GB")
    print(f"快取: {cached:.2f} GB")
    print(f"最大使用: {max_used:.2f} GB")
```

## 比較 CPU vs GPU

```python
import torch
import time

def compare_cpu_gpu():
    size = 2048
    iterations = 50
    
    # CPU
    a = torch.randn(size, size)
    b = torch.randn(size, size)
    
    start = time.time()
    for _ in range(iterations):
        _ = torch.matmul(a, b)
    cpu_time = time.time() - start
    
    # GPU
    a = a.cuda()
    b = b.cuda()
    
    for _ in range(10):  # 預熱
        _ = torch.matmul(a, b)
    
    start = time.time()
    for _ in range(iterations):
        _ = torch.matmul(a, b)
    gpu_time = time.time() - start
    
    print(f"CPU 時間: {cpu_time:.3f}s")
    print(f"GPU 時間: {gpu_time:.3f}s")
    print(f"加速比: {cpu_time/gpu_time:.1f}x")

compare_cpu_gpu()
```

## Multi-GPU 檢測

```python
import torch

if torch.cuda.device_count() > 1:
    print(f"使用 {torch.cuda.device_count()} GPUs")
    for i in range(torch.cuda.device_count()):
        print(f"GPU {i}: {torch.cuda.get_device_name(i)}")
```

## 參考資源

- https://www.google.com/search?q=PyTorch+GPU+verification+CUDA+memory+check+tutorial+2020
- https://www.google.com/search?q=CPU+vs+GPU+PyTorch+benchmark+performance+comparison
- https://www.google.com/search?q=torch.cuda+memory+allocated+reserved+max+memory+tracking