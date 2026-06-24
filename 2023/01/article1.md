# 二進位與布林代數

## 1. 引言

現代計算機的資訊表示與運算建立在兩個基礎之上：二進位數值系統（Binary Number System）和布林代數（Boolean Algebra）。二進位提供了資訊的表示方式，布林代數提供了資訊的運算規則。本文將深入探討這兩個基礎概念，並透過 Python 實作來加深理解。

## 2. 二進位系統

### 2.1 位元與位元組

計算機中最小的資訊單位是位元（bit），可以表示 0 或 1 兩種狀態。8 個位元組成一個位元組（byte），可以表示 256（2⁸）種不同的值。

### 2.2 不同進位制的轉換

十進位、二進位、八進位和十六進位之間的轉換是計算機科學的基本技能：

```python
def to_binary(n):
    if n == 0:
        return '0'
    bits = []
    while n > 0:
        bits.append(str(n % 2))
        n //= 2
    return ''.join(reversed(bits))

def from_binary(s):
    result = 0
    for c in s:
        result = result * 2 + int(c)
    return result
```

### 2.3 補數表示法

有號整數在計算機中最常見的表示方式為二補數（Two's complement）：

- 正數：與無號二進位相同
- 負數：對所有位元取反（一補數）後加 1

```
+5 = 0101
-5 = 1011（0101 → 1010 + 1 → 1011）
```

二補數的優點是加減法可以用同一套電路實現。

## 3. 布林代數

### 3.1 基本運算

布林代數有三個基本運算：

- **AND（且）**：兩者都為真時結果為真
- **OR（或）**：至少一個為真時結果為真
- **NOT（非）**：對真值取反

```python
def boolean_algebra():
    print("基本布林運算：")
    for a in [False, True]:
        for b in [False, True]:
            print(f"{a} AND {b} = {a and b}")
            print(f"{a} OR  {b} = {a or b}")
    print(f"NOT True = {not True}")
    print(f"NOT False = {not False}")
```

### 3.2 布林代數定理

**基本定理**：

| 定理 | AND 形式 | OR 形式 |
|------|---------|--------|
| 同一律 | A · 1 = A | A + 0 = A |
| 零律 | A · 0 = 0 | A + 1 = 1 |
| 補餘律 | A · A' = 0 | A + A' = 1 |
| 等冪律 | A · A = A | A + A = A |
| 雙重否定 | (A')' = A | (A')' = A |

**狄摩根定律（De Morgan's Laws）**：

```
(A · B)' = A' + B'
(A + B)' = A' · B'
```

狄摩根定律是數位電路設計中最重要的化簡工具之一。

### 3.3 Python 實現的布林代數驗證

```python
def verify_de_morgan():
    for a in [0, 1]:
        for b in [0, 1]:
            left = not (a and b)
            right = (not a) or (not b)
            assert left == right, "De Morgan fails!"
    print("De Morgan's laws verified!")
```

## 4. 布林表達式化簡

### 4.1 代數化簡

利用布林代數定理將複雜的表達式化簡為最簡形式。

**範例**：化簡 `F = A'BC + AB'C + ABC' + ABC`

```
F = A'BC + AB'C + ABC' + ABC
  = BC(A' + A) + AB'C + ABC'    (分配律)
  = BC + AB'C + ABC'             (補餘律)
  = C(B + AB') + ABC'            (分配律)
  = C(B + A) + ABC'              (吸收律)
  = BC + AC + ABC'               (分配律)
  = BC + A(C + BC')              (分配律)
  = BC + A(C + B)                (吸收律)
  = BC + AC + AB                 (分配律)
```

### 4.2 卡諾圖（Karnaugh Map）

卡諾圖是一種圖形化的布林表達式化簡方法：

```python
def karnaugh_simplify_2var(a, b, c, d):
    """2 變數卡諾圖：F(A,B)
    方格排列：
        B=0  B=1
    A=0  a    b
    A=1  c    d
    """
    # 找出相鄰的 1 進行化簡
    terms = []
    if a and b: terms.append('A\'')  # B 變化，A 不變
    if c and d: terms.append('A')   # B 變化，A 不變
    if a and c: terms.append('B\'') # A 變化，B 不變
    if b and d: terms.append('B')   # A 變化，B 不變
    return ' + '.join(terms) if terms else '0'
```

## 5. 從布林代數到硬體

布林代數的真值表可以直接映射為邏輯閘電路。每個 AND 對應一個 AND 閘，每個 OR 對應一個 OR 閘，每個 NOT 對應一個 NOT 閘。

這種映射關係是計算機設計的基礎——任何布林函式都可以用邏輯閘實作，任何計算都可以化約為布林函式。

## 6. 結語

二進位與布林代數看似簡單，但它們構成了整個數位世界的基礎。從最早的繼電器計算機到現代的量子電腦，二進位和布林代數始終是資訊科學的基石。理解這些基礎概念，是深入理解計算機組織與架構的第一步。

---

**下一步**：[邏輯閘與組合電路](article2.md)

## 延伸閱讀

- [Boolean Algebra Laws](https://www.google.com/search?q=Boolean+algebra+laws+theorems)
- [De Morgan's Theorem](https://www.google.com/search?q=De+Morgan's+theorem+explained)
- [Karnaugh Map Tutorial](https://www.google.com/search?q=Karnaugh+map+tutorial+simplification)
