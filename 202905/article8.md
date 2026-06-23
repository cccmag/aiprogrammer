# 領域特定基準建立

## 1. 通用基準的不足

通用基準（MMLU、HellaSwag）無法反映專業領域的真實需求。醫療、法律、金融等領域需要專門設計的評估任務。

## 2. 領域基準設計原則

高品質領域基準需滿足：專家審核的答案、真實場景任務、明確的評分標準與足夠的題目數量。設計時應優先選取從業者日常面臨的任務。

```python
def domain_benchmark_pipeline(domain_name, task_list):
    questions = []
    for task in task_list:
        items = collect_expert_questions(domain_name, task)
        validated = expert_review(items)
        questions.extend(validated)
    return BenchmarkDataset(domain=domain_name, items=questions)
```

## 3. 醫療領域案例

MedQA 與 PubMedQA 評估模型在醫學執照考試與文獻理解上的表現。更進一步的 ClinicalBench 要求模型閱讀病歷並提供診斷建議。

## 4. 法律領域案例

CaseHOLD、LEX 等基準評估法律推理與判例搜尋。模型需理解法條結構、先例引用與法律推論鏈。

## 5. 金融領域案例

FinBench、CFA 模擬題測試模型在財務分析、風險評估與合規判斷上的能力。表格理解與數字推理是關鍵挑戰。

## 6. 結語

建立領域特定基準需要領域專家與 AI 工程師的密切合作。從真實工作流程提煉評估任務，才能確保基準反映實際應用價值。領域基準也是模型落地前的最終驗證關卡。

- https://www.google.com/search?q=medical+LLM+benchmark+MedQA
- https://www.google.com/search?q=legal+AI+benchmark+CaseHOLD
