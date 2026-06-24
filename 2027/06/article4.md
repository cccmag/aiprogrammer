# RAG 系統設計模式：從 Naive 到 Agentic

## 前言

檢索增強生成（Retrieval-Augmented Generation, RAG）已成為 LLM 落地應用的主流架構。透過在生成前檢索外部知識，RAG 有效解決了 LLM 的幻覺問題與知識更新難題。本文將系統性介紹 RAG 的演進歷程，從 Naive RAG 到 Agentic RAG，並提供完整的 Python 實作。

## Naive RAG：檢索 + 生成

最基礎的 RAG 模式包含三個步驟：索引（Indexing）、檢索（Retrieval）、生成（Generation）：

```python
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.llms import HuggingFacePipeline

# 1. 載入與分割文件
with open("knowledge_base.txt") as f:
    documents = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", " ", ""]
)
chunks = text_splitter.create_documents([documents])

# 2. 建立向量索引
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh-v1.5")
vectorstore = Chroma.from_documents(chunks, embeddings)

# 3. 建立 RAG Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=HuggingFacePipeline.from_model_id(
        model_id="Qwen/Qwen2.5-7B-Instruct",
        task="text-generation",
    ),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
    chain_type="stuff"  # 將檢索結果直接填入 prompt
)

result = qa_chain.invoke("Transformer 的注意力機制如何運作？")
print(result)
```

Naive RAG 的局限在於：一次檢索可能遺漏關鍵資訊，且無法處理需要多步推理的複雜問題。

## Advanced RAG：重排序與混合檢索

進階 RAG 引入了檢索後重排序（Reranking）與混合檢索（Hybrid Search）：

```python
from sentence_transformers import CrossEncoder
from langchain.retrievers import ContextualCompressionRetriever

# 重排序模型
reranker = CrossEncoder("BAAI/bge-reranker-v2-m3")

class RerankRetriever:
    def __init__(self, base_retriever, reranker, top_k=3):
        self.base_retriever = base_retriever
        self.reranker = reranker
        self.top_k = top_k

    def get_relevant_documents(self, query):
        docs = self.base_retriever.get_relevant_documents(query)
        pairs = [(query, doc.page_content) for doc in docs]
        scores = self.reranker.predict(pairs)
        scored = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
        return [doc for doc, _ in scored[:self.top_k]]

# 混合檢索：向量 + BM25
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 5

vector_retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, vector_retriever],
    weights=[0.3, 0.7]  # BM25 與向量檢索的權重
)
```

## Modular RAG：查詢路由與轉換

當系統需要處理多樣化的查詢時，引入路由與查詢轉換機制：

```python
from langchain.chains.router import LLMRouterChain

# 查詢路由：判斷查詢類型
router_prompt = """根據使用者的問題，選擇最適合的資料來源：
1. 技術文件（technical）
2. 產品手冊（product）
3. 常見問題（faq）

問題：{query}
請只回答資料來源名稱。"""

# 查詢轉換：擴寫、分解、HyDE
from langchain.chains.query_constructor import QueryConstructor

def query_transformation(query):
    """HyDE: 先讓 LLM 產生假答案，再用假答案檢索"""
    hypothetical = llm.invoke(f"請簡短回答：{query}")
    return hypothetical
```

## Agentic RAG：多步驟推理

最新的 RAG 模式引入 Agent 架構，支援多輪檢索與推理：

```python
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

tools = [
    Tool(
        name="vector_search",
        func=lambda q: vectorstore.similarity_search(q, k=3),
        description="使用向量檢索知識庫"
    ),
    Tool(
        name="web_search",
        func=lambda q: search_web(q),
        description="搜尋最新網路資訊"
    ),
]

agent_prompt = PromptTemplate.from_template("""
你是一個 RAG Agent。使用可用工具逐步回答問題。

問題：{input}

思考過程：
1. 我是否需要檢索資訊？
2. 使用哪個工具？
3. 根據檢索結果回答。

{agent_scratchpad}""")

agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=5
)

result = agent_executor.invoke({
    "input": "Transformer 與 LSTM 的差異是什麼？在 2026 年有什麼新的進展？"
})
```

## RAG 評測框架

RAG 系統需要從檢索品質與生成品質兩個維度評估：

```python
@dataclass
class RAGEvalResult:
    retrieval_recall: float
    answer_relevance: float
    faithfulness: float

def evaluate_rag(qa_chain, test_set):
    results = []
    for item in test_set:
        answer = qa_chain.invoke(item["query"])
        # 使用 LLM 作為評判
        eval_prompt = f"""問題：{item['query']}
標準答案：{item['answer']}
模型回答：{answer}

評估：
1. 回答是否忠於檢索內容？(yes/no)
2. 回答是否相關？(1-5)
3. 是否包含幻覺？(yes/no)"""
        results.append(llm.invoke(eval_prompt))
    return results
```

## 參考資源

- [RAG 架構演進論文](https://www.google.com/search?q=Retrieval+Augmented+Generation+survey+paper)
- [LangChain RAG 教學](https://www.google.com/search?q=langchain+rag+tutorial+advanced)
- [LlamaIndex RAG 模式](https://www.google.com/search?q=llamaindex+rag+patterns+guide)
