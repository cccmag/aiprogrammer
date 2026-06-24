# NVIDIA Ampere 架構

## Ampere 概述

NVIDIA Ampere 架構於 2020 年發布，是 Turing 架構的後繼者，带來顯著效能提升：

### A100 Tensor Core GPU

| 規格 | 數值 |
|------|------|
| 晶体管數 | 542 億 |
| CUDA 核心 | 6912 |
| Tensor Core | 432 |
| 記憶體 | 40GB HBM2 |
| 頻寬 | 1.6 TB/s |

### 关键创新

1. **第三代 Tensor Core**
   - 支援 TF32、BF16、FP64
   - 加速矩陣運算

2. **結構化稀疏**
   - 硬體支援的稀疏運算
   - 兩倍吞吐量

3. **MIG（Multi-Instance GPU）**
   - 分割 GPU 為多個實例
   - 更好的資源利用

## RTX 30 系列

| 型號 | RTX 3090 | RTX 3080 | RTX 3070 |
|------|----------|----------|----------|
| CUDA 核心 | 10496 | 8704 | 5888 |
| 記憶體 | 24GB | 10GB | 8GB |
| 記憶體類型 | GDDR6X | GDDR6X | GDDR6 |

## 與前代比較

```
效能提升（相較 Turing）：
- 深度學習訓練：提升 6 倍
- 光線追蹤：提升 2 倍
- 張量運算：提升 2 倍
```

---

## 延伸閱讀

- [Ampere+架構白皮書](https://www.google.com/search?q=NVIDIA+Ampere+whitepaper+A100)
- [RTX+30系列規格](https://www.google.com/search?q=RTX+3090+3080+3070+specs)
- [TensorCore+詳解](https://www.google.com/search?q=NVIDIA+TensorCore+explained)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*