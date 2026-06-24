# 計算機架構模擬器

## 概述

本期的程式專案是一個用 Python 實作的計算機架構模擬器。它模擬了計算機組織與架構中的四個核心概念：

1. **ALU 運算**——算術邏輯單元的加法、減法、AND、OR、XOR 等運算
2. **管線階段**——五階級管線（IF、ID、EX、MEM、WB）的執行模擬
3. **快取模擬**——直接映射快取的讀寫行為與命中率統計
4. **CPI 計算**——基於指令混合比例的 CPI 與執行時間估算

## 核心實作

### 1. ALU 模擬

```python
class ALU:
    def execute(self, op: str, a: int, b: int) -> int:
        ops = {
            'ADD': lambda: a + b,
            'SUB': lambda: a - b,
            'AND': lambda: a & b,
            'OR':  lambda: a | b,
            'XOR': lambda: a ^ b,
            'MUL': lambda: a * b,
        }
        return ops[op]()
```

ALU 是 CPU 的計算核心，負責執行所有算術和邏輯運算。現代 ALU 還支援移位、比較和位元操作。

### 2. 五階級管線模擬

管線化的核心概念是將指令執行分解為五個階段，每個階段由獨立的硬體單元處理：

| 階段 | 名稱 | 功能 |
|------|------|------|
| IF | 指令提取 | 從記憶體讀取指令 |
| ID | 指令解碼 | 解析指令與讀取暫存器 |
| EX | 執行 | ALU 運算或位址計算 |
| MEM | 記憶體存取 | 資料記憶體讀寫 |
| WB | 寫回 | 結果寫回暫存器 |

模擬器每時脈週期讓一個階段的指令前進，並追蹤每個指令的完成週期。

### 3. 快取模擬

採用直接映射快取（Direct-mapped cache）設計：

```python
class Cache:
    def __init__(self, size=1024, block_size=64):
        self.blocks = [None] * (size // block_size)
        self.hits = self.misses = 0

    def read(self, address):
        idx = (address // self.block_size) % len(self.blocks)
        tag = address // (self.block_size * len(self.blocks))
        if self.blocks[idx] == tag:
            self.hits += 1
            return True
        self.blocks[idx] = tag
        self.misses += 1
        return False
```

快取利用時間局部性（temporal locality）和空間局部性（spatial locality）來加速記憶體存取。

### 4. CPI 計算

CPI（Cycles Per Instruction）是衡量處理器效能的重要指標：

```
CPI = Σ(指令比例 × 該指令類型的 CPI)
CPU 時間 = 指令數 × CPI × 時脈週期
```

模擬器支援不同指令類型的混合比例計算，並展示 Amdahl 定律的影響。

## 執行結果

```
=== ALU Operations ===
ADD(10, 20) = 30
SUB(10, 20) = -10
AND(10, 20) = 0
OR(10, 20) = 30
XOR(10, 20) = 30
MUL(10, 20) = 200

=== Pipeline Simulation ===
Cycle   1: IF(inst0)
Cycle   2: IF(inst1)  ID(inst0)
Cycle   3: IF(inst2)  ID(inst1)  EX(inst0)
Cycle   4: IF(inst3)  ID(inst2)  EX(inst1)  MEM(inst0)
Cycle   5: IF(inst4)  ID(inst3)  EX(inst2)  MEM(inst1)  WB(inst0)
...

=== Cache Simulation ===
Hits: 5, Misses: 5, Hit rate: 50.0%

=== CPI Calculation ===
CPI: 1.94
Total instructions: 800

=== Amdahl's Law Demo ===
P=0.50, S=10: speedup=1.82
P=0.75, S=10: speedup=3.08
P=0.90, S=10: speedup=5.26
P=0.95, S=10: speedup=6.90
P=0.99, S=10: speedup=9.17
```

## 模擬器教會我們的事

### 1. 管線化不是免費的

雖然管線化可以提升吞吐量，但資料冒險、控制冒險和結構冒險會降低實際加速比。分支預測和轉發（forwarding）是解決這些問題的關鍵技術。

### 2. 快取的效能取決於存取模式

順序存取（sequential access）的快取命中率遠高於隨機存取（random access）。這正是為什麼程式設計中「遍歷陣列」比「隨機存取連結串列」更有效率。

### 3. CPI 不是固定的

不同類型指令的 CPI 不同——記憶體存取指令通常比暫存器指令需要更多週期。程式的指令混合比例直接影響整體效能。

### 4. Amdahl 定律無處不在

```
加速比 = 1 / ((1 - P) + P/S)
```

其中 P 是可平行化比例，S 是加速倍數。這告訴我們：效能的瓶頸總是來自於無法加速的部分。

---

## 延伸閱讀

- [完整程式碼](_code/computer_arch.py)
- [Computer Architecture Simulators](https://www.google.com/search?q=computer+architecture+simulator+python)
- [Gem5 模擬器](https://www.google.com/search?q=gem5+simulator)
- [SimpleScalar 工具集](https://www.google.com/search?q=SimpleScalar+simulator)
