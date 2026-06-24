# 正則表達式與 Kleene 定理

## 正則表達式的起源

正則表達式 (Regular Expression) 的概念源自 1956 年 Stephen Kleene 的論文《Representation of Events in Nerve Nets and Finite Automata》。Kleene 在論文中提出了一個重要的問題：如何用代數的方式來描述有限自動機所能辨識的語言？

## Kleene 定理

Kleene 定理是正則語言理論的核心結果。它指出：

**一個語言是正則語言，若且唯若它可以被正則表達式描述。**

這個定理建立了兩種觀點的等價性：
- **機械觀點**：有限自動機（DFA/NFA）——以狀態轉移來辨識語言
- **代數觀點**：正則表達式——以符號運算來描述語言

這意味著我們可以在兩者之間自由轉換：從正則表達式可以建構等價的自動機（用於匹配），從自動機也可以推導出對應的正則表達式（用於分析）。

## 正則表達式的運算

正則表達式由三種基本運算組成：

### 聯集 (Union)

符號為 `|`。R|S 表示匹配 R 或 S 中的任一個。

```
(a|b) 匹配 "a" 或 "b"
```

### 串接 (Concatenation)

符號為隱式或 `.`。RS 表示匹配 R 後緊跟 S。

```
ab 匹配 "ab"
```

### Kleene 星號 (Kleene Star)

符號為 `*`。R* 表示匹配 R 的零次或多次重複。

```
a* 匹配 "", "a", "aa", "aaa" ...
```

## 從正則表達式到 NFA：Thompson 建構

Thompson 建構 (Thompson's Construction) 是將正則表達式轉換為等價 NFA 的標準演算法。其核心思想是為每種運算定義一個對應的 NFA 片段：

1. **單一字元 a**：兩個狀態，一個 ε 轉移
2. **聯集 R|S**：加入一個新的起始狀態和接受狀態，用 ε 轉移連接到 R 和 S
3. **串接 RS**：將 R 的接受狀態連接到 S 的起始狀態
4. **Kleene 星號 R***：加入 ε 迴路

Thompson 建構是大多數正則表達式引擎的基礎。例如，Python 的 re 模組、AWK、grep 等工具都使用了基於自動機的匹配策略。

## 從 DFA 到正則表達式

反過來，從 DFA 推導正則表達式的過程涉及消除狀態。常用的方法包括：

1. **狀態消除法**：逐步移除 DFA 的狀態，同時更新路徑標籤
2. **Arden 引理**：用線性方程組求解正則表達式
3. **傳遞閉包法**：類似 Floyd-Warshall 演算法

## 正則表達式的限制

正則表達式雖然強大，但有其根本限制——它們只能描述正則語言。無法用正則表達式描述的語言包括：

- 匹配括號的語言 {a^n b^n}
- 迴文語言 {ww^R}
- 程式語言的嵌套結構（如 if 內嵌套 if）

這些需要更強大的語言類別——上下文無關語言——才能描述。

## 實際應用

正則表達式是現代程式設計的基本工具：

- **文字處理**：搜尋、取代、分割
- **驗證**：電子郵件、電話號碼、身分證字號
- **詞法分析**：編譯器的第一個階段
- **網路安全**：入侵檢測系統的規則描述

## 參考資料

- [https://www.google.com/search?q=Kleene+theorem+regular+expression+automata](https://www.google.com/search?q=Kleene+theorem+regular+expression+automata)
- [https://www.google.com/search?q=regular+expression+engine+implementation](https://www.google.com/search?q=regular+expression+engine+implementation)
- [https://www.google.com/search?q=正則表達式+Kleene+定理](https://www.google.com/search?q=正則表達式+Kleene+定理)
