# Deep Learning 硬體革命：GPU 運算時代來臨

## 前言

2007 年，NVIDIA 發布了 CUDA 1.0，這是一個改變機器學習歷史的決定。GPU 的平行運算能力，讓深度學習的訓練速度提升了數十倍。

## CUDA 與機器學習

### GPU 的平行優势

GPU 適合深度學習的原因：

```
GPU vs CPU 運算比較：
─────────────────────────
項目          GPU          CPU
─────────────────────────────
核心數        數百-數千    數個
執行緒數      數萬         數十
記憶體頻寬    高           中
FP16/FP32     原生支援     有限
功耗          高           中
─────────────────────────────
```

### CUDA 基本概念

```c
// CUDA 核心函數：向量加法
__global__ void vectorAdd(float *a, float *b, float *c, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        c[i] = a[i] + b[i];
    }
}

// 主程式呼叫
int main() {
    // 配置執行參數
    int blockSize = 256;
    int numBlocks = (n + blockSize - 1) / blockSize;

    // 核心呼叫
    vectorAdd<<<numBlocks, blockSize>>>(d_a, d_b, d_c, n);
}
```

## 深度學習框架的 GPU 支援

### Theano（2007 年）

Theano 是最早支援 GPU 的深度學習框架之一：

```python
import theano
from theano import function, tensor as T

# 啟用 GPU
theano.config.device = 'gpu'
theano.config.floatX = 'float32'

# 定義計算
a = T.matrix('a')
b = T.matrix('b')
c = a + b

f = function([a, b], c)
```

## GPU 對深度學習的影響

### 訓練速度的提升

```
GPU 加速效果（ImageNet 訓練時間）：
──────────────────────────────────
年份    單一 CPU    GPU         加速倍數
──────────────────────────────────
2006    數週        -           1x
2007    數週        數天        ~10x
2009    數天        數小時      ~50x
2012    數小時      分鐘        ~100x
──────────────────────────────────
```

## 結語

GPU 運算的興起，是深度學習能夠成功的關鍵因素之一。從 2007 年的 CUDA 1.0，到今天的張量處理器（TPU），硬體創新持續推動 AI 的進步。

---

## 延伸閱讀

- [CUDA+1.0+2007+NVIDIA](https://www.google.com/search?q=CUDA+1.0+2007+NVIDIA)
- [GPU+deep+learning+revolution](https://www.google.com/search?q=GPU+deep+learning+revolution)

---