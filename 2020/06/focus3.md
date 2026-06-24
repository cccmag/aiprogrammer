# 3. 規模法則與湧現能力

## 規模法則 (Scaling Laws)

OpenAI 的研究發現，語言模型的效能可以透過以下公式預測：

```
Loss ~ N^(-0.076) + D^(-0.095) + C^(-0.050)
```

其中：
- N = 參數數量
- D = 訓練資料 tokens 數量
- C = 計算量（FLOPs）

這意味著，只要持續增加模型規模、資料量與計算量，效能就能可預測地提升。

## Power Laws 圖示

實驗結果顯示：
- Loss 與 N、D、C 呈現平滑的冪律關係
- 增加任一因素都能提升效能
- 三者存在可互換性（可以用更多資料彌補較小的模型）

## 湧現能力 (Emergent Abilities)

當模型規模超過某個閾值時，會突然展現出此前小型模型無法展現的能力：

| 能力 | 湧現規模 |
|------|---------|
| 3-digit 加法 | ~10B 參數 |
| 詞典解釋 | ~10B 參數 |
| 執行多步推理 | ~100B 參數 |
| 抗干擾能力 | ~100B 參數 |

這種「湧現」現象使得大型語言模型的能力評估變得困難，因為小模型的失敗不代表大模型也會失敗。

## 規模與 Few-shot 能力

GPT-3 的實驗顯示，Few-shot 能力隨模型規模增長而顯著提升：

- 小型模型（< 1B）：Few-shot 效果有限
- 中型模型（1-10B）：開始展現 Few-shot 能力
- 大型模型（> 10B）：Few-shot 能力顯著
- GPT-3（175B）：Few-shot 能力達到頂尖水準

## 規模法則的爭議

也有研究者對規模法則提出批評：

1. **收益遞減**：規模法則預測最終會遇到瓶頸
2. **湧現不可預測**：無法預測何種能力會在何規模湧現
3. **環境影響**：訓練大型模型的碳足跡驚人
4. **規模不等於智慧**：更大的模型不等於真正的理解

## 規模的代價

| 規模 | 訓練成本 | 記憶體需求 |
|------|---------|-----------|
| 1B | ~$10,000 | ~4GB |
| 10B | ~$100,000 | ~40GB |
| 100B | ~$1,000,000 | ~400GB |
| 175B | ~$12,000,000 | ~800GB |

## 參考資源

- https://www.google.com/search?q=GPT-3+scaling+laws+Kaplan+OpenAI+emergent+abilities+2020
- https://www.google.com/search?q=language+model+scaling+laws+compute+data+efficiency+power+law
- https://www.google.com/search?q=emergent+capabilities+large+language+models+scale+threshold+prediction