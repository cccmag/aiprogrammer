# RAG 評估框架

## 前言

RAG 系統的評估比傳統 NLP 任務更複雜，因為它涉及檢索（retrieval）與生成（generation）兩個相互影響的環節。一個好的評估框架不僅衡量最終答案的品質，還要診斷檢索環節與生成環節各自的問題。本文介紹 RAGAS、RGB 等主流評估框架的實作。

## RAGAS 指標

RAGAS（RAG Assessment）是最廣泛使用的 RAG 評估框架，包含四個核心維度：

```python
def faithfulness(answer: str, context: str, llm) -> float:
    """答案是否忠於上下文（無幻覺）"""
    prompt = f"""判斷答案中的每個事實是否都來自上下文：
上下文：{context}
答案：{answer}
回覆 JSON：{{"faithfulness_score": 0.0-1.0}}"""
    result = json.loads(llm.generate(prompt))
    return result["faithfulness_score"]

def answer_relevance(question: str, answer: str, llm) -> float:
    """答案是否與問題相關"""
    prompt = f"""問題：{question}
答案：{answer}
回覆 JSON：{{"relevance_score": 0.0-1.0}}"""
    result = json.loads(llm.generate(prompt))
    return result["relevance_score"]

def context_precision(question: str, context: list[str], llm) -> float:
    """檢索結果中相關片段的佔比"""
    relevant = 0
    for chunk in context:
        judgment = llm.generate(
            f"「{chunk}」是否與「{question}」相關？回答 yes/no"
        )
        if judgment.strip().lower() == "yes":
            relevant += 1
    return relevant / len(context) if context else 0

def context_recall(question: str, context: list[str],
                   answer: str, llm) -> float:
    """答案所需資訊是否都在檢索結果中"""
    prompt = f"""答案：{answer}
上下文：{context}
判斷上下文是否包含回答所需的所有資訊？回覆 0.0-1.0"""
    result = json.loads(llm.generate(prompt))
    return result["recall_score"]
```

## 自動化評估管線

將評估整合到 CI/CD 管線中，每次更新知識庫或檢索策略時自動執行：

```python
class RAGEvaluator:
    def __init__(self, test_set: list[dict]):
        self.test_set = test_set  # [{"question": ..., "golden_answer": ...}]

    def evaluate(self, rag_system) -> dict:
        scores = {"faithfulness": [], "relevance": [],
                  "precision": [], "recall": []}

        for item in self.test_set:
            result = rag_system.query(item["question"])
            scores["faithfulness"].append(
                faithfulness(result["answer"], result["context"], llm))
            scores["relevance"].append(
                answer_relevance(item["question"], result["answer"], llm))
            scores["precision"].append(
                context_precision(item["question"],
                                  result["context_chunks"], llm))
            scores["recall"].append(
                context_recall(item["question"],
                               result["context_chunks"],
                               result["answer"], llm))

        return {k: sum(v)/len(v) for k, v in scores.items()}
```

## 人工評估輔助

自動化評估無法完全取代人工判斷。設計一個評分介面讓標註人員回饋：

```python
def human_evaluation_interface(rag_system, questions: list[str]):
    evaluations = []
    for q in questions:
        result = rag_system.query(q)
        print(f"\nQ: {q}")
        print(f"A: {result['answer']}")
        relevance = input("相關性 (1-5): ")
        accuracy = input("準確性 (1-5): ")
        evaluations.append({
            "question": q,
            "answer": result["answer"],
            "relevance": int(relevance),
            "accuracy": int(accuracy)
        })
    return evaluations
```

## 檢索與生成的脫鉤評估

定位問題來源是 RAG 除錯的關鍵。將檢索與生成分開評估：

```python
def diagnose_rag(rag_system, test_set: list[dict]) -> dict:
    retrieval_issues = 0
    generation_issues = 0

    for item in test_set:
        result = rag_system.query(item["question"])
        # Is the context sufficient?
        recall = context_recall(item["question"],
                                result["context_chunks"],
                                item["golden_answer"], llm)
        if recall < 0.8:
            retrieval_issues += 1
        # Is the answer faithful to sufficient context?
        if recall >= 0.8:
            faithful = faithfulness(result["answer"],
                                    result["context"], llm)
            if faithful < 0.8:
                generation_issues += 1

    return {
        "retrieval_issue_rate": retrieval_issues / len(test_set),
        "generation_issue_rate": generation_issues / len(test_set)
    }
```

## 評估資料集建構

好的評估資料集是 RAG 評估的基石。建議包含三類問題：簡單事實類（單一檢索即可回答）、複雜推理類（需要多跳檢索）、時序類（需要最新資訊）。

## 總結

RAG 評估需要多維度的指標與系統性的方法。RAGAS 的四個指標（faithfulness、relevance、context precision、context recall）提供了基礎框架。更重要的是將檢索與生成脫鉤評估，才能精確定位系統瓶頸。自動化評估結合人工抽樣驗證是生產環境的最佳實務。

---

**參考資料**

- https://www.google.com/search?q=RAGAS+retrieval+augmented+generation+evaluation
- https://www.google.com/search?q=RAG+faithfulness+score+context+precision
- https://www.google.com/search?q=RGB+RAG+bank+evaluation+framework
- https://www.google.com/search?q=RAG+CI+CD+automated+evaluation+pipeline
