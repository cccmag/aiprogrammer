# 量子 ML 硬體

## 從實驗室到資料中心（2020-2029）

### 量子硬體的技術路線

2020 年代，量子 ML 的硬體基礎主要來自四條技術路線：

| 技術 | 領先者 | 優勢 | 劣勢 |
|------|--------|------|------|
| 超導量子位元 | IBM, Google | 閘速度快 (ns) | 需極低溫 (15mK) |
| 離子阱 | IonQ, Quantinuum | 高保真度 (>99.9%) | 閘速度慢 (μs) |
| 光量子 | Xanadu, PsiQuantum | 室溫運作 | 難以擴展 |
| 中性原子 | QuEra, Harvard | 易於擴展 | 糾纏保真度低 |

### 量子位元數量與品質

對 ML 任務而言，量子位元數並非唯一指標：

```python
def quantum_volume(n_qubits: int, fidelity: float, depth: int) -> float:
    """量子體積：綜合衡量硬體能力"""
    effective_depth = min(depth, int(-1 / math.log2(fidelity)))
    return 2 ** min(n_qubits, effective_depth)
```

2023 年，IBM 發布了 1121 量子位元的 Condor 處理器。但對 ML 任務最有用的量子體積（不是量子位元數）在 2025 年左右達到約 10⁶。

### 雜訊與誤差校正

量子 ML 對雜訊特別敏感——訓練需要高精度的梯度估計：

1. **閘錯誤率**（2020-2029 年改善）
   - 2020: ~10⁻³（超導）
   - 2023: ~10⁻⁴（超導）
   - 2026: ~10⁻⁵（離子阱 > 超導）
   - 2029: ~10⁻⁶（surface code 校正）

2. **讀取錯誤**：當前約 1-5%，對 ML 訓練影響巨大。

### NISQ 與容錯時代

**NISQ（2020-2026）**：50-1000 量子位元，無完整誤差校正。VQA 和量子核方法在此階段主導。

**早期容錯（2026-2029）**：Google 和 IBM 展示了邏輯量子位元（由多個物理量子位元編碼而成）的可行性。2028 年，第一個 100 邏輯量子位元的處理器實現了低於物理閘的錯誤率。

### 專用量子 ML 硬體

2024-2025 年，出現了**針對量子 ML 任務優化的專用處理器**：

- **等時性量子處理單元**（Tensor Processing Unit 的類比）：硬體支援量子電路的特定拓撲
- **量子記憶體**：用量子重複器實現的量子 RAM（QRAM），允許隨機存取量子資料
- **量子感測器陣列**：直接從量子系統讀取資料，繞過經典感測-編碼的瓶頸

### 2029 年硬體供應商

目前主要的量子雲服務：
- **IBM Quantum Network**：100+ 量子位元，Strangefellows 架構
- **Google Quantum AI**：Sycamore 到 Willow 處理器
- **Amazon Braket**：多供應商聚合平台
- **Microsoft Azure Quantum**：聚焦離子阱和中性原子

硬體進步仍然是量子 ML 發展的最大制約——但趨勢明確：**量子硬體正沿著「類摩爾定律」的路徑每 2-3 年翻倍**。

---

**下一步**：[量子 ML 的未來](focus7.md)

## 延伸閱讀

- [IBM Quantum 路線圖](https://www.google.com/search?q=IBM+quantum+roadmap+2029)
- [Google Quantum AI Willow](https://www.google.com/search?q=Google+Willow+quantum+processor)
- [Surface Code 誤差校正](https://www.google.com/search?q=surface+code+quantum+error+correction)
