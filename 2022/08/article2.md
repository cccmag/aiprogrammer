# 同步 vs 非同步 SGD

## 同步 SGD

同步 SGD（同步梯度下降）是目前最主流的分散式更新策略。所有 worker 在每個訓練步驟完成反向傳播後，透過 All-Reduce 交換並平均梯度，然後同時更新模型參數。

**優點**：
- 收斂行為與單 GPU SGD 一致，容易調參
- 具有確定的訓練軌跡，可完全重現
- 梯度的統計特性與大 batch 訓練相同

**缺點**：
- 所有 worker 必須等待最慢的 worker（straggler problem）
- 通訊與計算無法重疊，GPU 利用率受通訊時間影響
- 擴展到大規模時效率下降

## 非同步 SGD

非同步 SGD 允許各 worker 獨立更新全局參數，不需要互相等待。每個 worker 從參數伺服器拉取最新參數，計算梯度後推送更新。

**優點**：
- 無 straggler 問題，heterogeneous 環境下表現好
- 可擴展到更大規模（數百 worker）
- 通訊開銷較低

**缺點**：
- 梯度延遲（gradient staleness）導致收斂不穩定
- 需要更謹慎的學習率調整
- 理論收斂保證較弱

## 混合策略

實務上最常見的是同步 SGD 搭配梯度累積。透過累積梯度放大 batch size，在保持收斂品質的同時提升通訊效率。

## 選擇建議

同步 SGD 適合 GPU 效能相近且有高速互連的叢集。非同步 SGD 適合計算資源異質性高的場景。對於絕大多數深度學習團隊，同步 SGD 是更安全的首選。

[搜尋同步 vs 非同步 SGD](https://www.google.com/search?q=synchronous+vs+asynchronous+SGD+distributed)
[搜尋梯度延遲問題](https://www.google.com/search?q=gradient+staleness+asynchronous+SGD)
