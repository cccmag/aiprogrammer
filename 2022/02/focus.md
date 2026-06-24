# 本期焦點

## GPU 運算與平行計算 — CUDA 與硬體加速

### 引言

2022 年是 GPU 運算領域極為重要的一年。NVIDIA Hopper H100 的問世、AMD Instinct MI250 的追擊、以及 Intel Ponte Vecchio 的登場，宣告了異構加速計算的時代正式來臨。從深度學習訓練到科學模擬，從雲端 AI 推論到邊緣裝置的即時推理，GPU 早已不只是顯示卡，而是現代計算基礎設施的核心。

然而，要真正發揮 GPU 的潛力，程式設計師需要理解一個根本的思維轉變：從 CPU 的序列執行模式，轉換為 GPU 的大規模平行思維。這不僅是工具層面的轉變，更是思考方式的革命。

本期雜誌將帶領讀者深入探索 GPU 運算的世界，從底層架構到高階框架，從理論模型到實戰技巧，全面掌握這項當代最重要的計算技術。

### 大綱

- [程式：GPU 運算概念模擬](focus_code.md)
   - CUDA 執行模型與 SIMT
   - Tiled 矩陣乘法實作
   - 記憶體層次結構模擬
   - Warp Divergence 分析

1. [GPU 架構 vs CPU 架構](focus1.md)
   - CPU 的序列執行模式
   - 從 CPU 到 GPU：什麼改變了
   - 程式設計師的思維轉變
   - 平行計算的 Amdahl's Law

2. [CUDA 程式設計模型](focus2.md)
   - SIMT 執行模型
   - Kernel 啟動與配置
   - Thread / Block / Grid 層次
   - CUDA 程式開發流程

3. [矩陣運算與平行化](focus3.md)
   - Tiled 矩陣乘法
   - 共享記憶體的使用
   - 計算與記憶體頻寬的平衡
   - 自動調優與 cuBLAS

4. [cuDNN 與深度學習加速](focus4.md)
   - cuDNN 的卷積演算法
   - Tensor Core 與混合精度
   - 高度最佳化的 kernel
   - 與框架的整合

5. [多 GPU 訓練策略](focus5.md)
   - Data Parallelism（資料平行）
   - Model Parallelism（模型平行）
   - Pipeline Parallelism（管線平行）
   - NCCL 通訊協定

6. [TPU 與專用 AI 晶片](focus6.md)
   - Google TPU 架構
   - MXU 矩陣乘法單元
   - AI 加速器生態
   - FPGA 與 ASIC 的取捨

7. [GPU 記憶體管理與最佳化](focus7.md)
   - Global / Shared / Local Memory
   - Unified Memory 與自動遷移
   - 記憶體池化技術
   - Memory Coalescing

### 結論與展望

GPU 運算正在從深度學習的加速器，轉變為通用計算的核心支柱。從 CUDA 到 SYCL，從 NVIDIA 到 AMD、Intel、Google，異構運算的生態正在快速成熟。掌握平行思維與 GPU 程式設計，將成為未來程式設計師不可或缺的技能。
