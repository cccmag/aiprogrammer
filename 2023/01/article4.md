# 正反器與循序電路

## 1. 引言

組合電路的輸出只取決於當前的輸入，沒有記憶功能。但計算機需要儲存狀態——暫存器需要記住資料，計數器需要追蹤數值，CPU 需要記住目前執行到哪條指令。

循序電路（Sequential Circuit）透過回饋迴路實現狀態儲存。正反器（Flip-Flop）是最基本的循序電路元件。

## 2. 鎖存器

### 2.1 SR 鎖存器

SR 鎖存器（Set-Reset Latch）是最基本的記憶電路：

```python
class SRLatch:
    def __init__(self):
        self.q = 0
        self.qn = 1

    def clock(self, s, r):
        if s == 1 and r == 0:
            self.q, self.qn = 1, 0    # Set
        elif s == 0 and r == 1:
            self.q, self.qn = 0, 1    # Reset
        elif s == 0 and r == 0:
            pass                       # Hold
        else:  # s == 1 and r == 1
            self.q, self.qn = 0, 0    # Invalid
```

### 2.2 D 型鎖存器

D 型鎖存器（Data Latch）只有一個資料輸入：

```python
class DLatch:
    def __init__(self):
        self.q = 0

    def clock(self, d, enable):
        if enable:
            self.q = d
```

## 3. 邊緣觸發正反器

### 3.1 D 型正反器

D 型正反器（D Flip-Flop）只在時脈的上升邊緣（或下降邊緣）取樣輸入：

```python
class DFlipFlop:
    def __init__(self):
        self.q = 0
        self.last_clk = 0

    def clock(self, d, clk):
        # 檢測上升邊緣
        if clk == 1 and self.last_clk == 0:
            self.q = d
        self.last_clk = clk
```

相比鎖存器，邊緣觸發正反器可以避免「穿通」（Transparency）問題。

### 3.2 JK 正反器

JK 正反器解決了 SR 正反器的無效狀態問題：

```python
class JKFlipFlop:
    def __init__(self):
        self.q = 0
        self.last_clk = 0

    def clock(self, j, k, clk):
        if clk == 1 and self.last_clk == 0:
            if j == 0 and k == 0:
                pass           # Hold
            elif j == 0 and k == 1:
                self.q = 0     # Reset
            elif j == 1 and k == 0:
                self.q = 1     # Set
            else:
                self.q = 1 - self.q  # Toggle
        self.last_clk = clk
```

### 3.3 T 型正反器

T 型正反器（Toggle Flip-Flop）在每個時脈邊緣翻轉狀態：

```python
class TFlipFlop:
    def __init__(self):
        self.q = 0
        self.last_clk = 0

    def clock(self, t, clk):
        if clk == 1 and self.last_clk == 0:
            if t == 1:
                self.q = 1 - self.q
        self.last_clk = clk
```

T 型正反器是建構計數器的理想元件。

## 4. 暫存器

### 4.1 n 位元暫存器

將 n 個 D 型正反器並聯，共用同一個時脈信號：

```python
class Register:
    def __init__(self, bits=8):
        self.bits = bits
        self.flip_flops = [DFlipFlop() for _ in range(bits)]
        self.last_clk = 0

    def load(self, data, clk):
        if clk == 1 and self.last_clk == 0:
            for i in range(self.bits):
                d = (data >> i) & 1
                self.flip_flops[i].clock(d, clk)
        self.last_clk = clk

    def read(self):
        result = 0
        for i in range(self.bits):
            result |= (self.flip_flops[i].q << i)
        return result
```

## 5. 計數器

### 5.1 漣波計數器

使用 T 型正反器的級聯：

```python
class RippleCounter:
    def __init__(self, bits=4):
        self.bits = bits
        self.ffs = [TFlipFlop() for _ in range(bits)]

    def clock(self, clk):
        prev = clk
        for ff in self.ffs:
            ff.clock(1, prev)
            prev = ff.q

    def value(self):
        v = 0
        for i, ff in enumerate(self.ffs):
            v |= (ff.q << i)
        return v
```

## 6. 有限狀態機

### 6.1 狀態機模型

有限狀態機（FSM）由三個部分組成：
- **狀態暫存器**：儲存當前狀態
- **下一狀態邏輯**：根據當前狀態和輸入計算下一狀態
- **輸出邏輯**：根據當前狀態（和輸入）計算輸出

### 6.2 設計範例：交通號誌控制器

```python
class TrafficLightFSM:
    STATES = ['GREEN', 'YELLOW', 'RED']
    def __init__(self):
        self.state = 0  # 0: GREEN, 1: YELLOW, 2: RED

    def clock(self, car_detected):
        if self.state == 0:  # GREEN
            if not car_detected:
                self.state = 1  # → YELLOW
        elif self.state == 1:  # YELLOW
            self.state = 2      # → RED
        elif self.state == 2:  # RED
            self.state = 0      # → GREEN
        return self.STATES[self.state]
```

## 7. 結語

正反器和循序電路是計算機中記憶功能的基礎。從單個 D 型正反器到 64 位元暫存器，從簡單計數器到複雜的有限狀態機——循序電路的應用無處不在。

在計算機組織中，循序電路用於建構：
- 暫存器檔案（Register File）
- 程式計數器（Program Counter）
- 管線暫存器（Pipeline Registers）
- 控制單元的狀態機

---

**下一步**：[管線化冒險與解決](article5.md)

## 延伸閱讀

- [Flip-Flop Types: SR, D, JK, T](https://www.google.com/search?q=SR+D+JK+T+flip+flop+difference)
- [Finite State Machine Design](https://www.google.com/search?q=finite+state+machine+design+tutorial)
- [Sequential Logic Circuits](https://www.google.com/search?q=sequential+logic+circuits+explained)
