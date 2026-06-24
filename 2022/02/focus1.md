# GPU 架構 vs CPU 架構

## 從序列到平行的思維革命

### CPU 的設計哲學

中央處理器（CPU）的設計目標是「快速執行序列程式」。為此，CPU 採用了多層快取、分支預測、暫存器重新命名、亂序執行等複雜技術，以最小化單一執行緒的延遲。典型的現代 CPU 擁有 4 到 16 個核心，每個核心獨立執行任務，並透過共享 L3 快取進行通訊。

CPU 的強項在於「複雜控制流」和「低延遲」。當程式包含大量條件分支、間接跳轉和遞迴時，CPU 的亂序執行引擎和分支預測器可以有效隱藏延遲。但代價是電晶體利用率不高——大部分晶片面積被控制邏輯和快取佔據，而非算術邏輯單元。

### GPU 的設計哲學

圖形處理器（GPU）的設計目標是「大規模資料平行處理」。GPU 捨棄了複雜的控制邏輯，將大量電晶體投入運算單元。以 NVIDIA A100 為例，它擁有 6912 個 CUDA 核心，分成 108 個串流多處理器（SM），每個 SM 包含 64 個 CUDA 核心。

GPU 的關鍵概念是 SIMT（Single Instruction, Multiple Threads）：32 個執行緒構成一個 warp，在同一時間執行同一指令，但操作不同的資料。這極大簡化了控制單元，使得 GPU 可以在同一晶片上容納更多算術單元。

### 架構差異總結

CPU 與 GPU 在本質上適合不同的工作負載：

- **延遲導向 vs 吞吐量導向**：CPU 優化單執行緒延遲，GPU 優化整體吞吐量
- **控制邏輯**：CPU 大量面積用於控制邏輯，GPU 將面積讓給運算單元
- **快取階層**：CPU 使用大容量快取（L1/L2/L3）減少記憶體延遲，GPU 使用小快取但搭配高頻寬 HBM
- **執行緒模型**：CPU 執行緒切換成本高，GPU 擁有數萬個輕量執行緒可零成本切換

### Amdahl's Law 與加速比

Amdahl's Law 描述了平行化對程式加速的理論上限：

```
Speedup = 1 / ((1 - P) + P / N)
```

其中 P 是可平行化的比例，N 是處理器數量。這條定律提醒我們：即使使用無限多的 GPU，程式的序列部分仍會成為瓶頸。因此 GPU 運算的關鍵在於盡可能提高程式的可平行化比例。

### 從 CPU 到 GPU 的思維轉變

程式設計師在從 CPU 轉向 GPU 時，面臨的核心挑戰是「平行思維」的建立：

- 將問題分解為大量獨立的子任務
- 避免 raace condition 和控制流分歧
- 優化資料存取模式以實現 memory coalescing
- 權衡計算量與資料傳輸成本

### 常見誤區

#### 誤區一：GPU 能加速所有程式

GPU 只擅長資料平行的計算密集型任務。對於 IO 密集型、分支密集型、或者資料量太小的任務，GPU 可能比 CPU 更慢。

#### 誤區二：執行緒越多越快

GPU 的執行緒是一種「隱藏延遲」的工具。當某些執行緒等待記憶體時，GPU 可以切換到其他執行緒執行。但如果執行緒過多，暫存器和共享記憶體不足，反而降低效能。

#### 誤區三：CPU 和 GPU 獨立運作

實際上，典型的 GPU 運算是 CPU 和 GPU 協同工作的結果。CPU 負責控制邏輯與任務排程，GPU 專注於大規模平行運算。

### 延伸閱讀

- [NVIDIA CUDA C++ Programming Guide](https://www.google.com/search?q=CUDA+C+Programming+Guide)
- [Amdahl's Law](https://www.google.com/search?q=Amdahl%27s+Law+parallel+computing)
- [GPU vs CPU: Architectural Comparison](https://www.google.com/search?q=GPU+vs+CPU+architecture+difference)
