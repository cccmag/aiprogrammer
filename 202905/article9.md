# 評估指標選擇指南

## 1. 指標選擇的原則

選擇評估指標需考慮任務類型、模型輸出格式與應用場景。沒有萬能指標——每個指標都有其偏誤與侷限。

## 2. 分類任務指標

準確率在類別不平衡時有誤導性。F1 分數平衡精確率與召回率，適用於多數分類場景。Matthews 相關係數對不平衡資料更穩健。

```python
from sklearn.metrics import classification_report, matthews_corrcoef

def evaluate_classification(y_true, y_pred):
    report = classification_report(y_true, y_pred, output_dict=True)
    mcc = matthews_corrcoef(y_true, y_pred)
    return {"f1_macro": report["macro avg"]["f1-score"], "mcc": mcc}
```

## 3. 生成任務指標

BLEU 衡量 n-gram 重疊，ROUGE 著重召回率，METEOR 引入同義詞比對。BERTScore 使用語義嵌入計算相似度，更接近人類判斷。

```python
def bleu_bert_comparison(reference, candidate):
    bleu = sentence_bleu(reference, candidate)
    bert = BERTScore()
    bert_score = bert.score([candidate], [reference])
    return {"bleu": bleu, "bertscore": bert_score["f1"][0]}
```

## 4. 多維度評分框架

單一指標無法全面反映品質。建立多維度評估框架：流暢度、相關性、事實性、完整性。每個維度獨立評分後加權匯總。

## 5. 指標間的相關性

不同指標對同一模型排序可能不同。使用 Spearman 相關性比較指標間的一致性。若某指標與人類判斷相關性低於 0.3，應謹慎使用。

## 6. 結語

好的評估始於對指標本質的理解。選擇指標時應思考：這個指標真正衡量的是什麼？它與人類判斷的相關性如何？在邊界案例中它是否會失效？

- https://www.google.com/search?q=BERTScore+evaluation+metric+LLM
- https://www.google.com/search?q=BLEU+ROUGE+METEOR+comparison+generation
