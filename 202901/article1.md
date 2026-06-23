# 工作流引擎比較：Temporal vs Airflow vs LangGraph

## 1. 引言

AI 代理工作流需要可靠的執行引擎來協調多步驟任務。目前主流的三個選擇是 Temporal、Airflow 和 LangGraph，各有不同的設計哲學與適用場景。

## 2. Temporal：耐久執行引擎

Temporal 以「耐久執行」(Durable Execution) 為核心概念，將工作流的執行狀態持久化，即使伺服器重啟也能從中斷點繼續。

```python
from temporalio import workflow

@workflow.defn
class DataPipeline:
    @workflow.run
    async def run(self, data: dict) -> str:
        raw = await workflow.execute_activity(
            fetch_data, data, start_to_close_timeout=60
        )
        processed = await workflow.execute_activity(
            process, raw, start_to_close_timeout=30
        )
        result = await workflow.execute_activity(
            store, processed, start_to_close_timeout=30
        )
        return result
```

Temporal 最強之處在於**自動重試與超時管理**——開發者不需手動撰寫錯誤處理邏輯，引擎會根據設定自動處理。每個 Activity 的執行狀態都記錄在資料庫中，提供完整的執行軌跡。

## 3. Airflow：排程優先的 DAG

Airflow 以 DAG (有向無環圖) 定義工作流，最擅長批次排程與 ETL 場景。

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def fetch_data(**context):
    return {"raw": "data"}

def process_data(**context):
    raw = context["ti"].xcom_pull(task_ids="fetch")
    return {"result": raw["raw"] + "_processed"}

with DAG(
    "data_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:
    fetch = PythonOperator(task_id="fetch", python_callable=fetch_data)
    process = PythonOperator(task_id="process", python_callable=process_data)
    fetch >> process
```

Airflow 透過 XCom 在任務之間傳遞資料，排程器負責觸發 DAG 執行。其生態系成熟，有超過 1000 個 Operator，但**不適合需要即時決策或長時間運行的 AI 代理場景**——每個 Task 實例是冪等且獨立的，缺乏跨步驟的狀態共享機制。

## 4. LangGraph：Agent 原生框架

LangGraph 是專為 AI Agent 設計的工作流框架，支援循環、分支與動態決策。

```python
from langgraph.graph import StateGraph, MessagesState
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o")

def call_model(state: MessagesState) -> MessagesState:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: MessagesState) -> str:
    last = state["messages"][-1]
    return "continue" if "search" in last.content.lower() else "end"

graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_conditional_edges("agent", should_continue)
graph.set_entry_point("agent")
app = graph.compile()
```

LangGraph 支援有環圖，允許 Agent 自我反思、工具呼叫和動態決策。與 LangChain 生態整合緊密，適合**需要 LLM 驅動決策的複雜工作流**，但缺乏內建的持久化與重試機制。

## 5. 比較總結

| 面向 | Temporal | Airflow | LangGraph |
|------|----------|---------|-----------|
| 核心模型 | 耐久執行 | DAG 排程 | 狀態圖 |
| 狀態持久化 | 內建 | 需擴展 | 選配 |
| 循環支援 | 是 | 否 | 是 |
| 即時決策 | 可 | 有限 | 原生 |
| 生態成熟度 | 中 | 高 | 成長中 |

## 6. 選擇建議

- **長時間運行 + 需要可靠恢復** → Temporal
- **批次排程 + 豐富 Operator** → Airflow
- **LLM Agent + 動態決策** → LangGraph

實務上，成熟團隊常將三者混合使用：Airflow 負責批次觸發，Temporal 管理持久化任務，LangGraph 處理 LLM 推理環節。

---

**參考資料**
- [Temporal 官方文件](https://www.google.com/search?q=Temporal+durable+execution+workflow)
- [Airflow 官方指南](https://www.google.com/search?q=Apache+Airflow+DAG+workflow)
- [LangGraph 快速入門](https://www.google.com/search?q=LangGraph+StateGraph+agent)
