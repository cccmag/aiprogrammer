# 資料平行 DataParallel

## 基本原理

資料平行是最早被廣泛使用的分散式訓練策略。其核心概念是：每個 GPU 持有完整的模型副本，但只處理資料集的一個子集。每個訓練步驟中，所有 GPU 獨立計算前向與反向傳播，然後透過 All-Reduce 通訊同步梯度。

## 實作方式

PyTorch 提供了兩種資料平行實作：

**DataParallel (DP)**：單一進程、多 GPU，適用於單機。主 GPU 負責梯度彙總與參數更新，容易產生主 GPU 瓶頸。

**DistributedDataParallel (DDP)**：多進程、多 GPU，可跨機器。每個進程獨立運算，透過 NCCL 進行梯度 All-Reduce，效率遠高於 DP。

## 優點與限制

優點：
- 實作最簡單，僅需少量程式碼修改
- 對於模型能放入單 GPU 的場景非常有效
- 擴展性良好，理論上可線性加速

限制：
- 模型必須能完整放入單一 GPU 記憶體
- 當 batch size 過大時，收斂品質可能下降
- 通訊成本隨 GPU 數量線性成長

## 適用場景

資料平行適合模型參數量在數億以下的場景，例如 ResNet、EfficientNet、BERT-base 等。對於 GPT-3 等級的超大模型，則需要搭配模型平行策略。

[搜尋 PyTorch DistributedDataParallel](https://www.google.com/search?q=PyTorch+DistributedDataParallel+tutorial)
[搜尋 Data Parallelism 深度學習](https://www.google.com/search?q=data+parallelism+deep+learning)
