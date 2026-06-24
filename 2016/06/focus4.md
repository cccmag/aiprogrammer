# 主題四：正規語言的封閉性

## 什麼是封閉性？

如果一個語言類別對某種運算封閉，意思是：如果 L 和 M 屬於這個語言類別，則運算結果也屬於這個類別。

正規語言對以下運算封閉：
- 並集（Union）
- 連接（Concatenation）
- 克林閉包（Kleene Star）
- 交集（Intersection）
- 補集（Complement）
- 反轉（Reversal）
- 同態（Homomorphism）
- 逆同態（Inverse Homomorphism）

## 並集封閉性

如果 L1 和 L2 是正規的，則 L1 ∪ L2 也是正規的。

### 構造法

```python
# 合併兩個 DFA 為一個
def union_dfa(dfa1, dfa2):
    """
    構造 L(dfa1) ∪ L(dfa2) 的 DFA
    新狀態是狀態對的笛卡爾積
    """
    new_states = []
    for q1 in dfa1.Q:
        for q2 in dfa2.Q:
            new_states.append((q1, q2))

    new_delta = {}
    for (q1, q2) in new_states:
        for symbol in dfa1.sigma:
            new_delta[((q1, q2), symbol)] = (
                dfa1.delta.get((q1, symbol), None),
                dfa2.delta.get((q2, symbol), None)
            )

    new_initial = (dfa1.q0, dfa2.q0)
    new_finals = [(q1, q2) for q1 in dfa1.F for q2 in dfa2.Q] + \
                [(q1, q2) for q1 in dfa1.Q for q2 in dfa2.F]

    return new_states, new_delta, new_initial, new_finals
```

### 直覺理解

構造一個「同時模擬兩個自動機」的並行系統。

## 連接封閉性

如果 L1 和 L2 是正規的，則 L1L2 也是正規的。

### 構造法

```python
def concatenate_nfa(nfa1, nfa2):
    """
    構造 L(nfa1)L(nfa2) 的 NFA
    連接 nfa1 的接受狀態到 nfa2 的初始狀態
    """
    new_delta = dict(nfa1.delta)
    new_delta.update(nfa2.delta)

    # 從 nfa1 的接受狀態 ε 轉換到 nfa2 的初始狀態
    for state in nfa1.F:
        new_delta[(state, '')] = {nfa2.q0}

    return nfa1.Q | nfa2.Q, nfa1.F | {nfa2.q0} if state in nfa1.F else nfa2.F
```

## 克林閉包封閉性

如果 L 是正規的，則 L* 也是正規的。

### 構造法

```python
def kleene_star_nfa(nfa):
    """
    構造 L(nfa)* 的 NFA
    添加從接受狀態到初始狀態的 ε 轉換
    """
    new_delta = dict(nfa.delta)

    # 從每個接受狀態 ε 轉換回初始狀態
    for state in nfa.F:
        new_delta[(state, '')] = {nfa.q0}

    # 添加新的初始狀態（也是接受狀態）
    new_initial = 'new_start'
    new_delta[(new_initial, '')] = {nfa.q0}

    return nfa.Q | {new_initial}, nfa.F | {new_initial}
```

## 交集封閉性

如果 L1 和 L2 是正規的，則 L1 ∩ L2 也是正規的。

### 構造法（乘積構造）

```python
def intersect_dfa(dfa1, dfa2):
    """
    構造 L(dfa1) ∩ L(dfa2) 的 DFA
    """
    new_states = []
    for q1 in dfa1.Q:
        for q2 in dfa2.Q:
            new_states.append((q1, q2))

    new_delta = {}
    for (q1, q2) in new_states:
        for symbol in dfa1.sigma:
            new_delta[((q1, q2), symbol)] = (
                dfa1.delta.get((q1, symbol)),
                dfa2.delta.get((q2, symbol))
            )

    new_initial = (dfa1.q0, dfa2.q0)
    # 只有兩個 DFA 都在接受狀態時才是接受狀態
    new_finals = [(q1, q2) for q1 in dfa1.F for q2 in dfa2.F]

    return new_states, new_delta, new_initial, new_finals
```

## 補集封閉性

如果 L 是正規的，則 L̄（補集）也是正規的。

### 構造法

```python
def complement_dfa(dfa):
    """
    構造 L(dfa) 補集的 DFA
    """
    # 所有非接受狀態變成接受狀態
    new_finals = set(dfa.Q) - dfa.F
    return dfa.Q, dfa.sigma, dfa.delta, dfa.q0, new_finals
```

## 反轉封閉性

如果 L 是正規的，則 L^R（反轉）也是正規的。

```python
def reverse_regex(regex):
    """
    反轉正規表達式
    """
    # 實現反轉
    pass
```

## 德摩根定律

從交集和補集的封閉性可得：

```
L1 ∪ L2 = (L1̄ ∩ L2̄)̄
L1 ∩ L2 = (L1̄ ∪ L2̄)̄
```

## 同態

同態（Homomorphism）是將字母表中的符號映射為字串的函式。

如果 h 是字母表 Σ 到 Δ* 的同態，則：

- h(L) = {h(w) | w ∈ L}
- h⁻¹(L) = {w | h(w) ∈ L}

```python
# 同態映射示例
def homomorphism(word, mapping):
    """應用同態映射"""
    result = ""
    for char in word:
        result += mapping.get(char, "")
    return result

mapping = {'a': '0', 'b': '1'}
print(homomorphism("ab", mapping))  # "01"
```

## 封閉性的應用

### 證明語言不是正規的

```python
def prove_not_regular():
    """
    使用泵浦引理和封閉性證明 L = {0^n 1^n | n ≥ 0} 不是正規的

    證明：
    假設 L 是正規的
    因為 {0^n 1^n} = {0^n} ∩ {1^n}*
    如果 L 是正規的，則交集也是正規的（封閉性）
    但 {0^n} ∩ {1^n}* 不是正規的（泵浦引理）
    矛盾！
    """
    pass
```

## 小結

正規語言的封閉性是理論和應用的重要基礎。它讓我們能夠组合简单的正規語言來構造更複雜的語言，也讓我們能夠用反證法證明某些語言不是正規的。