# 主題七：Turing 機器與可計算性

## 什麼是 Turing 機器？

Turing 機器（TM）是由 Alan Turing 在 1936 年提出的抽象計算模型。它是歷史上第一個通用的計算模型，被認為是可計算性的數學定義。

### Turing 機器的組成

TM M = (Q, Σ, Γ, δ, q₀, B, F)，其中：

- Q：有限狀態集合
- Σ：輸入字母表（不含空白符）
- Γ：帶字母表（Q ⊇ Σ，Γ 包含空白符 B）
- δ：Q × Γ → Q × Γ × {L, R, N}（轉換函式）
- q₀：初始狀態
- B：空白符（blank）
- F：接受狀態集合

## Turing 機器的運作

```python
class TuringMachine:
    def __init__(self, Q, sigma, gamma, delta, q0, B, F):
        self.Q = Q
        self.sigma = sigma
        self.gamma = gamma
        self.delta = delta
        self.q0 = q0
        self.B = B
        self.F = F

    def accept(self, input_string):
        """檢查是否接受輸入字串"""
        tape = list(input_string) + [self.B]
        head = 0
        state = self.q0

        while True:
            if state in self.F:
                return True

            symbol = tape[head]
            key = (state, symbol)

            if key not in self.delta:
                return False

            next_state, write, direction = self.delta[key]
            tape[head] = write
            state = next_state

            if direction == 'R':
                head += 1
                if head >= len(tape):
                    tape.append(self.B)
            elif direction == 'L':
                head = max(0, head - 1)

    def run(self, input_string, max_steps=10000):
        """執行並返回過程"""
        tape = list(input_string) + [self.B]
        head = 0
        state = self.q0
        history = []

        for _ in range(max_steps):
            history.append((state, list(tape), head))

            if state in self.F:
                return history, True

            symbol = tape[head]
            key = (state, symbol)

            if key not in self.delta:
                return history, False

            next_state, write, direction = self.delta[key]
            tape[head] = write
            state = next_state

            if direction == 'R':
                head += 1
                if head >= len(tape):
                    tape.append(self.B)
            elif direction == 'L':
                head = max(0, head - 1)

        return history, False
```

## Turing 機器的示例

### 識別 {0^n 1^n | n ≥ 1}

```python
def tm_0n1n():
    """
    Turing 機器：識別 {0^n 1^n | n >= 1}
    """
    Q = {'q0', 'q1', 'q2', 'q3', 'q4', 'q5'}
    sigma = {'0', '1'}
    gamma = {'0', '1', 'X', 'B'}
    B = 'B'
    F = {'q5'}

    delta = {
        # q0: 找到最左邊的 0，標記為 X
        ('q0', '0'): ('q1', 'X', 'R'),
        ('q0', 'X'): ('q0', 'X', 'R'),
        ('q0', 'B'): ('q4', 'B', 'L'),

        # q1: 向右找到第一個未標記的 1
        ('q1', '0'): ('q1', '0', 'R'),
        ('q1', '1'): ('q2', 'X', 'L'),
        ('q1', 'Y'): ('q1', 'Y', 'R'),

        # q2: 向左找到 X
        ('q2', '0'): ('q2', '0', 'L'),
        ('q2', 'X'): ('q0', 'X', 'R'),
        ('q2', 'Y'): ('q2', 'Y', 'L'),

        # q4: 向左檢查是否完成
        ('q4', 'Y'): ('q4', 'Y', 'L'),
        ('q4', 'X'): ('q5', 'X', 'R'),
    }

    return TuringMachine(Q, sigma, gamma, delta, 'q0', B, F)

# 測試
tm = tm_0n1n()
tests = ['01', '0011', '000111', '001', '011']
for t in tests:
    print(f"'{t}': {tm.accept(t)}")
```

### 識別迴文

```python
def tm_palindrome():
    """
    Turing 機器：識別 {w w^R | w ∈ {a,b}*}
    """
    Q = {'q0', 'q1', 'q2', 'q3', 'q4'}
    sigma = {'a', 'b'}
    gamma = {'a', 'b', 'X', 'B'}
    B = 'B'
    F = {'q4'}

    delta = {
        # q0: 標記最左字母
        ('q0', 'a'): ('q1', 'X', 'R'),
        ('q0', 'b'): ('q1', 'X', 'R'),

        # q1: 向右找到對應字母
        ('q1', 'a'): ('q1', 'a', 'R'),
        ('q1', 'b'): ('q1', 'b', 'R'),
        ('q1', 'X'): ('q1', 'X', 'R'),
        ('q1', 'Y'): ('q1', 'Y', 'R'),
        ('q1', 'B'): ('q2', 'B', 'L'),

        # q2: 回溯匹配
        ('q2', 'a'): ('q3', 'Y', 'L'),
        ('q2', 'b'): ('q3', 'Y', 'L'),
        ('q2', 'Y'): ('q2', 'Y', 'L'),
        ('q2', 'X'): ('q0', 'X', 'R'),

        # q3: 向左找 X
        ('q3', 'a'): ('q3', 'a', 'L'),
        ('q3', 'b'): ('q3', 'b', 'L'),
        ('q3', 'X'): ('q0', 'X', 'R'),
        ('q3', 'Y'): ('q3', 'Y', 'L'),
    }

    return TuringMachine(Q, sigma, gamma, delta, 'q0', B, F)
```

## 多帶 Turing 機器

### 標準化

任何多帶 TM 都可以轉換為等價的單帶 TM。

```python
class MultiTapeTM:
    def __init__(self, num_tapes, Q, sigma, gamma, delta, q0, B, F):
        self.num_tapes = num_tapes
        self.Q = Q
        self.sigma = sigma
        self.gamma = gamma
        self.delta = delta  # (state, symbols) -> (new_state, writes, moves)
        self.q0 = q0
        self.B = B
        self.F = F

    def accept(self, input_string):
        """轉換為單帶 TM 模擬"""
        tapes = [list(input_string) + [self.B]]
        for _ in range(self.num_tapes - 1):
            tapes.append([self.B])

        heads = [0] * self.num_tapes
        state = self.q0

        while state not in self.F:
            symbols = tuple(tapes[i][heads[i]] for i in range(self.num_tapes))
            key = (state, symbols)

            if key not in self.delta:
                return False

            next_state, writes, moves = self.delta[key]

            for i in range(self.num_tapes):
                tapes[i][heads[i]] = writes[i]
                if moves[i] == 'R':
                    heads[i] += 1
                    if heads[i] >= len(tapes[i]):
                        tapes[i].append(self.B)
                elif moves[i] == 'L':
                    heads[i] = max(0, heads[i] - 1)

            state = next_state

        return True
```

## Turing 機器的變體

### 增加stay移動

L, R, S（N 表示 stay）與標準 TM 等價。

### 半無限帶

只有左側邊界，與標準 TM 等價。

### 多維帶

二維或多維無界帶，與標準 TM 等價。

## Turing 完整性

### 定義

如果一個計算系統可以模擬任何 Turing 機器，則它是 Turing 完整的。

```python
def is_turing_complete(system):
    """
    檢查系統是否 Turing 完整
    根據 Church-Turing 論題，這無法被數學證明
    但可以透過模擬已知 Turing 完整的系統來論證
    """
    # 如果系統可以模擬以下任何一個，那就是 Turing 完整的：
    # 1. Turing 機器
    # 2. Lambda Calculus
    # 3. 通用寄存器機
    # 4. 隨機存取機 (RAM)
    # 5. 任何程式語言（假設無限記憶體）
    pass
```

## 可計算性理論

### 可判定語言

存在 TM 可以在有限時間內對任何輸入給出正確答案。

```python
def is_decidable(L):
    """
    語言 L 是可判定的，当且仅当存在 TM M 使得：
    - 如果 w ∈ L，則 M 接受 w
    - 如果 w ∉ L，則 M 拒絕 w
    """
    pass
```

### 不可判定問題

存在沒有 TM 可以解決的問題。

```python
def halts(p, w):
    """
    停機問題：給定程式 p 和輸入 w，p 是否會停機？
    這是不可判定的
    """
    # 假設存在 halts 函式
    # 可以構造 Russell's Paradox 式的矛盾
    pass
```

## Church-Turing 論題

**論題**：直觀上可計算的函式正好是 Turing 可計算的函式。

這不是一個數學定理，而是一個經驗假設，因為「直觀可計算」沒有數學定義。

## 小結

Turing 機器是計算理論的核心模型。它展示了：
1. 任何 Turing 機器可以計算的函式稱為 Turing 可計算的
2. 存在 Turing 可計算但不可判定問題（如停機問題）
3. 所有合理的計算模型都是等價的（Church-Turing 論題）

Turing 機器的概念不僅是理論電腦科學的基石，也為現代電腦的設計提供了概念框架。