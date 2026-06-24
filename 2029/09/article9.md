# 開放科學與 AI

## AI 推動開放科學

開放科學倡導數據、程式碼、論文的自由共享。AI 在其中扮演雙重角色：它既是開放科學的受益者（需要大量訓練數據），也是推動者（降低分析門檻）。

## 預印本與開放數據

arXiv、bioRxiv 等預印本伺服器讓研究成果即時公開。AI 摘要工具如 PaperQA 和 Elicit 幫助科學家從海量預印本中篩選相關研究。Kaggle、Zenodo、Figshare 等平台促進數據共享。

```python
# 簡單的開放科學貢獻度分析
import re

class OpenScienceAnalyzer:
    def __init__(self):
        self.metrics = {
            "preprint": 0, "data": 0, "code": 0, "reproduce": 0
        }
    
    def analyze_paper(self, text):
        if re.search(r'arxiv|biorxiv|medrxiv', text, re.I):
            self.metrics["preprint"] += 1
        if re.search(r'github|zenodo|figshare|data available', text, re.I):
            self.metrics["data"] += 1
        if re.search(r'open.?source|code.?available', text, re.I):
            self.metrics["code"] += 1
        if re.search(r'reproduc|replicat', text, re.I):
            self.metrics["reproduce"] += 1
        return self.metrics
    
    def openness_score(self):
        total = sum(self.metrics.values())
        return total / 4.0  # 歸一化

analyzer = OpenScienceAnalyzer()
text = "We release our code on GitHub and data on Zenodo. Preprint on arXiv."
score = analyzer.analyze_paper(text)
print(f"開放科學指標: {score}")
print(f"開放度分數: {analyzer.openness_score():.2f}")
```

## AI 生成論文與倫理

AI 輔助寫作引發學術倫理討論。哪些程度的 AI 使用需要披露？如何防止論文工廠利用 LLM 自動生成低品質論文？Nature 和 Science 等期刊已制定 AI 使用規範，要求作者明確聲明 AI 角色。

## 公民科學與 AI

Zooniverse 等公民科學平台與 AI 形成人機協作。AI 先進行初始分類，人類志願者驗證邊緣案例。這種模式在 Galaxy Zoo、Snapshot Serengeti 等項目中取得巨大成功。

> 參考資料：https://www.google.com/search?q=AI+open+science+citizen+science+2025
