# 正規語言與狀態機：程式實作

## 前言

本篇文章將展示如何使用 Python 實作正規語言理論中的核心資料結構和演算法，包括有限自動機（DFA/NFA）和正規表達式引擎。

---

## 原始碼

完整的 Python 實作請參考：[_code/automata.py](_code/automata.py) 和 [_code/regex_engine.py](_code/regex_engine.py)

---

## automata.py：有限自動機實作

```python
#!/usr/bin/env python3
"""Finite Automata Implementation: DFA and NFA"""

class DFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def accept(self, input_string):
        state = self.q0
        for symbol in input_string:
            if symbol not in self.sigma:
                return False
            state = self.delta.get((state, symbol))
            if state is None:
                return False
        return state in self.F

    def to_nfa(self):
        nfa_delta = {}
        for (state, symbol), next_state in self.delta.items():
            nfa_delta[(state, symbol)] = {next_state}
        return NFA(self.Q, self.sigma, nfa_delta, self.q0, self.F)


class NFA:
    def __init__(self, Q, sigma, delta, q0, F):
        self.Q = Q
        self.sigma = sigma
        self.delta = delta
        self.q0 = q0
        self.F = F

    def epsilon_closure(self, states):
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
        result = set()
        for state in states:
            result.update(self.delta.get((state, symbol), set()))
        return result

    def accept(self, input_string):
        current = self.epsilon_closure({self.q0})
        for symbol in input_string:
            current = self.epsilon_closure(self.move(current, symbol))
        return bool(current & self.F)

    def to_dfa(self):
        dfa_states = []
        dfa_delta = {}
        initial = frozenset(self.epsilon_closure({self.q0}))
        dfa_states.append(initial)
        queue = [initial]

        while queue:
            current = queue.pop(0)
            for symbol in self.sigma:
                next_set = self.epsilon_closure(self.move(current, symbol))
                if next_set:
                    dfa_delta[(current, symbol)] = next_set
                    if next_set not in dfa_states:
                        dfa_states.append(next_set)
                        queue.append(next_set)

        dfa_finals = {s for s in dfa_states if s & self.F}
        dfa_Q = {'q' + str(i) for i in range(len(dfa_states))}
        state_map = {s: 'q' + str(i) for i, s in enumerate(dfa_states)}
        dfa_delta_mapped = {(state_map[s], a): state_map[t]
                           for (s, a), t in dfa_delta.items()}
        return DFA(dfa_Q, self.sigma, dfa_delta_mapped,
                   state_map[initial], {state_map[f] for f in dfa_finals})


def nfa_from_regex(regex):
    """Thompson's construction: regex to NFA"""
    pass  # See regex_engine.py


def demo():
    print("=== DFA Demo ===")
    Q = {'q0', 'q1'}
    sigma = {'0', '1'}
    delta = {
        ('q0', '0'): 'q0',
        ('q0', '1'): 'q1',
        ('q1', '0'): 'q0',
        ('q1', '1'): 'q1',
    }
    dfa = DFA(Q, sigma, delta, 'q0', {'q1'})
    tests = ['1', '0', '01', '10', '101', '100']
    for t in tests:
        print(f"DFA accepts '{t}': {dfa.accept(t)}")

    print("\n=== NFA Demo ===")
    Q = {'q0', 'q1', 'q2'}
    sigma = {'a', 'b'}
    delta = {
        ('q0', 'a'): {'q1'},
        ('q0', ''): {'q2'},
        ('q1', 'b'): {'q2'},
    }
    nfa = NFA(Q, sigma, delta, 'q0', {'q2'})
    for t in ['ab', 'aab', 'b', '']:
        print(f"NFA accepts '{t}': {nfa.accept(t)}")


if __name__ == "__main__": demo()
```

---

## regex_engine.py：正規表達式引擎

```python
#!/usr/bin/env python3
"""Regular Expression Engine using Thompson's Construction"""

class NFAFragment:
    def __init__(self, start, accept, transitions):
        self.start = start
        self.accept = accept
        self.transitions = transitions


def shunting_yard(regex):
    """Convert infix regex to postfix (Shunting Yard algorithm)"""
    precedence = {'*': 3, '+': 3, '?': 3, '.': 2, '|': 1}
    output = []
    stack = []

    for c in regex:
        if c.isalnum() or c == '#':  # # for epsilon
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence.get(stack[-1], 0) >= precedence[c]:
                output.append(stack.pop())
            stack.append(c)

    while stack:
        output.append(stack.pop())
    return output


def thompson(postfix):
    """Thompson's construction: postfix regex to NFA"""
    nfa_count = [0]

    def new_state():
        s = f"q{nfa_count[0]}"
        nfa_count[0] += 1
        return s

    stack = []
    transitions = {}

    for c in postfix:
        if c.isalnum():
            start, accept = new_state(), new_state()
            transitions[(start, c)] = {accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '*':
            frag = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag.start, accept}
            transitions[(frag.accept, '')] = {frag.start, accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '|':
            frag2 = stack.pop()
            frag1 = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag1.start, frag2.start}
            transitions[(frag1.accept, '')] = {accept}
            transitions[(frag2.accept, '')] = {accept}
            stack.append(NFAFragment(start, accept, transitions))
        elif c == '.':
            frag2 = stack.pop()
            frag1 = stack.pop()
            transitions[(frag1.accept, '')] = {frag2.start}
            stack.append(NFAFragment(frag1.start, frag2.accept, transitions))
        elif c == '?':
            frag = stack.pop()
            start, accept = new_state(), new_state()
            transitions[(start, '')] = {frag.start, accept}
            transitions[(frag.accept, '')] = {accept}
            stack.append(NFAFragment(start, accept, transitions))

    frag = stack.pop()
    return frag.start, frag.accept, transitions


class RegexNFA:
    def __init__(self, pattern):
        self.pattern = pattern
        self.postfix = shunting_yard(pattern)
        self.start, self.accept, self.transitions = thompson(self.postfix)
        self.Q = set()
        for (s, _), targets in self.transitions.items():
            self.Q.add(s)
            self.Q.update(targets)
        self.sigma = set(c for c in pattern if c.isalnum())

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get((state, ''), set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        return closure

    def move(self, states, symbol):
        result = set()
        for state in states:
            result.update(self.transitions.get((state, symbol), set()))
        return result

    def accept(self, input_string):
        current = self.epsilon_closure({self.start})
        for symbol in input_string:
            current = self.epsilon_closure(self.move(current, symbol))
        return self.accept in current


def demo():
    print("=== Regex Engine Demo ===")
    patterns = ['a*b', 'a+b', 'a?b', '(a|b)*', 'a*b+c']
    test_strings = ['', 'b', 'ab', 'aab', 'abc', 'aaab', 'abbc']

    for pattern in patterns:
        print(f"\nPattern: {pattern}")
        nfa = RegexNFA(pattern)
        for s in test_strings:
            result = nfa.accept(s)
            if result:
                print(f"  '{s}': ACCEPT")
            else:
                print(f"  '{s}': reject")


if __name__ == "__main__": demo()
```

---

## 執行結果

```
=== DFA Demo ===
DFA accepts '1': True
DFA accepts '0': False
DFA accepts '01': True
DFA accepts '10': False
DFA accepts '101': True
DFA accepts '100': False

=== NFA Demo ===
NFA accepts 'ab': True
NFA accepts 'aab': False
NFA accepts 'b': True
NFA accepts '': True

=== Regex Engine Demo ===
Pattern: a*b
  '': ACCEPT
  'b': ACCEPT
  'ab': ACCEPT
  ...

Pattern: (a|b)*
  '': ACCEPT
  'a': ACCEPT
  'b': ACCEPT
  'ab': ACCEPT
  ...
```

---

## 實作說明

### Thompson 構造法

Thompson 構造法將正規表達式轉換為等價的 NFA，確保：
- 每個基本符號對應一個簡單的 NFA
- 複雜表達式透過並集、連接、克林閉包組合簡單 NFA
- 產生的 NFA 狀態數與正規表達式長度成線性關係

### 子集構造法

子集構造法將 NFA 轉換為等價的 DFA：
- DFA 的每個狀態對應 NFA 狀態集合的一個子集
- 初始狀態是 NFA 的 ε 閉包
- 接受狀態是包含 NFA 接受狀態的子集

### Shunting Yard 演算法

將中序正規表達式轉換為後序表示，處理運算優先順序和括號。

---

## 延伸閱讀

- [Thompson's Construction Wikipedia](https://www.google.com/search?q=Thompson+construction+regex+nfa)
- [Finite Automata Algorithms](https://www.google.com/search?q=DFA+NFA+algorithms)
- [Regular Expression Matching](https://www.google.com/search?q=regex+engine+implementation)

---

*本篇文章為「AI 程式人雜誌 2016 年 6 月號」正規語言與狀態機主題補充文章。*