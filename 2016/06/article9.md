# 圖靈機與通用計算

## 前言

圖靈機不僅是計算理論的基礎，更是現代電腦科學的理論基石。理解圖靈機幫助我們理解計算的本質、極限，以及為什麼現在的電腦能做這麼多事情。

## Turing 機器的基本概念

### 形式化定義

```python
class TuringMachine:
    def __init__(self, Q, sigma, gamma, delta, q0, B, F):
        self.Q = Q          # 狀態集合
        self.sigma = sigma  # 輸入字母表
        self.gamma = gamma  # 帶字母表
        self.delta = delta  # 轉換函式
        self.q0 = q0        # 初始狀態
        self.B = B          # 空白符
        self.F = F          # 接受狀態集合

    def step(self, state, symbol):
        """執行一步計算"""
        return self.delta.get((state, symbol))

    def accepts(self, input_string):
        """判斷是否接受"""
        tape = list(input_string)
        head = 0
        state = self.q0

        while state not in self.F:
            symbol = tape[head] if head < len(tape) else self.B
            transition = self.step(state, symbol)

            if transition is None:
                return False

            new_state, new_symbol, direction = transition
            tape[head] = new_symbol
            state = new_state

            if direction == 'R':
                head += 1
                if head >= len(tape):
                    tape.append(self.B)
            elif direction == 'L':
                head = max(0, head - 1)

        return True


def basic_tm():
    print("Turing Machine Definition:")
    print("  M = (Q, Σ, Γ, δ, q₀, B, F)")
    print("  Q: finite states")
    print("  Σ: input alphabet")
    print("  Γ: tape alphabet (includes B)")
    print("  δ: transition function")
    print("  q₀: initial state")
    print("  B: blank symbol")
    print("  F: accepting states")

basic_tm()
```

## 通用圖靈機

### 模擬其他圖靈機

```python
class UniversalTuringMachine:
    """
    通用圖靈機可以模擬任何其他圖靈機
    這是電腦的理論模型
    """
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = 'q0'

    def load_program(self, program):
        """載入要模擬的圖靈機"""
        self.program = program

    def load_input(self, input_string):
        """載入輸入"""
        self.tape = list(input_string)
        self.head = 0
        self.state = 'q0'

    def step(self):
        """執行一步"""
        symbol = self.tape[self.head] if self.head < len(self.tape) else self.program['B']
        key = (self.state, symbol)

        if key not in self.program['delta']:
            return False

        new_state, new_symbol, direction = self.program['delta'][key]
        self.tape[self.head] = new_symbol
        self.state = new_state

        if direction == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.program['B'])
        elif direction == 'L':
            self.head = max(0, self.head - 1)

        return True

    def run(self, max_steps=10000):
        """執行直到停機"""
        for _ in range(max_steps):
            if self.state in self.program['F']:
                return True
            if not self.step():
                return False
        return False


def universal_tm():
    print("Universal Turing Machine:")
    print("  Can simulate ANY other Turing machine")
    print("  Takes description of M and input w")
    print("  Returns same result as M(w)")
    print("  This is what a stored-program computer does!")


universal_tm()
```

## Turing 完整性

### 什麼是 Turing 完整性？

```python
def turing_completeness():
    """
    一個系統是 Turing 完整的，如果它可以模擬任何 Turing 機器
    """
    systems = [
        "Python",
        "C",
        "JavaScript",
        "Lambda Calculus",
        " Cellular Automata (Rule 110)",
        "Brainfuck",
    ]

    print("Turing Complete Systems:")
    for system in systems:
        print(f"  - {system}")
    print("")
    print("All can simulate any computable function!")


turing_completeness()
```

## 可計算性理論

### 停機問題

```python
class HaltingProblem:
    """
    停機問題是不可判定的
    不存在程式可以判斷任意程式是否會停機
    """
    def __init__(self):
        self.description = """
        Proof sketch (contradiction):
        1. Assume H(P, w) = 'yes' if P(w) halts, 'no' otherwise
        2. Consider K(P) = if H(P, P) == 'yes' then infinite_loop else halt
        3. What does K(K) do?
           - If K(K) halts, then H(K, K) = 'yes', so K(K) loops
           - If K(K) loops, then H(K, K) = 'no', so K(K) halts
        4. Contradiction! So H cannot exist.
        """

    def explain(self):
        print("Halting Problem:")
        print(self.description)


HaltingProblem().explain()
```

### 可判定 vs 不可判定

```python
def decidable_vs_undecidable():
    problems = {
        "Decidable": [
            "Regular language membership",
            "CFG membership (CYK algorithm)",
            "Boolean satisfiability (SAT)",
            "Graph connectivity",
        ],
        "Undecidable": [
            "Halting problem",
            "Most interesting properties of programs",
            "Equation solvability (Hilbert's 10th)",
            "Language equivalence (for CFGs)",
        ]
    }

    print("Decidable Problems:")
    for p in problems["Decidable"]:
        print(f"  + {p}")

    print("")
    print("Undecidable Problems:")
    for p in problems["Undecidable"]:
        print(f"  - {p}")


decidable_vs_undecidable()
```

## Turing 機器的現代意義

### 量子 Turing 機

```python
def quantum_turing():
    """
    量子 Turing 機是經典 Turing 機的推廣
    使用量子位元，可以同時處於多個狀態
    """
    print("Quantum Turing Machine:")
    print("  - Same structure as classical TM")
    print("  - States are quantum superpositions")
    print("  - Can be in multiple states at once (superposition)")
    print("  - Leads to quantum speedup for some problems")
    print("  - Still limited by computability theory")


quantum_turing()
```

## Church-Turing 論題

```python
def church_turing():
    """
    Church-Turing Thesis:
    Intuitive notion of computable = Turing computable
    """
    print("Church-Turing Thesis:")
    print("  'Effectively calculable' functions")
    print("  = functions computable by Turing machine")
    print("")
    print("Evidence:")
    print("  - All known models are equivalent")
    print("  - No counterexample found")
    print("  - Accepted as definition, not proven")


church_turing()
```

## Turing 機與現代電腦

```python
def tm_to_modern_computer():
    print("Turing Machine to Modern Computer:")
    print("")
    print("Turing Machine:")
    print("  - Infinite tape (memory)")
    print("  - State register")
    print("  - Transition table (program)")
    print("")
    print("Modern Computer:")
    print("  - RAM (tape)")
    print("  - CPU state (registers)")
    print("  - Program (instructions)")
    print("")
    print("Key insight: All computable problems are computable")


tm_to_modern_computer()
```

## 小結

圖靈機是 20 世紀最重要的理論貢獻之一。它不僅定義了計算的概念，還揭示了計算的根本限制。理解圖靈機讓我們：
1. 知道什麼是可計算的，什麼是不可計算的
2. 理解現代電腦的理論基礎
3. 欣賞形式化方法的力量

---

**延伸閱讀**

- [Turing Machine Wikipedia](https://www.google.com/search?q=Turing+machine+history+alan+turing)
- [Halting Problem Proof](https://www.google.com/search?q=halting+problem+proof)
- [Computability Theory](https://www.google.com/search?q=computability+theory+textbook)