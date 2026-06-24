# 深度學習硬體：GPU 選購指南

## 1. 為什麼深度學習需要 GPU？

GPU 的並行運算能力遠超 CPU：

```python
# CPU 矩陣乘法
import numpy as np
a = np.random.randn(1000, 1000)
b = np.random.randn(1000, 1000)
%timeit np.dot(a, b)
# ~200ms on CPU

# GPU（CUDA）矩陣乘法
import cupy as cp
a_gpu = cp.asarray(a)
b_gpu = cp.asarray(b)
%timeit cp.dot(a_gpu, b_gpu)
# ~5ms on GPU（速度提升 ~40x）
```

## 2. NVIDIA GPU 架構

| 架構 | 發布年份 | 代表型號 | Tensor Core |
|------|----------|----------|-------------|
| Maxwell | 2015 | GTX 900 系列 | 無 |
| Pascal | 2016 | GTX 1000 系列 | 無 |
| Volta | 2017 | V100 | 有 |
| Turing | 2018 | RTX 2000 系列 | 有 |

## 3. 2018 年推薦 GPU

### 消費級

| 型號 | 記憶體 | 張量核心 | 建議場景 |
|------|--------|----------|----------|
| GTX 1080 Ti | 11GB | 無 | 個人研究、性價比 |
| RTX 2080 Ti | 11GB | 有 | 最佳消費級效能 |
| GTX 1080 | 8GB | 無 | 預算有限 |

### 專業級

| 型號 | 記憶體 | 張量核心 | 建議場景 |
|------|--------|----------|----------|
| V100 | 16GB | 有 | 大規模訓練、論文研究 |
| P100 | 16GB | 無 | 標準深度學習 |
| P40 | 24GB | 無 | 大模型推論 |

## 4. CUDA 與 cuDNN

```bash
# 安裝 CUDA
wget https://developer.nvidia.com/compute/cuda/9.0/Prod/local_installers/cuda_9.0.176_384.81_linux-run
sudo sh cuda_9.0.176_384.81_linux-run

# 安裝 cuDNN
# 下載 cudnn-9.0-linux-x64-v7.tgz
tar -xzvf cudnn-9.0-linux-x64-v7.tgz
sudo cp cuda/include/* /usr/local/cuda/include/
sudo cp cuda/lib64/* /usr/local/cuda/lib64/
```

## 5. 多 GPU 設定

```python
# TensorFlow 分散式訓練
mirrored_strategy = tf.distribute.MirroredStrategy(
    devices=["/gpu:0", "/gpu:1", "/gpu:2", "/gpu:3"]
)

with mirrored_strategy.scope():
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
```

## 6. 記憶體需求估算

```python
# 模型記憶體估算
def estimate_memory(model):
    total_params = 0
    for layer in model.trainable_weights:
        total_params += np.prod(layer.shape)
    
    # 假設 float32（4 bytes）
    param_memory = total_params * 4 / (1024 ** 2)  # MB
    
    # 訓練時需要約 4 倍記憶體（梯度、優化器狀態等）
    total_memory = param_memory * 4
    
    return param_memory, total_memory

# 估算
# 100M 參數：~400MB（模型）+ ~1.6GB（訓練）= ~2GB
```

## 7. 雲端 GPU 選項

| 服務 | GPU 選項 | 價格（$/小時） |
|------|----------|----------------|
| AWS | V100, P3, G3 | 3-31 |
| Google Cloud | V100, P100, TPU | 1.5-30 |
| FloydHub | V100, P100 | 0.5-4 |
| Paperspace | V100, P5000 | 0.5-3 |

## 8. 小結

2018 年是深度學習硬體爆發的一年，RTX 系列和 V100 讓一般研究者也能使用高效能 GPU。選擇 GPU 時應考慮：記憶體大小、Tensor Core 支援、性價比。

---

**參考資料**
- [GPU Benchmarks for Deep Learning 2018](https://www.google.com/search?q=GPU+benchmark+deep+learning+2018)
- [CUDA Installation Guide](https://www.google.com/search?q=CUDA+installation+tensorflow+2018)