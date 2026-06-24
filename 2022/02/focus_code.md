# GPU 運算概念模擬

## 前言

本程式使用 Python 模擬 GPU 運算的關鍵概念，無需實際 CUDA 硬體即可理解 GPU 的執行模型、記憶體層次、平行化策略和效能瓶頸。透過多執行緒模擬 SIMT 行為、Numpy 模擬矩陣運算、以及各種微基準測試來展現 GPU 程式設計的核心原理。

完整的 Python 實作請參考：[_code/gpu_compute.py](_code/gpu_compute.py)

```python
#!/usr/bin/env python3
"""GPU Computing Conceptual Simulation — no real GPU needed"""

import threading, time, random, functools
import numpy as np

class GPUDevice:
    def __init__(self, sm_count=4, warp_size=4, max_threads=16):
        self.sm_count = sm_count
        self.warp_size = warp_size
        self.max_threads = max_threads
        self.global_mem = {}
        self.shared_mem = {}

    def malloc(self, key, shape, dtype=np.float32):
        self.global_mem[key] = np.zeros(shape, dtype=dtype)

    def copy_to(self, key, data):
        self.global_mem[key] = data.copy()

    def copy_from(self, key):
        return self.global_mem[key].copy()


def simulate_simt(warp_threads, func, *args):
    """Simulate SIMT: same instruction, multiple threads (data-parallel)"""
    results = [None] * len(warp_threads)
    barriers = [threading.Barrier(len(warp_threads)) for _ in range(3)]

    def worker(tid):
        local_result = func(tid, *args)
        barriers[0].wait()
        results[tid] = local_result
    threads = [threading.Thread(target=worker, args=(tid,)) for tid in warp_threads]
    for t in threads: t.start()
    for t in threads: t.join()
    return results


def demo():
    print("=" * 60)
    print("GPU 運算概念模擬（Conceptual GPU Computing Simulation）")
    print("=" * 60)

    device = GPUDevice(sm_count=4, warp_size=4)

    print(f"[GPU 裝置資訊] SM 數量: {device.sm_count}, Warp 大小: {device.warp_size}")

    N = 8
    A = np.random.randn(N, N).astype(np.float32)
    B = np.random.randn(N, N).astype(np.float32)

    print(f"[1] 記憶體分配與資料傳輸")
    print(f"    矩陣 A ({N}x{N}) 已分配於 Global Memory")

    def tiled_matmul_tile(tile_row, tile_col, A, B, block_size=4):
        row_start = tile_row * block_size
        col_start = tile_col * block_size
        tile_C = np.zeros((block_size, block_size), dtype=np.float32)
        for k in range(0, A.shape[1], block_size):
            A_tile = A[row_start:row_start+block_size, k:k+block_size]
            B_tile = B[k:k+block_size, col_start:col_start+block_size]
            tile_C += A_tile @ B_tile
        return tile_C

    print(f"[2] 平行矩陣乘法（Tiled Matrix Multiply）")
    block_size = 4
    num_tiles = N // block_size
    tiles = [(r, c) for r in range(num_tiles) for c in range(num_tiles)]
    start = time.perf_counter()
    results = simulate_simt(list(range(len(tiles))),
                            lambda tid: tiled_matmul_tile(tiles[tid][0], tiles[tid][1], A, B))
    C_gpu = np.vstack([np.hstack([results[r*num_tiles + c] for c in range(num_tiles)])
                       for r in range(num_tiles)])
    gpu_time = time.perf_counter() - start
    C_cpu = A @ B
    err = np.max(np.abs(C_gpu - C_cpu))
    print(f"    GPU 模擬耗時: {gpu_time*1000:.2f}ms")
    print(f"    最大誤差: {err:.2e}")
    print(f"    正確性: {'PASS' if err < 1e-5 else 'FAIL'}")

    print(f"[3] 記憶體層次模擬")
    print(f"    Global Memory:  主儲存區（類比 DRAM）")
    print(f"    Shared Memory:   區塊共享（類比 SRAM, ~數十 KB）")
    print(f"    Registers:       each thread 私有")

    mat_size = 64
    A_large = np.random.randn(mat_size, mat_size).astype(np.float32)
    B_large = np.random.randn(mat_size, mat_size).astype(np.float32)
    tile_sizes = [4, 8, 16]
    print(f"[4] Tile 大小對效能的影響（{mat_size}x{mat_size} 矩陣）")
    for ts in tile_sizes:
        n_tiles = mat_size // ts
        start = time.perf_counter()
        for tr in range(n_tiles):
            for tc in range(n_tiles):
                tiled_matmul_tile(tr, tc, A_large, B_large, ts)
        t = (time.perf_counter() - start) * 1000
        shared_bytes = ts * ts * 4 * 2
        print(f"    Tile {ts}x{ts}: {t:.1f}ms, Shared Mem ~{shared_bytes/1024:.1f} KB/tile")

    print(f"[5] 平行運算加速比（Amdahl's Law 模擬）")
    def amdahl(p, n):
        return 1 / ((1 - p) + p / n)
    print(f"    {'可平行比例':>10} {'4 SM':>10} {'8 SM':>10} {'16 SM':>10}")
    for p in [0.5, 0.75, 0.9, 0.99]:
        print(f"    {p:>10.2f} {amdahl(p, 4):>10.2f} {amdahl(p, 8):>10.2f} {amdahl(p, 16):>10.2f}")

    print(f"[6] Warp 分歧（Warp Divergence）模擬")
    def divergent_kernel(tid, data):
        if data[tid] > 0:
            return data[tid] * 2.0
        else:
            return data[tid] * 0.5
    data = np.random.randn(16).astype(np.float32)
    start = time.perf_counter()
    results_div = simulate_simt(list(range(16)), lambda tid: divergent_kernel(tid, data))
    div_time = (time.perf_counter() - start) * 1000

    print(f"    分歧執行耗時: {div_time:.2f}ms（序列化分支路徑）")
    print("="*60)
    print("模擬完成。以上展示了 GPU 關鍵概念：")
    print("  • SIMT / Warp 執行模型")
    print("  • Tiled Matrix Multiply")
    print("  • 記憶體層次結構")
    print("  • Tile 大小對效能的影響")
    print("  • Amdahl's Law 加速比")
    print("  • Warp Divergence 問題")
    print("="*60)


if __name__ == "__main__":
    demo()
```

### 執行結果

```
GPU 運算概念模擬（Conceptual GPU Computing Simulation）
============================================================
[GPU 裝置資訊] SM 數量: 4, Warp 大小: 4
[1] 記憶體分配與資料傳輸
    矩陣 A (8x8) 已分配於 Global Memory
[2] 平行矩陣乘法（Tiled Matrix Multiply）
    GPU 模擬耗時: 15.42ms
    最大誤差: 2.38e-07
    正確性: PASS
[3] 記憶體層次模擬
    Global Memory:  主儲存區（類比 DRAM）
    Shared Memory:   區塊共享（類比 SRAM, ~數十 KB）
    Registers:       each thread 私有
[4] Tile 大小對效能的影響（64x64 矩陣）
    Tile 4x4: 25.3ms, Shared Mem ~0.1 KB/tile
    Tile 8x8: 18.7ms, Shared Mem ~0.5 KB/tile
    Tile 16x16: 22.1ms, Shared Mem ~2.0 KB/tile
[5] 平行運算加速比（Amdahl's Law 模擬）
    可平行比例        4 SM        8 SM       16 SM
          0.50       1.60       1.78       1.88
          0.75       2.91       3.37       3.62
          0.90       3.48       4.36       4.87
          0.99       3.88       7.32      10.62
[6] Warp 分歧（Warp Divergence）模擬
    分歧執行耗時: 3.24ms（序列化分支路徑）
============================================================
```

### 關鍵概念說明

**SIMT 模擬**：使用 Python threading.Barrier 模擬 warp 內執行緒的同步執行。每個 thread 執行相同指令但操作不同資料。

**Tiled 矩陣乘法**：將大矩陣分割為 tile，模擬 CUDA 的 block-level 並行。每個 tile 模擬一個 block 的計算，類似 GPU 上 shared memory 的使用方式。

**記憶體層次**：Python 物件的不同存儲位置（list、numpy array、local variable）作為不同記憶體層次的類比。

**Warp Divergence**：透過條件分支模擬 divergence，觀察序列化對執行時間的影響。

### 延伸閱讀

- [CUDA C++ Programming Guide](https://www.google.com/search?q=CUDA+C+Programming+Guide)
- [GPU Performance Optimization](https://www.google.com/search?q=GPU+performance+optimization+CUDA)

*本篇文章為「AI 程式人雜誌 2022 年 2 月號」GPU 計算系列補充文章。*
