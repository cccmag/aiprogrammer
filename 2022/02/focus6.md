# TPU 與專用 AI 晶片

## Google TPU 與 AI 加速器生態

### Google TPU 的誕生

2015 年，Google 發表了第一代 Tensor Processing Unit（TPU），這是專門為 TensorFlow 工作負載設計的 ASIC 加速器。第一代 TPU 僅支援推理，採用 INT8 量化，在 Google 搜尋和 RankBrain 中部署，效能功耗比是同期 GPU 的 10 倍以上。

### TPU v4 架構深度解析

2022 年，Google 公布了 TPU v4 的詳細架構，這是訓練 5400 億參數 PaLM 模型的關鍵硬體：

- **MXU 矩陣乘法單元**：TPU 的核心是 MXU（Matrix Multiply Unit），每個 MXU 由 128×128 個乘累加器組成。一個 MXU 單次操作可完成 128² = 16384 個 MAC 運算。TPU v4 擁有 4 個 MXU，總共 65536 MAC/cycle。
- **記憶體系統**：每個 TPU v4 晶片配備 32 GB HBM2e 記憶體，頻寬 1200 GB/s。與 GPU 不同，TPU 沒有 L1/L2 快取，而是依賴 HBM 和晶片間互連。
- **光學互連**：TPU v4 使用 OCS（Optical Circuit Switching）實現晶片間互連，可動態重構網路拓撲。4096 個 TPU v4 可組合成一個巨大的多維環面（torus）。
- **向量處理單元**：除了 MXU，TPU 還包含向量處理器用於處理非矩陣運算（如 softmax、激活函數、歸一化）。

### TPU vs GPU 的架構差異

| 特性 | NVIDIA GPU (A100) | Google TPU v4 |
|-----|------------------|---------------|
| 製程 | 7nm | 7nm |
| 運算核心 | CUDA Core (6912) | MXU (4×128×128) |
| 記憶體 | 80GB HBM2e | 32GB HBM2e |
| 記憶體頻寬 | 2039 GB/s | 1200 GB/s |
| 單晶片 FP16 | 312 TFLOPS | 275 TFLOPS |
| 晶片間互連 | NVLink 600 GB/s | OCS 自訂拓撲 |
| 靈活性 | 通用平行運算 | JIT 編譯器（XLA） |

### AI 加速器生態

除了 NVIDIA 和 Google，多家公司也在爭奪 AI 加速器市場：

#### AMD Instinct

AMD 的 CDNA 架構採用 Matrix Core（類似 Tensor Core）進行矩陣加速。MI250 配備 128GB HBM2e，FP16 運算能力達 383 TFLOPS。ROCm 開源軟體堆疊的成熟度是關鍵挑戰。

#### Intel Habana Gaudi

Intel 收購 Habana Labs 後的 Gaudi 處理器專注於 AI 訓練。Gaudi 內建整合乙太網路介面，無需額外連接網路卡，簡化大規模部署。

#### Graphcore IPU

Graphcore 的 Intelligence Processing Unit（IPU）採用 MIMD（Multiple Instruction, Multiple Data）架構，適合稀疏運算和圖神經網路。

#### Cerebras WSE-2

Cerebras 的 Wafer-Scale Engine-2 是單晶圓整合的巨型晶片，擁有 2.6 兆電晶體和 850,000 個運算核心。其獨特的「晶圓級」設計消除了晶片間通訊的需求。

### 邊緣 AI 加速器

在邊緣側，低功耗 AI 加速器快速發展：

- **NVIDIA Jetson AGX Orin**：2048 CUDA Core + 64 Tensor Core，15-75W
- **Apple Neural Engine**：iPhone 內建 16 核心 NPU，17 TOPS
- **Qualcomm Hexagon NPU**：Snapdragon 內建 AI 引擎
- **Google Edge TPU**：Coral 平台的 USB 加速器，推論功耗僅 2W

### 延伸閱讀

- [TPU v4 Architecture](https://www.google.com/search?q=TPU+v4+architecture+paper)
- [AI Accelerator Comparison](https://www.google.com/search?q=AI+accelerator+comparison+2022)
- [Cerebras Wafer Scale Engine](https://www.google.com/search?q=Cerebras+Wafer+Scale+Engine)
