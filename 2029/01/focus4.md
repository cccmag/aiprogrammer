# 人機協作工作流（2023-2029）

## AI 輔助 vs AI 自主

### 前言

人機協作工作流的核心問題是：**讓 AI 做什麼，讓人做什麼**？2023 年以來，答案不斷演化。

### 人工在迴圈中（Human-in-the-Loop）

HITL 是最早也是最穩健的模式：

```python
# Human-in-the-Loop
def hitl_workflow(task):
    draft = llm(f"生成初稿：{task}")
    
    # 關鍵決策點：人工審核
    human_feedback = input(f"審核以下內容，輸入修改建議：{draft}")
    
    if human_feedback.strip():
        final = llm(f"根據建議修改：{human_feedback}\n\n原文：{draft}")
    else:
        final = draft
    
    return final
```

### 漸進式自主（Progressive Autonomy）

2025 年後，流行的模式是「漸進式自主」——AI 逐步證明自己後獲得更多自主權：

```python
# Progressive Autonomy
class ProgressiveAgent:
    def __init__(self, trust_level=0):
        self.trust = trust_level  # 0-100
    
    def run(self, task):
        if self.trust < 30:
            return self.supervised_execution(task)
        elif self.trust < 70:
            return self.semi_autonomous(task)
        else:
            return self.fully_autonomous(task)
    
    def supervised_execution(self, task):
        result = llm(task)
        approval = input(f"核准此結果？{result} (y/n)")
        if approval == "y":
            self.trust += 10
        return result
```

### 異常升級（Exception Escalation）

系統在無法處理時自動升級給人類：

```python
# Exception Escalation
def escalated_workflow(task):
    try:
        result = autonomous_agent.run(task)
        if result.confidence < 0.7:
            raise LowConfidenceError(result)
        return result
    except (LowConfidenceError, UnknownError) as e:
        # 升級給人類操作員
        human_result = assign_to_human(str(e), task)
        return human_result
```

### 平行協作

人類和 AI 平行工作的模式：

```python
# 人機平行協作
def parallel_collaboration():
    import asyncio

    async def ai_part():
        return await llm_async("分析資料並生成報表")

    async def human_part():
        return await get_human_input("請提供策略方向")

    ai_result, human_input = await asyncio.gather(
        ai_part(), human_part()
    )
    return llm(f"整合 AI 分析：{ai_result}\n人類策略：{human_input}")
```

### 小結

人機協作的最佳實踐不是「AI 取代人類」，而是**建立高效的互動介面**——讓 AI 處理重複性工作，讓人類專注於創造性決策。

---

**下一步**：[錯誤處理與恢復策略](focus5.md)

## 延伸閱讀

- [Human-in-the-Loop 設計](https://www.google.com/search?q=Human+in+the+loop+AI+workflow+best+practices)
- [AI 自主程度框架](https://www.google.com/search?q=AI+autonomy+levels+human+collaboration)
- [人機協作案例研究](https://www.google.com/search?q=human+AI+collaboration+workflow+case+study)
