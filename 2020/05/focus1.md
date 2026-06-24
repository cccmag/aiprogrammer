# 1. CUDA 程式設計基礎

## CUDA 簡介

CUDA（Compute Unified Device Architecture）是 NVIDIA 開發的平行運算平台與程式模型。透過 CUDA，開發者可以使用 C、C++、Python 等語言直接操控 GPU 進行高效能運算。

## 基本概念

### 主機端與設備端

- **主機端（Host）**：CPU 記憶體與處理器
- **設備端（Device）**：GPU 記憶體與處理器
- 資料需要在主機端與設備端之間傳輸

### 執行模型

```python
import torch

# 確認 CUDA 可用
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
print(f"GPU name: {torch.cuda.get_device_name(0)}")

# 將張量移到 GPU
x = torch.randn(1000, 1000)
x_gpu = x.cuda()  # 或 x.to("cuda")

# 在 GPU 上運算
y_gpu = torch.matmul(x_gpu, x_gpu)
```

## CUDA 核心 (Kernel)

CUDA 核心是在 GPU 上並行執行的函數：

```python
# PyTorch 的底層其實使用了 CUDA
output = torch.nn.functional.relu(input)  # 會在 GPU 上執行
```

## 常見錯誤

1. **CUDA out of memory**：記憶體不足，需減少批次大小或使用梯度累積
2. **GPU not available**：檢查驅動與 CUDA 安裝
3. **数据类型不匹配**：確保 CPU 與 GPU 使用相同的 dtype

## nvidia-smi 指令

```bash
# 查看 GPU 狀態
nvidia-smi

# 即時監控
watch -n 1 nvidia-smi

# 查看特定 GPU
nvidia-smi -i 0
```

## 記憶體監控

```python
import torch

def print_gpu_memory():
    if torch.cuda.is_available():
        allocated = torch.cuda.memory_allocated(0) / 1024**3
        cached = torch.cuda.memory_reserved(0) / 1024**3
        print(f"GPU 記憶體：已分配 {allocated:.2f} GB，快取 {cached:.2f} GB")

print_gpu_memory()
```

## 參考資源

- https://www.google.com/search?q=CUDA+programming+PyTorch+GPU+basics+tutorial+2020
- https://www.google.com/search?q=CUDA+memory+management+torch.cuda+tips+tricks
- https://www.google.com/search?q=nvidia-smi+GPU+monitoring+memory+usage+commands