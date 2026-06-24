# 5. 線性碼與漢明碼

## 線性碼基礎

線性碼是一種通道編碼，其編碼操作是一個線性變換。若訊息向量 $\mathbf{m} \in \{0,1\}^k$，碼字 $\mathbf{c} \in \{0,1\}^n$，則：

$$\mathbf{c} = \mathbf{m} \mathbf{G}$$

其中 $\mathbf{G}$ 是 $k \times n$ 的生成矩陣。線性碼的關鍵特性是任意兩個碼字的和（XOR）仍然是碼字。

## 漢明距離

兩個碼字之間不同位元的個數稱為漢明距離（Hamming Distance）。一個碼的最小漢明距離 $d_{\min}$ 決定了它的錯誤修正能力：

- 可偵測 $d_{\min} - 1$ 個錯誤
- 可修正 $\lfloor (d_{\min} - 1) / 2 \rfloor$ 個錯誤

## 漢明碼 (7,4)

漢明碼是 R. W. Hamming 在 1950 年發明的線性碼。最經典的 (7,4) 漢明碼將 4 個資料位元編碼為 7 個位元，可以修正單一位元錯誤。

生成矩陣：

$$\mathbf{G} = \begin{bmatrix}
1 & 1 & 1 & 0 & 0 & 0 & 0 \\
1 & 0 & 0 & 1 & 1 & 0 & 0 \\
0 & 1 & 0 & 1 & 0 & 1 & 0 \\
1 & 1 & 0 & 1 & 0 & 0 & 1
\end{bmatrix}$$

同位檢查矩陣 $\mathbf{H}$ 滿足 $\mathbf{H} \mathbf{c}^T = \mathbf{0}$ 對所有碼字成立。解碼時計算伴隨式（Syndrome）$\mathbf{s} = \mathbf{H} \mathbf{r}^T$，從伴隨式可以定位錯誤位元的位置。

## Python 實作

```python
def hamming_encode(bits4):
    d = list(bits4)
    p1 = d[0] ^ d[1] ^ d[3]
    p2 = d[0] ^ d[2] ^ d[3]
    p3 = d[1] ^ d[2] ^ d[3]
    return [p1, p2, d[0], p3, d[1], d[2], d[3]]
```

解碼時計算三個伴隨式位元，其二進位值即為錯誤位置（1-indexed）。將該位元反轉即可完成糾錯。

## 參考資源

- https://www.google.com/search?q=linear+code+generator+matrix+parity+check+Hamming+distance+error+correction
- https://www.google.com/search?q=Hamming+code+7+4+encode+decode+syndrome+tutorial+example
- https://www.google.com/search?q=Hamming+code+single+error+correction+double+error+detection+SEC+DEC
