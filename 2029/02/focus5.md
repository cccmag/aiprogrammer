# 合成資料品質評估（2022-2029）

## 如何衡量合成資料的好壞

合成資料品質評估是合成資料能否實際應用的關鍵。沒有嚴格的品質評估，合成資料只是華麗的垃圾。

### 核心評估維度

1. **忠實度（Fidelity）**：合成資料與真實資料的統計分布相似度。常用指標包括：Maximum Mean Discrepancy（MMD）、Wasserstein Distance、Precision & Recall（P&R）
2. **多樣性（Diversity）**：合成資料涵蓋的真實分布範圍。覆蓋率不足會導致模型過擬合於少數模式
3. **可用性（Utility）**：用合成資料訓練的模型在真實測試集上的表現

```python
# 簡單品質評估範例
from _code.synthetic_data import SyntheticDataGenerator
import random

gen = SyntheticDataGenerator()
real_labels = [random.choice(["pos", "neg"]) for _ in range(100)]
synth = gen.generate_text(100)
synth_labels = [r.label for r in synth]

label_dist_real = {l: real_labels.count(l) / 100 for l in ["pos", "neg"]}
label_dist_synth = {l: synth_labels.count(l) / 100 for l in ["pos", "neg"]}

for label in ["pos", "neg"]:
    diff = abs(label_dist_real[label] - label_dist_synth[label])
    print(f"{label}: 真實={label_dist_real[label]:.2f} 合成={label_dist_synth[label]:.2f} 差異={diff:.2f}")
```

### 自動化評估工具

2024 年後出現多個評估框架：
- **SynthEval**：整合 Fidelity、Diversity、Utility 三大維度
- **DataEval**：Google 開源的合成資料評估函式庫
- **LLM-as-Judge**：用 LLM 評估 LLM 生成的合成文字品質

### 2025-2029：語義評估時代

傳統統計指標無法捕捉語義差異。2025 年後語義評估成為主流：
- **Semantic MMD**：在 Embedding 空間計算分布距離
- **LLM-based Factuality**：檢查合成內容的事實正確性
- **Adversarial Validation**：訓練分類器區分合成與真實資料

### 實務建議

- 先跑小規模品質評估，再進行大規模合成
- 使用多種評估指標，不要只看單一數字
- 保留驗證集，定期監控合成資料的品質漂移

## 延伸閱讀

- [Synthetic data quality evaluation 2024](https://www.google.com/search?q=synthetic+data+quality+evaluation+fidelity+diversity+utility)
- [SynthEval framework 2025](https://www.google.com/search?q=SynthEval+synthetic+data+evaluation+framework)
- [Semantic evaluation synthetic data 2025](https://www.google.com/search?q=semantic+evaluation+synthetic+data+embedding)
