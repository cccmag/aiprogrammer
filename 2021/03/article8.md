# TensorCore 運算

## TensorCore 功能

TensorCore 是專為矩陣運算設計的硬體單元：

```cpp
// 使用 TensorCore 進行矩陣乘法
__half a[16][16], b[16][16], c[16][16];
// wmma 程式設計介面
#include <mma.h>

using namespace nvcuda::wmma;

fragment<matrix_a, 16, 16, 16, __half, row_major> frag_a;
fragment<matrix_b, 16, 16, 16, __half, col_major> frag_b;
fragment<accumulator, 16, 16, 16, __half> frag_c;

load_matrix_sync(frag_a, a, 16);
load_matrix_sync(frag_b, b, 16);
load_matrix_sync(frag_c, c, 16);

mma_sync(frag_c, frag_a, frag_b, frag_c);

store_matrix_sync(c, frag_c, 16, mem_row_major);
```

## 支援的精度

| 精度格式 | 說明 |
|----------|------|
| FP32 | 標準單精度 |
| FP16 | 半精度 |
| BF16 | Brain Float |
| TF32 | TensorFloat-32 |
| INT8 | 整數 |

## TF32 格式

TensorFloat-32 是 Ampere 引入的新格式：
- 10 位元尾數
- 8 位元指數
- 與 FP32 相同的範圍

## 混合精度訓練

```python
# PyTorch 混合精度
scaler = torch.cuda.amp.GradScaler()

with torch.cuda.amp.autocast():
    output = model(input)
    loss = criterion(output, target)

scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

---

## 延伸閱讀

- [TensorCore+介紹](https://www.google.com/search?q=NVIDIA+TensorCore+explained)
- [WMMA+程式設計](https://www.google.com/search?q=WMMA+CUDA+programming)
- [TF32+格式](https://www.google.com/search?q=TF32+TensorFloat+explained)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*