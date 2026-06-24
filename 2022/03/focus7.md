# Jupyter 生態與互動式開發

## 從 IPython 到 Jupyter

Jupyter 的故事始於 2001 年，當時 Fernando Pérez 正在攻讀物理博士學位。他需要一個更好的 Python 互動式環境，於是創建了 IPython。這個專案最初只是對標準 Python 直譯器的增強，卻在二十年後發展成為整個資料科學領域的標準開發平台。

2014 年，IPython 專案重大轉型，IPython Notebook 分離為獨立的 Jupyter Notebook 專案。Jupyter 這個名字來自三種核心語言的縮寫：Julia、Python、R。

```
2001 ── IPython (Fernando Pérez)
2011 ── IPython Notebook
2014 ── Jupyter Notebook 誕生
2018 ── JupyterLab 發布
2022 ── JupyterLab 3.3 + Notebook 7
```

## Jupyter Notebook 與 Lab

Jupyter 提供了兩種主要的開發環境：

### Jupyter Notebook（經典介面）

傳統的基於網頁的筆記本介面，以 `.ipynb` 格式儲存程式碼、文字和圖表。

### JupyterLab（現代化 IDE）

JupyterLab 是下一代的使用者介面，提供了類似 VS Code 的多分頁佈局：

```
┌──────────────────────────────────────────┐
│  File  Edit  View  Run  Kernel  Git  Tab  │
├──────────────┬───────────────────────────┤
│              │                           │
│  File        │  Notebook (cell-based)    │
│  Browser     │                           │
│              │  ┌───────────────────────┐ │
│  notebooks/  │  │ In [1]: import numpy │ │
│  data/       │  │         as np        │ │
│  scripts/    │  ├───────────────────────┤ │
│              │  │ Out[1]: numpy.loaded  │ │
│              │  └───────────────────────┘ │
│              │                           │
│              │  Terminal / Console       │
├──────────────┴───────────────────────────┤
│  Inspector / Debugger                    │
└──────────────────────────────────────────┘
```

## IPython 核心功能

IPython 作為 Jupyter 的核心，提供了豐富的互動式功能：

```python
# Tab 自動補全
import numpy as np
np.  # 按 Tab 顯示所有方法

# 魔術指令
%timeit   # 計時
%debug    # 除錯
%who      # 列出變數
%run      # 執行腳本
%matplotlib inline  # 行內繪圖

# Shell 命令
!ls -la
!pip install requests
```

## 互動式資料科學工作流

Jupyter 最強大的地方在於支援探索性的資料科學工作流：

```python
# 1. 載入資料
import pandas as pd
df = pd.read_csv("data.csv")
df.head()

# 2. 探索與清洗（逐步探索）
df.info()
df.describe()
df.isnull().sum()

# 3. 視覺化探索
import matplotlib.pyplot as plt
df.hist(figsize=(10, 8))

# 4. 建模（保留前步驟的環境）
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

## 協作與分享

Jupyter 生態提供了多種分享方式：

- **NBViewer**：直接分享 notebook 連結
- **JupyterHub**：團隊共享的 Jupyter 伺服器
- **Binder**：讓他人直接執行線上 notebook
- **Voilà**：將 notebook 轉為互動式儀表板
- **Papermill**：參數化 notebook 執行

## 延伸閱讀

- [Jupyter 官方網站](https://www.google.com/search?q=Jupyter+official)
- [IPython 文件](https://www.google.com/search?q=IPython+documentation)
- [JupyterLab 教學](https://www.google.com/search?q=JupyterLab+tutorial)

---

*本篇文章為「AI 程式人雜誌 2022 年 3 月號」歷史回顧系列之一。*
