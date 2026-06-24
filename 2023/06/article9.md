# Cook-Levin 定理導論

## 計算理論的里程碑

1971 年，Stephen Cook 在多倫多大學發表了一篇題為《The Complexity of Theorem-Proving Procedures》的論文。在這篇論文中，Cook 證明了 SAT（布林可滿足性問題）是 NP-Complete 的。幾乎同時，蘇聯數學家 Leonid Levin 獨立得到了相同的結果。這個定理現在被稱為 Cook-Levin 定理，是計算複雜度理論的奠基性成果。

## 定理陳述

> **Cook-Levin 定理**：SAT 問題是 NP-Complete 的。

這意味著：
1. SAT ∈ NP（可以在多項式時間內驗證一個 SAT 的解答）
2. SAT 是 NP-Hard（所有 NP 問題都可以在多項式時間內歸約到 SAT）

## 為什麼這個定理如此重要？

在 Cook-Levin 定理之前，NP-Complete 的概念還不存在。Cook 不僅定義了這個概念，還給出了第一個具體的 NP-Complete 問題。有了 SAT 作為「錨點」，其他問題的 NP-Completeness 就可以透過歸約來證明：

一旦我們有了第一個 NP-Complete 問題（SAT），要證明另一個問題 B 是 NP-Complete，只需要：
1. 證明 B ∈ NP
2. 證明 SAT ≤ₚ B（將 SAT 歸約到 B）

## 證明的核心思路

Cook 證明的核心是：任意 NP 問題都可以用一個 SAT 實例來編碼。

給定一個非確定性圖靈機 M 和一個輸入 w，我們需要構造一個布林公式 φ，使得：

> M 在 w 上接受 ⇔ φ 是可滿足的

φ 使用以下變數來描述 M 的計算過程：

1. **狀態變數**：T(i, j, t) — 在第 t 步，紙帶的第 i 格是否包含符號 j
2. **狀態變數**：H(i, t) — 在第 t 步，讀寫頭是否在第 i 格
3. **狀態變數**：Q(q, t) — 在第 t 步，機器是否處於狀態 q

## φ 的構造

φ 是以下四個部分的合取：

### φ₁：初始狀態
描述計算開始時的紙帶內容、讀寫頭位置和狀態。

### φ₂：每一步的唯一性
在每一步，紙帶的每個格子只能有一個符號，讀寫頭只能在一個位置，機器只能處於一個狀態。

### φ₃：轉移的正確性
描述每一步如何從前一步合法轉移過來。這需要對每對相鄰的格子編碼轉移函式的約束。

### φ₄：接受狀態
描述計算最終進入接受狀態。

整個公式的大小是 O(p(n)²)，其中 p(n) 是 M 的執行時間（多項式）。

## 變數數量

假設 M 的執行時間是 T = p(|w|)：

- 紙帶長度：最多 T 格（因為頭最多移動 T 步）
- 紙帶符號數量：|Γ|
- 狀態數量：|Q|
- 時間步數：T

總變數數量大約是 O(T² × log|Γ| + T × log|Q|) = O(p(n)²)。

## 證明的深遠意義

### 理論意義

1. **NP-Completeness 概念的確立**：為整個複雜度理論提供了基礎
2. **歸約方法論**：建立了「用已知 NP-Complete 問題證明新問題」的標準流程
3. **P vs NP 的焦點**：將 P vs NP 問題濃縮到單一問題 SAT 上

### 實務意義

1. **SAT 求解器的發展**：現代 SAT 求解器可以解決數百萬變數的實際問題
2. **問題的編碼**：工程師學會將實際問題編碼為 SAT 並用求解器解決
3. **工具生態**：Z3、MiniSat、Glucose 等工具廣泛應用於工業界

## 從 Cook-Levin 到現代 SAT

```
Cook-Levin (1971)
    ↓
SAT 求解器研究（1970s-1990s）
    ├── DPLL 演算法
    └── 子句學習 (CDCL)
            ↓
現代 SAT 求解器（2000s-present）
    ├── MiniSat (2003)    → 開源的里程碑
    ├── Glucose           → 學習子句刪除策略
    ├── Z3 (2012)         → Microsoft 的 SMT 求解器
    └── CryptoMiniSat     → 專門處理 XOR 約束
```

## 延伸閱讀

- [Cook-Levin Theorem 證明詳解](https://www.google.com/search?q=Cook+Levin+theorem+proof+details)
- [SAT and NP-Completeness](https://www.google.com/search?q=SAT+NP+completeness+Cook+1971)
- [從 Cook-Levin 到現代 SAT 求解器](https://www.google.com/search?q=history+SAT+solver+DPLL+CDCL)
