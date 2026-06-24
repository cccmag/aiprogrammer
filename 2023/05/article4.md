# CFG 設計與語法樹

## CFG 的設計方法

設計上下文無關文法是一門藝術。與 DFA 設計不同，CFG 的設計沒有統一的演算法。然而，有一些常見的模式和技巧可以幫助我們。

### 遞迴結構

CFG 的核心是遞迴。如果一個語言包含嵌套或重複結構，遞迴產生規則通常是解決方案。

### 常見模式

**模式 1：計數**
```
L = {a^n b^n | n ≥ 0}
S → aSb | ε
```
核心技巧是用遞迴產生規則來保證兩邊的計數相等。

**模式 2：前綴與後綴**
```
L = {w w^R | w ∈ {a,b}*}
S → aSa | bSb | ε
```
這個文法保證對稱性——前綴和後綴互為反轉。

**模式 3：聯集**
```
L = {a^n b^n | n ≥ 0} ∪ {a^n b^(2n) | n ≥ 0}
S → A | B
A → aAb | ε
B → aBbb | ε
```
用多個起始產生規則來處理語言的併集。

**模式 4：串接**
```
L = {a^n b^n a^m b^m | n,m ≥ 0}
S → AB
A → aAb | ε
B → aBb | ε
```
將語言拆分為兩個獨立部分的串接。

## 語法樹的建構

語法樹 (Parse Tree / Syntax Tree) 是 CFG 推導過程的樹狀表示。

### 具體語法樹 (CST) vs 抽象語法樹 (AST)

**具體語法樹**：保留文法推導的所有細節，包括非終止符號節點。它與文法的結構完全對應。

**抽象語法樹**：去除文法推導的中間節點，只保留對語意分析有意義的資訊。例如，表達式 `3 + 4 * 5` 的 AST 直接顯示了運算子的優先級。

```
CST:                    AST:
    E                     (+)
  / | \                  /  \
 E  +  T                3    (*)
 |    / \                  /  \
 T   T  *  F              4    5
 |   |    |
 F   F    id(5)
 |   |
id  id
(3) (4)
```

### 語法樹的遍歷

語法樹的遍歷順序決定了程式碼生成的順序：
- **前序遍歷**：用於生成前綴表達式
- **中序遍歷**：用於生成原始程式碼
- **後序遍歷**：用於生成後綴表達式（便於堆疊機執行）

## 實際應用

CFG 在以下領域有廣泛應用：
- **程式語言設計**：定義語法的標準方式
- **文件格式**：JSON、XML、Markdown 的語法定義
- **自然語言處理**：句法分析
- **生物資訊學**：RNA 二級結構預測（使用上下文無關文法）

## 參考資料

- [https://www.google.com/search?q=context+free+grammar+design+patterns](https://www.google.com/search?q=context+free+grammar+design+patterns)
- [https://www.google.com/search?q=parse+tree+AST+vs+CST+compiler](https://www.google.com/search?q=parse+tree+AST+vs+CST+compiler)
- [https://www.google.com/search?q=CFG+設計+語法樹](https://www.google.com/search?q=CFG+設計+語法樹)
