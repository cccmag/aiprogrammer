# CoT 與 Tree-of-Thoughts 比較

## Chain-of-Thought 提示

CoT 透過中間推理步驟提升 LLM 的複雜問題解決能力。標準 CoT 使用「讓我們逐步思考」觸發鏈式推理。

```python
def zero_shot_cot(prompt):
    return llm.generate(f"{prompt}\n讓我們逐步思考。")

def few_shot_cot(prompt):
    examples = """
Q: 小明有 5 顆蘋果，給了小華 2 顆，又買了 3 顆，請問現在有幾顆？
A: 一開始有 5 顆。給了小華 2 顆，5-2=3。又買了 3 顆，3+3=6。答案是 6。
"""
    return llm.generate(f"{examples}\nQ: {prompt}\nA:")
```

## Tree-of-Thoughts

ToT 將推理擴展為樹狀搜尋，同時探索多條推理路徑，並使用評估函數剪枝。

```python
class TreeOfThoughts:
    def __init__(self, llm, max_branches=3, max_depth=5):
        self.llm = llm
        self.max_branches = max_branches
        self.max_depth = max_depth

    def solve(self, problem):
        root = {"state": problem, "depth": 0, "children": []}
        frontier = [root]

        for _ in range(self.max_depth):
            new_frontier = []
            for node in frontier:
                candidates = self._generate_thoughts(node["state"])
                scored = [(c, self._evaluate(c)) for c in candidates]
                scored.sort(key=lambda x: x[1], reverse=True)
                for thought, score in scored[:self.max_branches]:
                    child = {"state": thought, "depth": node["depth"] + 1,
                             "score": score, "children": []}
                    node["children"].append(child)
                    new_frontier.append(child)

            if any(self._is_solution(n["state"]) for n in new_frontier):
                break
            frontier = new_frontier

        return self._best_path(root)

    def _generate_thoughts(self, state):
        prompt = f"給定當前狀態：{state}\n請給出下一步可能的三種思考方向。"
        return self.llm.generate(prompt).split("\n")
```

## 比較

| 特性 | CoT | ToT |
|------|-----|-----|
| 搜尋空間 | 單一路徑 | 樹狀多路徑 |
| 回溯能力 | 無 | 支援 |
| 計算成本 | 低 | 高 |
| 適合問題 | 線性推理 | 需要探索的複雜問題 |

ToT 在數學證明、創意寫作等需要多角度探索的任務中表現更佳。詳見 https://www.google.com/search?q=Chain-of-Thought+vs+Tree-of-Thoughts+LLM。
