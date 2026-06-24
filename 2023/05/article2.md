# NFA 轉 DFA 子集建構

## 為什麼需要轉換？

NFA 在設計上比 DFA 更靈活——我們可以自由使用非確定性轉移和 ε-轉移，而不必擔心轉移的唯一性。然而，NFA 的模擬需要維護狀態集合，在實際實作中效率較低。DFA 雖然狀態數可能更多，但模擬速度更快（O(n)）。

子集建構法 (Subset Construction) 解決了這個問題：將 NFA 轉換為等價的 DFA。

## 子集建構法原理

核心思想：NFA 的「當前可能狀態集合」對應於 DFA 的「單一狀態」。

### 演算法步驟

1. DFA 的起始狀態 = NFA 起始狀態的 ε-閉包
2. 對每個 DFA 狀態（即 NFA 狀態集合 S）和每個符號 a：
    - 計算 T = ∪_{s∈S} δ(s, a)（所有可能轉移的聯集）
    - DFA 的 δ(S, a) = ε-閉包(T)
3. DFA 的接受狀態 = 包含至少一個 NFA 接受狀態的集合

### 完整範例

考慮一個簡單的 NFA：
- Q = {q0, q1, q2}, Σ = {0, 1}, F = {q2}
- δ(q0, 0) = {q0, q1}, δ(q0, 1) = {q0}
- δ(q1, 1) = {q2}

子集建構過程：

```
起始: ε-閉包({q0}) = {q0}
對 {q0}:
  δ({q0}, 0) = ε-閉包({q0, q1}) = {q0, q1}
  δ({q0}, 1) = ε-閉包({q0}) = {q0}
對 {q0, q1}:
  δ({q0, q1}, 0) = ε-閉包({q0, q1}) = {q0, q1}
  δ({q0, q1}, 1) = ε-閉包({q0, q2}) = {q0, q2}
對 {q0, q2}:
  δ({q0, q2}, 0) = ε-閉包({q0, q1}) = {q0, q1}
  δ({q0, q2}, 1) = ε-閉包({q0}) = {q0}
```

最終 DFA 有三個狀態（對應三個集合），接受狀態為 {q0, q2}。

## Python 實作

```python
def nfa_to_dfa(nfa):
    start = epsilon_closure(nfa, {nfa.start})
    dfa_states = {frozenset(start): 0}
    dfa_trans = {}
    queue = [start]
    dfa_accept = set()

    while queue:
        current = queue.pop(0)
        current_id = dfa_states[frozenset(current)]
        if current & nfa.accepts:
            dfa_accept.add(current_id)
        for sym in nfa.alphabet:
            next_states = set()
            for s in current:
                next_states |= nfa.transition.get((s, sym), set())
            next_states = epsilon_closure(nfa, next_states)
            if not next_states:
                continue
            key = frozenset(next_states)
            if key not in dfa_states:
                dfa_states[key] = len(dfa_states)
                queue.append(next_states)
            dfa_trans[(current_id, sym)] = dfa_states[key]
    return dfa_states, dfa_trans, dfa_accept
```

## 複雜度分析

最壞情況下，如果 NFA 有 n 個狀態，轉換後的 DFA 可能有多達 2^n 個狀態。這是因為 DFA 的每個狀態對應於 NFA 狀態集合的一個子集。

然而在實際應用中，大多數 NFA 轉換後的 DFA 狀態數遠小於指數級。例如，Thompson 建構產生的 NFA 轉 DFA 後，狀態數通常與原始正則表達式的長度成線性關係。

## 參考資料

- [https://www.google.com/search?q=subset+construction+NFA+to+DFA+algorithm](https://www.google.com/search?q=subset+construction+NFA+to+DFA+algorithm)
- [https://www.google.com/search?q=NFA+to+DFA+conversion+Python](https://www.google.com/search?q=NFA+to+DFA+conversion+Python)
- [https://www.google.com/search?q=NFA+轉+DFA+子集建構法](https://www.google.com/search?q=NFA+轉+DFA+子集建構法)
