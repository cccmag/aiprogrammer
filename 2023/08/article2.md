# LL 與 LR 解析

## 前言

語法分析是編譯器的核心階段。LL 和 LR 是兩種主要的解析策略，分別代表從左到右掃描（Left-to-right）搭配最左推導（Leftmost derivation）和最右推導的逆過程（Rightmost derivation in reverse）。本文深入比較這兩種策略。

## LL 解析

LL 解析是自上而下的策略：從起始符號開始，逐步展開非終結符，直到匹配輸入 Token。

### 遞迴下降解析

最常見的 LL 解析形式是遞迴下降解析器：

```python
def parse_expr(self):
    """expr → term {+ term}"""
    left = self.parse_term()
    while self.peek() == '+':
        self.consume('+')
        right = self.parse_term()
        left = BinOp('+', left, right)
    return left
```

### LL(1) 解析表

LL(1) 使用一個前瞻 Token 來決定採用哪條產生式。解析表以（非終結符, 終結符）為鍵：

```
E → T E'
E' → + T E' | ε
T → F T'
T' → * F T' | ε
F → ( E ) | id

解析表：
      id    +    *    (    )    $
E    T E'             T E'
E'         + T E'          ε    ε
T    F T'             F T'
T'         ε   * F T'      ε    ε
F    id                ( E )
```

### First 與 Follow 集合

建構 LL(1) 解析表需要計算 First 和 Follow 集合：

- **First(A)**：從 A 推導出的第一個終結符集合
- **Follow(A)**：在推導中緊跟在 A 之後的終結符集合

## LR 解析

LR 解析是自下而上的策略：從輸入 Token 開始，逐步歸約到起始符號。

### LR 解析引擎

LR 解析器由一個狀態棧和一個解析表組成：

```
stack = [0]     # 狀態棧
input = tokens  # 輸入緩衝
action = [...]  # ACTION 表
goto   = [...]  # GOTO 表

while True:
    state = stack[-1]
    token = input[0]
    
    act = action[state][token]
    if act == SHIFT(s):
        stack.append(s)
        input.pop(0)
    elif act == REDUCE(A → β):
        for _ in range(|β|): stack.pop()
        stack.append(goto[stack[-1]][A])
        print(A → β)
    elif act == ACCEPT:
        break
```

### LR 的變體

1. **LR(0)**：不使用前瞻，限制最多
2. **SLR(1)**：簡單 LR，使用 Follow 集合
3. **LR(1)**：完整 LR，每個項目包含前瞻 Token
4. **LALR(1)**：Look-Ahead LR，合併相同核心的 LR(1) 狀態

## LR 與 LL 的比較

### 文法的表達力

LR 可以處理比 LL 更大的文法集合：

```
# 左遞迴文法（LR 可處理，LL 不行）
E → E + T | T

# 左因子文法（LL 需要改造）
stmt → if E then stmt
     | if E then stmt else stmt  # LL 衝突！
```

### 實作難度

| 比較維度 | LL | LR |
|---|---|---|
| 手動實作 | 容易（遞迴下降） | 困難（狀態機） |
| 錯誤訊息 | 精確 | 含糊 |
| 文法除錯 | 直覺 | 需要了解狀態機 |
| 工具支援 | ANTLR, 手寫 | Yacc, Bison |

### 效能

現代 LR 解析器（如 LALR(1)）在解析速度上通常略快於遞迴下降解析器，因為 LR 使用表驅動而 LL 使用函式呼叫。但差異在大多數應用中不明顯。

## 如何選擇

1. **手寫解析器**：選擇 LL（遞迴下降），容易除錯和維護
2. **使用產生器**：選擇 LALR(1) 或 LR(1)，表達力更強
3. **複雜語法**：考慮 LR，避免改造文法
4. **需要好的錯誤回報**：選擇 LL

## 結語

LL 和 LR 是互補的技術，沒有絕對的優劣。理解兩者的原理，可以根據專案需求選擇合適的策略。對於大多數程式語言，遞迴下降解析器（LL）是實用且可靠的選擇。

## 延伸閱讀

- [LL 解析教學](https://www.google.com/search?q=LL+parsing+top+down+parser)
- [LR 解析教學](https://www.google.com/search?q=LR+parsing+bottom+up+parser)
- [ANTLR 解析器產生器](https://www.google.com/search?q=ANTLR+parser+generator)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列文章。*
