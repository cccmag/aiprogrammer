# GPU 硬體架構

## Streaming Multiprocessor（SM）

SM 是 GPU 的基本運算單元：

```
每個 SM 包含：
- CUDA 核心（運算單元）
- 暫存器檔案
- 共享記憶體
- L1 緩存
- 調度單元
```

### A100 SM 結構

| 組件 | 數量 |
|------|------|
| CUDA 核心 | 64 |
| Tensor Core | 4 |
| 共享記憶體 | 164KB |
| L1 緩存 | 192KB |

## 記憶體階層

```
全域記憶體（GDDR/HBM）
    ↓ 延遲 ~400-800 cycles
L2 緩存（每 GPC 共享）
    ↓ 延遲 ~100 cycles
L1 緩存（每 SM）
    ↓ 延遲 ~10 cycles
共享記憶體
    ↓ 延遲 ~1 cycle
暫存器
```

## 硬體執行模型

- **SIMT**：單指令多執行緒
- **Warp 調度**：每 SM 每時鐘週期選擇一個 Warp
- **指令流水線**：多指令同時執行

---

## 延伸閱讀

- [GPU+硬體架構詳解](https://www.google.com/search?q=NVIDIA+GPU+architecture+explained)
- [SM+結構介紹](https://www.google.com/search?q=streaming+multiprocessor+CUDA)
- [記憶體層級](https://www.google.com/search?q=GPU+memory+hierarchy)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*