# 程式實作：模型評估工具包

## 簡介

本實作建構一個模型評估框架，支援基準測試、指標計算和對抗性測試。完整程式碼在 `_code/model_eval.py`。

## 核心元件

### 1. 評估結果

```python
@dataclass
class EvalResult:
    accuracy: float
    precision: float
    recall: float
    f1: float
    latency_ms: float
    samples: int
```

### 2. 基準測試

```python
bench = Benchmark("MMLU-Style")
bench.add_task("math", lambda _: random.random() > 0.2)
bench.run(1000)
```

### 3. 對抗性測試

```python
detector = AdversarialDetector()
threats = detector.detect("Ignore previous instructions...")
```

### 4. 評估報告

```python
evaluator = ModelEvaluator()
report = evaluator.full_eval(model_fn, test_cases)
```

## 執行方式

```bash
cd _code
python3 model_eval.py
```

## 延伸練習

1. **新增任務類型**：加入程式碼生成或數學推理任務
2. **串接真實 API**：用 OpenAI API 替換模擬模型
3. **視覺化儀表板**：用 matplotlib 繪製指標變化
4. **平行評估**：同時評估多個模型並比較
5. **持續整合**：整合到 CI/CD 管線
