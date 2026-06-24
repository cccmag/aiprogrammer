# Article 2：NumPy 廣播機制深入解析

## 廣播原理

廣播允許 NumPy 在二元運算中自動擴充形狀不相符的陣列。核心規則是：從最後維度開始比較，如果維度大小相同或其中一個為 1，則相容。廣播時，維度為 1 的會被擴充為匹配大小。這種機制使得向量化程式碼無需顯式迴圈即可處理不同形狀的資料。

## 常見範例

向量與純量相加：`a + 1`，純量被廣播到向量每個元素。二維與一維相加：行或列被廣播到整個矩陣。三維與二維相加：二維被廣播到三維的每個切片。理解這些模式能幫助你預測廣播結果。

## 視覺化理解

想像較小的陣列被「拉伸」以匹配較大的陣列。拉伸只在需要時發生，且不改變實際儲存——NumPy 聰明地實現了虛擬拉伸，避免實際拷貝。這個視覺化模型有助於預測廣播結果和偵錯問題。

## 效能考量

廣播是高效的，因為它利用了現代 CPU 的 SIMD 能力。但過度複雜的廣播可能導致隱性記憶體拷貝。用 `np.broadcast_shapes()` 可預測結果形狀，用 `np.shares_memory()` 可檢查是否有拷貝發生。

## 參考資源

- NumPy Broadcasting：https://www.google.com/search?q=numpy+broadcasting+tutorial
- NumPy Shape Matching Rules：https://www.google.com/search?q=numpy+broadcast+rules