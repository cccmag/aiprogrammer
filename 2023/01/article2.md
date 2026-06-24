# 邏輯閘與組合電路

## 1. 引言

邏輯閘（Logic Gate）是數位電路的基本建構模組。每個邏輯閘實作一個簡單的布林函式，多個邏輯閘組合起來可以實作任意複雜的計算功能。本文將探討基本邏輯閘的原理與組合電路的設計方法。

## 2. 基本邏輯閘

### 2.1 七種基本邏輯閘

```python
class LogicGates:
    @staticmethod
    def AND(a, b): return a & b
    @staticmethod
    def OR(a, b): return a | b
    @staticmethod
    def NOT(a): return 1 - a
    @staticmethod
    def NAND(a, b): return 1 - (a & b)
    @staticmethod
    def NOR(a, b): return 1 - (a | b)
    @staticmethod
    def XOR(a, b): return a ^ b
    @staticmethod
    def XNOR(a, b): return 1 - (a ^ b)
```

### 2.2 真值表

以 XOR 閘為例：

```
A  B  |  A XOR B
0  0  |    0
0  1  |    1
1  0  |    1
1  1  |    0
```

### 2.3 邏輯閘的電晶體實作

在最底層，邏輯閘由電晶體（MOSFET）構成：

- **CMOS AND 閘**：NMOS 串聯 + PMOS 並聯 + NOT 閘
- **CMOS OR 閘**：NMOS 並聯 + PMOS 串聯 + NOT 閘
- **CMOS NOT 閘**：單一 PMOS + 單一 NMOS

## 3. 萬用閘

### 3.1 NAND 閘的通用性

NAND 閘被稱為「萬用閘」（Universal Gate），因為任何邏輯閘都可以用 NAND 閘構成：

```python
def NOT_from_NAND(a):
    return LogicGates.NAND(a, a)

def AND_from_NAND(a, b):
    return NOT_from_NAND(LogicGates.NAND(a, b))

def OR_from_NAND(a, b):
    return LogicGates.NAND(NOT_from_NAND(a), NOT_from_NAND(b))
```

NOR 閘同樣是萬用閘。這個性質在積體電路設計中非常重要——如果只需要一種閘，製造流程可以大幅簡化。

## 4. 組合電路

### 4.1 組合電路的特性

組合電路（Combinational Circuit）的輸出只取決於當前的輸入，沒有記憶功能。這是與循序電路（Sequential Circuit）的根本區別。

### 4.2 多工器（Multiplexer）

多工器根據選擇信號從多個輸入中選擇一個輸出：

```python
class Mux:
    @staticmethod
    def mux_2to1(sel, a, b):
        """2-to-1 多工器"""
        return (a & (1 - sel)) | (b & sel)

    @staticmethod
    def mux_4to1(sel, inputs):
        """4-to-1 多工器"""
        s0, s1 = sel >> 0 & 1, sel >> 1 & 1
        mux0 = Mux.mux_2to1(s0, inputs[0], inputs[1])
        mux1 = Mux.mux_2to1(s0, inputs[2], inputs[3])
        return Mux.mux_2to1(s1, mux0, mux1)
```

多工器在 CPU 的資料路徑中廣泛應用——例如選擇 ALU 的輸入來源（暫存器或立即數）。

### 4.3 解碼器（Decoder）

解碼器將 n 位元輸入轉換為 2ⁿ 位元輸出，只有一個輸出為 1：

```python
def decoder_2to4(inp):
    """2-to-4 解碼器"""
    a, b = inp >> 0 & 1, inp >> 1 & 1
    return [
        LogicGates.AND(LogicGates.NOT(a), LogicGates.NOT(b)),  # 00
        LogicGates.AND(LogicGates.NOT(a), b),                  # 01
        LogicGates.AND(a, LogicGates.NOT(b)),                  # 10
        LogicGates.AND(a, b),                                  # 11
    ]
```

解碼器用於記憶體位址解碼和指令解碼。

### 4.4 編碼器（Encoder）

編碼器將 2ⁿ 位元輸入轉換為 n 位元輸出，是解碼器的反向操作。

## 5. 組合電路設計流程

### 5.1 標準設計步驟

1. **規格定義**：確定輸入和輸出
2. **真值表**：列出所有輸入組合對應的輸出
3. **布林表達式**：從真值表推導布林表達式
4. **化簡**：使用布林代數或卡諾圖化簡
5. **電路實現**：將化簡後的表達式映射為邏輯閘

### 5.2 設計範例：1 位元比較器

```python
def comparator_1bit(a, b):
    """1 位元比較器：回傳 (eq, lt, gt)"""
    eq = LogicGates.XNOR(a, b)
    lt = LogicGates.AND(LogicGates.NOT(a), b)
    gt = LogicGates.AND(a, LogicGates.NOT(b))
    return eq, lt, gt
```

## 6. 傳播延遲與時序

組合電路有一個重要的非功能性特性：傳播延遲（Propagation Delay）。

每個邏輯閘都需要一定的時間才能根據輸入變化產生正確的輸出。多級邏輯閘的總延遲是所有級聯閘延遲之和：

```
總延遲 = Σ(每級邏輯閘的延遲)
```

傳播延遲決定了電路可以運作的最大時脈頻率。

## 7. 結語

邏輯閘是數位世界的原子單位。從簡單的 AND/OR 閘到複雜的 CPU，所有數位電路都是邏輯閘的組合。理解邏輯閘的原理和組合電路的設計方法，是深入學習計算機組織與架構的必經之路。

---

**下一步**：[加法器與 ALU 實作](article3.md)

## 延伸閱讀

- [Digital Logic Gates Tutorial](https://www.google.com/search?q=digital+logic+gates+tutorial)
- [CMOS Gate Design](https://www.google.com/search?q=CMOS+logic+gate+design)
- [Combinational vs Sequential Circuits](https://www.google.com/search?q=combinational+vs+sequential+circuits)
