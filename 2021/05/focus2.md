# Focus 2：梯度下降與優化器比較

## 梯度下降的三種變體

根據每次使用的資料量，梯度下降分為三種：批量梯度下降（BGD）使用全部資料，穩定但緩慢；隨機梯度下降（SGD）每次用一個樣本，快速但噪聲大；小批量梯度下降（MBGD）介於兩者之間，是實際默認選擇。MBGD 的關鍵參數是批量大小，它影響梯度估計的噪聲和收斂速度。

## SGD 與動量

標準 SGD 的問題是：梯度估計有噪聲，導致收斂路徑振盪。動量（Momentum）模擬物理中的慣性概念：累積之前的梯度方向，減少垂直方向的振盪，加速水平方向。數學上，v_t = βv_{t-1} + (1-β)∇θ，其中 β 通常設為 0.9。

## Adam 的理論

Adam（Adaptive Moment Estimation）結合了動量和 RMSProp 的思想。它維護兩個估計：梯度的一階矩估計（類似動量）和二階矩估計（用於自適應學習率）。公式複雜但實務效果好，是目前最常用的優化器。β1=0.9，β2=0.999，ε=1e-8 是常見配置。

## 何時用哪個

沒有絕對的答案，但有一些指導原則。在計算機視覺領域，SGD + Momentum 仍是預訓練模型的主流選擇，泛化表現通常優於 Adam。在自然語言處理領域，Adam 更常見。在遷移學習場景，建議用較小的學習率配合 Adam。實務經驗是：如果訓練時間有限，優先嘗試 Adam；如果追求最終精度，用 SGD。

## 參考資源

- Adam Paper：https://www.google.com/search?q=Adam+optimizer+paper+2015
- An overview of gradient descent：https://www.google.com/search?q=gradient+descent+optimization+overview