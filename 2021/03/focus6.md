# GPU 叢集運算

## 多 GPU 訓練

### 同一節點多卡

```python
import torch

# 資料平行
model = torch.nn.DataParallel(model, device_ids=[0, 1, 2, 3])
output = model(input)
```

### NCCL 通訊

```python
import torch.distributed as dist

dist.init_process_group(backend="nccl")
model = torch.nn.parallel.DistributedDataParallel(model)
```

## NVLink 互連

| 顯示卡組合 | NVLink 頻寬 |
|-----------|-------------|
| RTX 3090 x2 | 100 GB/s |
| A100 x4 | 200 GB/s |

## 叢集架構

```
       CPU
        │
    InfiniBand / NVLink
       /     \     \
    GPU 1  GPU 2  GPU 3 ...
```

## MPI 基礎

```cpp
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);

    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);

    printf("Rank %d of %d\n", rank, size);

    MPI_Finalize();
    return 0;
}
```

## 效能考量

1. **通訊與計算重疊**
2. **減少資料傳輸**
3. **負載平衡**

---

## 延伸閱讀

- [Multi-GPU+訓練教學](https://www.google.com/search?q=PyTorch+multi-GPU+training)
- [NCCL+使用說明](https://www.google.com/search?q=NCCL+distributed+training)
- [NVLink+介紹](https://www.google.com/search?q=NVLink+technology+explained)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*