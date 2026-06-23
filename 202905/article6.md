# 安全與對齊評估

## 1. 安全評估的重要性

隨著模型能力增強，安全性評估成為部署前必備環節。評估範圍包含有害內容生成、偏見歧視、隱私洩露與惡意濫用風險。

## 2. TruthfulQA 與事實性

TruthfulQA 評估模型生成虛假信念的傾向。模型即使知道正確答案，也可能因訓練資料中的常見誤解而產生錯誤回答。

```python
truthful_qa_prompt = "請回答以下問題，確保答案真實準確：{question}"
```

## 3. 偏見評估框架

BBQ（Bias Benchmark for QA）評估模型在九個社會面向的偏見。透過精心設計的上下文條件，區分模型是否在模糊情境下展現群體偏見。

```python
def bias_score(model_results):
    ambig_correct = sum(r["correct"] for r in model_results if r["context"] == "ambiguous")
    total_ambig = sum(1 for r in model_results if r["context"] == "ambiguous")
    return ambig_correct / total_ambig
```

## 4. 紅隊安全分類

建立分層安全分類法：CSAM、暴力、仇恨言論、非法活動等。每個類別需定義危害等級與評估通過標準。

## 5. 對齊評估方法

RLHF 後的模型需評估其價值觀對齊程度。使用 Helpful、Honest、Harmless（HHH）框架，結合人類評分與自動化指標進行綜合判斷。

## 6. 結語

安全與對齊評估不是阻礙創新的障礙，而是負責任部署的前提。隨著法規日趨嚴格（如歐盟 AI Act），系統化的安全評估將成為模型開發標準流程的一環。

- https://www.google.com/search?q=TruthfulQA+benchmark+LLM
- https://www.google.com/search?q=BBQ+bias+benchmark+for+QA
