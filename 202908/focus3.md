# 量子核方法

## 在希爾伯特空間中尋找模式（2019-2029）

### 核技巧的量子版本

經典核方法（如 SVM）的核心是將資料映射到高維特徵空間，然後計算內積。2019 年，**量子核方法**提出一個大膽的想法：**用量子態的內積來取代經典核函數**。

量子核的定義：

```python
class QuantumKernel:
    def similarity(self, x: list[float], y: list[float]) -> float:
        dot = sum(a * b for a, b in zip(x, y))
        n_x = math.sqrt(sum(a*a for a in x))
        n_y = math.sqrt(sum(b*b for b in y))
        return math.exp(-0.5 * (1 - dot / (n_x * n_y + 1e-10)))
```

### 為什麼量子核可能更好？

**經典核函數**（如 RBF）對應到一個固定的、由核函數隱含定義的特徵空間。**量子核**則可以根據量子電路的設計，產生經典計算難以有效模擬的特徵空間。

```python
def quantum_kernel_estimation(x, y, circuit):
    """用量子電路估計 |⟨φ(x)|φ(y)⟩|²"""
    # 將 x, y 編碼到量子態
    circuit.encode(x)
    circuit.encode_dagger(y)
    # 測量全 |0⟩ 的機率 = 量子核的值
    return circuit.measure_zero_probability()
```

### 量子優勢的證據

2021 年，理論研究證明了某些學習任務存在**量子優勢**——經典核方法需要指數級更多的資料或計算才能達到相同的準確率。這為量子 ML 提供了理論基礎。

然而，**2023 年的重要論文指出**：如果將經典資料用經典特徵映射預處理，很多號稱量子優勢的任務可以被經典方法匹配。量子核方法的優勢局限於特定的、高結構化的問題。

### 量子核 vs. 變分量子電路

| 特性 | 量子核方法 | 變分量子電路 |
|------|-----------|-------------|
| 訓練方式 | 解析核矩陣 + 經典 SVM | 梯度下降優化電路參數 |
| 量子部分 | 僅用於計算核 | 全程使用量子電路 |
| 理論保證 | VC 維度理論清晰 | 缺乏泛化理論 |
| 可擴展性 | 核矩陣 O(N²) 開銷 | 線性迭代 |

### 2029 年的進展

量子核方法在以下領域展現潛力：
- **量子化學資料**：分子性質預測，量子核自然匹配問題結構
- **高能物理**：LHC 事件分類，量子核有效捕捉高維相關性
- **組合最佳化**：圖資料的量子核嵌入

關鍵突破來自**誤差緩解核估計**（2025），使當前量子裝置上的核估計誤差降低到可接受範圍。

---

**下一步**：[量子神經網路](focus4.md)

## 延伸閱讀

- [量子核方法綜述](https://www.google.com/search?q=quantum+kernel+methods+review)
- [量子優勢理論（2021）](https://www.google.com/search?q=quantum+advantage+kernel+methods+2021)
- [Error-mitigated kernel methods](https://www.google.com/search?q=error+mitigated+quantum+kernel+methods)
