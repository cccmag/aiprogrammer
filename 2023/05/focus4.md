# 上下文無關語言 CFG

## 從正則語言到上下文無關語言

正則語言雖然有用，但表達能力有限。例如，我們無法用正則表達式描述一個語言，其中 a 和 b 的數量相同——L = {a^n b^n | n ≥ 0}。為了解決這個限制，我們需要更強大的文法：上下文無關文法 (Context-Free Grammar, CFG)。

CFG 由 Chomsky 在 1956 年提出，旨在描述自然語言的句法結構。後來人們發現，CFG 恰好是描述程式語言語法的理想工具——幾乎所有程式語言的核心語法都可以用 CFG 定義。

## CFG 的定義

一個上下文無關文法 G 是一個四元組 (V, T, P, S)：

- V：非終止符號 (Nonterminal) 的有窮集合
- T：終止符號 (Terminal) 的有窮集合，V ∩ T = ∅
- P：產生規則 (Production) 的有窮集合，形式為 A → γ，其中 A ∈ V，γ ∈ (V ∪ T)*
- S：起始符號 (Start Symbol)，S ∈ V

「上下文無關」的含義是：產生規則 A → γ 可以在任何時候應用，無論 A 的上下文是什麼。

## 範例：算術表達式

下面是一個簡單算術表達式的 CFG：

```
E → E + T | T
T → T * F | F
F → (E) | id
```

這個文法描述了包含加法、乘法和括號的表達式。例如，表達式 `id + id * id` 的推導過程為：

```
E ⇒ E + T ⇒ T + T ⇒ F + T ⇒ id + T
⇒ id + T * F ⇒ id + F * F ⇒ id + id * id
```

## 語法樹 (Parse Tree)

CFG 的推導過程可以視覺化為一棵語法樹。語法樹的根節點是起始符號 S，內部節點是非終止符號，葉節點是終止符號。語法樹展示了字串的結構化表示，對於編譯器的後續階段（語意分析、程式碼生成）至關重要。

上例中 `id + id * id` 的語法樹顯示了運算子的優先級：乘法的位置比加法更低，因此乘法先被計算。

## 歧義文法

如果一個文法可以為同一個字串產生兩個不同的語法樹，則稱該文法是歧義的 (Ambiguous)。

```
E → E + E | E * E | (E) | id
```

這個文法對 `id + id * id` 可以產生兩種語法樹——一種對應 `(id + id) * id`，另一種對應 `id + (id * id)`。為了消除歧義，我們需要改寫文法，將運算符優先級和結合性編碼到文法結構中。

## 正規形式

CFG 有幾種重要的正規形式：

### Chomsky 正規形式 (CNF)

所有產生規則的形式為 A → BC 或 A → a。任何 CFG 都可以轉換為 CNF。CNF 在 CYK 演算法中使用，可以在 O(n^3) 時間內判斷一個字串是否屬於該語言。

### Greibach 正規形式 (GNF)

所有產生規則的形式為 A → aα，其中 a 是終止符號，α 是非終止符號序列。GNF 使得遞迴下推解析 (Recursive Descent Parsing) 更加直接。

## 實際應用

CFG 在編譯器設計中扮演核心角色：

- **語法分析**：將原始碼解析為語法樹
- **靜態分析**：基於語法樹進行型別檢查和作用域分析
- **程式碼生成**：從語法樹生成目標程式碼
- **程式碼格式化**：利用語法樹重建格式化的文字

Yacc、Bison、ANTLR 等解析器生成器都以 CFG 為輸入，自動產生高效的語法分析器。

## 參考資料

- [https://www.google.com/search?q=context+free+grammar+CFG+programming+languages](https://www.google.com/search?q=context+free+grammar+CFG+programming+languages)
- [https://www.google.com/search?q=parse+tree+syntax+analysis+compiler](https://www.google.com/search?q=parse+tree+syntax+analysis+compiler)
- [https://www.google.com/search?q=上下文無關文法+CFG](https://www.google.com/search?q=上下文無關文法+CFG)
