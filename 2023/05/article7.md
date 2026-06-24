# PDA 設計實例

## PDA 設計的基本原則

設計 PDA 的關鍵是善用堆疊來儲存需要的資訊。與 DFA 不同，PDA 的堆疊提供了無限的記憶空間。

### 通用設計策略

1. **確定堆疊用途**：堆疊可以存儲計數、模式、嵌套層級等資訊
2. **設計狀態**：通常只需少量狀態（甚至一個狀態），大部分資訊存放在堆疊中
3. **設計堆疊操作**：決定何時推入 (push)、何時彈出 (pop)、何時讀取但不修改

## 實例 1：回文語言

### L = {w w^R | w ∈ {a,b}*}

這個語言由一個任意字串 w 和其反轉 w^R 串接而成。PDA 的策略是：

1. 讀取 w 的部分時，將每個字元推入堆疊
2. 猜測中點位置（NFA 的非確定性），進入匹配模式
3. 在匹配模式中，讀取輸入字元並與堆疊頂端比對
4. 如果完全匹配且堆疊為空，則接受

轉移函數設計：
```
δ(q0, a, Z) → (q0, aZ)   # 推入 a
δ(q0, b, Z) → (q0, bZ)   # 推入 b
δ(q0, a, a) → (q0, aa)   # 繼續推入
δ(q0, a, b) → (q0, ab)
δ(q0, b, a) → (q0, ba)
δ(q0, b, b) → (q0, bb)
δ(q0, ε, a) → (q1, a)    # 猜測中點，進入 q1
δ(q0, ε, b) → (q1, b)
δ(q1, a, a) → (q1, ε)    # 匹配並彈出
δ(q1, b, b) → (q1, ε)
δ(q1, ε, Z) → (q1, ε)    # 空堆疊時接受
```

## 實例 2：多重計數

### L = {a^i b^j c^k | i = j 或 i = k}

這個語言需要處理「或」條件。PDA 可以使用非確定性來猜測哪個條件成立：

**分支 1（i = j）**：
- 讀取 a：在堆疊中計數（推入 A）
- 讀取 b：從堆疊中彈出 A
- 如果 b 的數量和 a 相同（堆疊回到空狀態），則繼續處理任意數量的 c

**分支 2（i = k）**：
- 讀取 a：在堆疊中計數（推入 A）
- 讀取任意數量的 b（忽略，不操作堆疊）
- 讀取 c：從堆疊中彈出 A

這個範例展示了 PDA 如何利用非確定性來處理邏輯「或」條件——DPDA 無法做到這一點。

## 實例 3：巢狀括號

### L = {w ∈ {(,)}* | w 的括號是匹配的}

這是程式語言中最常見的結構之一。

```
δ(q0, (, Z) → (q0, (Z)   # 遇到左括號，推入
δ(q0, (, () → (q0, (()
δ(q0, ), () → (q0, ε)    # 遇到右括號，彈出
δ(q0, ε, Z) → (q1, Z)    # 堆疊清空，進入接受狀態
```

這個 PDA 是確定性的——DPDA 即可處理。實際上，匹配括號的語言是 DPDA 可以辨識的典型範例。

## 實作筆記

PDA 的模擬與 NFA 類似，但需要考慮堆疊內容。由於堆疊可以是無限的，模擬時需要謹慎處理（可能無法終止）。

在 `automata.py` 中，我們使用簡化的 PDA 模型來演示核心概念。

## 參考資料

- [https://www.google.com/search?q=pushdown+automaton+design+examples](https://www.google.com/search?q=pushdown+automaton+design+examples)
- [https://www.google.com/search?q=PDA+balanced+parentheses+palindrome](https://www.google.com/search?q=PDA+balanced+parentheses+palindrome)
- [https://www.google.com/search?q=PDA+設計+實例](https://www.google.com/search?q=PDA+設計+實例)
