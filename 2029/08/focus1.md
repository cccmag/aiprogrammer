# 量子 ML 導論

## 量子計算與機器學習的交叉（2014-2029）

### 為什麼需要量子機器學習？

2014 年，物理學家 **Seth Lloyd** 提出了量子機器學習的基本框架。他發現量子計算機在處理高維特徵空間時，擁有經典計算機難以比擬的優勢——**量子平行性**允許量子位元同時表示多個狀態，這對機器學習中的線性代數運算至關重要。

量子 ML 的核心問題是：**量子計算能否在機器學習任務上提供指數級加速？**

### 量子資訊的基礎

一個量子位元（qubit）的狀態可以表示為：

```python
import math, random, cmath

class Qubit:
    def __init__(self):
        self.alpha = 1.0 + 0j  # |0⟩ 的振幅
        self.beta = 0.0 + 0j   # |1⟩ 的振幅
    
    def measure(self) -> int:
        prob0 = abs(self.alpha)**2
        return 0 if random.random() < prob0 else 1
```

量子狀態 |ψ⟩ = α|0⟩ + β|1⟩，其中 |α|² + |β|² = 1。測量時坍縮到 |0⟩ 或 |1⟩——這與經典機率不同：量子振幅可以互相干涉，產生經典機率無法表達的相關性。

### 從 Hadamard 到糾纏

```python
class Qubit:
    def apply_hadamard(self):
        self.alpha, self.beta = (
            (self.alpha + self.beta) / math.sqrt(2),
            (self.alpha - self.beta) / math.sqrt(2),
        )
```

Hadamard 閘是量子 ML 的基礎操作——它將 |0⟩ 轉換為 (|0⟩ + |1⟩)/√2，創造疊加態。結合 CNOT 閘可以產生糾纏態：|00⟩ + |11⟩，這是量子計算優於經典計算的核心資源。

### 量子 ML 的分類

1. **變分量子演算法（2018）**：參數量子電路 + 經典優化
2. **量子核方法（2019）**：用量子狀態內積取代經典核函數
3. **量子神經網路（2020）**：量子版的深度學習

### 2029 年的現狀

量子 ML 尚未實現公認的量子霸權，但已經在以下方面展示潛力：
- 小分子模擬的資料生成
- 高能物理中的事件分類
- 量子誤差校正的解碼器

最重要的認識是：**近期的量子 ML 將是混合的**——量子處理器處理特定運算，經典計算機負責其餘部分。

---

**下一步**：[變分量子演算法](focus2.md)

## 延伸閱讀

- [Seth Lloyd 的量子 ML 論文](https://www.google.com/search?q=Seth+Lloyd+quantum+machine+learning+2014)
- [量子計算入門](https://www.google.com/search?q=quantum+computing+introduction+tutorial)
- [Quantum ML 綜述 2025](https://www.google.com/search?q=quantum+machine+learning+survey+2025)
