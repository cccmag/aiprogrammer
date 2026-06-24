# 主題二：有限自動機

## 什麼是有限自動機？

有限自動機（Finite Automaton）是一種數學模型，用於識別正規語言。它由以下部分組成：

- **有限的狀態集合 Q**
- **有限的輸入字母表 Σ**
- **轉換函式 δ**
- **初始狀態 q₀ ∈ Q**
- **接受狀態集合 F ⊆ Q**

## 確定性有限自動機（DFA）

### 形式定義

DFA M = (Q, Σ, δ, q₀, F)，其中：

- Q：有限狀態集合
- Σ：輸入字母表
- δ：Q × Σ → Q（轉換函式）
- q₀：初始狀態
- F：接受狀態集合

### DFA 的運作

```python
# DFA 定義
class DFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q  # 狀態集合
        self.sigma = sigma  # 輸入字母表
        self.delta = delta  # 轉換函式: (state, symbol) -> state
        self.q0 = q0  # 初始狀態
        self.F = F  # 接受狀態集合

    def accept(self, input_string):
        """檢查是否接受輸入字串"""
        state = self.q0
        for symbol in input_string:
            if symbol not in self.sigma:
                return False
            state = self.delta.get((state, symbol), None)
            if state is None:
                return False
        return state in self.F

# 示例：接受所有以 '1' 結尾的二進位字串
# 狀態：q0（未看到1）, q1（看到1）
# 轉換：q0 -0-> q0, q0 -1-> q1, q1 -0-> q0, q1 -1-> q1
Q = {'q0', 'q1'}
sigma = {'0', '1'}
delta = {
    ('q0', '0'): 'q0',
    ('q0', '1'): 'q1',
    ('q1', '0'): 'q0',
    ('q1', '1'): 'q1',
}
q0 = 'q0'
F = {'q1'}

dfa = DFA(Q, sigma, delta, q0, F)

# 測試
test_strings = ['1', '0', '01', '10', '101', '100', '110']
for s in test_strings:
    print(f"'{s}': {dfa.accept(s)}")
```

### 狀態圖表示

```
       0           0
  ┌─────────┐   ┌─────────┐
  ▼         │   ▼         │
→ q0 ──1──► q1 ◄──1───    │
  ▲         │   ▲         │
  └─────0───┘   └─────0───┘
       (q1 是接受狀態)
```

### DFA 轉換表

| 狀態 | 0 | 1 |
|-----|---|---|
| →q0 | q0 | q1 |
| *q1 | q0 | q1 |

（→ 表示初始狀態，* 表示接受狀態）

## 非確定性有限自動機（NFA）

### NFA 與 DFA 的區別

NFA 的轉換函式 δ：Q × Σ → 2^Q（返回狀態集合）

一個字串被接受當且僅當存在至少一條接受路徑。

```python
# NFA 定義
class NFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta  # (state, symbol) -> set of states
        self.q0 = q0
        self.F = F

    def epsilon_closure(self, states):
        """計算狀態集的 ε 閉包"""
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.delta.get((state, ''), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        """從狀態集出發，讀入符號後可達的狀態"""
        result = set()
        for state in states:
            result.update(self.delta.get((state, symbol), set()))
        return result

    def accept(self, input_string):
        current_states = self.epsilon_closure({self.q0})
        for symbol in input_string:
            current_states = self.epsilon_closure(self.move(current_states, symbol))
        return bool(current_states & self.F)
```

### NFA 示例

```python
# NFA 接受所有以 '01' 結尾的二進位字串
Q = {'q0', 'q1', 'q2'}
sigma = {'0', '1'}
delta = {
    ('q0', '0'): {'q1'},
    ('q0', '1'): {'q0'},
    ('q1', '1'): {'q2'},
    ('q1', '0'): {'q1'},
    ('q2', '0'): {'q1'},
    ('q2', '1'): {'q0'},
}
q0 = 'q0'
F = {'q2'}

nfa = NFA(Q, sigma, delta, q0, F)
```

## ε 轉換

ε 轉換允許在不看任何輸入的情況下轉換狀態。

```python
# ε-NFA 示例
# 接受以 '0' 開頭或以 '1' 結尾的字串
delta = {
    ('q0', '0'): {'q1'},
    ('q0', ''): {'q3'},  # ε 轉換
    ('q1', '1'): {'q2'},
    ('q2', ''): {'q3'},  # ε 轉換
}
```

## DFA 與 NFA 的等價性

**定理**：DFA 和 NFA 識別相同的語言類別。

### 子集構造法

將 NFA 轉換為等價的 DFA：

```python
def nfa_to_dfa(nfa):
    """將 NFA 轉換為 DFA"""
    dfa_states = []
    dfa_transitions = {}
    initial = frozenset(nfa.epsilon_closure({nfa.q0}))
    dfa_states.append(initial)
    queue = [initial]

    while queue:
        current = queue.pop(0)
        for symbol in nfa.sigma:
            next_states = nfa.epsilon_closure(nfa.move(current, symbol))
            if next_states:
                dfa_transitions[(current, symbol)] = next_states
                if next_states not in dfa_states:
                    dfa_states.append(next_states)
                    queue.append(next_states)

    dfa_finals = {s for s in dfa_states if s & nfa.F}
    return dfa_states, dfa_transitions, initial, dfa_finals
```

## 正規語言的泵浦引理

**泵浦引理**：如果 L 是正規語言，則存在正整數 p（泵浦長度），使得任何長度 ≥ p 的字串 w ∈ L 可以被分解為 w = xyz，其中：

1. |xy| ≤ p
2. |y| ≥ 1
3. 對於所有 i ≥ 0，xy^iz ∈ L

```python
# 泵浦引理應用
def pump_lemma_example():
    """
    證明 L = {0^n 1^n | n ≥ 0} 不是正規語言
    反證法：假設 L 是正規的，則存在泵浦長度 p
    考慮字串 w = 0^p 1^p ∈ L
    根據泵浦引理，w = xyz，|xy| ≤ p，|y| ≥ 1
    因為 |xy| ≤ p，y 只能全是 0
    考慮 xy^2z = 0^(p+|y|) 1^p ∉ L
    矛盾！所以 L 不是正規語言
    """
    pass
```

## 小結

有限自動機是識別正規語言的數學模型。DFA 和 NFA 在表達能力上等價，但結構不同。在實際應用中，我們通常使用正規表達式，它是最直覺的描述方式。