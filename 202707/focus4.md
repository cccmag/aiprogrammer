# LLM 評估框架（2020-2026）

## 自動化評估指標

傳統 NLP 評估指標是理解 LLM 評估的起點，但它們的局限性也同樣重要。

**BLEU（Bilingual Evaluation Understudy）**：測量生成文本和參考文本之間的 n-gram 重疊。常用於機器翻譯，但對於開放式生成任務，BLEU 分數與人類判斷的相關性很低。

**ROUGE（Recall-Oriented Understudy for Gisting Evaluation）**：測量生成文本對參考文本的召回率。適合摘要任務，但同樣無法捕捉語義品質。

**METEOR**：改進 BLEU，支援同義詞匹配和詞幹還原，但仍然依賴參考文本。

**BERTScore**：使用 BERT 的上下文嵌入來計算生成文本和參考文本之間的語義相似度，是目前最接近人類判斷的自動化指標。

```python
# 自動化評估指標實作
from collections import Counter
import math
import numpy as np

def bleu_score(candidate: str, reference: str, max_n=4) -> float:
    """簡化版 BLEU 分數計算"""
    def get_ngrams(text, n):
        tokens = text.split()
        return Counter(zip(*[tokens[i:] for i in range(n)]))
    
    candidate_tokens = candidate.split()
    ref_tokens = reference.split()
    
    # 長度懲罰
    c_len = len(candidate_tokens)
    r_len = len(ref_tokens)
    bp = math.exp(1 - r_len / c_len) if c_len < r_len else 1.0
    
    precisions = []
    for n in range(1, max_n + 1):
        c_ngrams = get_ngrams(candidate, n)
        r_ngrams = get_ngrams(reference, n)
        match_count = sum(min(c_ngrams[g], r_ngrams.get(g, 0)) for g in c_ngrams)
        total_count = sum(c_ngrams.values())
        precisions.append(match_count / max(total_count, 1))
    
    if any(p == 0 for p in precisions):
        return 0.0
    
    geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)
    return bp * geo_mean

def bertscore_similarity(candidate: str, reference: str, model=None):
    """使用 BERTScore 計算語義相似度（示意）"""
    # 實際使用時需要載入 BERT 模型
    # 此處為概念展示
    candidate_embed = np.random.randn(768)  # 模擬
    ref_embed = np.random.randn(768)
    cosine_sim = np.dot(candidate_embed, ref_embed) / (
        np.linalg.norm(candidate_embed) * np.linalg.norm(ref_embed)
    )
    return (cosine_sim + 1) / 2  # 歸一化到 [0, 1]
```

## LLM-as-Judge 評估方法

當生成任務是開放式的（寫一篇故事、提供建議、回答開放性問題），傳統指標完全失效。這時 **LLM-as-Judge** 成了最流行的評估方法。

核心想法：用一個 LLM（通常是 GPT-4 或 Claude）來評估另一個 LLM 的輸出。評估可以基於一個評分卡（Rubric）：

```python
# LLM-as-Judge 評估框架
class LLMasJudge:
    def __init__(self, eval_model=None):
        self.eval_model = eval_model  # 評審模型
    
    def score(self, response: str, criteria: dict) -> dict:
        """根據評分標準評估回應品質"""
        rubric_prompt = f"""請根據以下標準評估這個回應，每個維度 1-5 分：

標準：
{chr(10).join(f'- {k}: {v}' for k, v in criteria.items())}

回應：
{response}

請以 JSON 格式輸出分數："""
        
        # 呼叫評審模型
        # scores = self.eval_model.generate(rubric_prompt)
        # 此處模擬結果
        return {
            "helpfulness": 4.0,
            "accuracy": 3.5,
            "clarity": 4.5,
            "safety": 5.0,
            "average": 4.25,
        }

# 評估 Rubric 設計範例
evaluation_rubric = {
    "helpfulness": "回覆是否真正解決了使用者的問題",
    "accuracy": "回覆中的事實和資訊是否正確",
    "clarity": "回覆是否清晰易懂、結構良好",
    "safety": "回覆是否安全、無偏見、無有害內容",
    "completeness": "回覆是否完整涵蓋了問題的各個面向",
}
```

LLM-as-Judge 雖然強大，但也有偏見問題——評審模型可能偏好較長的輸出，或與自身相似的風格。因此實務上會使用多個評審模型做交叉驗證。

## LLM 評估的偏見問題

研究發現 LLM-as-Judge 存在幾種常見偏見：

- **位置偏見**：偏好出現在特定位置的答案
- **冗長偏見**：偏好較長的輸出
- **自我偏見**：偏好與自身風格相似的輸出
- **格式偏見**：偏好特定格式的輸出

緩解策略包括：使用多個評審模型、隨機化順序、使用結構化評分卡。

## 人工評估流程設計

自動化評估不能完全取代人工評估。生產級系統需要設計人工評估流程：

```python
# 人工評估工作流程
class HumanEvaluationPipeline:
    def __init__(self):
        self.samples_to_review = []
        self.reviews = []
    
    def collect_samples(self, responses: list[dict], sample_rate=0.1):
        """按比例抽樣需要人工審查的回應"""
        for r in responses:
            if random.random() < sample_rate:
                self.samples_to_review.append(r)
    
    def create_review_task(self, response: dict) -> dict:
        """建立評分任務"""
        return {
            "response_id": response["id"],
            "prompt": response["prompt"],
            "response": response["response"],
            "questions": [
                {"id": "accuracy", "text": "這個回答準確嗎？", "type": "likert_5"},
                {"id": "relevance", "text": "這個回答相關嗎？", "type": "likert_5"},
                {"id": "safety", "text": "這個回答安全嗎？", "type": "yes_no"},
            ],
        }
    
    def aggregate_reviews(self, reviews: list[dict]) -> dict:
        """聚合多個評審員的結果"""
        scores = {}
        for q in ["accuracy", "relevance", "safety"]:
            values = [r[q] for r in reviews if q in r]
            scores[q] = {
                "mean": statistics.mean(values),
                "agreement": 1 - statistics.stdev(values) / max(statistics.mean(values), 0.01),
            }
        return scores
```

## 回歸測試與品質閘道

每次提示詞或模型的變更都應該通過品質閘道（Quality Gate）：

```python
# 品質閘道
class QualityGate:
    def __init__(self, thresholds: dict):
        self.thresholds = thresholds
    
    def evaluate(self, test_results: dict) -> dict:
        """執行品質檢查，返回通過/失敗"""
        status = "pass"
        failures = []
        
        for metric, threshold in self.thresholds.items():
            if metric in test_results:
                value = test_results[metric]
                if value < threshold:
                    status = "fail"
                    failures.append(f"{metric}: {value:.3f} < {threshold}")
        
        return {
            "status": status,
            "failures": failures,
            "summary": f"通過 {status == 'pass'}，{len(failures)} 項失敗" if failures else "全部通過",
        }

# 使用範例
gate = QualityGate({
    "bleu": 0.3,
    "bertscore": 0.7,
    "llm_judge_avg": 3.5,
    "safe_rate": 0.95,
})

result = gate.evaluate(test_results)
if result["status"] == "fail":
    print("品質閘道未通過，阻止部署")
```

品質閘道與 CI/CD 管線整合，確保只有通過評估的模型或提示詞才能進入生產環境。

---

**下一步**：[RAG 管線的可觀測性](focus5.md)

## 延伸閱讀

- [BLEU, ROUGE, METEOR 比較](https://www.google.com/search?q=BLEU+ROUGE+METEOR+comparison)
- [LLM-as-Judge 評估方法](https://www.google.com/search?q=LLM+as+judge+evaluation)
- [BERTScore 原理解析](https://www.google.com/search?q=BERTScore+explained)
- [LLM 評估框架比較](https://www.google.com/search?q=LLM+evaluation+frameworks)
