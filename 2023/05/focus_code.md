# 自動機程式實作：Python 實戰演練

## 概述

本文介紹一個完整的 Python 自動機程式庫 `automata.py`，實作了 DFA、NFA、正則表達式引擎、CFG 解析器和 Turing Machine 模擬器。

## 程式架構

### DFA 模擬器

DFA 的實作非常直觀：將五元組 (Q, Σ, δ, q0, F) 儲存為資料結構，然後對輸入字串逐字元執行狀態轉移。

```python
class DFA:
    def __init__(self, states, alphabet, transition, start, accepts):
        self.transition = transition  # dict: (state, symbol) -> state
        self.start = start
        self.accepts = set(accepts)

    def accept(self, s):
        state = self.start
        for ch in s:
            state = self.transition.get((state, ch))
            if state is None:
                return False
        return state in self.accepts
```

### NFA 模擬器

NFA 從一個狀態讀入字元後可能轉移到多個狀態。模擬 NFA 的關鍵是維護一個**當前可能狀態集合**：

```python
class NFA:
    def __init__(self, ...):
        self.transition = transition  # dict: (state, symbol) -> set

    def epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        while stack:
            s = stack.pop()
            for ns in self.transition.get((s, ''), set()):
                if ns not in closure:
                    closure.add(ns)
                    stack.append(ns)
        return closure

    def accept(self, s):
        states = self.epsilon_closure({self.start})
        for ch in s:
            next_states = set()
            for st in states:
                next_states |= self.transition.get((st, ch), set())
            states = self.epsilon_closure(next_states)
        return bool(states & self.accepts)
```

### 正則表達式引擎

我們的簡易引擎支援三種運算：聯集 (`|`)、串接、Kleene 星號 (`*`)。使用 Thompson 建構將正則表達式轉換為 NFA，然後用 NFA 進行匹配。

### CFG 解析器

實作了一個簡單的遞迴下墜解析器 (Recursive Descent Parser)，可以解析算術表達式並建構語法樹。

### Turing Machine 模擬器

Turing Machine 的模擬需要維護磁帶內容和讀寫頭位置：

```python
class TuringMachine:
    def __init__(self, states, tape_alphabet, transition, start, accepts, blank='_'):
        self.tape = [blank]
        self.head = 0
        self.state = start
        self.transition = transition

    def step(self):
        symbol = self.tape[self.head]
        if (self.state, symbol) not in self.transition:
            return False
        next_state, write, move = self.transition[(self.state, symbol)]
        self.tape[self.head] = write
        if move == 'R':
            self.head += 1
            if self.head >= len(self.tape):
                self.tape.append(self.blank)
        else:
            self.head -= 1
        self.state = next_state
        return True
```

## demo() 函數

`automata.py` 的 `demo()` 函數會依序展示所有功能模組：

1. DFA 範例：辨識以 00 結尾的二進位字串
2. NFA 範例：辨識包含 "ab" 的字串
3. 正則表達式引擎範例
4. CFG 解析器範例：解析算術表達式
5. Turing Machine 範例：二進位加法

## 執行方式

```bash
python3 automata.py
```

## 完整程式碼

- [automata.py](_code/automata.py) — 所有自動機實作
- [test.sh](_code/test.sh) — 測試腳本

## 學習路徑建議

1. 先執行 DFA 範例，理解狀態轉移的概念
2. 比較 DFA 與 NFA 的行為差異
3. 觀察正則表達式如何轉換為 NFA
4. 用 CFG 解析器實驗不同文法
5. 最後嘗試修改 Turing Machine 的轉移函數

## 參考資料

- [https://www.google.com/search?q=automata+theory+Python+implementation](https://www.google.com/search?q=automata+theory+Python+implementation)
- [https://www.google.com/search?q=Python+DFA+NFA+simulation+tutorial](https://www.google.com/search?q=Python+DFA+NFA+simulation+tutorial)
