# 密度演化與 LDPC

## LDPC 碼的理論基礎

LDPC（Low-Density Parity-Check）碼是 Gallager 在 1960 年提出的一種線性區塊碼，其同位檢查矩陣 $\mathbf{H}$ 非常稀疏（大部分元素為 0）。這種稀疏性使得 LDPC 碼可以在線性時間內完成解碼，同時逼近 Shannon 極限。

LDPC 碼可以分為兩大類：
- **正則 LDPC**：每行有固定 $\gamma$ 個 1，每列有固定 $\rho$ 個 1
- **不規則 LDPC**：行重與列重可變，通常效能更好

## Tanner 圖表示

LDPC 碼可以用 Tanner 圖（二部圖）來表示：
- **變數節點**：對應碼字中的每個位元（矩陣的每一行）
- **檢查節點**：對應每個同位檢查方程式（矩陣的每一列）
- **邊**：連接變數節點與檢查節點，對應 $\mathbf{H}$ 中的非零元素

```
檢查節點:  [c1]──[c2]──[c3]
             │\  /│\  /│
             │ \/ │ \/ │
             │ /\ │ /\ │
             │/  \│/  \│
變數節點:  [v1] [v2] [v3] [v4]
```

## 信念傳播解碼

LDPC 的解碼使用信念傳播演算法（Belief Propagation, BP），又稱和積演算法（Sum-Product Algorithm）：

1. 變數節點將初始的通道觀測資訊傳遞給相鄰的檢查節點
2. 檢查節點根據傳入的資訊計算「外資訊」並傳回變數節點
3. 變數節點結合所有傳入的資訊更新其對位元值的信念
4. 重複直到滿足所有檢查方程式或達到最大迭代次數

## 密度演化

密度演化（Density Evolution）是分析 LDPC 碼解碼閾值的強大工具，由 Richardson 與 Urbanke 在 2001 年提出。其核心思想是追蹤 BP 解碼過程中訊息機率分布的演化。

在每次 BP 迭代中，訊息分布會根據固定的規則變化：
- 變數節點更新：輸入資訊的卷積
- 檢查節點更新：輸入資訊的非線性變換

當訊息分布收斂到正確解碼的分布時，表示解碼成功；若收斂到錯誤分布（或無法收斂），則解碼失敗。密度演化可以計算出一個雜訊閾值 $\sigma^*$，當通道雜訊低於此閾值時，碼長趨近於無限的 LDPC 碼可以實現任意低的錯誤率。

## 實務意義

密度演化讓編碼設計者可以在不進行大量模擬的情況下，預測給定 $\mathbf{H}$ 矩陣分布的解碼效能。這使得不規則 LDPC 碼的最佳化設計成為可能：通過調整度分布來最大化雜訊閾值。現代的 5G NR 與 Wi-Fi 6 LDPC 碼的最佳化都依賴於密度演化分析。

## 參考資源

- https://www.google.com/search?q=Density+evolution+LDPC+threshold+analysis+Richardson+Urbanke+algorithm
- https://www.google.com/search?q=belief+propagation+sum+product+algorithm+LDPC+decoding+tanner+graph+messages
- https://www.google.com/search?q=irregular+LDPC+code+design+degree+distribution+optimization+density+evolution
