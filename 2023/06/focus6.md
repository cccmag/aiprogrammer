# NP-Complete 與 NP-Hard

## NP 中的難題

在 NP 類別中，有些問題被認為比其他問題更「難」。NP-Complete 就是 NP 中最難的問題——如果其中任何一個可以在多項式時間內解決，那麼所有 NP 問題都可以。

## NP-Complete 的定義

一個問題 L 是 NP-Complete 的，當且僅當：

1. L ∈ NP（可以在多項式時間內驗證解答）
2. L 是 NP-Hard（所有 NP 問題都可以在多項式時間內歸約到 L）

一個問題是 NP-Hard 的，如果所有 NP 問題都可以歸約到它——但它本身不一定在 NP 中。

```
          ┌─────────────────────┐
          │       NP-Hard       │
          │  ┌───────────────┐  │
          │  │   NP-Complete │  │
          │  │  ┌──────┐     │  │
          │  │  │  NP  │     │  │
          │  │  │ ┌──┐ │     │  │
          │  │  │ │P │ │     │  │
          │  │  │ └──┘ │     │  │
          │  │  └──────┘     │  │
          │  └───────────────┘  │
          └─────────────────────┘
```

## Cook-Levin 定理

1971 年，Stephen Cook 在多倫多大學發表了開創性的論文《The Complexity of Theorem-Proving Procedures》，證明了 SAT 問題是 NP-Complete 的。幾乎同時，Leonid Levin 在蘇聯獨立得到了相同的結果。

Cook-Levin 定理的意義在於：它給出了**第一個** NP-Complete 問題。有了 SAT 之後，我們就可以利用歸約來證明其他問題是 NP-Complete 的。

## 經典 NP-Complete 問題

以下是最著名的 NP-Complete 問題（及其歸約鏈）：

```
SAT
 └─→ 3-SAT（將每個子句限制為恰好 3 個文字）
      └─→ 頂點覆蓋
      │    └─→ 獨立集
      │    └─→ 團
      └─→ 漢米爾頓路徑
      │    └─→ 旅行推銷員（TSP）
      └─→ 子集和
      │    └─→ 背包問題
      └─→ 圖著色
```

## 頂點覆蓋

給定一個無向圖 G = (V, E) 和一個整數 k，是否存在一個大小 ≤ k 的頂點集合 C，使得每條邊至少有一個端點在 C 中？

頂點覆蓋是 NP-Complete 的。它可以從 3-SAT 歸約得到：每個變數對應兩個頂點（x 和 ¬x）用邊連接，每個子句對應三個頂點的三角形，然後用連接器將文字與對應的子句頂點連接。

## 圖著色

給定一個無向圖 G = (V, E) 和一個整數 k，是否存在一個 k-著色方案，使得相鄰頂點顏色不同？

3-著色問題（判斷一個圖是否可以用 3 種顏色著色）是 NP-Complete 的。有趣的是，2-著色問題（判斷是否為二分圖）可以在線性時間內解決。

## 歸約技巧

證明一個問題是 NP-Complete 的標準步驟：

1. 證明該問題在 NP 中（給出多項式時間驗證器）
2. 選擇一個已知的 NP-Complete 問題
3. 構造從該已知問題到目標問題的多項式時間歸約
4. 證明歸約的正確性（如果且唯若）

常用的歸約元件：
- **變數元件**：表示布林變數
- **子句元件**：表示 CNF 子句
- **連接器**：將變數與子句連接起來
- **限制器**：確保某些條件成立

## NP-Hard 問題

NP-Hard 問題是所有 NP 問題都可以歸約到的問題，但它們不一定在 NP 中。常見的 NP-Hard 問題包括：

- **最佳化版本的 TSP**：找到最短的漢米爾頓迴路
- **整數規劃**：整數線性規劃的最優化解
- **停機問題**（事實上是不可判定的，比 NP-Hard 更難）

## NP-Complete 的實務意義

雖然 NP-Complete 問題在理論上很難，但在實務中：

1. **近似演算法**：許多 NP-Complete 問題有良好的近似演算法
2. **參數化演算法**：對於固定的參數 k，可以在 O(f(k) × n^c) 時間內解決
3. **啟發式演算法**：模擬退火、遺傳演算法在實務中表現良好
4. **SAT 求解器**：現代 SAT 求解器（如 MiniSat、Z3）可以解決數百萬變數的實例
5. **特殊情況**：某些 NP-Complete 問題在其他約束下可以高效解決

## 延伸閱讀

- [Cook-Levin Theorem](https://www.google.com/search?q=Cook+Levin+theorem+proof)
- [NP-Completeness 經典歸約](https://www.google.com/search?q=NP+complete+reductions)
- [Vertex Cover Problem](https://www.google.com/search?q=vertex+cover+NP+complete)
