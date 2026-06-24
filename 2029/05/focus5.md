# 領域特定評估（2023-2029）

## 通用模型 vs 專用評估

### 前言

MMLU 分數高不一定代表模型擅長寫程式或診斷疾病。領域特定評估填補了通用基準的盲區。

### 程式碼生成評估

HumanEval 和 MBPP 開創了功能正確性評估：

```python
# 功能正確性測試
def test_code_generation(model, problem):
    generated = model.generate_code(problem["prompt"])
    test_cases = problem["tests"]
    passed = 0
    for test in test_cases:
        try:
            exec(generated)
            exec(test["assertion"])
            passed += 1
        except:
            pass
    return passed / len(test_cases)
```

2025 年後，LiveCodeBench 加入執行環境和真實 API 呼叫。

### 醫療領域評估

醫療 AI 需要專業知識驗證：

```python
# 醫療評估
medical_benchmarks = {
    "MedQA": {"source": "USMLE", "questions": 1278},
    "MedMCQA": {"source": "印度醫學院", "questions": 194k},
    "PubMedQA": {"source": "文獻摘要", "questions": 500},
}

def medical_eval(model):
    scores = {}
    for name, bench in medical_benchmarks.items():
        accuracy = model.eval(bench)
        scores[name] = accuracy
        if accuracy < 0.6:
            print(f"警告：{name} 未達及格線")
    return scores
```

### 法律領域評估

法律推理需要精確引用法條和判例：

```python
# 法律評估
def legal_reasoning_eval(model, case):
    analysis = model.generate(f"分析此案件：{case}")
    citations = extract_citations(analysis)
    relevant = check_citations(citations, case["relevant_laws"])
    return {
        "citation_accuracy": len(relevant) / len(citations),
        "reasoning_score": expert_review(analysis),
    }
```

### 金融與科學

領域特定評估涵蓋範圍持續擴大：

```python
# 跨領域評估
domain_benches = {
    "金融": ["FinBench", "CFA-Exam"],
    "化學": ["ChemBench", "OCHeM"],
    "生物": ["BioBench", "ProteinQA"],
    "工程": ["EngBench", "FE-Exam"],
}

def cross_domain_eval(model):
    return {
        domain: {b: model.eval(b) for b in benches}
        for domain, benches in domain_benches.items()
    }
```

### 小結

領域特定評估揭示通用模型在專業領域的真實能力——**高 MMLU 不等於好醫生**。

---

**下一步**：[持續評估與監控](focus6.md)

## 延伸閱讀

- [HumanEval 程式碼生成基準](https://www.google.com/search?q=HumanEval+code+generation+benchmark)
- [MedQA 醫療評估資料集](https://www.google.com/search?q=MedQA+medical+question+answering+dataset)
- [領域特定 LLM 評估](https://www.google.com/search?q=domain+specific+LLM+evaluation+benchmark)
