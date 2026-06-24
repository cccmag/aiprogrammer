# RSA 數論基礎

## 質數的奧秘

質數（Prime Number）是大於 1 的自然數，且只能被 1 和自身整除。質數是數論的基本構建單元，也是 RSA 密碼系統的數學基石。

### 算術基本定理

每個大於 1 的整數都可以唯一地分解為質因數的乘積。例如：

```
60 = 2² × 3 × 5
```

這個定理看似簡單，但它的深遠含義是：如果我們不知道質因數，就很難還原出原始數字的結構。這就是 RSA 安全性的核心。

### 質數分布

質數在自然數中的分布是不規則的，但整體趨勢由質數定理（Prime Number Theorem）描述：

```
π(n) ≈ n / ln(n)
```

其中 π(n) 是小於等於 n 的質數個數。這意味著在大數範圍內，質數仍然足夠豐富——一個 1024 位元的隨機整數是質數的概率約為 1/355。

## 尤拉函數

尤拉函數 φ(n) 的定義是小於等於 n 且與 n 互質的正整數個數。

計算公式：
- 如果 p 是質數：φ(p) = p - 1
- 如果 n = p × q（p、q 為不同質數）：φ(n) = (p - 1)(q - 1)

**互質（Coprime）**：兩個整數的最大公因數為 1。

## 尤拉定理

尤拉定理（Euler's Theorem）是 RSA 正確性的核心：

```
a^φ(n) ≡ 1 (mod n)
```

其中 a 和 n 互質。這個定理告訴我們：在模 n 的意義下，a 的 φ(n) 次方等於 1。

### 費馬小定理

當 n 為質數 p 時，尤拉定理退化為費馬小定理（Fermat's Little Theorem）：

```
a^(p-1) ≡ 1 (mod p)
```

費馬小定理不僅是 RSA 的基礎，還被用於素性測試（Fermat 素性測試）。

## 模反元素

模反元素（Modular Inverse）是滿足以下條件的整數 d：

```
d × e ≡ 1 (mod φ(n))
```

d 是 e 在模 φ(n) 下的乘法逆元。RSA 中，d 就是私鑰指數。

擴展歐幾里得演算法（Extended Euclidean Algorithm）是計算模反元素的高效方法。其時間複雜度為 O(log min(a, b))。

```python
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1
```

## 快速模指數運算

RSA 需要計算大數的模指數（如 m^e mod n），直接計算 m^e 是不現實的——因為 m^e 的位元數極大。

快速模指數（Modular Exponentiation）使用平方-乘演算法（Square-and-Multiply），時間複雜度為 O(log e)：

```python
def mod_pow(base, exp, mod):
    result = 1
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result
```

這個演算法將指數運算的複雜度從指數級降低到多項式級。

## 因數分解難題

RSA 的安全性確保依賴於大整數因數分解的計算困難性。目前最快的因數分解演算法是通用數域篩法（GNFS）。

### 量子威脅

1994 年，Peter Shor 提出了 Shor 演算法，可以在多項式時間內完成因數分解。這意味著大規模量子電腦將徹底打破 RSA。目前，2048 位元的 RSA 被認為在可預見的未來是安全的，但密碼學界已經在積極開發後量子密碼學方案。

## 延伸閱讀

- [質數定理](https://www.google.com/search?q=prime+number+theorem)
- [尤拉定理證明](https://www.google.com/search?q=Euler+theorem+proof)
- [Shor 演算法](https://www.google.com/search?q=Shor+algorithm+quantum+factoring)
- [通用數域篩法](https://www.google.com/search?q=general+number+field+sieve)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」精選文章。*
