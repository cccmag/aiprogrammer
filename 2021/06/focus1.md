# Focus 1：資料平行 — 多卡訓練的基礎

## 資料平行的核心思想

資料平行（Data Parallelism）是最廣泛使用的分散式訓練策略。其核心思想很簡單：將輸入資料分割為多個子集，每個運算節點持有模型副本，獨立處理各自的資料子集，定期同步梯度以確保模型一致性。這種方法實現簡單，幾乎可以達到線性加速比。

## 同步 vs 非同步

同步資料平行在每個 step 後等待所有節點的梯度，計算平均後更新模型。這保證了與單卡訓練完全相同的收斂行為，但節點間需要同步等待。非同步資料平行允許節點獨立更新，不等待其他節點。雖然可能有 staleness 問題，但能完全利用每個節點的算力。在實務中，同步 SGD 更常見。

## 梯度平均

同步資料平行的關鍵步驟是梯度平均。每個節點計算本地梯度後，使用 AllReduce 操作將所有節點的梯度相加並平均。通訊複雜度為 O(N)，每個節點需要與所有其他節點通訊。InfiniBand 等高速網路對此至關重要。

## 記憶體優化

即使使用資料平行，每個節點仍需持有完整模型。對於大模型，這仍是瓶頸。Gradient Checkpointing 是一種常見技術，用計算換記憶體：只保存部分活化值，反向傳播時重新計算需要的部分。ZeRO 等分片技術可以進一步減少每節點的記憶體需求。

## 實務考量

1. Batch size 隨 GPU 數量增加而增加，但過大可能影響泛化
2. 學習率需要相應調整（linear scaling）
3. 確保網路頻寬足夠，否則通訊會成為瓶頸
4. 使用混合精度可減少記憶體使用和加速

## 參考資源

- Data Parallel Training：https://www.google.com/search?q=data+parallel+training+pytorch
- AllReduce Algorithm：https://www.google.com/search?q=allreduce+distributed+training