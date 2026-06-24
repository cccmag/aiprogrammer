# 領域特定基準建立

## 為什麼需要領域特定基準？

通用基準（如 MMLU、HellaSwag）雖然重要，但無法完全反映特定領域的需求。醫療、法律、金融等領域需要量身打造的評估基準。

## 建立基準的步驟

```python
class BenchmarkBuilder:
    def __init__(self, domain, language="zh-TW"):
        self.domain = domain
        self.language = language
        self.questions = []
        self.metadata = {}

    def collect_domain_data(self, sources):
        """從領域專家與文件中收集資料"""
        for source in sources:
            data = self.parse_source(source)
            self.questions.extend(data)

    def parse_source(self, source):
        # 解析領域特定文件
        questions = []
        for doc in source:
            qa_pairs = self.extract_qa_from_doc(doc)
            questions.extend(qa_pairs)
        return questions

    def extract_qa_from_doc(self, document):
        # 從文件中提取問答對
        qa_pairs = []
        paragraphs = document.split("\n\n")
        for para in paragraphs:
            if "?" in para or "？" in para:
                question, *answers = para.split("。")
                qa_pairs.append({
                    "question": question.strip(),
                    "answer": "。".join(answers).strip()
                })
        return qa_pairs

    def add_expert_curated(self, questions):
        """加入領域專家設計的問題"""
        self.questions.extend(questions)
```

## 評估指標計算

```python
def compute_domain_metrics(predictions, ground_truth):
    metrics = {
        "accuracy": sum(p == g for p, g in
                       zip(predictions, ground_truth)) / len(predictions),
        "hallucination_rate": compute_hallucination(predictions, ground_truth),
        "domain_consistency": compute_consistency(predictions)
    }
    return metrics

def compute_hallucination(predictions, ground_truth):
    # 檢測模型是否生成不在來源中的資訊
    hallucinated = 0
    for pred, truth in zip(predictions, ground_truth):
        extra_info = set(pred.split()) - set(truth.split())
        if len(extra_info) > len(pred.split()) * 0.3:
            hallucinated += 1
    return hallucinated / len(predictions)
```

## 結語

Google 搜尋「Domain Specific LLM Benchmark」可參考各領域的基準建立案例。好的領域基準需要領域專家深入參與，並定期更新以反映知識進展。
