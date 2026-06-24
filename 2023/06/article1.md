# 原始遞迴與 μ-遞迴函數

## 遞迴函數的起源

在 λ 演算和圖靈機之前，Kurt Gödel 在 1931 年證明不完全性定理時，使用了一種稱為「原始遞迴函數」（Primitive Recursive Functions）的概念。後來 Stephen Kleene 將這個概念推廣為「μ-遞迴函數」（μ-Recursive Functions），建立了可計算性的另一個等價定義。

## 原始遞迴函數

原始遞迴函數是從一些基本函數開始，透過有限次的組合與遞迴構造出來的函數。

### 基本函數

1. **零函數**：Z(x) = 0
2. **後繼函數**：S(x) = x + 1
3. **投影函數**：P_i^n(x₁, ..., xₙ) = xᵢ

### 構造規則

1. **複合**：f(g₁(x), ..., gₖ(x))
2. **原始遞迴**：f(0, x) = g(x), f(n+1, x) = h(f(n, x), n, x)

### 範例

加法：add(0, y) = y, add(n+1, y) = S(add(n, y))

```python
def add(n, y):
    if n == 0: return y
    return add(n - 1, y) + 1
```

乘法：mul(0, y) = 0, mul(n+1, y) = add(mul(n, y), y)

階乘：fact(0) = 1, fact(n+1) = mul(S(n), fact(n))

## 原始遞迴的局限

原始遞迴函數雖然強大，但存在重要局限：**所有原始遞迴函數都是全函數**（對所有輸入都會終止）。這意味著存在可計算但非原始遞迴的函數。

最著名的例子是 **Ackermann 函數**：

```
A(0, n) = n + 1
A(m, 0) = A(m-1, 1)
A(m, n) = A(m-1, A(m, n-1))
```

Ackermann 函數增長極快：A(4, 2) ≈ 2^65536 - 3，這不是任何原始遞迴函數可以表達的。

```python
def ackermann(m, n):
    if m == 0: return n + 1
    if n == 0: return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))
```

## μ-遞迴函數

為了超越原始遞迴的限制，Kleene 引入了 μ 算子（極小化算子）：

> μy[P(y, x)] = 最小的 y 使得 P(y, x) = 1，且對所有 z < y，P(z, x) 有定義

μ 算子允許我們搜尋滿足條件的 y。這個算子引入了一個關鍵特性：**部分函數**。μ-遞迴函數可能對某些輸入不收斂（不停機）。

### 三條規則

μ-遞迴函數 = 基本函數 + 複合 + 原始遞迴 + μ 算子

## 等價性

Kleene 證明了：

> μ-遞迴函數 ≡ 圖靈機可計算函數 ≡ λ 可定義函數

這三種模型的等價性鞏固了 Church-Turing 論題，也說明了「可計算性」這個概念的本質穩固性。

## 程式實作

```python
# 原始遞迴：階乘
def fact(n):
    if n <= 1: return 1
    return n * fact(n - 1)

# 原始遞迴：Fibonacci
def fib(n):
    if n <= 1: return n
    return fib(n - 1) + fib(n - 2)

# 非原始遞迴：Ackermann
def ack(m, n):
    if m == 0: return n + 1
    if n == 0: return ack(m - 1, 1)
    return ack(m - 1, ack(m, n - 1))

print(f"fib(10) = {fib(10)}")           # 55
print(f"fact(5) = {fact(5)}")            # 120
print(f"ack(3, 4) = {ack(3, 4)}")        # 125
```

## 延伸閱讀

- [Primitive Recursive Functions](https://www.google.com/search?q=primitive+recursive+function+definition)
- [Ackermann Function](https://www.google.com/search?q=Ackermann+function+recursive)
- [μ-Recursive Functions](https://www.google.com/search?q=mu+recursive+functions+Kleene)
