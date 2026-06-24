# 晶片與硬體回顧

## NVIDIA 的進展

### Turing 架構
2018 年 8 月發布：
- RT Core：光線追蹤硬體加速
- Tensor Core：深度學習加速
- 12nm 製程

### RTX 系列顯示卡
| 型號 | CUDA 核心 | 記憶體 | TDP |
|------|-----------|--------|-----|
| RTX 2080 Ti | 4352 | 11GB | 260W |
| RTX 2080 | 2944 | 8GB | 215W |
| RTX 2070 | 2304 | 8GB | 175W |

### 效能提升
相較 Pascal 架構：
- 深度學習訓練加速約 50%
- 功耗效率提升
- CUDA 10 優化支援

## Google TPU

### TPU v2 持續服務
雲端 TPU 服務穩定：
- 64 核心組成一塊 TPU
- 高頻寬記憶體互連
- 按需付費使用

### TPU v3 發布
效能進一步提升：
- 更快的時脈
- 更大記憶體容量
- TPU pods 可擴展

## Intel 的 AI 硬體

### Xeon Scalable
資料中心 CPU：
- AVX-512 指令集
- 深度學習加速優化
- 與 GPU 協同工作

### Nervana
專用 AI 晶片：
- Neural Network Processor (NNP)
- 專為深度學習設計

## AMD

### Vega 架構
Radeon Instinct 系列：
- 7nm 製程（後續）
- 高速記憶體
- ROCm 軟體棧

## 邊緣 AI 硬體

### Qualcomm Snapdragon 855
行動 AI 晶片：
- Hexagon 690 DSP
- 張量加速器
- 強化的 AI Engine

### Apple A12 Bionic
iPhone 使用的晶片：
- Neural Engine
- 8 核心神經網路引擎
- 設備端 AI 處理

### ARM Cortex-A 系列
移動處理器：
- 終端 AI 加速
- 輕量級模型支援

## 記憶體與互連

### HBM2
高頻寬記憶體：
- RTX 2080 Ti 採用
- 超過 600 GB/s 頻寬

### NVLink
高速互連：
- GPU 之間通訊
- 提升多 GPU 訓練效率

## 軟體優化

### CUDA 10
2018 年發布：
- 更好的效能
- 支援 Turing 架構
- 改善穩定性

### cuDNN 7
深度學習原語庫：
- 優化卷積、池化等操作
- 支援新架構

## 參考資源

- https://www.google.com/search?q=2018+AI+硬體+年度回顧+NVIDIA+Turing+TPU+Intel
- https://www.google.com/search?q=NVIDIA+RTX+2080+Ti+Turing+Tensor+Core+specs+2018
- https://www.google.com/search?q=TPU+v3+Google+cloud+AI+hardware+2018+performance