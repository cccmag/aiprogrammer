# 現代計算機架構趨勢

## 前言

計算機架構正在經歷一場深刻的變革。傳統的通用處理器（CPU）雖然仍然是計算系統的核心，但專用加速器（GPU、TPU、NPU）和異質計算架構正變得越來越重要。同時，量子計算也正在從理論走向實務。

## 異質計算架構

### 從同質到異質

傳統的多核心處理器使用相同的核心（同質），但現代處理器開始整合不同類型的核心：

**ARM big.LITTLE / Intel Hybrid 架構**：

```
┌─────────────────────────────┐
│  P-core  P-core  E-core E-core│
│  (高效能) (高效能) (高效能) (高效能)│
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐│
│  │L1/D1│ │L1/D1│ │L1/D1│ │L1/D1││
│  └─────┘ └─────┘ └─────┘ └─────┘│
│  ┌─────────────────────────────┐ │
│  │      共享 L3 快取           │ │
│  └─────────────────────────────┘ │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐│
│  │GPU  │ │NPU  │ │DSP  │ │ISP  ││
│  └─────┘ └─────┘ └─────┘ └─────┘│
└─────────────────────────────┘
```

- **P-core（Performance Core）**：高效能核心，處理計算密集型任務
- **E-core（Efficiency Core）**：高效能核心，處理背景任務和輕量工作
- **GPU**：圖形和通用平行計算
- **NPU（Neural Processing Unit）**：神經網路推理加速

### Chiplet 設計

Chiplet 是將大型晶片拆分成多個小晶片（chiplet），透過先進封裝技術整合在一起：

```
傳統 SoC：單一大晶片（良率低、成本高）
Chiplet：多個小晶片透過 Interconnect 連接（良率高、靈活）
```

Apple M2 Ultra 就是 Chiplet 設計的代表——將兩個 M2 Max 晶片透過 UltraFusion 封裝連接。

## 專用加速器

### GPU（圖形處理器）

GPU 從專用的圖形渲染器演變為通用平行計算引擎（GPGPU）：

- **數千個小型核心**：適合大規模資料平行
- **SIMT 執行模型**：單指令多執行緒
- **CUDA / ROCm 生態**：GPU 通用計算框架

### TPU（張量處理器）

Google TPU 專為神經網路計算設計：

- **脈動陣列（Systolic Array）**：矩陣乘法的專用硬體
- **低精度計算**：支援 BF16、INT8 等低精度格式
- **TPU v4**：4096 個 TPU 組成超級電腦

### NPU（神經處理單元）

NPU 整合在 SoC 中，專用於 AI 推理：

- Apple Neural Engine（16 核心，每秒 17 兆次運算）
- Qualcomm Hexagon（AI Engine）
- 能耗比遠優於 GPU

## 記憶體架構演進

### HBM（高頻寬記憶體）

HBM 透過 3D 堆疊技術將 DRAM 直接堆疊在處理器旁邊：

```
傳統：CPU → DDR DIMM（透過主機板走線）
HBM：CPU/GPU → HBM 堆疊（透過矽中介層）
```

- HBM2e：頻寬 ~460 GB/s
- HBM3：頻寬 ~819 GB/s

### CXL（Compute Express Link）

CXL 是基於 PCIe 的新一代互連協議，讓 CPU、記憶體和加速器之間共享一致的記憶體模型：

- CXL.io：I/O 協議（類似 PCIe）
- CXL.mem：記憶體擴展協議
- CXL.cache：快取一致性協議

## 量子計算

### 量子位元（Qubit）

與傳統位元不同，量子位元可以處於疊加態（superposition）：

```
傳統位元：0 或 1
量子位元：α|0⟩ + β|1⟩（α² + β² = 1）
```

### 量子閘

量子閘操作量子位元，類似傳統邏輯閘但作用於量子態：

- **Hadamard 閘**：創建疊加態
- **CNOT 閘**：糾纏兩個量子位元
- **Toffoli 閘**：通用量子閘

### 當前挑戰

- **退相干（Decoherence）**：量子態非常脆弱，容易受環境干擾
- **錯誤校正**：需要大量物理量子位元來實現一個邏輯量子位元
- **規模限制**：目前最大量子處理器約 1000 個量子位元

## AI 對架構設計的影響

AI 正在從三個層面影響計算機架構：

1. **AI 輔助設計**：使用強化學習自動化晶片佈局設計
2. **AI 專用硬體**：NPU、TPU 等加速器需求爆炸性成長
3. **架構探索自動化**：AI 自動搜尋最優微架構配置

## 小結

現代計算機架構正在從「通用 CPU 為中心」轉向「異質加速器協同」。Chiplet 設計讓晶片可以像樂高一樣組合，專用加速器讓特定任務的效能和能耗比大幅提升。同時，量子計算雖然仍處於早期階段，但可能從根本上改變計算的本質。

---

**下一步**：[回顧與結語](end.md)

## 延伸閱讀

- [Heterogeneous Computing Architecture](https://www.google.com/search?q=heterogeneous+computing+architecture)
- [Chiplet Design Guide](https://www.google.com/search?q=chiplet+design+guide+2023)
- [Quantum Computing Basics](https://www.google.com/search?q=quantum+computing+basics+for+engineers)
