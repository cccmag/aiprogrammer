# SAT 與 3-SAT

## 布林可滿足性問題

SAT（Boolean Satisfiability Problem）是計算理論中最核心的問題之一。給定一個布林公式（由 AND、OR、NOT 連接的布林變數組成），SAT 問題問：是否存在一組變數賦值，使整個公式為真？

例如，公式 (x ∨ y) ∧ (¬x ∨ ¬y) 是可滿足的：令 x = True, y = False。

## CNF 形式

SAT 的標準輸入格式是 CNF（合取正規形式）：

```
公式 = 子句₁ ∧ 子句₂ ∧ ... ∧ 子句ₖ
```

每個子句是文字的析取（OR）：

```
子句 = 文字₁ ∨ 文字₂ ∨ ... ∨ 文字ₘ
```

每個文字是一個布林變數或其否定。

例如：(x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂ ∨ x₃) ∧ (x₁ ∨ x₂ ∨ ¬x₃)

## 3-SAT

3-SAT 是 SAT 的一個重要限制版本：每個子句恰好包含 3 個文字。

雖然看起來 3-SAT 比一般 SAT 更「簡單」，但它們是等價的——一般 SAT 可以在多項式時間內歸約到 3-SAT。

## SAT 的演算法

### 暴力法

窮舉所有 2ⁿ 種賦值。當 n = 100 時，這需要比宇宙年齡更久的時間。

### DPLL 演算法

Davis-Putnam-Logemann-Loveland 演算法是現代 SAT 求解器的基礎：

```python
def dpll(clauses, assign):
    # 單位子句傳播
    while True:
        unit = find_unit(clauses, assign)
        if unit is None: break
        assign[abs(unit)] = unit > 0

    # 純文字消去
    while True:
        pure = find_pure(clauses, assign)
        if pure is None: break
        assign[abs(pure)] = pure > 0

    # 檢查是否滿足
    if all_satisfied(clauses, assign): return True
    if any_conflict(clauses, assign): return False

    # 選擇變數並遞迴
    v = choose_variable(clauses, assign)
    for val in [True, False]:
        assign[v] = val
        if dpll(clauses, assign): return True
        del assign[v]
    return False
```

### CDCL 演算法

現代 SAT 求解器（如 MiniSat、Z3、Glucose）使用 Conflict-Driven Clause Learning（CDCL），在 DPLL 的基礎上增加了：

1. **子句學習**：遇到衝突時，學習新的子句以避免重複搜尋
2. **回溯跳躍**：不是簡單回溯，而是跳回衝突原因所在層級
3. **啟發式賦值**：VSIDS（Variable State Independent Decaying Sum）啟發式
4. **重啟策略**：定期重啟搜尋以跳出局部困境

## SAT 求解器的應用

現代 SAT 求解器可以處理數百萬變數的實例，應用範圍極廣：

- **硬體驗證**：驗證晶片設計的正確性
- **軟體驗證**：符號執行與漏洞發現
- **自動規劃**：AI 規劃問題的編碼與求解
- **密碼分析**：破解密碼系統
- **數學定理證明**：輔助數學證明

## SAT 與 AI

SAT 在 AI 中有著關鍵作用：

- **知識表示**：用 SAT 編碼知識庫與推理規則
- **規劃與排程**：將規劃問題編碼為 SAT
- **模型 checking**：驗證系統的時序性質
- **約束求解**：求解 CSP（Constraint Satisfaction Problem）

## Python 範例

```python
from itertools import product

def brute_force_sat(clauses):
    vars = set(abs(l) for c in clauses for l in c)
    for values in product([True, False], repeat=len(vars)):
        assign = dict(zip(vars, values))
        if all(
            any(
                (l > 0 and assign[abs(l)]) or (l < 0 and not assign[abs(l)])
                for l in c
            )
            for c in clauses
        ):
            return assign
    return None

clauses = [[1, 2, -3], [-1, -2, 3], [1, -2, 3], [-1, 2, 3]]
sol = brute_force_sat(clauses)
print(f"Satisfiable: {sol is not None}")
if sol: print(f"Solution: {sol}")
```

## 延伸閱讀

- [SAT Solver 演算法](https://www.google.com/search?q=SAT+solver+DPLL+CDCL)
- [3-SAT NP-Completeness](https://www.google.com/search?q=3+SAT+NP+complete)
- [Modern SAT Solving](https://www.google.com/search?q=modern+SAT+solving+techniques)
