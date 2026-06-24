# 主題五：上下文無關文法

## 什麼是上下文無關文法？

上下文無關文法（Context-Free Grammar，CFG）是比正規文法更強大的文法系統，可以描述更複雜的語言結構，如巢狀括號、配對標籤等。

### 形式定義

CFG G = (V, Σ, R, S)，其中：

- V：變數的有窮集合（非終結符）
- Σ：終結符的有窮集合（與 V 不相交）
- R：產生式的有窮集合（形式為 A → α，其中 A ∈ V，α ∈ (V ∪ Σ)*）
- S：開始符號（S ∈ V）

### 與正規文法的區別

正規文法（3 型文法）限制為：

- A → aB 或 A → a（左線性或右線性）

上下文無關文法允許：

- A → α（任意產生式）

```python
# 正規文法示例（識別以 b 結尾的字串）
# S → aS | bT
# T → b | aT

# 上下文無關文法示例（識別配對的括號）
# S → SS | (S) | ε
```

## 推導

從開始符號出發，反覆套用產生式直到只剩終結符，這個過程稱為推導。

### 最左推導 vs 最右推導

```python
# 文法：S → aSb | ε
# 推導 "aabb"：

# 最左推導：
# S → aSb → aaSbb → aabSb → aabb

# 最右推導：
# S → aSb → aSSb → aSab → aabb
```

### 推導樹

```
        S
      / | \
     a  S  b
       / \
      a   S
         |
         b
```

## 語法分析樹

推導過程可以表示為語法分析樹（Parse Tree）。

```python
# 對應文法：E → E + E | E * E | (E) | id
# 表達式：(id + id) * id 的語法分析樹：

#        E
#     /  |  \
#    (   E   )
#      / | \
#     E  +  E
#     |     |
#    id    id
```

## 歧義性

一個文法可能對同一字串有多個推導樹，稱為**歧義（Ambiguity）**。

```python
# 歧義文法
# S → if E then S | if E then S else S | E
# E → true | false

# 字串 "if true then if false then true else false" 有兩種理解：
# 1. if true then (if false then true) else false
# 2. if true then (if false then true else false)
```

### 消除歧義

```python
# 無歧義文法
# S → if E then S | if E then S else S | A
# A → if E then A | E
# 或者使用優先級和結合性
```

## 喬姆斯基範式

任何上下文無關文法都可以轉換為喬姆斯基範式（CNF）。

CNF 要求產生式只能是：
- A → BC（A, B, C ∈ V）
- A → a（a ∈ Σ）

```python
def to_cnf(cfg):
    """
    將 CFG 轉換為 CNF
    步驟：
    1. 消除 ε 產生式
    2. 消除單位產生式
    3. 消除不便於終結符的變數
    4. 消除長度大於 2 的產生式
    """
    pass
```

## GLR 分析

GLR（Generalized LR）是一種能處理歧義文法的語法分析演算法。

```python
# 使用 GLR 的語法分析器
# yapps（Python 的語法分析生成器）
from yapps import grammar

grammar_str = """
    expr ::= expr '+' term | term
    term ::= term '*' factor | factor
    factor ::= '(' expr ')' | number
"""
```

## 實際應用

### JSON 語法

```json
{
  "json": "object",
  "example": {
    "nested": true,
    "array": [1, 2, 3]
  }
}
```

對應的文法：

```
value → object | array | string | number | true | false | null
object → '{' members? '}'
array → '[' elements? ']'
```

### 算術表達式

```
E → E + T | E - T | T
T → T * F | T / F | F
F → (E) | -F | primary
primary → NUMBER | IDENTIFIER
```

### 巢狀括號

```
S → S S | (S) | ε
```

## CYK 演算法

CYK（Cocke-Younger-Kasami）演算法可以在 O(n³) 時間內判定字串是否屬於 CFG。

```python
def cyk_parse(word, cfg):
    """
    CYK 演算法
    假設文法是 CNF 形式
    """
    n = len(word)
    if n == 0:
        return cfg.startsymbol in cfg.nullable

    # table[i][j] = 可推導出 word[i:j] 的變數集合
    table = [[set() for _ in range(n)] for _ in range(n)]

    # 長度為 1 的子字串
    for i, char in enumerate(word):
        for var, prods in cfg.productions.items():
            if char in prods:
                table[i][i].add(var)

    # 長度大於 1 的子字串
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            for k in range(i, j):
                for var, prods in cfg.productions.items():
                    for prod in prods:
                        if len(prod) == 2:
                            B, C = prod
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(var)

    return cfg.startsymbol in table[0][n-1]
```

## 小結

上下文無關文法是程式語言語法定義的基礎。理解 CFG 的理論對於編譯器設計和語言處理至關重要。