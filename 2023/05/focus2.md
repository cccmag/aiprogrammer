# 正則語言與有限自動機 DFA/NFA

## 正則語言

正則語言 (Regular Language) 是 Chomsky 階層中最簡單的一類語言，對應 Type-3 文法。它們擁有極其良好的性質——可以在常數空間內被辨識，時間複雜度為 O(n)。正則語言在計算機科學中無處不在：從文字搜尋到網路協定分析，從編譯器的詞法分析到 DNA 序列比對。

## 確定性有限自動機 (DFA)

DFA (Deterministic Finite Automaton) 是辨識正則語言的最直觀模型。一個 DFA 由五元組 (Q, Σ, δ, q0, F) 定義：

- Q：狀態的有窮集合
- Σ：輸入字母表
- δ：轉移函數，δ: Q × Σ → Q
- q0：起始狀態 (q0 ∈ Q)
- F：接受狀態集合 (F ⊆ Q)

DFA 的關鍵特性是**確定性**：對於每個狀態和每個輸入符號，恰好有一個下一狀態。這使得 DFA 的模擬非常簡單——從起始狀態開始，依序讀入輸入字串的每個字元，最後檢查是否落在接受狀態。

**範例**：辨識所有以 00 結尾的二進位字串

```
Q = {q0, q1, q2}, Σ = {0, 1}, F = {q2}
δ(q0, 0) = q1, δ(q0, 1) = q0
δ(q1, 0) = q2, δ(q1, 1) = q0
δ(q2, 0) = q2, δ(q2, 1) = q0
```

## 非確定性有限自動機 (NFA)

NFA (Nondeterministic Finite Automaton) 取消了 DFA 的確定性限制。在 NFA 中，從一個狀態讀入一個字元後，可能轉移到**多個**狀態，或者沒有轉移。此外，NFA 還允許 ε-轉移（不讀入任何字元就轉移）。

NFA 看似比 DFA 更強大，但實際上兩者的表達能力是**等價的**——每個 NFA 都可以轉換為等價的 DFA（子集建構法）。然而，NFA 往往比對應的 DFA 更加簡潔：最壞情況下，NFA 轉 DFA 會導致狀態數指數級增長。

**範例**：辨識包含 "ab" 或 "ba" 的字串——NFA 的描述比 DFA 簡潔得多

```
Q = {q0, q1, q2, q3, q4}, Σ = {a, b}, F = {q3, q4}
δ(q0, a) = {q0, q1}, δ(q0, b) = {q0, q2}
δ(q1, b) = {q3}
δ(q2, a) = {q4}
```

## 正則語言的封閉性

正則語言在以下運算下保持封閉：

1. **聯集**：若 L1 和 L2 是正則語言，則 L1 ∪ L2 也是
2. **交集**：若 L1 和 L2 是正則語言，則 L1 ∩ L2 也是
3. **補集**：若 L 是正則語言，則其補集也是
4. **串接**：L1 ∘ L2 也是正則語言
5. **Kleene 星號**：L* 也是正則語言

這些封閉性質是正則表達式能工作的理論基礎。

## Pumping Lemma

Pumping Lemma 是用來證明某個語言**不**是正則語言的重要工具。它指出：對於任何正則語言 L，存在一個 pumping 長度 p，使得任何長度 ≥ p 的字串 s ∈ L 都可以被拆分為 s = xyz，並且滿足 xy^iz ∈ L 對於所有 i ≥ 0。

這個引理可以用來證明 L = {a^n b^n | n ≥ 0} 不是正則語言——因為當我們「pump」時，會破壞 a 和 b 的數量相等關係。

## 實際應用

正則語言最著名的應用就是正則表達式 (Regex)。從 grep 到 sed，從 Python 的 re 模組到 JavaScript 的 RegExp——所有這些工具的核心都是一個自動機引擎。

## 參考資料

- [https://www.google.com/search?q=DFA+NFA+finite+automata+regular+language](https://www.google.com/search?q=DFA+NFA+finite+automata+regular+language)
- [https://www.google.com/search?q=regular+language+pumping+lemma](https://www.google.com/search?q=regular+language+pumping+lemma)
- [https://www.google.com/search?q=有限自動機+DFA+NFA](https://www.google.com/search?q=有限自動機+DFA+NFA)
