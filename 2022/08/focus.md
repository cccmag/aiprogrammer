# 分散式訓練總覽

## 為什麼需要分散式訓練

隨著深度學習模型規模不斷成長，從2018年的 BERT（3.4億參數）到2022年的 GPT-3（1750億參數），單一 GPU 的記憶體已遠遠無法容納整個模型。分散式訓練成為大規模 AI 模型的必備技術。

## 四大平行策略

### 資料平行 (DataParallel)
最直觀的方法：將資料集分割成多份，每份分配到不同 GPU，各 GPU 持有完整的模型副本。優點是實作簡單，缺點是模型過大時仍無法放入單一 GPU。

### 模型平行 (ModelParallel)
將模型架構按層切割，不同層放在不同 GPU 上。資料依序通過各 GPU，同一時間只有一個 GPU 處於活躍狀態，GPU 利用率較低。

### 管線平行 (PipelineParallel)
模型平行的改良版：將 micro-batch 分批送入管線，讓多個 GPU 同時處理不同 micro-batch，大幅提升 GPU 利用率。

### 張量平行 (TensorParallel)
在運算層級進行切割：將一個線性層的權重矩陣分割到多個 GPU，共同計算同一層的輸出。適合超大模型如 GPT-3、LLaMA。

## 記憶體最佳化

### ZeRO 系列
- Stage 1：分割最佳化器狀態
- Stage 2：分割梯度
- Stage 3：分割模型參數

### 梯度檢查點 (Gradient Checkpointing)
以額外計算換取記憶體：在反向傳播時重新計算中間活化值，而非全部儲存。

## 通訊基礎設施

All-Reduce 是分散式訓練中最關鍵的通訊原語，NVIDIA NCCL 提供了高效實作。叢集管理則仰賴 SLURM 或 Kubernetes 進行資源調度。

[搜尋分散式訓練](https://www.google.com/search?q=分散式訓練+深度學習+2022)
[搜尋 Distributed Training](https://www.google.com/search?q=distributed+deep+learning+training+2022)
