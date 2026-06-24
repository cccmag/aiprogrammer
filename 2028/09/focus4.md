# 模型可解釋性方法（2017-2028）

## 為什麼需要可解釋性？

深度學習模型在醫療、金融等領域的應用面臨監管要求——歐盟 GDPR 的「解釋權」條款（2018）推動了 XAI 研究爆發。

## 事後解釋方法

### LIME（2016）

在預測點附近擬合一個簡單的線性模型來解釋黑盒決策。每個特徵的權重代表其貢獻程度。

### SHAP（2017）

基於合作賽局理論的 Shapley Value，計算每個特徵對預測的邊際貢獻。提供一致的局部與全局解釋。

### 可解釋性瓶頸

將因果結構嵌入模型架構——先預測因果概念，再用其預測最終輸出。這讓解釋與因果推論合而為一。

## 因果可解釋性（2020-2028）

因果思維為 XAI 提供了新視角：與其解釋「模型看到什麼」，不如回答「什麼改變會翻轉預測？」。反事實解釋因此成為主流。

## Python 範例：使用 SHAP

```python
import shap
import xgboost as xgb
from sklearn.datasets import load_diabetes

X, y = load_diabetes(return_X_y=True)
model = xgb.XGBRegressor().fit(X, y)
explainer = shap.Explainer(model, X)
shap_values = explainer(X[:100])
shap.summary_plot(shap_values, X[:100])
```

參考：[搜尋 SHAP explainability](https://www.google.com/search?q=SHAP+feature+importance) | [搜尋 LIME explainable AI](https://www.google.com/search?q=LIME+XAI)
