# 下推自動機 PDA

## 從有限記憶到無限堆疊

有限自動機 (DFA/NFA) 的記憶能力受限於其狀態數量。一旦狀態數固定，自動機能「記住」的資訊就是有限的。這解釋了為什麼有限自動機無法辨識 {a^n b^n} 這類需要計數的語言。

下推自動機 (Pushdown Automaton, PDA) 在有限自動機的基礎上增加了一個**堆疊 (Stack)**——一個具有無限容量的後進先出記憶體。這個堆疊賦予了 PDA 辨識上下文無關語言的能力。

## PDA 的定義

一個 PDA 由七元組 (Q, Σ, Γ, δ, q0, Z0, F) 定義：

- Q：狀態的有窮集合
- Σ：輸入字母表
- Γ：堆疊字母表
- δ：轉移函數，δ: Q × (Σ ∪ {ε}) × Γ → Q × Γ* 的有限子集
- q0：起始狀態
- Z0：初始堆疊符號
- F：接受狀態集合

PDA 的每一步操作包含：讀取當前狀態、輸入字元（或 ε）、堆疊頂端符號；然後轉移到新狀態，並對堆疊執行推入或彈出操作。

## 兩種接受方式

PDA 有兩種等價的接受條件：

1. **以接受狀態接受**：讀完整個輸入後，PDA 處於接受狀態
2. **以空堆疊接受**：讀完整個輸入後，PDA 的堆疊為空

這兩種定義方式在表達能力上是等價的。

## 範例：{a^n b^n} 的 PDA

考慮語言 L = {a^n b^n | n ≥ 1}。以下是其 PDA：

1. 讀入 a：將 A 推入堆疊（計數 a 的數量）
2. 讀入 b：彈出堆疊中的一個 A（配對 b 與 a）
3. 輸入結束且堆疊為空：接受

這個 PDA 展示了堆疊如何提供「計數」能力，這是有限自動機無法做到的。

## PDA 與 CFG 的等價性

PDA 和 CFG 是描述上下文無關語言的兩種等價形式：

**定理**：一個語言是上下文無關語言，若且唯若它可以被某個 PDA 辨識。

這個定理的證明包含兩個方向：
1. **CFG → PDA**：從文法構造一個 PDA，使其能辨識該文法產生的所有字串。基本思路是用 PDA 的堆疊來模擬文法的最左推導。
2. **PDA → CFG**：從 PDA 構造一個 CFG，使其產生 PDA 能接受的所有字串。

## 確定性 vs 非確定性 PDA

與有限自動機不同，**確定性 PDA (DPDA)** 和**非確定性 PDA (NPDA)** 的表達能力並不等價。

- DPDA 可以辨識所有正則語言和一部分上下文無關語言（如 {a^n b^n}）
- NPDA 可以辨識所有上下文無關語言（包括 {ww^R} 這類語言）

也就是說，某些上下文無關語言不能被任何 DPDA 辨識。這與有限自動機的情況（DFA = NFA）形成了鮮明對比。

## 實際應用

PDA 在編譯器設計中有直接應用：

- **LL 解析器**：使用 DPDA 的自上而下解析
- **LR 解析器**：使用 DPDA 的自下而上解析，被 Yacc/Bison 等工具採用
- **語法導向翻譯**：在語法分析的同時執行語意動作

## 參考資料

- [https://www.google.com/search?q=pushdown+automaton+PDA+context+free+language](https://www.google.com/search?q=pushdown+automaton+PDA+context+free+language)
- [https://www.google.com/search?q=deterministic+pushdown+automaton+DPDA](https://www.google.com/search?q=deterministic+pushdown+automaton+DPDA)
- [https://www.google.com/search?q=下推自動機+PDA](https://www.google.com/search?q=下推自動機+PDA)
