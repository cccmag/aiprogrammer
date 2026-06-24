# Focus 1：反向傳播算法詳解

## 反向傳播的由來

反向傳播（Backpropagation）是深度學習的核心算法，由 Rumelhart、Hinton 和 Williams 在 1986 年提出。其核心思想是利用微分鏈式法則，高效計算網路引數的梯度。這個演算法的意義在於：將計算梯度所需的運算量從與參數數量成正比降低到與計算量成正比，使得大規模神經網路的訓練成為可能。

## 計算圖與鏈式法則

現代深度學習框架都基於計算圖（Computational Graph）進行自動微分。向前傳播時，每個節點計算並儲存輸入；向後傳播時，每個節點利用已計算的梯度，計算輸入的梯度並繼續向後傳遞。關鍵洞察是：每個節點只需知道如何計算自己的局部梯度（輸入對輸出的導數），框架自動组合這些局部梯度得到最終梯度。

## 鏈式法則

若 y = f(g(x))，則 dy/dx = (df/dg) * (dg/dx)。在多層網路中，這個鏈會非常長。反向傳播的精髓是從輸出層開始，逐層向後計算並傳遞梯度，每層的計算代價僅與該層的計算代價相當。

## 實作要點

實際實現反向傳播時有幾個關鍵點。首先是順序：必須確保向前傳播完成後才能開始向後傳播。其次是記憶體：需要儲存向前傳播的中間結果用於向後計算，這是gradient checkpointing 的理論基礎。第三是向量化：利用矩陣運算而非迴圈，大幅提升效率。

## 參考資源

- Backpropagation Original Paper：https://www.google.com/search?q=backpropagation+rumelhart+1986
- Automatic Differentiation：https://www.google.com/search?q=automatic+differentiation+pytorch