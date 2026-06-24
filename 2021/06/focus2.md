# Focus 2：模型平行與管線平行

## 為何需要模型平行

資料平行要求每個節點持有完整模型。當模型大到單節點記憶體無法容納時，需要模型平行（Model Parallelism）：將模型分割到多個節點，每個節點只持有模型的一部分。這種策略適合數十億參數的大模型。

## 模型分割策略

最直觀的分割方式是按層分割：將連續的層組放到不同節點。forward 時，資料在節點間流動；backward 時，梯度反向傳播。這種方式實現簡單，但只有在使用管線時才能高效。

## 管線平行的問題

層級分割會導致節點空閒：當第一個節點處理 batch 1 的 forward 時，其他節點閒置。為解決這個問題，引入管線平行（Pipeline Parallelism）：將輸入資料划分为多個 micro-batches，流水線式地通過各個階段。這樣所有節點可以同時工作，只是處理不同的 micro-batches。

## PipeDream 的設計

PipeDream 是管線平行的經典實現。每個節點維護自己的模型副本（非同步更新）。當一個節點完成某個 micro-batch 的 forward 和 backward 後，合併結果並更新。這種設計隐藏了通訊延遲，但引入了 staleness。

## 記憶體考量

管線平行節省的是模型狀態記憶體，但每個節點仍需要儲存對應層的活化值。對於大模型，結合資料平行（模型平行 + 資料平行）成為常見策略。這種組合可以訓練數萬億參數的模型。

## 參考資源

- Pipeline Parallelism：https://www.google.com/search?q=pipeline+parallelism+deep+learning
- PipeDream Paper：https://www.google.com/search?q=PipeDream+model+parallelism