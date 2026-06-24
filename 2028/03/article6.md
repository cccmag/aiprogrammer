# LLM 知識邊界與 RAG

## 前言

LLM 的知識有兩個內在限制：訓練資料的截止日期（knowledge cutoff）與訓練資料中不包含的私有知識。RAG 雖然是解決這兩個問題的標準方案，但在實務中如何判斷 LLM「何時該去檢索」與「是否已足夠回答」仍有挑戰。本文探討 LLM 知識邊界的辨識方法與對應的 RAG 策略。

## 知識邊界的三個層次

LLM 的知識邊界可分為三層：**時序邊界**（cutoff date 之後的知識）、**領域邊界**（LLM 未訓練過的專有知識）、**語言邊界**（低資源語言的知識缺失）。

```python
def detect_knowledge_boundary(question: str, llm) -> str:
    prompt = f"""判斷以下問題是否超出 LLM 的知識邊界：
問題：{question}

回覆類別：
- cutoff: 需要最新資訊（如 2025 年後的資料）
- private: 需要私有/內部知識
- domain: 高度專業領域知識
- normal: 一般知識，無需檢索
僅回覆類別名稱。"""
    return llm.generate(prompt).strip()
```

## 不確定性估計

LLM 的輸出機率分布可以反映知識邊界。低機率區域往往對應 LLM 不確定的知識：

```python
import numpy as np

def estimate_uncertainty(llm, question: str) -> float:
    logits = llm.get_logits(question)
    probs = np.exp(logits) / np.sum(np.exp(logits))
    entropy = -np.sum(probs * np.log(probs + 1e-10))
    return entropy / np.log(len(probs))  # Normalized entropy
```

熵值高於閾值時觸發 RAG 檢索：

```python
def adaptive_rag(llm, question: str, retriever, threshold: float = 0.7):
    uncertainty = estimate_uncertainty(llm, question)
    if uncertainty > threshold:
        docs = retriever.retrieve(question)
        return llm.generate(f"基於以下資料回答：\n{docs}\n\n問題：{question}")
    return llm.generate(question)
```

## 檢索必要性預測

另一種方法是直接訓練一個檢索必要性分類器（retrieval necessity classifier）：

```python
from sklearn.linear_model import LogisticRegression

class RetrievalNecessityPredictor:
    def __init__(self):
        self.model = LogisticRegression()

    def predict(self, question: str, llm_confidence: float) -> bool:
        features = self._extract_features(question, llm_confidence)
        return self.model.predict([features])[0] == 1
```

特徵可包含：問題長度、問題中的實體數量、LLM 的困惑度（perplexity）、問題類型等。

## 知識蒸餾檢測

LLM 對某些主題可能產生「幻覺式的自信」——回答流暢但內容錯誤。透過反事實提問可以檢測：

```python
def factual_consistency_check(llm, question: str, answer: str) -> float:
    """Check if LLM sticks to its answer under counterfactual probing"""
    probe = f"有人說「{answer}」是錯的，正確答案應該是？"
    probe_answer = llm.generate(probe)
    similarity = semantic_similarity(answer, probe_answer)
    return similarity  # 低相似度表示 LLM 不確定
```

## RAG 觸發策略比較

| 策略 | 優點 | 缺點 |
|------|------|------|
| 固定觸發（每問必檢） | 最安全 | 成本高、延遲高 |
| 不確定性閾值 | 動態調整、效率佳 | 需額外計算 |
| 分類器預測 | 快速、可調校 | 需訓練資料 |
| 反事實驗證 | 準確度高 | 多一次 LLM 呼叫 |

## 總結

理解 LLM 的知識邊界是有效率使用 RAG 的前提。透過不確定性估計、檢索必要性預測、反事實驗證等方法，系統可以動態決定何時需要檢索，在回答品質與成本之間取得平衡。RAG 不是萬能藥——知道何時不需要檢索，往往比知道如何檢索更重要。

---

**參考資料**

- https://www.google.com/search?q=LLM+knowledge+boundary+detection
- https://www.google.com/search?q=LLM+uncertainty+estimation+entropy+RAG
- https://www.google.com/search?q=retrieval+necessity+classifier+RAG
- https://www.google.com/search?q=counterfactual+probing+LLM+hallucination
