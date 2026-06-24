# 加法器與 ALU 實作

## 1. 引言

ALU（Arithmetic Logic Unit）是 CPU 的計算核心。本文將從最基本的半加器出發，逐步建構完整的 ALU。這個過程展示了數位電路設計的核心思想：從簡單的元件開始，透過組合來建構複雜的系統。

## 2. 加法器

### 2.1 半加器（Half Adder）

半加器是最基本的加法電路，將兩個 1 位元數字相加：

```
A + B = Sum + Carry
   0 + 0 = 0 + 0
   0 + 1 = 1 + 0
   1 + 0 = 1 + 0
   1 + 1 = 0 + 1
```

```python
def half_adder(a, b):
    sum_bit = a ^ b       # XOR
    carry = a & b         # AND
    return sum_bit, carry
```

### 2.2 全加器（Full Adder）

全加器增加了進位輸入（Cin），可以串接實現多位元加法：

```python
def full_adder(a, b, cin):
    sum1 = a ^ b
    sum_bit = sum1 ^ cin
    carry = (a & b) | (cin & sum1)
    return sum_bit, carry
```

### 2.3 漣波進位加法器（Ripple Carry Adder）

將 n 個全加器串聯，每個全加器的進位輸出連接到下一位的進位輸入：

```python
def ripple_carry_adder(a, b, bits=4):
    result = 0
    carry = 0
    for i in range(bits):
        a_bit = (a >> i) & 1
        b_bit = (b >> i) & 1
        s, carry = full_adder(a_bit, b_bit, carry)
        result |= (s << i)
    return result, carry
```

**缺點**：高位元需要等待低位元的進位，延遲與位元數成正比。

### 2.4 超前進位加法器（Carry Lookahead Adder）

超前進位加法器透過預先計算進位來減少延遲：

```python
def carry_lookahead_adder(a, b, bits=4):
    generate = (a & b)    # Gi = Ai & Bi
    propagate = (a ^ b)   # Pi = Ai ^ Bi
    carry = [0] * (bits + 1)
    for i in range(bits):
        gi = (generate >> i) & 1
        pi = (propagate >> i) & 1
        carry[i+1] = gi | (pi & carry[i])
    result = propagate ^ (carry[0] << 0)
    for i in range(1, bits):
        ci = (carry[i] << i)
        result ^= ci
    carry_out = carry[bits]
    return result, carry_out
```

CLA 的延遲遠小於 RCA，但硬體複雜度更高。

## 3. ALU 實作

### 3.1 4 位元 ALU 設計

一個完整的 ALU 需要支援算術和邏輯運算：

```python
class ALU:
    OPS = {
        0: 'ADD', 1: 'SUB', 2: 'AND',
        3: 'OR',  4: 'XOR', 5: 'NOT A',
    }

    def __init__(self, bits=4):
        self.bits = bits
        self.flags = {'zero': False, 'carry': False, 'negative': False, 'overflow': False}

    def compute(self, opcode, a, b):
        mask = (1 << self.bits) - 1
        a, b = a & mask, b & mask
        if opcode == 0:  # ADD
            result, carry = ripple_carry_adder(a, b, self.bits)
        elif opcode == 1:  # SUB
            b_comp = ((~b) + 1) & mask
            result, carry = ripple_carry_adder(a, b_comp, self.bits)
        elif opcode == 2:  # AND
            result = a & b
            carry = 0
        elif opcode == 3:  # OR
            result = a | b
            carry = 0
        elif opcode == 4:  # XOR
            result = a ^ b
            carry = 0
        elif opcode == 5:  # NOT A
            result = (~a) & mask
            carry = 0
        else:
            result = 0
            carry = 0
        self.flags['zero'] = (result == 0)
        self.flags['carry'] = bool(carry)
        self.flags['negative'] = bool((result >> (self.bits-1)) & 1)
        self.flags['overflow'] = self.flags['carry'] ^ self.flags['negative']
        return result
```

### 3.2 狀態標誌的意義

- **Zero Flag**：結果為 0 時設為 1，用於條件分支
- **Carry Flag**：加法進位或減法借位，用於多精度運算
- **Negative Flag**：結果為負數（最高位元為 1），用於有號數比較
- **Overflow Flag**：有號數溢位，用於錯誤檢測

### 3.3 ALU 測試

```python
def test_alu():
    alu = ALU(4)
    # 測試加法：3 + 2 = 5
    r = alu.compute(0, 0b0011, 0b0010)
    assert r == 0b0101, f"3+2 should be 5, got {r}"
    # 測試 AND：1100 AND 1010 = 1000
    r = alu.compute(2, 0b1100, 0b1010)
    assert r == 0b1000, f"AND failed"
    # 測試 NOT：NOT 1010 = 0101
    r = alu.compute(5, 0b1010, 0)
    assert r == 0b0101, f"NOT failed"
    print("All ALU tests passed!")
```

## 4. 從 ALU 到 CPU

ALU 雖然是 CPU 的重要元件，但它只負責計算。完整的 CPU 還需要：
- 控制單元：解碼指令並產生控制信號
- 暫存器檔案：儲存運算元和中間結果
- 資料路徑：連接各元件的匯流排

在下一篇文章中，我們將探討正反器和循序電路——這是建構暫存器和控制單元的基礎。

## 5. 結語

從半加器到完整的 ALU，這個逐步建構的過程展示了數位電路設計的核心思想：抽象層次（Abstraction Layers）。每一個層次都隱藏了下層的複雜度，讓設計者可以專注於當前層次的問題。這也是計算機科學中最重要的設計原則之一。

---

**下一步**：[正反器與循序電路](article4.md)

## 延伸閱讀

- [Adder Circuits: Half, Full, Ripple, Lookahead](https://www.google.com/search?q=half+adder+full+adder+carry+lookahead)
- [ALU Design Tutorial](https://www.google.com/search?q=ALU+design+digital+logic+tutorial)
- [Carry Lookahead vs Ripple Carry](https://www.google.com/search?q=carry+lookahead+vs+ripple+carry+adder)
