# Article 9：標籤平滑的理論基礎

## 標籤平滑的概念

標準的 cross-entropy 損失對於正確類別給予 100% 的概率，對於其他類別給予 0%。這可能導致兩個問題：模型對訓練資料过度自信，降低了泛化能力；決策邊界可能過於尖銳，對噪聲敏感。

## 數學表示

Label smoothing 將 hard label 轉換為 soft label：對於 K 類分類，真實標籤 y 從 (0, 1, 0, ..., y_k=1, ..., 0) 變為 (ε/K, ε/K, ..., 1-ε+ε/K, ..., ε/K)。這鼓勵模型對所有類別保持一定程度的概率，而非全力押注某一類。

## 對損失函數的影響

Label smoothing 修改了目標分佈，使損失函數更加平滑。當模型犯錯時，損失不會急劇增加。這類似於正則化的效果，使模型避免對訓練資料过度擬合。

## 與 Label Smoothing 的其他方法

One-hot 編碼加上小的機率給其他類別稱為 label smoothing。Mixup 和 CutMix 等資料增強技術也間接實現了類似的效果。這些方法都促進了類別之間的資訊流動，而非簡單的正確/錯誤標籤。

## 實務建議

Label smoothing 參數 ε 通常設為 0.1。對於噪聲標籤，可以考慮更大的值。並非所有任務都受益於 label smoothing——在某些場景下可能輕微降低精度。

## 參考資源

- Label Smoothing paper：https://www.google.com/search?q=label+smoothing+cross+entropy
- When to use label smoothing：https://www.google.com/search?q=label+smoothing+in+practice