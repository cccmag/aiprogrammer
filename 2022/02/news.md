# 本月新知

## 2022 年 2 月 GPU 與 AI 技術動態

### NVIDIA 發表 Hopper H100 GPU

NVIDIA 於 GTC 2022 正式發表 Hopper 架構的 H100 GPU，採用台積電 4N 製程，擁有 800 億個電晶體。H100 首次支援 Transformer Engine，可自動切換 FP8 與 FP16 精度，大幅加速大型語言模型訓練。H100 配備第四代 NVLink，頻寬達 900 GB/s，並支援 PCIe 5.0。

### AMD Instinct MI250 加入戰局

AMD 發表 Instinct MI250 加速器，採用 CDNA 2 架構，配備 128 GB HBM2e 記憶體，在 HPC 和 AI 訓練領域與 NVIDIA 正面競爭。ROCm 5.0 開源軟體堆疊同時發布，支援 PyTorch 和 TensorFlow。

### Intel Ponte Vecchio 細節公開

Intel 在 ISSCC 2022 上公開 Xe-HPC Ponte Vecchio 的更多技術細節，採用 EMIB 和 Foveros 先進封裝技術，整合 47 個 tile，超過 1000 億電晶體。這是 Intel 重返獨立 GPU 市場的關鍵產品。

### PyTorch 1.11 發布

PyTorch 團隊發布 1.11 版本，重點強化 GPU 訓練效能。新版本支援 Distributed Data Parallel（DDP）的銅級通訊最佳化，以及 torch.cuda.amp 的混合精度訓練工具正式穩定。TorchScript 的 GPU 推理效能提升顯著。

### AI 訓練規模創紀錄

Google 發表 PaLM（Pathways Language Model）論文，參數量達 5400 億，在 6144 個 TPU v4 晶片上訓練。同時 Microsoft 與 NVIDIA 合作展示 Megatron-Turing NLG 530B 模型，採用 2240 個 A100 GPU 進行分散式訓練。

### TensorFlow 2.8 強化 GPU 支援

TensorFlow 2.8 發布，導入 tf.distribute.MultiWorkerMirroredStrategy 的效能改進，並支援 GPU 間的 NCCL 通訊協定最佳化。新版本也加強了對 TF32 精度的支援。

### OpenCL 3.0 普及

Khronos Group 宣布 OpenCL 3.0 獲得主流硬體支援，讓跨平台的 GPU 加速程式設計更加便利。Apple Silicon 的 Metal 實作也開始支援 OpenCL 3.0 子集。

### MLPerf 訓練 2.0 結果公布

MLPerf 公布訓練 2.0 基準測試結果，NVIDIA H100 在影像分類、物體偵測和自然語言處理等項目奪冠。AMD MI250 在部分 HPC 負載展現競爭力。

### AI 推論與邊緣運算

NVIDIA 發表 Jetson AGX Orin 邊緣 AI 平台，搭載 Ampere 架構 GPU，功耗僅 15-75W，提供 200 TOPS 的 AI 算力。同時 Qualcomm 發表 Cloud AI 100 加速器，專注於低延遲 AI 推論。

### 其他業界動態

- Google 發表 Pathways System 架構，支援超大規模分散式 AI 訓練
- Graphcore 推出第二代 IPU（Intelligence Processing Unit），採用台積電 7nm 製程
- Cerebras 推出 Wafer-Scale Engine-2（WSE-2），單晶片整合 2.6 兆電晶體
- Groq 發表 LPU（Language Processing Unit），專為 LLM 推理設計
- IBM 發表第二代 Telum 處理器，內建 AI 加速核心
