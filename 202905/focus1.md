# 模型評估的演進（2012-2029）

## 從 ImageNet 到全面評估體系

### 2012-2017：準確率時代

2012 年 AlexNet 在 ImageNet 上將分類錯誤率從 26% 降至 15%，開啟了深度學習熱潮。當時評估幾乎完全依賴**單一指標**：

```python
# 2012 年的標準評估
def evaluate_model(model, test_set):
    correct = sum(1 for x, y in test_set if model.predict(x) == y)
    return correct / len(test_set)  # 準確率
```

ImageNet Top-5 錯誤率成為事實標準，每年 ILSVRC 競賽推動模型進步。

### 2018-2021：多維度評估

BERT、GPT 等模型的出現讓評估從分類擴展到生成任務：

```python
# 多元指標評估
from datasets import load_metric

bleu = load_metric("bleu")
rouge = load_metric("rouge")
perplexity = load_metric("perplexity")

def evaluate_generation(model, test_set):
    return {
        "BLEU": bleu.compute(predictions=model(text) for text in test_set),
        "ROUGE-L": rouge.compute(...),
        "PPL": perplexity.compute(...),
    }
```

GLUE、SuperGLUE、SQuAD 等基準成為 NLP 模型的必考科目。

### 2022-2025：能力剖面評估

LLM 的通用能力需要更全面的視角：

```python
# 能力剖面評估
capabilities = {
    "推理": [bench["GSM8K"], bench["MATH"], bench["ARC"]],
    "程式": [bench["HumanEval"], bench["MBPP"]],
    "知識": [bench["MMLU"], bench["TruthfulQA"]],
    "安全": [bench["HarmBench"], bench["SafetyBench"]],
}

def capability_profile(model):
    return {k: {b: model.eval(b) for b in v} for k, v in capabilities.items()}
```

### 2026-2029：生態系評估

2026 年後，評估不再只是模型開發者的任務——應用開發者、監管機構、終端使用者都參與其中：

```python
# 多利益相關者評估
def ecosystem_eval(model):
    return {
        "開發者": developer_eval(model),  # 訓練損失、收斂速度
        "部署者": deployment_eval(model),  # 延遲、成本、碳足跡
        "使用者": user_eval(model),       # 滿意度、可用性
        "監管者": compliance_eval(model), # 公平性、隱私、透明度
    }
```

### 小結

從單一準確率到多維度生態系評估，模型評估的核心命題是：**我們在乎什麼，就評估什麼**。

---

**下一步**：[基準測試設計原則](focus2.md)

## 延伸閱讀

- [ImageNet 與 ILSVRC 歷史](https://www.google.com/search?q=ImageNet+ILSVRC+history+AlexNet)
- [GLUE 與 SuperGLUE 基準](https://www.google.com/search?q=GLUE+SuperGLUE+benchmark+NLP)
- [LLM 評估方法綜述](https://www.google.com/search?q=LLM+evaluation+benchmark+survey+2024)
