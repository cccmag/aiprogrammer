# PLT 範例整合：λ 演算、型別檢查、Monad

## 概述

本文展示的 [`plt_demo.py`](_code/plt_demo.py) 是一個 Python 腳本，整合了程式語言理論的四個核心概念：

1. **λ 演算直譯器**：Church numerals、算術運算、Y combinator
2. **型別檢查器**：簡單型別 λ 演算的型別推導
3. **高階函數與組合子**：map、filter、reduce、currying
4. **Monad 模擬**：Maybe、List、Either monad

## 執行方式

```bash
cd _code
python3 plt_demo.py
```

## 核心設計

### 1. λ 演算

Church numerals 將自然數編碼為高階函數。數字 `n` 表示「將函數 f 應用 n 次」：

```python
CHURCH_ZERO = lambda f: lambda x: x
CHURCH_ONE  = lambda f: lambda x: f(x)
CHURCH_TWO  = lambda f: lambda x: f(f(x))

church_to_int(n) = n(lambda x: x + 1)(0)
```

Y combinator 實現了不動點遞迴，無需語言內建遞迴機制即可定義階乘等函數。

### 2. 型別檢查器

實作了一個簡單的型別檢查器，支援 Int、Bool、函數類型和條件表達式。檢查器遍歷 AST，在環境中追蹤變數型別，並在類型不匹配時拋出錯誤。

### 3. 高階函數

用 Python 實作了 curry/uncurry 轉換和函數組合，展示了高階函數在程式碼重構中的作用。

### 4. Monad

Monad 是函數式程式設計中最強大的抽象之一。本實作展示了三個常見的 Monad：

- **Maybe Monad**：安全的失敗傳播
- **List Monad**：非確定性計算
- **Either Monad**：帶錯誤訊息的失敗處理

## 執行結果

```
--- 1. Lambda Calculus ---
1 + 2 = 3
2 * 2 = 4
fact(5) = 120

--- 2. Type Checker ---
Type of (λx:Int. x + 1): (Int -> Int)
Type error caught: Cond must be Bool, got Int

--- 3. Higher-Order Functions ---
map(x2, [1,2,3,4,5]) = [2, 4, 6, 8, 10]
filter(even, [1,2,3,4,5]) = [2, 4]
curry(+)(1)(5) = 6

--- 4. Monad ---
Just(10) >>= safe_div(_,2): Just(5)
Just(10) >>= safe_div(_,0): Nothing
List cartesian product: ListM([(1,3),(1,4),(2,3),(2,4)])
Either sqrt(16): Right(4.0)
Either sqrt(-1): Left(negative)
```

## 延伸練習

- 加入代數資料型別（Algebraic Data Types）
- 實作更完整的 λ 演算歸約（β-reduction、η-conversion）
- 加入 State Monad 和 IO Monad
- 實作型別推斷演算法（Hindley-Milner）

---

**完整程式碼**：[`_code/plt_demo.py`](_code/plt_demo.py)
