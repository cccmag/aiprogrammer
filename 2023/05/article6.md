# Chomsky 正規形式

## 什麼是 Chomsky 正規形式？

Chomsky 正規形式 (Chomsky Normal Form, CNF) 是上下文無關文法的一種標準化形式。在 CNF 中，所有產生規則都限制為以下兩種形式之一：

1. **A → BC**：一個非終止符號產生兩個非終止符號
2. **A → a**：一個非終止符號產生一個終止符號

此外，如果語言包含空字串 ε，則允許規則 S → ε（其中 S 是起始符號）。

任何上下文無關文法都可以轉換為 CNF。這說明 CNF 的表達能力與 CFG 完全相同，但形式更加規範。

## 為什麼需要 CNF？

CNF 的重要性來自兩個方面：

**理論層面**：CNF 簡化了關於 CFG 的許多定理證明，例如 Pumping Lemma 和 CYK 演算法的正確性證明。

**實務層面**：CNF 使得語法分析演算法的時間複雜度可控。CYK (Cocke-Younger-Kasami) 演算法使用 CNF 在 O(n^3) 時間內解決「給定字串是否屬於該語言」的成員資格問題。

## 轉換為 CNF 的步驟

將 CFG 轉換為 CNF 包含以下步驟：

### 步驟 1：引入新的起始符號

創建一個新的起始符號 S0，並加入規則 S0 → S。這確保起始符號不會出現在任何產生式的右側。

### 步驟 2：消除 ε-產生式

移除所有形式為 A → ε 的規則（除 S0 → ε 外）。然後調整其他規則以補償被移除的空產生式。

### 步驟 3：消除單元產生式

移除形式為 A → B 的規則（一個非終止符號產生另一個非終止符號）。對於每個 A → B，如果 B → α，則加入 A → α。

### 步驟 4：轉換剩餘規則

對於形式為 A → X1 X2 ... Xk (k ≥ 3) 的規則，引入新的非終止符號將其拆分為二元形式。對於包含終止符號的規則，將終止符號替換為新的非終止符號。

## 範例

考慮文法：
```
S → aSa | bSb | a | b | ε
```

轉換為 CNF 後：
```
S0 → AR | BR | AS | BS | ε
S → AR | BR | AS | BS | a | b
R → SA
A → a
B → b
```

## CYK 演算法

CYK 演算法利用 CNF 進行字串的成員資格判定。其核心是動態規劃：

```python
def cyk(grammar, string):
    n = len(string)
    table = [[set() for _ in range(n)] for _ in range(n)]

    # 初始化：填入長度為 1 的子字串
    for i, ch in enumerate(string):
        for A, rhs in grammar.items():
            if rhs == ch or (isinstance(rhs, tuple) and rhs[0] == ch):
                table[i][i].add(A)

    # 填表：從長度 2 到 n
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for A, rhs in grammar.items():
                    if isinstance(rhs, tuple) and len(rhs) == 2:
                        B, C = rhs
                        if B in table[i][k] and C in table[k+1][j]:
                            table[i][j].add(A)
    return grammar.start in table[0][n-1]
```

CYK 演算法的時間複雜度為 O(n^3)，空間複雜度為 O(n^2)。

## 參考資料

- [https://www.google.com/search?q=Chomsky+normal+form+conversion+algorithm](https://www.google.com/search?q=Chomsky+normal+form+conversion+algorithm)
- [https://www.google.com/search?q=CYK+algorithm+parsing+CNF](https://www.google.com/search?q=CYK+algorithm+parsing+CNF)
- [https://www.google.com/search?q=Chomsky+正規形式+CNF](https://www.google.com/search?q=Chomsky+正規形式+CNF)
