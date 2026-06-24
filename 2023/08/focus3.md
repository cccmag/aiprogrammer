# 語法分析：上下文無關文法與 Parser

## 從 Token 到語法樹

詞法分析將原始碼轉換為 Token 序列後，語法分析（Parsing）的任務是根據語言的文法規則，將這些 Token 組織成語法樹。這個階段確定了程式的結構——哪些表達式嵌套在哪些表達式中，哪些陳述式屬於哪些區塊。

## 上下文無關文法（CFG）

上下文無關文法（Context-Free Grammar, CFG）是描述程式語言語法的標準形式。一個 CFG 由四部分組成：

- **終結符（Terminals）**：實際的 Token，如 `+`、`(`、`42`
- **非終結符（Non-terminals）**：語法範疇，如 `expr`、`stmt`
- **產生式（Productions）**：規則，如 `expr → expr + term`
- **起始符（Start Symbol）**：文法的根，如 `program`

### 範例：簡單算術表達式

```
expr  → term
       | expr + term
       | expr - term

term  → factor
       | term * factor
       | term / factor

factor → NUMBER
        | IDENT
        | ( expr )
```

這個文法規定了運算子的優先級：乘除優先於加減，括號可以改變優先級。

## 推導與語法樹

給定一個輸入 `3 + 4 * 2`，語法分析器會進行推導：

```
expr
→ expr + term
→ term + term
→ factor + term
→ 3 + term
→ 3 + term * factor
→ 3 + factor * factor
→ 3 + 4 * factor
→ 3 + 4 * 2
```

對應的語法樹（Parse Tree）為：

```
      expr
     / | \
  expr + term
   |     / | \
  term  term * factor
   |     |      |
 factor factor 2
   |     |
   3     4
```

## 解析策略

### 自上而下解析（Top-Down Parsing）

從起始符號開始，逐步展開非終結符，直到匹配輸入。LL 解析器（如遞迴下降解析器）是典型代表：

```python
def parse_expr(self):
    left = self.parse_term()
    while self.peek() in ('+', '-'):
        op = self.consume()
        right = self.parse_term()
        left = AST('BinOp', op=op, left=left, right=right)
    return left
```

### 自下而上解析（Bottom-Up Parsing）

從輸入開始，逐步歸約到起始符號。LR 解析器（如 Yacc/Bison）是典型代表。LR 解析器可以處理更大的文法集合，但難以手動實作。

### LL vs LR 對比

| 特性 | LL 解析 | LR 解析 |
|---|---|---|
| 策略 | 自上而下的推導 | 自下而上的歸約 |
| 文法限制 | 不能有左遞迴 | 可處理更多文法 |
| 實作難度 | 容易手動實作 | 自動產生器為主 |
| 錯誤回報 | 可精確定位 | 較難定位 |
| 代表工具 | ANTLR, 手寫解析器 | Yacc, Bison, LALRPop |
| 應用場景 | 遞迴下降解析器 | 編譯器產生器 |

## 消除左遞迴

LL 解析器不能處理左遞迴文法：
```
expr → expr + term  # 左遞迴！
```
需要改寫為右遞迴或使用疊代：

```
expr  → term expr'
expr' → + term expr' | ε
```

## 本期實作

迷你編譯器使用遞迴下降解析器（Recursive Descent Parser），是 LL 解析的一種形式。每個非終結符對應一個方法，方法之間可以互相遞迴呼叫。解析器同時建構 AST，將線性的 Token 序列轉換為樹狀結構。

## 延伸閱讀

- [上下文無關文法教學](https://www.google.com/search?q=context+free+grammar+tutorial)
- [遞迴下降解析器實作](https://www.google.com/search?q=recursive+descent+parser+implementation)
- [Yacc 與 Bison 教學](https://www.google.com/search?q=Yacc+Bison+parser+generator+tutorial)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之三。*
