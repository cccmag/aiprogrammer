# 4. AI 硬體加速

## GPU 的持續進化

### NVIDIA Turing 架構
2018 年 8 月發布，旗艦顯示卡 RTX 2080 Ti：
- RT Core：硬體加速光線追蹤
- Tensor Core：深度學習矩陣加速
- 12nm 製程

### 效能提升
相比 Pascal 架構：
- FP32 效能提升約 50%
- Tensor Core 提供 120 TFLOPS 的深度學習效能
- 記憶體頻寬大幅增加

## TPU 的進展

### TPU v3
Google 發布 TPU v3，效能進一步提升：
- TPU v3 pods 達到 100+ PFLOPS
- 記憶體容量大幅增加
- 支援更大的模型

## 其他 AI 晶片

### Intel Nervana
Intel 持續開發深度學習加速器：
- Nervana Neural Network Processor (NNP)
- 專為深度學習設計

### 專用晶片興起
多家公司發布 AI 專用晶片：
- Graphcore IPU
- Tesla Full Self-Driving 晶片
- 華為 Ascend（但這是 2019 年）

## 邊緣運算

終端 AI 處理需求增長：
- Qualcomm AI Engine：Snapdragon 855
- Apple Neural Engine：A12 晶片
- 邊緣部署場景增多

## 軟硬整合

深度學習框架與硬體的整合優化：
- CUDA 10：更好的效能與穩定性
- cuDNN 7：深度學習原語加速
- TensorRT：推理優化工具

## 算力比較

| 硬體 | FP32 效能 | 用途 |
|------|-----------|------|
| RTX 2080 Ti | 14 TFLOPS | 個人研究 |
| V100 | 14 TFLOPS | 資料中心 |
| TPU v3 | 90 TFLOPS | Google Cloud |

## 參考資源

- https://www.google.com/search?q=2018+AI+硬體+年度回顧+NVIDIA+Turing+TPU+進展
- https://www.google.com/search?q=NVIDIA+RTX+2080+Ti+Turing+Tensor+Core+AI+效能+2018
- https://www.google.com/search?q=TPU+v3+Google+2018+效能+規格+cloud