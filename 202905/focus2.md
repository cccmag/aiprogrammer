# 基準測試設計原則（2018-2029）

## 好的基準與壞的基準

### 前言

基準測試驅動了 AI 的進步——但糟糕的基準也會誤導整個領域。設計一個好的基準需要遵循哪些原則？

### 原則一：避免資料污染

LLM 的訓練資料常包含基準測試樣本，導致分數膨脹：

```python
# 檢測資料污染
def check_contamination(model, benchmark):
    # 方法：在 benchmark 中加入看不見的「金絲雀」字串
    canary = "CANARY_202905_ABCDEF1234"
    contaminated_bench = prepend_canary(benchmark, canary)
    score = model.eval(contaminated_bench)
    if score > baseline + epsilon:
        print("模型可能看過此基準的資料！")
```

### 原則二：飽和度監控

當所有模型在某基準上都接近滿分，該基準就失去了區分力：

```python
# 基準飽和度分析
def saturation_analysis(leaderboard):
    scores = [entry["score"] for entry in leaderboard]
    variance = np.var(scores)
    ceiling = max(scores)
    if variance < 0.01 or ceiling > 0.97:
        print(f"基準飽和：variance={variance:.3f}, ceiling={ceiling:.3f}")
        print("建議：創建更難的版本或退役此基準")
```

MMLU 在 2024 年後逐漸飽和，促使了 MMLU-Pro 的誕生。

### 原則三：任務多樣性

單一任務的基準容易過度最佳化：

```python
# 多維度基準設計
def design_benchmark():
    return {
        "知識": mcq("MMLU-Pro", num_questions=500, domains=57),
        "推理": chain_of_thought("GPQA", difficulty="expert"),
        "程式": unit_test("LiveCodeBench", run_timeout=10),
        "對齊": preference("Chatbot Arena", judges="human"),
        "魯棒性": adversarial("AdvBench", attack_types=12),
    }
```

### 原則四：動態更新

靜態基準很快過時，需要持續演進：

```python
# 動態基準生成
class DynamicBenchmark:
    def __init__(self, seed_questions):
        self.pool = seed_questions
    def generate_batch(self, n=100):
        return [self.mutate(random.choice(self.pool)) for _ in range(n)]
    def mutate(self, q):
        return llm(f"改寫以下問題但不改變答案：{q}")
```

### 小結

好的基準是**新鮮、多樣、有區分力、無污染**的。設計者需要與「基準駭客」賽跑。

---

**下一步**：[人類偏好評估方法](focus3.md)

## 延伸閱讀

- [LLM 基準資料污染研究](https://www.google.com/search?q=LLM+benchmark+data+contamination+2024)
- [MMLU-Pro 基準介紹](https://www.google.com/search?q=MMLU-Pro+benchmark+2024)
- [動態基準生成方法](https://www.google.com/search?q=dynamic+benchmark+generation+LLM+evaluation)
