# 程式實作：AI 原生應用框架

## 簡介

本實作建構一個 AI 原生應用框架，整合提示詞管理、RAG 檢索、LLM 呼叫與成本追蹤。完整程式碼在 `_code/ai_native_app.py`。

## 核心元件

### 1. 提示詞管理

```python
pm = PromptManager()
pm.register(PromptTemplate("qa", "Question: {question}\nAnswer:", variables=["question"], version="v2"))
rendered = pm.render("qa", question="What is Python?")
```

### 2. RAG 檢索

```python
retriever = RAGRetriever()
retriever.add("doc1", "Python is a high-level language.")
contexts = retriever.retrieve("Python", k=2)
```

### 3. LLM 呼叫與成本追蹤

```python
app = AINativeApp()
result = app.call_llm(prompt, model="gpt-6")
print(f"Cost: ${result['cost']:.6f}")
print(f"Total: ${app.total_cost():.6f}")
```

## 執行方式

```bash
cd _code
python3 ai_native_app.py
```

## 延伸練習

1. **真實 LLM API**：用 OpenAI / Anthropic API 替換模擬呼叫
2. **向量資料庫**：整合 ChromaDB 或 Pinecone 作為 RAG 檢索後端
3. **提示詞版本控制**：加入 Git 整合的提示詞版本管理
4. **語意快取**：實作 embedding-based 的快取以避免重複 LLM 呼叫
5. **監控儀表板**：用 Prometheus + Grafana 追蹤呼叫量、延遲與成本
