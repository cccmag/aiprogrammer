# 知識蒸餾到 RAG

## 前言

知識蒸餾（Knowledge Distillation）原是將大型教師模型的能力壓縮到小型學生模型的技術。將此概念應用到 RAG 領域，可以用大型模型（如 GPT-4）生成高品質的檢索資料，用來優化小型模型的檢索或生成能力。本文探討三種知識蒸餾在 RAG 中的應用方式。

## 蒸餾檢索資料集

使用教師 LLM 生成查詢-文件配對，用以訓練更輕量的檢索模型：

```python
def distill_retrieval_dataset(teacher_llm, documents: list[str],
                              num_pairs: int = 1000) -> list[dict]:
    dataset = []
    for doc in documents[:num_pairs]:
        prompt = f"""根據以下文件，生成一個應該能檢索到這份文件的查詢：
文件：{doc[:500]}
格式：查詢：<查詢文字>"""
        query = teacher_llm.generate(prompt).replace("查詢：", "").strip()
        dataset.append({"query": query, "document": doc})
    return dataset
```

此資料集可用於微調小型檢索編碼器（如小型的 Sentence-BERT），使其檢索品質接近教師模型。

## 蒸餾上下文精煉

教師 LLM 可以將檢索結果摘要為更精簡的上下文，降低學生 LLM 的輸入長度：

```python
def distill_context(teacher_llm, raw_docs: list[str],
                    max_tokens: int = 500) -> str:
    prompt = f"""將以下文件精煉為不超過 {max_tokens} 字的摘要，
保留所有關鍵事實與數據：

{chr(10).join(f'- {d[:200]}' for d in raw_docs)}"""
    return teacher_llm.generate(prompt)
```

學生模型使用精煉後的上下文，不僅減少 token 消耗，回答品質也因焦點集中而提升。

## 蒸餾檢索決策策略

Agentic RAG 中，教師 LLM 可示範何時檢索、何時停止：

```python
def distill_retrieval_policy(teacher_llm, questions: list[str],
                             retriever) -> list[dict]:
    demonstrations = []
    for q in questions:
        response = teacher_llm.generate(
            f"問題：{q}\n想回答這個問題，需要檢索嗎？需要什麼資訊？"
        )
        # Record the teacher's decision process
        docs = retriever.retrieve(q) if "需要" in response else []
        demonstrations.append({
            "question": q,
            "teacher_reasoning": response,
            "retrieved": len(docs) > 0,
            "docs": docs[:3]
        })
    return demonstrations
```

這些示範可用於訓練學生 Agent 的檢索決策模型，減少不必要的 LLM 呼叫。

## 蒸餾管線實作

完整的知識蒸餾管線包含三個階段：

```python
class RAGDistillationPipeline:
    def __init__(self, teacher: str, student: str):
        self.teacher = teacher  # 例如 "gpt-4"
        self.student = student  # 例如 "llama-3-8b"

    def run(self, corpus: list[str]) -> dict:
        # Phase 1: Distill retrieval dataset
        retrieval_data = distill_retrieval_dataset(self.teacher, corpus)
        fine_tune_retriever(self.student, retrieval_data)

        # Phase 2: Distill context summarization
        summarization_data = []
        for docs in chunk(corpus, 5):
            summary = distill_context(self.teacher, docs)
            summarization_data.append({"docs": docs, "summary": summary})
        fine_tune_summarizer(self.student, summarization_data)

        # Phase 3: Distill retrieval policy
        questions = generate_questions_from_corpus(corpus)
        policy_data = distill_retrieval_policy(self.teacher, questions, None)
        fine_tune_policy_model(self.student, policy_data)

        return {
            "retrieval_pairs": len(retrieval_data),
            "summaries": len(summarization_data),
            "policy_demos": len(policy_data)
        }
```

## 效益分析

知識蒸餾後的學生 RAG 系統在檢索召回率上可達到教師模型的 90-95%，但延遲降低 3-5 倍，成本降低 10-20 倍。特別適合在邊緣裝置或高吞吐量的生產環境中部署。

## 總結

知識蒸餾為 RAG 系統提供了一條從「高品質但昂貴」到「經濟且高效」的遷移路徑。透過蒸餾檢索資料集、上下文精煉與檢索決策策略，可以將 GPT-4 等級的 RAG 能力壓縮到開源小模型中，大幅降低營運成本。

---

**參考資料**

- https://www.google.com/search?q=knowledge+distillation+RAG+retrieval
- https://www.google.com/search?q=LLM+distillation+dataset+generation
- https://www.google.com/search?q=context+summarization+distillation+RAG
- https://www.google.com/search?q=distilled+retrieval+policy+agentic+RAG
