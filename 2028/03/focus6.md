# RAG 評估與監控（2023-2028）

## 評估為什麼重要？

RAG 系統有多個組件：檢索器、排序器、生成器。任一環節出錯都會影響最終結果。需要端到端評估與組件級評估。

## 核心指標

### 檢索評估
| 指標 | 說明 |
|------|------|
| Hit Rate | 相關文檔是否被召回 |
| MRR | 第一個相關結果的排名 |
| NDCG | 排序品質加權評估 |

### 生成評估
| 指標 | 說明 |
|------|------|
| Faithfulness | 回答是否忠於檢索結果 |
| Relevance | 回答是否相關 |
| Correctness | 事實準確性 |

```python
# RAGAS 評估框架 (簡化)
def evaluate_rag(questions, answers, contexts):
    scores = {}
    for q, a, ctx in zip(questions, answers, contexts):
        scores[q] = {
            "faithfulness": faithfulness_score(a, ctx),
            "relevance": relevance_score(a, q),
            "context_precision": context_precision(ctx, q),
        }
    return scores
```

## 評估框架演進

2023 年 RAGAS 首個專用評估框架誕生。2024 年 TruLens 加入鏈追蹤。2025 年 LangSmith 與 Weights & Biases 提供生產級監控。2026 年自動化回歸測試。2027 年即時評估與告警。2028 年可解釋評估。

## 生產監控

```python
def monitor_pipeline(query, response, latency):
    metrics = {
        "retrieval_time": latency["retrieval"],
        "generation_time": latency["generation"],
        "total_latency": latency["total"],
        "context_length": len(response["context"]),
        "has_hallucination": detect_hallucination(
            response["answer"], response["context"]
        ),
    }
    log_metrics(metrics)
    if metrics["has_hallucination"] > 0.3:
        alert("Hallucination rate too high!")
```

## 延伸閱讀

- [RAGAS 評估框架](https://www.google.com/search?q=RAGAS+retrieval+augmented+generation+evaluation)
- [TruLens RAG 監控](https://www.google.com/search?q=TruLens+RAG+evaluation+monitoring)
- [RAG 生產監控最佳實踐](https://www.google.com/search?q=RAG+production+monitoring+best+practices+2026)

---

*本篇文章為「AI 程式人雜誌 2028 年 3 月號」焦點系列之六。*
