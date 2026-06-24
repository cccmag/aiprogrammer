# 2. Jupyter Notebook 6.0

## 新功能與改進

Jupyter Notebook 6.0 於 2019 年 5 月發布，是多年來最大的版本更新。對於仍在使用 5.x 版本的用戶，建議升級以獲得更好的使用體驗。

## 改進的歡迎介面

新版本預設顯示一個「Welcome」Notebook，介紹基本操作與新功能。這對初學者非常友善。

## 互動式滑桿（S游乐场元素）

Notebook 6.0 改進了互動式 widget 的渲染效能。透過 ipywidgets 可以建立滑桿、下拉選單等互動元素：

```python
from ipywidgets import interact

@interact(x=(0, 100, 1))
def show(x=50):
    return f"x = {x}"
```

## 安全改進

6.0 版本強化了輸出執行防護，防止惡意輸出自動執行程式碼。這對安全性要求高的環境非常重要。

## Notebook 匯出格式

支援更多的匯出格式：
- HTML（靜態網頁）
- LaTeX（學術論文）
- PDF（透過 LaTeX）
- Markdown（文字格式）
- ReStructuredText
- Slides（簡報）

## 協作功能

雖然 Jupyter Notebook 本身的即時協作能力有限，但透過以下方式可以實現協作：
- JupyterHub（多人同時使用）
- Google Colab（Google 文件式協作）
- Git + Notebook 版本控制

## Notebook 6.0 的限制

Notebook 6.0 是經典介面，對於需要多文件、多面板的複雜工作流程，建議使用 JupyterLab 1.x。JupyterLab 是未來主要的開發方向。

## 升級 Notebook

```bash
# 升級 Jupyter Notebook
pip install --upgrade notebook

# 升級 JupyterLab（建議同時安裝）
pip install --upgrade jupyterlab
```

## 參考資源

- https://www.google.com/search?q=Jupyter+Notebook+6.0+release+May+2019+new+features
- https://www.google.com/search?q=Jupyter+Notebook+6.0+security+output+execution+improvements
- https://www.google.com/search?q=Jupyter+Notebook+vs+JupyterLab+differences+2020