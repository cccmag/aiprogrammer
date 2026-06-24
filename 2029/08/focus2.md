# 變分量子演算法

## 參數量子電路與經典優化的協同（2018-2029）

### VQA 的基本思想

2018 年，**變分量子演算法**（Variational Quantum Algorithm, VQA）成為 NISQ（含雜訊中等規模量子）時代的主流範式。核心想法很簡單：**用量子電路計算損失函數，用經典計算機優化參數**。

VQA 的通用架構：

```python
import math, random

class VariationalQuantumCircuit:
    def __init__(self, n_qubits: int = 2):
        self.params = [random.uniform(0, 2*math.pi)
                       for _ in range(n_qubits)]
    
    def forward(self, x: list[float]) -> list[int]:
        for angle in self.params:
            p0 = math.cos(angle / 2)**2
            # 基於參數的旋轉編碼
        return self.measure_all()
```

### VQE：變分量子特徵值求解器

VQE 是 VQA 最早的成功案例。它被用來估計化學分子的基態能量——這對量子化學至關重要。

```python
def vqe_cost(params, hamiltonian):
    """計算期望值 ⟨ψ(θ)|H|ψ(θ)⟩"""
    circuit = VariationalQuantumCircuit(4)
    state = circuit.run(params)
    return sum(obs * prob for obs, prob in zip(hamiltonian, state))
```

與經典計算相比，VQE 需要的量子位元數遠少於完全量子模擬，使其成為 NISQ 裝置的理想候選。

### 資料重新上傳（Data Re-uploading）

2019-2020 年間，研究發現**資料重新上傳**可以顯著提升 VQC 的表達能力。不是一次性地將資料編碼到量子態，而是在多層電路中重複編碼：

```python
def data_reuploading_circuit(x, params, depth=3):
    for d in range(depth):
        # 編碼層：將 x 映射到量子態
        for i, xi in enumerate(x):
            apply_rotation(i, xi * params[d][i])
        # 糾纏層：創造量子相關性
        apply_entangling_layer()
```

這使得 VQC 能近似任意的量子運算，類似於經典神經網路的通用近似定理。

### VQA 的挑戰

1. **荒原高原（Barren Plateau）**：當電路深度足夠大時，梯度指數級消失，使隨機參數無法有效優化。2021 年理論證明了這個問題的結構性本質。
2. **測量開銷**：量子測量是機率性的，需要大量取樣才能獲得精確期望值。
3. **雜訊累積**：當前量子硬體的閘錯誤率約 0.1-1%，限制了電路深度。

### 2029 年的 VQA

當前最先進的 VQA 方案結合了**誤差緩解技術**和**層級訓練策略**。IBM 和 Google 的量子處理器在 100+ 量子位元規模上成功演示了小分子模擬。VQA 仍是量子 ML 最實用的框架。

---

**下一步**：[量子核方法](focus3.md)

## 延伸閱讀

- [VQE 論文（2014）](https://www.google.com/search?q=variational+quantum+eigensolver+VQE)
- [資料重新上傳](https://www.google.com/search?q=data+re-uploading+quantum+circuit)
- [Barren Plateau 理論](https://www.google.com/search?q=barren+plateau+variational+quantum+algorithm)
