# 從 CPU 到 GPU 的思維轉變

## 程式設計師的平行計算啟蒙

### 序列思維的慣性

大多數程式設計師的第一門程式語言——無論是 C、Java 還是 Python——都教授序列執行的觀念：程式一行一行執行，函式一個一個呼叫，for 迴圈依序迭代。這種思維深植在我們的潛意識中，以至於當我們第一次面對 GPU 程式設計時，往往會感到強烈的不適應。

序列思維的慣性表現在：習慣性地認為「一個執行緒或程序」是程式的基本單位；習慣性地使用鎖和共享狀態來處理並行；習慣性地依賴直覺來預測程式的行為。

### 平行思維的基本原則

要真正掌握 GPU 程式設計，需要建立一套全新的思維模型：

**資料平行性**：與其思考「如何讓一個執行緒更快」，不如思考「如何讓 10000 個執行緒同時工作」。資料平行性（Data Parallelism）的核心理念是：對大量資料應用相同的操作。這正是 GPU 最擅長的模式。

**延遲隱藏**：在 CPU 上，我們用快取來減少記憶體延遲。在 GPU 上，我們用執行緒切換來隱藏延遲——當某些執行緒等待記憶體時，GPU 立即切換到其他就緒的執行緒。這意味著我們需要足夠多的執行緒來「填滿」記憶體管線。

**吞吐量優先**：GPU 的設計哲學是「吞吐量優先，延遲其次」。一個 GPU 操作可能比 CPU 慢 10 倍（因為啟動 Kernel 的開銷），但當處理 100 萬個資料點時，GPU 可能比 CPU 快 1000 倍。

### 常見的思維轉換場景

場景一：假設你需要對一個包含 100 萬個元素的陣列執行元素級操作。在 CPU 上，你可能使用 for 迴圈或 OpenMP 的 #pragma omp parallel for。在 GPU 上，你啟動一個包含 100 萬個執行緒的 kernel，每個執行緒處理一個元素。

```python
# CPU 思維
for i in range(1_000_000):
    result[i] = data[i] * 2 + 1

# GPU 思維（透過 PyTorch）
result = data * 2 + 1  # 自動平行化
```

場景二：神經網路的訓練。在 CPU 上，你可能會逐層計算。在 GPU 上，你將整個批次數據一次交給 GPU，讓它同時計算所有樣本的所有層。

場景三：批次推理。在 CPU 上，一次處理一個請求。在 GPU 上，等待多個請求湊成一個 batch，然後一次處理，以最大化硬體利用率。

### 資料傳輸的成本

從 CPU 思維到 GPU 思維最重要的轉變之一，是認識到資料傳輸的成本。在 CPU 上，記憶體訪問是均勻的（UMA）。在 GPU 上，CPU 和 GPU 之間有明確的 PCIe 邊界：

```
CPU → GPU 資料傳輸: ~12 GB/s (PCIe 4.0 x16)
GPU Global Memory 頻寬: ~2000 GB/s (HBM2e)
```

這意味著一次跨 PCIe 的資料傳輸比一次 GPU 記憶體訪問慢 100 倍以上。因此，GPU 程式設計的最高原則之一：**盡量減少 CPU 和 GPU 之間的資料傳輸**。

### 實戰建議

- 從 PyTorch 或 TensorFlow 開始，不必直接寫 CUDA C++
- 先理解資料布局：shape、stride、memory format（NCHW vs NHWC）
- 使用 torch.cuda.Event 來測量 GPU 操作的時間
- 理解 torch.no_grad() 和 eval() 在推理時的用途
- 善用 torch.jit.script 和 torch.compile 優化 GPU Kernel

### 延伸閱讀

- [CUDA Programming Model](https://www.google.com/search?q=CUDA+programming+model+overview)
- [Think Parallel: GPU Programming Concepts](https://www.google.com/search?q=GPU+parallel+programming+concepts)
