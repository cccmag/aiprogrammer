# Jupyter 與互動式開發：從 Notebook 到 Lab

## 前言

Jupyter Notebook 以其互動式的開發體驗和直觀的資料視覺化能力，成為資料科學領域不可或缺的工具。本篇文章介紹 Jupyter 的起源、核心概念和使用技巧。

## Jupyter 的起源

### 從 IPython 到 Jupyter

Jupyter 的名字來源於三種語言的組合：**JU**lia、**PYT**hon 和 **R**。但實際上 Jupyter 支援上百種程式語言。

```
IPython (2001) ──► Jupyter (2014)
     │                   │
     │                   ├── Jupyter Notebook
     │                   ├── JupyterHub
     │                   └── JupyterLab
     │
     └── 互動式 Python shell
```

### Notebook 的核心概念

Jupyter Notebook 是一個基於 Web 的應用程式，允許開發者：
- 編寫和執行代碼
- 包含敘述文字、公式和圖表
- 呈現視覺化結果
- 分享和重現分析過程

```bash
# 安裝 Jupyter
pip install jupyter

# 啟動 Notebook 伺服器
jupyter notebook
```

## Notebook 界面

### 主要元件

```
┌─────────────────────────────────────────────────────┐
│ Jupyter Notebook                                     │
├─────────────────────────────────────────────────────┤
│ [File] [Edit] [View] [Insert] [Cell] [Kernel] [Help]│
├─────────────────────────────────────────────────────┤
│                                                     │
│  In [1]: import numpy as np                        │
│  In [2]: import matplotlib.pyplot as plt            │
│  In [3]: x = np.linspace(0, 2*np.pi, 100)           │
│  In [4]: plt.plot(x, np.sin(x))                     │
│  Out[4]: [<matplotlib.lines.Line2D at 0x...>]       │
│                                                     │
├─────────────────────────────────────────────────────┤
│  [Code] [Markdown] [Raw] [Heading]                 │
└─────────────────────────────────────────────────────┘
```

### 細胞類型

| 類型 | 用途 |
|------|------|
| Code | 編寫和執行 Python 代碼 |
| Markdown | 編寫格式化文字、公式 |
| Raw | 純文字，不被執行 |
| Heading | 標題（已廢棄，用 Markdown 替代）|

### 快捷鍵

```bash
# 命令模式（按 Esc 進入）
Enter          # 進入編輯模式
Shift+Enter    # 執行當前格並移到下一格
Ctrl+Enter     # 執行當前格
A              # 在上方插入細胞
B              # 在下方插入細胞
DD             # 刪除細胞（按兩次 D）
M              # 轉換為 Markdown
Y              # 轉換為 Code
Z              # 撤銷刪除

# 編輯模式（按 Enter 進入）
Ctrl+Shift+-   # 分割細胞
Tab            # 代碼補全
Shift+Tab      # 查看文件
```

## 實際應用

### 資料探索工作流

```python
# 1. 載入資料
import pandas as pd
import numpy as np

df = pd.read_csv('data.csv')

# 2. 初步檢視
df.head()
df.describe()
df.info()

# 3. 視覺化探索
import matplotlib.pyplot as plt

df['column'].hist(bins=30)
plt.show()

df.plot.scatter(x='col1', y='col2')
plt.show()
```

### Markdown 功能

```markdown
# 標題

## 二級標題

**粗體** 和 *斜體*

- 項目符號
- 列表

1. 編號列表
2. 第二項

| 表格 | 欄位1 | 欄位2 |
|------|-------|-------|
| 資料 |  A    |  B    |

數學公式（使用 LaTeX 語法）：
$$E = mc^2$$

$$f(x) = \int_{-\infty}^{\infty} e^{-x^2} dx$$
```

### Magic 命令

Jupyter 提供了特殊的「magic」命令：

```python
# 行 magic
%timeit sum(range(1000000))

# 細胞 magic
%%timeit
total = 0
for i in range(1000000):
    total += i

# 顯示 matplotlib 圖表在 Notebook 內
%matplotlib inline

# 载入外部檔案
%load_ext sql
%sql sqlite:///mydb.db

# 環境管理
%env PATH=/usr/bin
```

## JupyterLab：下一世代

### JupyterLab 簡介

JupyterLab 是 Jupyter 的下一代界面，提供了更靈活和強大的開發體驗：

```bash
# 安裝 JupyterLab
pip install jupyterlab

# 啟動 JupyterLab
jupyter lab
```

### JupyterLab 的新功能

- **靈活佈局**：像 IDE 一樣自由拖放面板
- **多文件支援**：同時開啟多個 Notebook、Terminal、檔案
- **即時預覽**：編輯 Markdown、CSV 時即時預覽
- **主題支援**：自訂編輯器外觀

### 擴展套件

```bash
# 安裝擴展
pip install jupyterlab-lsp  # 語言伺服器協議

# 主題擴展
jupyter lab install @jupyterlab/theme-dark
```

## 結論

Jupyter 徹底改變了資料科學家的開發方式：

- **互動式探索**：即時看到程式執行結果
- **文件一體**：代碼、說明、圖表融為一體
- **易於分享**：Notebook 檔案方便傳播和重現

2017 年的 Jupyter 正在快速發展，JupyterLab 的推出預示著更美好的未來。對於任何從事資料分析、機器學習或 AI 研究的人來說，掌握 Jupyter 是必備技能。

---

## 延伸閱讀

- [Jupyter 官方網站](https://www.google.com/search?q=Jupyter+Notebook+official+tutorial)
- [IPython 文件](https://www.google.com/search?q=IPython+tutorial+interactive)
- [JupyterLab 文档](https://www.google.com/search?q=JupyterLab+tutorial+interface)
- [Jupyter 擴展推薦](https://www.google.com/search?q=Jupyter+Notebook+extensions+productivity)

---

*本篇文章為「AI 程式人雜誌 2017 年 1 月號」焦點系列之一。*