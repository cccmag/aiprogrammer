# GPU 效能分析 nvprof

## 使用 NVIDIA 工具鏈定位效能瓶頸

### 為什麼需要 GPU Profiling

「我的 GPU 程式為什麼這麼慢？」這是一直困擾 GPU 程式設計師的問題。與 CPU 不同，GPU 的執行是高度非同步的：kernel 啟動立即返回，實際執行在 GPU 上排程。傳統的 printf 除錯和時間測量完全失效。

GPU Profiling 工具可以回答以下問題：

- Kernel 的實際執行時間是多少？（而非啟動時間）
- GPU 利用率有多高？是否有閒置時間？
- 記憶體頻寬是否飽和？
- 是否存在 warp divergence？
- 資料傳輸是否是瓶頸？

### nvprof：命令列 Profiler

nvprof 是 NVIDIA 的命令列 Profiling 工具（CUDA 5-10），提供全面的 GPU 活動分析：

```bash
# 基本使用
nvprof python train.py

# 只分析 kernel 執行時間
nvprof --print-gpu-trace python train.py

# 分析 API 調用時間
nvprof --print-api-trace python train.py

# 匯出為 NVIDIA Visual Profiler 格式
nvprof -o profile.nvprof python train.py
```

執行後 nvprof 會輸出：
- GPU 各 kernel 的執行時間、佔用率、記憶體使用量
- CUDA API 調用（cudaMemcpy、cudaMalloc 等）的次數和時間
- 資料傳輸的頻寬
- 記憶體複製和 kernel 執行的時間線

### Nsight Systems：現代化 Profiler

從 CUDA 11 開始，NVIDIA 推薦使用 Nsight Systems（nsys）替代 nvprof：

```bash
# 基礎分析
nsys profile -o profile python train.py

# GPU kernel 和記憶體傳輸分析
nsys profile --stats=true python train.py

# 帶有 CUDA API trace 的分析
nsys profile --trace=cuda,nvtx python train.py
```

Nsight Systems 提供更現代的 GUI（Nsight Systems GUI），可視化時間線：

```
CUDA Timeline
┌─────────────────────────────────────────────┐
│ CPU: DataLoader                             │
│ GPU: Kernel 1 (matmul)             ████████ │
│ GPU: Kernel 2 (softmax)                ████ │
│ CPU→GPU: cudaMemcpy                  ███    │
│ GPU→CPU: cudaMemcpy                      ██ │
└─────────────────────────────────────────────┘
```

### 關鍵效能指標

**佔用率（Occupancy）**：每個 SM 上活躍 warp 數量與最大可能 warp 數量的比值。低佔用率表示 GPU 資源未被充分利用，可能原因：block 太小、每個 thread 使用太多暫存器、shared memory 用量過大。

```bash
# 檢查佔用率
nvprof --metrics achieved_occupancy python train.py
```

**記憶體頻寬利用率**：實際記憶體頻寬與理論頻寬的比值。低於 50% 表示記憶體訪問模式不佳（如非合併訪問）。

```bash
nvprof --metrics gld_efficiency,gst_efficiency python train.py
```

**Warp 執行效率**：每個 warp 中活躍執行緒的比例。低於 100% 表示存在 warp divergence。

```bash
nvprof --metrics branch_efficiency python train.py
```

### 在 PyTorch 中使用 Profiler

PyTorch 1.8+ 內建 Profiler，可直接在 Python 程式中使用：

```python
import torch.profiler as profiler

with profiler.profile(
    activities=[profiler.ProfilerActivity.CUDA],
    schedule=profiler.schedule(wait=1, warmup=1, active=3),
    on_trace_ready=profiler.tensorboard_trace_handler("./logs")
) as p:
    for step in range(10):
        train_step()
        p.step()
```

結果可在 TensorBoard 中視覺化查看。

### 常見效能問題

1. **GPU 利用率低**：batch size 太小、資料載入瓶頸。解決：增大 batch、增加 num_workers
2. **頻繁的 CPU-GPU 傳輸**：每次 step 都調用 .cuda()。解決：預先將資料移至 GPU
3. **小 Kernel 過多**：啟動開銷大於計算時間。解決：融合 kernel、使用 CUDA Graph
4. **記憶體瓶頸**：非合併訪問導致頻寬浪費。解決：調整資料布局、使用 shared memory
5. **低佔用率**：資源使用過多限制並行。解決：減少每 thread 暫存器數、增大 block 大小

### 延伸閱讀

- [NVIDIA Profiling Tools](https://www.google.com/search?q=NVIDIA+Nsight+Systems+profiling)
- [PyTorch Profiler](https://www.google.com/search?q=PyTorch+profiler+tutorial)
