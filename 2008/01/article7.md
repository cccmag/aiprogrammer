# GPU 運算與平行處理

## 前言

2008 年是 GPU 運算的轉捩點。NVIDIA 的 CUDA 平台和 ATI 的 Stream 技術讓研究者開始使用顯示晶片進行通用運算，這對人工智慧的發展產生了深遠的影響。

## GPU 的歷史演進

### 從遊戲到運算

GPU（Graphics Processing Unit）原本是為了電腦繪圖而設計：

```
GPU 發展時間線：

1995：3D 遊戲興起，GPU 需求浮現
1999：NVIDIA GeForce 256，第一個消費級 GPU
2001：Shader 技術出現，可程式化繪圖管線
2006：NVIDIA CUDA 發布，通用運算可能
2008：GPU 運算開始普及於學術研究
```

### GPU vs CPU 架構

| 特性 | CPU | GPU |
|------|-----|-----|
| 核心數 | 2-8 | 數百到數千 |
| 執行緒 | 少 | 非常多 |
| 快取 | 大 | 小 |
| 彈性 | 高 | 低 |
| 適合 | 順序執行 | 平行運算 |

```
CPU 架構：                    GPU 架構：
┌─────────────┐            ┌─────────────┐
│  Cache  大   │            │  Cache 小   │
├─────────────┤            ├─────────────┤
│ ┌───┐ ┌───┐ │            │┌─┐┌─┐┌─┐┌─┐┌─┐│
│ │Core│ │Core│ │            ││ ││ ││ ││ ││ │
│ └───┘ └───┘ │            │└─┘└─┘└─┘└─┘└─┘│
│ ┌───┐ ┌───┐ │            │┌─┐┌─┐┌─┐┌─┐┌─┐│
│ │Core│ │Core│ │            ││ ││ ││ ││ ││ │
│ └───┘ └───┘ │            │└─┘└─┘└─┘└─┘└─┘│
└─────────────┘            └─────────────────┘
  少量強核心                  多量弱核心
```

## CUDA 的興起

### CUDA 簡介

CUDA（Compute Unified Device Architecture）是 NVIDIA 於 2006 年發布的平行運算平台：

```python
# CUDA 概念示意（Python + CUDA語法概念）
# 這不是實際可執行的程式碼，而是概念展示

# 主機端程式碼（CPU）
def main():
    # 配置 GPU
    initialize_gpu()

    # 準備資料
    data = load_data()
    data_gpu = copy_to_gpu(data)

    # 執行 GPU 核心
    result_gpu = gpu_kernel(data_gpu, blocks=100, threads=256)

    # 取回結果
    result = copy_from_gpu(result_gpu)

# GPU 核心函數（顯示卡執行）
__global__ def gpu_kernel(data, blocks, threads):
    # 每個執行緒計算一個元素
    idx = blockIdx.x * blockDim.x + threadIdx.x
    data[idx] = process(data[idx])
```

### CUDA 程式模型

```
CUDA 程式模型：

主機端（CPU）                  裝置端（GPU）
┌─────────────────┐          ┌─────────────────┐
│  主程式         │   ──→   │  GPU 核心函數   │
│  記憶體配置     │  資料   │  平行執行       │
│  核心啟動       │  ──→   │                 │
│  結果取回       │  結果   │                 │
└─────────────────┘          └─────────────────┘
```

## GPU 運算的優勢

### 效能比較

GPU 在特定任務上的效能遠超 CPU：

| 運算類型 | GPU 加速比 |
|----------|-----------|
| 矩陣乘法 | 10-100x |
| 類神經網路訓練 | 10-50x |
| 物理模擬 | 20-200x |
| 影像處理 | 10-50x |

### 為何 GPU 適合平行運算？

```python
# GPU 適合的運算模式

suitable_patterns = {
    "資料平行": "相同的運算套用到大量資料",
    "任務平行": "獨立的任務同時執行",
    "SIMD": "單一指令多筆資料",
    "運算密集": "計算量大，記憶體存取少"
}

# 類神經網路的矩陣運算正是這種模式
# y = W * x 對每個輸出都是獨立的計算
```

## GPU 與類神經網路

### 早期類神經網路的限制

在 GPU 運算普及之前，類神經網路的訓練受到硬體限制：

```python
# 1990s-2000s 類神經網路訓練的限制
limitations = {
    "訓練時間": "大型網路需要數天到數週",
    "網路規模": "受限於記憶體和計算力",
    "資料規模": "無法處理海量資料",
    "迭代次數": "受時間限制無法充分訓練"
}
```

### GPU 改變了一切

```
GPU 運算帶來的改變：

以前（純 CPU）：
- 100萬筆資料訓練時間：數天
- 網路規模：數十萬參數
- 可訓練的網路深度：3-4 層

現在（GPU 加速）：
- 100萬筆資料訓練時間：數小時
- 網路規模：數億參數
- 可訓練的網路深度：數十層到數百層
```

## 深度學習的硬體基礎

### GPU 讓深度學習成為可能

深度學習的三大要素：

```python
deep_learning_elements = {
    "資料": "大規模標註資料（ImageNet 等）",
    "演算法": "深度網路、反向傳播、ReLU 等",
    "算力": "GPU 運算能力"  # ← GPU 在此扮演關鍵角色
}
```

### 時間軸

| 年份 | 事件 | 意義 |
|------|------|------|
| 2006 | NVIDIA 發布 CUDA | GPU 通用運算開端 |
| 2007 | CUDA 1.0 發布 | 生態系統建立 |
| 2008 | GPU 運算開始普及 | 研究社群採用 |
| 2009 | GPU 被用於深度學習 | 深度學習硬體基礎 |
| 2012 | AlexNet 使用 GPU | 深度學習突破 |

## 實際應用場景

### 語音辨識

2008 年前後，語音辨識研究開始使用 GPU：

```python
# 語音辨識中的 GPU 應用
speech_recognition_pipeline = {
    "特徵提取": "MFCC → GPU 加速",
    "聲學模型": "深度類神經網路 → GPU 訓練",
    "語言模型": "神經網路 → GPU 訓練",
    "解碼": "Viterbi → GPU 加速"
}
```

### 影像辨識

影像處理是 GPU 的傳統強項：

```python
# 影像處理的 GPU 加速
image_processing_operations = [
    "卷積（Convolution）",
    "池化（Pooling）",
    "正規化（Normalization）",
    "邊緣偵測（Edge Detection）"
]

# 這些都是 GPU 擅長的運算
```

## 平行計算的基礎概念

### 任務分配

```
GPU 工作分配：

主機（CPU）：
- 任務協調
- 資料傳輸
- 邏輯控制

GPU：
- 大量平行計算
- 矩陣運算
- 圖形處理
```

### 記憶體層級

```python
memory_hierarchy = {
    "GPU 暫存器": "最快，執行緒私有",
    "Shared Memory": "區塊內共享",
    "Global Memory": "全部執行緒可見，較慢",
    "主機記憶體": "需透過匯流排傳輸，最慢"
}

# 最佳化記憶體使用是 GPU 程式設計的關鍵
```

## 未來展望

### 2008 年的未來預測

```
GPU 運算的發展趨勢（2008 預測）：

短期（2008-2010）：
- GPU 運算更加普及
- CUDA 生態系統成熟
- 更多領域採用

中期（2010-2015）：
- 深度學習成為主流
- 專業 AI 硬體出現
- 雲端 GPU 服務

長期（2015+）：
- TPU 等 AI 專用晶片
- 邊緣運算普及
- 神經網路硬體一體化
```

### 其他運算加速技術

GPU 之外還有其他選項：

| 技術 | 優點 | 缺點 |
|------|------|------|
| GPU (CUDA) | 生態完整 | 功耗高 |
| FPGA | 可客製化 | 開發困難 |
| Cell BE | 效能高 | 程式設計複雜 |
| 多核心 CPU | 易用 | 平行度有限 |

---

**延伸閱讀**

- [GPU computing history](https://www.google.com/search?q=GPU+computing+history)
- [CUDA+programming+guide](https://www.google.com/search?q=CUDA+programming+guide)
- [GPU+neural+network+training](https://www.google.com/search?q=GPU+neural+network+training)