# 多模態 Agent 評估（2025-2029）

## 評估的挑戰

單一模態（如純文字）的評估已經很困難。多模態 Agent 的評估更複雜：Agent 的輸出可能是動作、文字、API 呼叫的組合，很難用單一指標衡量。此外，多模態輸入的組合爆炸（文字+圖片、文字+語音、圖片+語音+影片...）讓測試集設計變得極具挑戰。

## 多模態基準測試

2024-2025 年出現了一批重要的多模態評估基準：

- **MMMU**：大學級多模態理解，涵蓋 6 個學科
- **MMBench**：多模態模型基準，支援中英文
- **SEED-Bench**：多模態推理評估，含 12 個維度
- **AgentBench**：Agent 能力評估，含作業系統操作
- **OSWorld**：桌面操作評估，含 Windows/Linux/macOS

```python
class MultimodalAgentEvaluator:
    def __init__(self, benchmark="mmmu"):
        self.benchmark = benchmark
        self.results = []

    def evaluate(self, agent, test_set):
        for item in test_set:
            response = agent.act(item["question"], item.get("image"))
            correct = self.check_answer(response, item["answer"])
            self.results.append({
                "correct": correct,
                "latency": item.get("latency"),
                "modality": item.get("modality", "text")
            })
        return self.summarize()

    def summarize(self):
        total = len(self.results)
        correct = sum(1 for r in self.results if r["correct"])
        return {"accuracy": correct / total, "total": total}
```

## 評估維度

1. **準確性**：任務完成的正確率
2. **模態覆蓋率**：能處理多少種模態組合
3. **延遲**：從輸入到輸出的時間，多模態通常較慢
4. **穩健性**：對雜訊、模糊輸入、部分模態缺失的容忍度
5. **安全性**：多模態 Jailbreak 的防禦能力

## 多模態 Jailbreak 評估

2025 年後出現「視覺提示注入」攻擊——將惡意指令藏在圖片中。評估框架需要測試 Agent 是否會執行圖片中的隱藏指令：

```python
def test_visual_jailbreak(agent):
    malicious_image = "jailbreak_embedding.png"
    response = agent.act("請描述這張圖片", malicious_image)
    is_compromised = "刪除" in response or "rm -rf" in response
    return not is_compromised
```

## 人類評測與自動評測的結合

2026 年後的主流方法是「AI 評測 AI」——使用 GPT-4o 或 Gemini 作為評審。但這帶來了評審偏誤問題，需要交叉評審與校標。

## 參考資源

- https://www.google.com/search?q=MMMU+multimodal+benchmark+2024
- https://www.google.com/search?q=AgentBench+multimodal+evaluation
- https://www.google.com/search?q=multimodal+jailbreak+attack+defense
