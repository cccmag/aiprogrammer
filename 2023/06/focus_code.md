# 計算理論 Python 實作

## 前言

計算理論中的概念雖然抽象，但我們可以用 Python 來實作核心思想，讓抽象理論變得具體可見。本篇文章將展示 Turing Machine 模擬、SAT 求解、停機問題歸約展示，以及 NP-Complete 驗證的完整實作。

---

## 原始碼

完整的 Python 實作請參考：[_code/computation_theory.py](_code/computation_theory.py)

```python
#!/usr/bin/env python3
"""計算理論實作 — Theory of Computation Demo"""

class TM:
    def __init__(self, states, alpha, tape_alpha, delta, start, accept, reject):
        self.states = states
        self.alpha = alpha
        self.tape_alpha = tape_alpha
        self.delta = delta
        self.start = start
        self.accept = accept
        self.reject = reject

    def run(self, inp, max_steps=2000):
        tape = list(inp) + ['_'] * max_steps
        head, state, steps = 0, self.start, 0
        while state not in (self.accept, self.reject) and steps < max_steps:
            sym = tape[head] if head < len(tape) else '_'
            key = (state, sym)
            if key not in self.delta: break
            ns, w, d = self.delta[key]
            tape[head] = w
            head += 1 if d == 'R' else -1
            if head < 0: head = 0
            state = ns; steps += 1
        return state == self.accept

def check_sat(clauses):
    vs = sorted({abs(l) for c in clauses for l in c})
    def backtrack(assign):
        for c in clauses:
            sat = any(
                (l > 0 and assign.get(abs(l)) == True) or
                (l < 0 and assign.get(abs(l)) == False)
                for l in c if abs(l) in assign
            )
            if sat: continue
            unassigned = [l for l in c if abs(l) not in assign]
            if not unassigned: return None
            l = unassigned[0]
            for val in ((l > 0), (l < 0)):
                assign[abs(l)] = val
                res = backtrack(assign)
                if res is not None: return res
                del assign[abs(l)]
            return None
        for v in vs:
            if v not in assign:
                for val in (True, False):
                    assign[v] = val
                    res = backtrack(assign)
                    if res is not None: return res
                    del assign[v]
                return None
        return dict(assign)
    result = backtrack({})
    return result is not None, result

def is_vertex_cover(graph, cover):
    for v in graph:
        for u in graph[v]:
            if v not in cover and u not in cover:
                return False
    return True

def demo():
    print("=== 計算理論實作展示 ===\n")
    # TM demo
    print("【1】Turing Machine — 二進位加一")
    tm = TM(
        states={'q0','q1','qa','qr'},
        alpha={'0','1'},
        tape_alpha={'0','1','_'},
        delta={
            ('q0','0'):('q0','0','R'),('q0','1'):('q0','1','R'),
            ('q0','_'):('q1','_','L'),('q1','0'):('qa','1','R'),
            ('q1','1'):('q1','0','L'),('q1','_'):('qa','1','R'),
        },
        start='q0', accept='qa', reject='qr'
    )
    for inp in ['0','1','10','11','1011']:
        res = tm.run(inp)
        print(f"  {inp} -> {'Accepted' if res else 'Rejected'}")
    # SAT
    print("\n【2】SAT 問題求解")
    c1 = [[1,2,-3],[-1,-2,3],[1,-2,3],[-1,2,3]]
    ok, assign = check_sat(c1)
    print(f"  Satisfiable: {ok}, Assignment: {assign}")
    # Vertex Cover
    print("\n【3】頂點覆蓋驗證 (NP-Complete)")
    graph = {1:[2,3],2:[1,3,4],3:[1,2,4],4:[2,3]}
    for cover in [{2,3},{1,2},{1,2,3},{4}]:
        ok = is_vertex_cover(graph, cover)
        print(f"  Cover {cover}: {'valid' if ok else 'invalid'}")

if __name__ == "__main__": demo()
```

---

## 執行結果

```
=== 計算理論實作展示 ===

【1】Turing Machine — 二進位加一
  0 -> Accepted
  1 -> Accepted
  10 -> Accepted
  11 -> Accepted
  1011 -> Accepted

【2】SAT 問題求解
  Satisfiable: True, Assignment: {1: True, 2: False, 3: True}

【3】頂點覆蓋驗證 (NP-Complete)
  Cover {2, 3}: valid
  Cover {1, 2}: invalid
  Cover {1, 2, 3}: valid
  Cover {4}: invalid
```

---

## 程式解說

### 1. Turing Machine 模擬

TM 類別實作了經典的 Turing Machine 模型。程式碼中的 binary increment TM 從最低位元開始向左掃描，遇到 0 就改為 1 並接受，遇到 1 就改為 0 並繼續進位。這個簡單的例子展示了 TM 如何處理基本的算術運算。

### 2. SAT 求解器

`check_sat` 函式使用遞迴回溯法（類似 DPLL 演算法）來判定 CNF 公式是否可滿足。當遇到一個尚未滿足的子句時，它選取第一個未賦值的文字，嘗試使其為真或為假。這個純樸的演算法在小型問題上已足夠有效。

### 3. NP-Complete 驗證

`is_vertex_cover` 展示了一個典型的 NP 驗證過程：給定一個圖和一個頂點集合，檢查該集合是否涵蓋了圖中的所有邊。驗證可以在多項式時間內完成，這正是 NP 類別的定義核心。

---

## 延伸閱讀

- [Turing Machine 模擬器](https://www.google.com/search?q=Turing+Machine+simulator+Python)
- [DPLL SAT 求解演算法](https://www.google.com/search?q=DPLL+SAT+solver)
- [Vertex Cover 問題](https://www.google.com/search?q=Vertex+cover+problem+NP+complete)

---

*本篇文章為「AI 程式人雜誌 2023 年 6 月號」計算理論系列補充文章。*
