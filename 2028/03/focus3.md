# 多跳檢索與推理（2023-2028）

## 什麼是多跳推理？

單跳檢索：問「Transformer 使用什麼機制？」→ 檢索 Transformer 文檔 →「Attention」。

多跳檢索：問「BERT 用什麼機制？誰發明的？」→ 需要 BERT → Transformer → Attention 三跳。

```
BERT ──based_on──> Transformer ──uses──> Attention
```

## 多跳檢索挑戰

1. **組合爆炸**：每跳可擴展到多個節點，搜索空間指數增長
2. **信號衰減**：距離越遠的資訊相關性越低
3. **終止條件**：何時停止搜尋？

## Beam Search 多跳檢索

```python
def multi_hop_retrieve(query, kg, beam_size=3, max_hops=3):
    # 初始實體
    current = [e for e in kg.entities
               if query.lower() in e.name.lower()]
    paths = [[e] for e in current]

    for hop in range(max_hops):
        candidates = []
        for path in paths:
            last = path[-1]
            for neighbor in kg.get_neighbors(last.id):
                score = kg.entities[neighbor].weight
                candidates.append((path + [neighbor], score))
        # Beam selection
        candidates.sort(key=lambda x: -x[1])
        paths = [p for p, _ in candidates[:beam_size]]
    return paths
```

## 2024-2028 演進

2024 年 IRCoT（Interleaving Retrieval and CoT）交替檢索與推理。2025 年 ReAct 模式將推理與行動結合。2026 年 Tree-of-Thought 搜尋多條推理路徑。2027 年 Graph-of-Thought 在圖譜上推理。2028 年自我反思式多跳檢索。

## 實際應用

- 法律案件推理：從法條→判例→事實
- 醫療診斷：從症狀→疾病→治療方案
- 科學研究：從論文→方法→實驗結果

## 延伸閱讀

- [IRCoT 交錯檢索推理](https://www.google.com/search?q=IRCoT+Interleaving+Retrieval+CoT+2024)
- [ReAct 推理行動模式](https://www.google.com/search?q=ReAct+reasoning+acting+2023)
- [Tree-of-Thought 推論](https://www.google.com/search?q=Tree+of+Thought+prompting+2023)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之三。*
