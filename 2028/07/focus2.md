# 思維鏈與推理增強生成（2022-2028）

## 讓模型學會思考

### 思維鏈提示（Chain-of-Thought）

2022 年，Google 研究人員發表了思維鏈提示（Chain-of-Thought Prompting, CoT）。核心洞察非常簡單：**讓模型在回答前先產生中間推理步驟**。

```python
# 標準提示 vs 思維鏈提示
standard_prompt = "Q: 小明有 12 個蘋果，給了小華 3 個，又買了 5 個，現在有幾個？"
# 模型可能直接猜錯

cot_prompt = """
Q: 小明有 12 個蘋果，給了小華 3 個，又買了 5 個，現在有幾個？
A: 小明原本有 12 個蘋果。
   給了小華 3 個，所以剩下 12 - 3 = 9 個。
   又買了 5 個，所以現在有 9 + 5 = 14 個。
   答案是 14。
"""
```

### 思維鏈的數學原理

CoT 的有效性來自於一個關鍵觀察：**語言模型在 Token 空間中進行推理時，中間步驟提供了「計算暫存器」**。這類似於圖靈機的工作帶。

```python
# 模擬 CoT 的暫存器效應
def cot_reasoning(question):
    scratchpad = []
    # Step 1: 解析問題
    scratchpad.append(parse_question(question))
    # Step 2: 分解子問題
    sub_problems = decompose(scratchpad[-1])
    for sub in sub_problems:
        # Step 3: 逐步解決
        result = solve_sub_problem(sub)
        scratchpad.append(result)
    # Step 4: 合併結果
    return synthesize(scratchpad)
```

### Zero-shot CoT

2023 年的突破：不需要範例，只需在提示後加上「讓我們一步步思考」就能啟動推理：

```python
zero_shot_cot = f"""
{question}

讓我們一步步思考。
"""
# 模型會自動產生推理鏈
```

這個發現意義重大——它意味著 CoT 不是提示工程的技巧，而是**模型內部能力的湧現**。

### Tree-of-Thought（ToT）

2023 年底，Princeton 和 Google DeepMind 提出了思維樹（Tree-of-Thought）。CoT 是單一路徑，ToT 則探索多條推理路徑：

```python
class TreeOfThought:
    def search(self, problem):
        root = Node(problem)
        for level in range(max_depth):
            candidates = []
            for node in current_level:
                thoughts = self.generate_thoughts(node)
                scored = self.evaluate(thoughts)
                candidates.extend(scored)
            current_level = self.select_best(candidates, width=3)
        return self.backtrack(current_level)
```

### Graph-of-Thought（GoT）

2024 年，思維圖（Graph-of-Thought）進一步允許推理節點間任意連接，形成網路狀推理圖。

### 推理增強生成（RAG + CoT）

2024-2025 年，RAG 與 CoT 開始整合。模型在推理過程中動態檢索資訊：

```python
def rag_cot(query):
    chain = []
    while not has_answer(chain):
        thought = model.think(chain, query)
        if needs_search(thought):
            info = retrieve(thought.search_query)
            thought = model.integrate(thought, info)
        chain.append(thought)
    return chain
```

### OpenAI o1 的秘密

2024 年 9 月，OpenAI 發表 o1 系列。o1 的核心技術就是**強化學習 + 思維鏈**——模型被訓練來產生更長的內部推理鏈，並在 Token 空間中進行自我校正。

### 2026-2028：隱式推理

最新趨勢是**隱式推理**：模型在內部表示空間中進行推理，而不是將推理步驟寫成文字。這使得推理更快、更節省 Token：

```python
# 隱式推理示意（概念）
def implicit_reasoning(input_text):
    hidden = model.encode(input_text)
    for _ in range(reasoning_steps):
        hidden = model.reason_step(hidden)  # 在隱空間中推理
    return model.decode(hidden)
```

### 小結

從 CoT 到 ToT 再到 GoT，推理增強技術的演化反映了**一個核心趨勢：讓模型的「思考過程」更接近人類的系統性推理**。

---

**下一步**：[工具使用與 API 整合](focus3.md)

## 延伸閱讀

- [Chain-of-Thought Prompting 論文](https://www.google.com/search?q=Chain-of-Thought+Prompting+reasoning+LLM)
- [Tree-of-Thought: 多路徑推理](https://www.google.com/search?q=Tree-of-Thought+reasoning+LLM)
- [OpenAI o1 推理模型解析](https://www.google.com/search?q=OpenAI+o1+reasoning+model+chain+of+thought)
