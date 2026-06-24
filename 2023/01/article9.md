# GPU 架構導論

## 1. 引言

圖形處理器（GPU）最初是為加速圖形渲染而設計的專用處理器。然而，隨著可程式化能力的增強，GPU 已經演變為強大的通用平行計算引擎（GPGPU），在科學計算、深度學習和資料分析等領域發揮著關鍵作用。

## 2. GPU 的核心設計理念

### 2.1 CPU vs GPU 的根本差異

| 特性 | CPU | GPU |
|------|-----|-----|
| 核心數量 | 4-24 | 數千 |
| 核心類型 | 大型複雜核心 | 小型簡單核心 |
| 快取 | 大（數十 MB） | 小（數 MB） |
| 控制單元 | 複雜（分支預測、亂序執行） | 簡單 |
| 記憶體頻寬 | 50-100 GB/s | 500-2000 GB/s |
| 適合任務 | 延遲敏感、序列化 | 吞吐量導向、平行化 |

### 2.2 SIMT 執行模型

GPU 採用 SIMT（Single Instruction, Multiple Threads）執行模型：

```python
class SIMTProcessor:
    def __init__(self, num_cores=1024, warp_size=32):
        self.cores = num_cores
        self.warp_size = warp_size  # 一個 warp 包含 32 個執行緒

    def execute_warp(self, instruction, threads):
        """一個 warp 中的所有執行緒執行同一條指令"""
        results = []
        for t in threads:
            if t.active:
                results.append(self.execute_one(instruction, t))
        return results
```

與 CPU 的 SIMD 不同，SIMT 允許每個執行緒有獨立的執行狀態和暫存器。

## 3. GPU 架構層次

### 3.1 從 Streaming Multiprocessor 到 GPU

```
NVIDIA GPU 架構層次：

GPU
├── GPC (Graphics Processing Cluster)
│   ├── SM (Streaming Multiprocessor)
│   │   ├── CUDA Cores × 128
│   │   ├── Shared Memory (96 KB)
│   │   ├── Register File (256 KB)
│   │   └── Warp Scheduler × 4
│   └── SM
│       └── ...
└── Memory System
    ├── L2 Cache
    ├── HBM/HBM2 Memory
    └── Memory Controller
```

### 3.2 CUDA 核心模擬

```python
class CudaCore:
    def __init__(self, id):
        self.id = id
        self.regs = [0] * 64
        self.pc = 0

    def execute(self, inst):
        if inst.op == 'FADD':
            return self.regs[inst.dst] + self.regs[inst.src]
        elif inst.op == 'FMUL':
            return self.regs[inst.dst] * self.regs[inst.src]
        elif inst.op == 'FFMA':
            return self.regs[inst.dst] * self.regs[inst.src] + self.regs[inst.acc]

class StreamingMultiprocessor:
    def __init__(self, num_cores=128):
        self.cores = [CudaCore(i) for i in range(num_cores)]
        self.shared_memory = [0] * (96 * 1024)  # 96 KB
        self.warp_schedulers = 4

    def issue_warp(self, warp):
        for core in self.cores[:len(warp.threads)]:
            if warp.threads[core.id].active:
                core.execute(warp.instruction)
```

## 4. GPU 記憶體層次

### 4.1 記憶體類型

```python
class GPUMemory:
    def __init__(self):
        self.global_memory = [0] * (24 * 1024**3)  # 24 GB HBM
        self.texture_memory = {}   # 唯讀快取
        self.constant_memory = {}  # 唯讀，廣播到所有執行緒
        self.shared_memory = {}    # 每個 SM 私有

    def access_global(self, addr):
        return self.global_memory[addr]

    def access_shared(self, sm_id, addr):
        return self.shared_memory[sm_id][addr]
```

### 4.2 記憶體合併存取

GPU 效能的一個關鍵是**記憶體合併存取**（Memory Coalescing）：同一 warp 的執行緒存取連續的記憶體位置時，可以合併為一次記憶體請求：

```python
def memory_coalescing_example():
    # 合併存取：所有執行緒存取連續位址
    # Thread 0: addr 0, Thread 1: addr 1, ..., Thread 31: addr 31
    # → 1 次記憶體請求

    # 非合併存取：隨機位址
    # Thread 0: addr 0, Thread 1: addr 100, Thread 2: addr 200
    # → 32 次記憶體請求（效能嚴重下降）
    pass
```

## 5. GPU 程式設計模型

### 5.1 CUDA 程式範例

```python
# 等價的 CUDA C 程式碼概念
def vector_add_gpu(a, b, c, n):
    """向量加法：c = a + b，每個執行緒計算一個元素"""
    for tid in range(n):
        c[tid] = a[tid] + b[tid]
    # 實際在 GPU 上，這個迴圈由數千個執行緒平行執行
```

### 5.2 執行緒組織

GPU 執行緒的組織層次：

- **Thread**：最小的執行單元
- **Warp**：32 個執行緒組成的執行群組
- **Block**：多個 warp 組成，共享 shared memory
- **Grid**：多個 block 組成，構成完整任務

## 6. GPU 在 AI 中的應用

### 6.1 矩陣乘法加速

GPU 的強項是大規模矩陣運算，這是深度學習的核心操作：

```python
def matmul_gpu(A, B, C, M, N, K):
    """簡化的 GPU 矩陣乘法"""
    for i in range(M):
        for j in range(N):
            total = 0
            for k in range(K):
                total += A[i * K + k] * B[k * N + j]
            C[i * N + j] = total
```

### 6.2 Tensor Core

NVIDIA 從 Volta 架構開始引入了 Tensor Core——專為深度學習中的矩陣乘加運算設計的硬體單元：

```
D = A × B + C

其中 A、B、C、D 都是 4×4 矩陣
Tensor Core 可以在一個週期內完成上述運算
```

## 7. 結語

GPU 從專用圖形處理器發展為通用平行計算引擎，代表了計算機架構從通用到專用的演進方向。GPU 的成功說明了：針對特定類型的計算任務（資料平行），專用架構可以達到比通用 CPU 高數十倍的效能和效率。

---

**下一步**：[效能評估：CPI 與 Amdahl 定律](article10.md)

## 延伸閱讀

- [CUDA GPU Architecture](https://www.google.com/search?q=CUDA+GPU+architecture+explained)
- [SIMT vs SIMD](https://www.google.com/search?q=SIMT+vs+SIMD+execution+model)
- [NVIDIA Tensor Core](https://www.google.com/search?q=NVIDIA+Tensor+Core+deep+learning)
