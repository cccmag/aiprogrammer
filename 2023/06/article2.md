# λ 演算與 Church 數

## 用函式定義一切

Alonzo Church 的 λ 演算只有三條規則：變數、抽象、應用。但從這三條規則出發，可以定義出所有數學概念。這就是 Church 編碼（Church Encoding）的核心思想。

## Church 布林值

Church 將布林值編碼為選擇函式：

```
TRUE  = λt.λf.t    -- 選擇第一個參數
FALSE = λt.λf.f    -- 選擇第二個參數
IF    = λp.λa.λb.p a b  -- 條件表達式
```

布林運算：
```
AND = λp.λq.p q p          -- 如果 p 為真，回傳 q，否則回傳 p（FALSE）
OR  = λp.λq.p p q          -- 如果 p 為真，回傳 p，否則回傳 q
NOT = λp.λa.λb.p b a       -- 反轉選擇
```

## Church 數字

Church 將自然數 n 編碼為「對函式 f 套用 n 次」：

```
0 = λf.λx.x
1 = λf.λx.f x
2 = λf.λx.f (f x)
3 = λf.λx.f (f (f x))
```

Church 數字 n 就是一個高階函式：它接受一個函式 f 和一個參數 x，然後將 f 套用到 x 上 n 次。

## 算術運算

後繼函式（加一）：
```
SUCC = λn.λf.λx.f (n f x)
```

加法（套用 f 的次數相加）：
```
PLUS = λm.λn.λf.λx.m f (n f x)
```

乘法（將 n f 套用 m 次）：
```
MULT = λm.λn.λf.m (n f)
```

指數（將 m 套用 n 次）：
```
POWER = λm.λn.n m
```

## 前驅與減法

前驅函式（減一）比較複雜：
```
PRED = λn.λf.λx.n (λg.λh.h (g f)) (λu.x) (λu.u)
```

## Python 實作

```python
# Church 布林值
TRUE  = lambda t: lambda f: t
FALSE = lambda t: lambda f: f
AND   = lambda p: lambda q: p(q)(p)
OR    = lambda p: lambda q: p(p)(q)
NOT   = lambda p: lambda a: lambda b: p(b)(a)

# Church 數字
ZERO  = lambda f: lambda x: x
ONE   = lambda f: lambda x: f(x)
TWO   = lambda f: lambda x: f(f(x))
THREE = lambda f: lambda x: f(f(f(x)))

def church_to_int(n):
    return n(lambda x: x + 1)(0)

# 算術
SUCC  = lambda n: lambda f: lambda x: f(n(f)(x))
PLUS  = lambda m: lambda n: lambda f: lambda x: m(f)(n(f)(x))
MULT  = lambda m: lambda n: lambda f: m(n(f))
POWER = lambda m: lambda n: n(m)

# 測試
print(f"Church 3 = {church_to_int(THREE)}")     # 3
two = PLUS(ONE)(ONE)
three = SUCC(two)
print(f"1 + 1 = {church_to_int(two)}")          # 2
print(f"2 + 1 = {church_to_int(three)}")        # 3
print(f"2 * 3 = {church_to_int(MULT(TWO)(THREE))}")  # 6
```

## λ 演算的美學

λ 演算最令人驚嘆的地方在於：沒有數字、沒有布林值、沒有資料結構，只用函式就定義了一切。這種極簡主義不僅是數學上的優雅，更揭示了計算的本質——一切都是函式應用。

## 延伸閱讀

- [Church Encoding](https://www.google.com/search?q=Church+encoding+lambda+calculus)
- [Lambda Calculus 入門](https://www.google.com/search?q=lambda+calculus+tutorial+programming)
- [Church Numerals 運算](https://www.google.com/search?q=Church+numerals+arithmetic)
