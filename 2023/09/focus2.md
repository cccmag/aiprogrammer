# 型別系統導論

## 型別安全的基礎

### 什麼是型別系統？

型別系統是程式語言中一組規則，用於標記和檢查變數與表達式的「型別」。型別決定了哪些操作是合法的——例如，整數可以和整數相加，但不能與字串相加（除非語言定義了轉換規則）。

### 型別安全

**型別安全**（type safety）是指程式不會執行非法操作的保證。例如，不會將整數當作函數呼叫，不會存取不存在的欄位。

型別安全可分為：

- **強型別安全**：語言保證所有操作都型別正確（Rust、Haskell）
- **弱型別安全**：語言允許某些隱式轉換，可能導致執行時期錯誤（C、JavaScript）

### 簡單型別 λ 演算

簡單型別 λ 演算（Simply Typed Lambda Calculus, STLC）是型別系統的理論基礎。它為 λ 演算中的每個表達式標記型別：

```python
# 語法：e ::= x | λx:T.e | e1 e2 | n | e1 + e2
# 型別：T ::= Int | T1 -> T2

# (λx:Int. x + 1) : Int -> Int
# 類型檢查：在假設 x:Int 的環境中，x+1 是 Int
```

### 型別檢查演算法

型別檢查器遍歷 AST，使用環境（environment）記錄變數型別：

```python
class TypeChecker:
    def check(self, expr, env):
        if isinstance(expr, EInt): return TInt()
        if isinstance(expr, EVar): return env[expr.name]
        if isinstance(expr, EAbs):
            env[expr.var] = expr.var_type
            ret = self.check(expr.body, env)
            return TFun(expr.var_type, ret)
        if isinstance(expr, EApp):
            ft = self.check(expr.fn, env)
            at = self.check(expr.arg, env)
            # 檢查 ft 是否為函數型別且參數型別匹配
            return ft.ret
```

### 型別系統的特性

- **可靠（Sound）**：通過型別檢查的程式不會型別錯誤
- **完備（Complete）**：所有不會型別錯誤的程式都能通過檢查
- **可判定（Decidable）**：型別檢查演算法保證終止

### 主流語言的型別系統

| 語言 | 型別特性 |
|------|---------|
| Python | 動態、漸進型別（3.5+ 支援型別提示） |
| TypeScript | 靜態、結構子型別、逐步採用 |
| Rust | 靜態、強型別、所有權系統 |
| Haskell | 靜態、強型別、全域推斷 |

### 延伸閱讀

- [型別系統理論](https://www.google.com/search?q=type+system+programming+languages)
- [簡單型別 λ 演算](https://www.google.com/search?q=simply+typed+lambda+calculus)

---

**下一篇**：[多型與泛型](focus3.md)
