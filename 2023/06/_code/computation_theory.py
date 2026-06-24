#!/usr/bin/env python3
"""計算理論實作 — Theory of Computation Demo"""

# ── Turing Machine ──
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
            if key not in self.delta:
                break
            ns, w, d = self.delta[key]
            tape[head] = w
            head += 1 if d == 'R' else -1
            if head < 0: head = 0
            state = ns
            steps += 1
        return state == self.accept

# ── SAT Solver (recursive backtracking) ──
def check_sat(clauses):
    vs = sorted({abs(l) for c in clauses for l in c})

    def backtrack(assign):
        for c in clauses:
            sat = any(
                (l > 0 and assign.get(abs(l)) == True) or
                (l < 0 and assign.get(abs(l)) == False)
                for l in c if abs(l) in assign
            )
            if sat:
                continue
            unassigned = [l for l in c if abs(l) not in assign]
            if not unassigned:
                return None
            l = unassigned[0]
            for val in ((l > 0), (l < 0)):
                assign[abs(l)] = val
                res = backtrack(assign)
                if res is not None:
                    return res
                del assign[abs(l)]
            return None
        for v in vs:
            if v not in assign:
                for val in (True, False):
                    assign[v] = val
                    res = backtrack(assign)
                    if res is not None:
                        return res
                    del assign[v]
                return None
        return dict(assign)

    result = backtrack({})
    return result is not None, result

# ── Vertex Cover Verification ──
def is_vertex_cover(graph, cover):
    for v in graph:
        for u in graph[v]:
            if v not in cover and u not in cover:
                return False
    return True

# ── Demo ──
def demo():
    print("=== 計算理論實作展示 ===\n")

    # 1. Turing Machine — increment binary
    print("【1】Turing Machine — 二進位加一")
    tm = TM(
        states={'q0', 'q1', 'qa', 'qr'},
        alpha={'0', '1'},
        tape_alpha={'0', '1', '_'},
        delta={
            ('q0', '0'): ('q0', '0', 'R'),
            ('q0', '1'): ('q0', '1', 'R'),
            ('q0', '_'): ('q1', '_', 'L'),
            ('q1', '0'): ('qa', '1', 'R'),
            ('q1', '1'): ('q1', '0', 'L'),
            ('q1', '_'): ('qa', '1', 'R'),
        },
        start='q0', accept='qa', reject='qr'
    )
    for inp in ['0', '1', '10', '11', '1011']:
        res = tm.run(inp)
        print(f"  {inp} -> {'Accepted' if res else 'Rejected'}")

    # 2. SAT
    print("\n【2】SAT 問題求解")
    c1 = [[1, 2, -3], [-1, -2, 3], [1, -2, 3], [-1, 2, 3]]
    ok, assign = check_sat(c1)
    print(f"  Clauses: {c1}")
    print(f"  Satisfiable: {ok}, Assignment: {assign}")
    c2 = [[1], [-1]]
    ok2, assign2 = check_sat(c2)
    print(f"  Clauses: {c2}")
    print(f"  Satisfiable: {ok2}")

    # 3. Halting problem reduction (conceptual)
    print("\n【3】停機問題歸約（概念展示）")
    print("  H(program, input) = 如果 program(input) 停機則 True")
    print("  若存在 H，則可構造 paradox(): if H(paradox) then loop")
    print("  矛盾 → 停機問題不可判定")

    # 4. NP-Complete: Vertex Cover
    print("\n【4】頂點覆蓋驗證 (NP-Complete)")
    graph = {1: [2, 3], 2: [1, 3, 4], 3: [1, 2, 4], 4: [2, 3]}
    for cover in [{2, 3}, {1, 2}, {1, 2, 3}, {4}]:
        ok = is_vertex_cover(graph, cover)
        print(f"  Cover {cover}: {'valid' if ok else 'invalid'}")

    print("\n=== 展示完畢 ===")

if __name__ == "__main__":
    demo()
