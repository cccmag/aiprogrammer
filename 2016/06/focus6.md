# 主題六：Pushdown Automata

## 什麼是 Pushdown Automata？

Pushdown Automata（PDA）是一種擴展了堆疊記憶體的有限自動機。它可以用來識別上下文無關語言（Context-Free Language，CFL）。

### 為何需要 PDA？

有限自動機只能記憶有限的狀態，但無法計數。例如：

- `L = {0^n 1^n | n ≥ 0}`（相同數量的 0 和 1）
- `L = {w w^R | w ∈ {0,1}*}`（回文）

這些語言需要「計數」能力，而有限自動機的狀態是有限的，無法做到。

### PDA 的組成

PDA M = (Q, Σ, Γ, δ, q₀, Z₀, F)，其中：

- Q：有限狀態集合
- Σ：輸入字母表
- Γ：堆疊字母表
- δ：Q × (Σ ∪ {ε}) × Γ → Q × Γ*（轉換函式）
- q₀：初始狀態
- Z₀：初始堆疊符號
- F：接受狀態集合

## PDA 的運作

### 形式化定義

```python
class PDA:
    def __init__(self, Q, sigma, gamma, delta, q0, Z0, F):
        self.Q = Q
        self.sigma = sigma
        self.gamma = gamma
        self.delta = delta  # (state, input_symbol, stack_top) -> (next_state, stack_push)
        self.q0 = q0
        self.Z0 = Z0
        self.F = F

    def accept(self, input_string):
        """檢查是否接受輸入字串"""
        stack = [self.Z0]
        state = self.q0

        for symbol in input_string:
            if symbol not in self.sigma:
                return False

            top = stack[-1] if stack else None
            if top is None:
                return False

            key = (state, symbol, top)
            if key in self.delta:
                next_state, push = self.delta[key]
                state = next_state
                stack.pop()
                stack.extend(reversed(push))
            else:
                return False

        return state in self.F
```

### PDA 運作示例

```
識別 L = {0^n 1^n | n ≥ 0}

轉換規則：
δ(q0, 0, Z0) = (q0, XZ0)    # 讀到 0，推入 X
δ(q0, 0, X) = (q0, XX)      # 讀到 0，推入 X
δ(q0, 1, X) = (q1, ε)       # 讀到 1，彈出 X
δ(q1, 1, X) = (q1, ε)       # 讀到 1，彈出 X
δ(q1, ε, Z0) = (q2, Z0)     # 空轉換，進入接受狀態
```

## PDA 的兩種接受方式

### 1. 接受狀態方式

最終狀態在接受狀態集合 F 中。

```python
def accepts_by_final_state(pda, input_string):
    """按接受狀態方式"""
    stack = [pda.Z0]
    state = pda.q0

    for symbol in input_string:
        top = stack[-1]
        key = (state, symbol, top)
        if key in pda.delta:
            next_state, push_str = pda.delta[key]
            state = next_state
            stack.pop()
            stack.extend(reversed(push_str))

    return state in pda.F
```

### 2. 空堆疊方式

堆疊最終為空。

```python
def accepts_by_empty_stack(pda, input_string):
    """按空堆疊方式"""
    stack = [pda.Z0]
    state = pda.q0

    for symbol in input_string:
        top = stack[-1]
        key = (state, symbol, top)
        if key in pda.delta:
            next_state, push_str = pda.delta[key]
            state = next_state
            stack.pop()
            stack.extend(reversed(push_str))

    return len(stack) == 0
```

## PDA 與 CFG 的等價性

**定理**：上下文無關文法產生的語言正好是 PDA 識別的語言。

### CFG → PDA 轉換

```python
def cfg_to_pda(cfg):
    """
    將 CFG 轉換為 PDA
    使用同時模擬最左推導的方法
    """
    Q = {'q', 'p'}  # q: 模擬狀態, p: 接受狀態
    sigma = cfg.terminals
    gamma = cfg.variables | cfg.terminals | {'$'}  # $ 是底部標記
    Z0 = '$'
    F = {'p'}

    delta = {}

    # 初始化：將開始符號推入堆疊
    delta[('q', '', Z0)] = ('q', cfg.start + Z0)

    # 對每個變數 A，添加產生式
    for A, productions in cfg.productions.items():
        for prod in productions:
            # 推導 A -> α
            delta[('q', '', A)] = ('q', prod)

    # 匹配終結符
    for a in cfg.terminals:
        delta[('q', a, a)] = ('q', '')

    # 空轉換到接受狀態
    delta[('q', '', Z0)] = ('p', Z0)

    return PDA(Q, sigma, gamma, delta, 'q', Z0, F)
```

## PDA 的應用

### 括號匹配

```python
def balanced_parens_pda():
    """
    識別 balanced = { (^n )^n | n >= 0 }
    """
    Q = {'q0', 'q1', 'q2'}
    sigma = {'(', ')'}
    gamma = {'Z', '('}
    Z0 = 'Z'

    delta = {
        ('q0', '(', 'Z'): ('q0', '(Z'),
        ('q0', '(', '('): ('q0', '(('),
        ('q0', ')', '('): ('q0', ''),
        ('q0', '', 'Z'): ('q1', 'Z'),
        ('q1', '', 'Z'): ('q2', 'Z'),
    }

    return PDA(Q, sigma, gamma, delta, 'q0', Z0, {'q2'})

# 測試
pda = balanced_parens_pda()
tests = ['', '()', '(())', '()()', '(()))']
for t in tests:
    print(f"'{t}': {pda.accept(t)}")
```

### 回文識別

```python
def palindrome_pda():
    """
    識別 L = {w w^R | w ∈ {a,b}*}
    """
    Q = {'q0', 'q1', 'q2'}
    sigma = {'a', 'b'}
    gamma = {'Z', 'a', 'b'}
    Z0 = 'Z'

    delta = {
        # 讀入前半部分，推入堆疊
        ('q0', 'a', 'Z'): ('q0', 'aZ'),
        ('q0', 'b', 'Z'): ('q0', 'bZ'),
        ('q0', 'a', 'a'): ('q0', 'aa'),
        ('q0', 'b', 'b'): ('q0', 'bb'),
        ('q0', 'a', 'b'): ('q0', 'ab'),
        ('q0', 'b', 'a'): ('q0', 'ba'),
        # 非確定性地猜測中點
        ('q0', 'a', 'a'): ('q1', ''),
        ('q0', 'b', 'b'): ('q1', ''),
        ('q0', '', 'Z'): ('q1', 'Z'),
        # 讀取後半部分，彈出堆疊
        ('q1', 'a', 'a'): ('q1', ''),
        ('q1', 'b', 'b'): ('q1', ''),
        ('q1', '', 'Z'): ('q2', 'Z'),
    }

    return PDA(Q, sigma, gamma, delta, 'q0', Z0, {'q2'})
```

## Deterministic PDA（DPDA）

### 定義

一個 PDA 是確定的，如果對每個 (q, a, X) 最多只有一個可能的轉換。

```python
def is_deterministic(pda):
    """檢查 PDA 是否為確定的"""
    for (state, symbol, top), (next_state, push) in pda.delta.items():
        # 檢查是否有多個可能的轉換
        count = 0
        for (s, sym, t), (ns, p) in pda.delta.items():
            if s == state and t == top:
                if sym == symbol or sym == '':
                    count += 1
        if count > 1:
            return False
    return True
```

### DPDA 與 LR(k) 文法

確定性 PDA 對應 LR(k) 文法，這是大多數程式語言語法分析器使用的文法類別。

## 空堆疊 vs 接受狀態

### 定理

一個語言 L 可以被某個 PDA 以空堆疊方式接受，iff L 可以被某個 PDA 以接受狀態方式接受。

### 轉換方法

```python
def empty_stack_to_final_state(pda):
    """將空堆疊接受 PDA 轉換為接受狀態 PDA"""
    new_F = {'new_accept'}

    # 添加新的接受狀態和轉換
    delta = dict(pda.delta)
    delta[('new_start', '', pda.Z0)] = (pda.q0, pda.Z0 + 'X')

    # 從原接受狀態空轉換到新接受狀態
    for q in pda.Q:
        delta[(q, '', pda.Z0)] = ('new_accept', pda.Z0)

    return PDA(pda.Q | {'new_start', 'new_accept'},
               pda.sigma, pda.gamma | {'X'},
               delta, 'new_start', pda.Z0, new_F)
```

## 小結

Pushdown Automata 是識別上下文無關語言的計算模型。它透過增加一個無限堆疊，突破了有限自動機的狀態限制，使得語言識別能力大幅提升。

PDA 與 CFG 的等價性是形式語言理論中的重要定理，為編譯器的語法分析提供了理論基礎。LR 分析器就是確定性 PDA 的典型應用。