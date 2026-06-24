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

    print(f"\n[GPU 裝置資訊] SM 數量: {device.sm_count}, Warp 大小: {device.warp_size}")

    N = 8
    A = np.random.randn(N, N).astype(np.float32)
    B = np.random.randn(N, N).astype(np.float32)

    print(f"\n[1] 記憶體分配與資料傳輸")
    print(f"    矩陣 A ({N}x{N}) 已分配於 Global Memory")

    def tiled_matmul_tile(tile_row, tile_col, A, B, block_size=4):
        """Simulate one tile's computation — each 'thread' handles one element"""
        row_start = tile_row * block_size
        col_start = tile_col * block_size
        tile_C = np.zeros((block_size, block_size), dtype=np.float32)
        for k in range(0, A.shape[1], block_size):
            A_tile = A[row_start:row_start+block_size, k:k+block_size]
            B_tile = B[k:k+block_size, col_start:col_start+block_size]
            tile_C += A_tile @ B_tile
        return tile_C

    print(f"\n[2] 平行矩陣乘法（Tiled Matrix Multiply）")
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

    print(f"\n[3] 記憶體層次模擬")
    print(f"    Global Memory:  主儲存區（類比 DRAM）")
    print(f"    Shared Memory:   區塊共享（類比 SRAM, ~數十 KB）")
    print(f"    Registers:       each thread 私有")
    mat_size = 64
    A_large = np.random.randn(mat_size, mat_size).astype(np.float32)
    B_large = np.random.randn(mat_size, mat_size).astype(np.float32)
    tile_sizes = [4, 8, 16]
    print(f"\n[4] Tile 大小對效能的影響（{mat_size}x{mat_size} 矩陣）")
    for ts in tile_sizes:
        n_tiles = mat_size // ts
        start = time.perf_counter()
        for tr in range(n_tiles):
            for tc in range(n_tiles):
                tiled_matmul_tile(tr, tc, A_large, B_large, ts)
        t = (time.perf_counter() - start) * 1000
        shared_bytes = ts * ts * 4 * 2
        print(f"    Tile {ts}x{ts}: {t:.1f}ms, Shared Mem ~{shared_bytes/1024:.1f} KB/tile")

    print(f"\n[5] 平行運算加速比（Amdahl's Law 模擬）")
    def amdahl(p, n):
        return 1 / ((1 - p) + p / n)
    print(f"    {'可平行比例':>10} {'4 SM':>10} {'8 SM':>10} {'16 SM':>10}")
    for p in [0.5, 0.75, 0.9, 0.99]:
        print(f"    {p:>10.2f} {amdahl(p, 4):>10.2f} {amdahl(p, 8):>10.2f} {amdahl(p, 16):>10.2f}")

    print(f"\n[6] Warp 分歧（Warp Divergence）模擬")
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

    print(f"\n{'='*60}")
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
