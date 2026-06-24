# Article 1：從微分到反向傳播

## 導數的回顧

導數描述函數輸出相對於輸入的變化率。對於 f(x) = x²，導數 f'(x) = 2x。導數的鏈式法則允許我們計算複合函數的導數：若 y = f(g(x))，則 dy/dx = (df/dg) * (dg/dx)。

## 計算圖

將神經網路視為計算圖，每個節點是張量，每條邊是運算。向前傳播時，從輸入到輸出逐節點計算。向後傳播時，利用鏈式法則從輸出到輸入逐節點計算梯度。計算圖可以是有向無環圖（DAG），框架負責正確的求導順序。

## 向量化導數

實務中常使用矩陣/張量運算。需要記住幾個關鍵導數：∂(XY)/∂X = Y^T、∂(XW+b)/∂W = X^T、∂L/∂X = Σ_i (∂L/∂Y_i) * ∂Y_i/∂X。這些公式在推導神經網路梯度時反覆使用。

## 實現要點

實作反向傳播時的幾個關鍵點：
1. 記錄向前傳播的中間結果
2. 從輸出層開始計算梯度
3. 利用鏈式法則逐層向後傳遞
4. 梯度是增加值，非替代值

## 參考資源

- Chain Rule Calculus：https://www.google.com/search?q=chain+rule+matrix+derivative
- Autograd in PyTorch：https://www.google.com/search?q=pytorch+autograd+backpropagation