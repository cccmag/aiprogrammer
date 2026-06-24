# Article 2：PyTorch DDP 實作解析

## DDP 的核心原理

DDP 內部的核心是梯度同步。當呼叫 `loss.backward()` 時，每個 GPU 計算本地梯度。然後 DDP 通過 Ring-AllReduce 演算法同步梯度：每個 GPU 只與鄰居通訊，最終所有 GPU 獲得相同的梯度平均值。

## Ring-AllReduce 的優勢

簡單的 AllReduce 需要一個 GPU 與所有其他 GPU 通訊，成為瓶頸。Ring-AllReduce 將通訊組織為環形，每個 GPU 只與兩個鄰居交換資料，通訊負載均勻分布。對於 N 個 GPU，通訊複雜度為 O(N)。

## 梯度 bucketing

為减少通訊開銷，DDP 使用梯度 bucketing。將多個層的梯度組成一個 bucket，一次 AllReduce 完成多個梯度同步。這樣可以隱藏通訊延遲，提高 GPU 利用率。

## 同步點優化

DDP 的設計減少了同步點。每個 GPU 在本地執行優化器步驟，不需要等待其他 GPU。但 AllReduce 本身是同步的，需要所有 GPU 都完成梯度計算才能開始。

## 常見效能瓶頸

1. 網路頻寬不足：梯度同步成為瓶頸
2. 負載不均衡：某些 GPU 處理更慢
3. 小 batch size：通訊計算比太低

## 參考資源

- DDP Source Code：https://www.google.com/search?q=DistributedDataParallel+pytorch+source+code
- Ring-AllReduce：https://www.google.com/search?q=ring+allreduce+distributed+training