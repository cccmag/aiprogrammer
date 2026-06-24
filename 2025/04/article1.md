# Jupyter Notebook 使用指南

## 前言

Jupyter Notebook 是資料科學領域最受歡迎的互動式開發環境之一。它允許使用者將程式碼、文字說明、圖表和執行結果整合在單一文件中，非常適合資料探索、教學和協作。本文將從安裝開始，逐步介紹 Jupyter Notebook 的核心功能與進階技巧。

## 安裝與啟動

### 安裝

```bash
# 使用 pip 安裝
pip install jupyter

# 使用 conda 安裝
conda install jupyter

# 安裝 JupyterLab (推薦)
pip install jupyterlab
```

### 啟動

```bash
# 啟動 Jupyter Notebook
jupyter notebook

# 啟動 JupyterLab
jupyter lab
```

啟動後，瀏覽器會自動打開本機的 8888 埠，顯示 Notebook 的檔案管理介面。

## 核心概念

### 儲存格（Cell）

Notebook 由多個儲存格組成，主要分為三種：

- **Code Cell**：執行 Python 程式碼
- **Markdown Cell**：撰寫文字說明（支援 Markdown 語法）
- **Raw Cell**：未轉換的原始文字

```python
# 這是 Code Cell
print("Hello, Jupyter!")
```

### 執行模式

- **Cell Mode**：按下 `Shift + Enter` 執行目前儲存格並移動到下一個
- **Edit Mode**：編輯儲存格內容（綠色邊框）
- **Command Mode**：操作儲存格（藍色邊框）

## 常用快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| `Shift + Enter` | 執行儲存格並移至下一個 |
| `Ctrl + Enter` | 執行儲存格不移動 |
| `A` | 在上方插入儲存格 |
| `B` | 在下方插入儲存格 |
| `DD` | 刪除儲存格 |
| `M` | 轉為 Markdown 儲存格 |
| `Y` | 轉為 Code 儲存格 |

## 資料分析範例

```python
import pandas as pd
import matplotlib.pyplot as plt

# 載入資料
df = pd.read_csv("sales.csv")

# 資料預覽
df.head()

# 統計摘要
df.describe()

# 繪圖
df.plot(kind="bar", x="month", y="revenue")
plt.show()
```

## 魔術指令

Jupyter 提供了以 `%` 開頭的魔術指令，大幅提升工作效率：

```python
# 計時
%time sum(range(1000000))

# 檢視變數
%who

# 內嵌 Matplotlib 圖表
%matplotlib inline

# 執行外部腳本
%run data_analysis.py
```

## 進階技巧

### 使用 LaTeX 公式

在 Markdown Cell 中使用 `$` 包裹 LaTeX 語法：

```markdown
$ \mu = \frac{1}{n} \sum_{i=1}^{n} x_i $
```

### 互動式 Widget

```python
from ipywidgets import interact

@interact(x=(0, 10, 0.5))
def plot_sine(x):
    plt.plot(np.sin(np.linspace(0, x, 100)))
    plt.show()
```

## 結語

Jupyter Notebook 是資料科學家的必備工具。透過互動式的開發環境、豐富的視覺化支援和活躍的社群生態，無論是資料探索、教學演示還是協作開發，Jupyter 都能提供出色的使用體驗。

---

**延伸閱讀**
- [Jupyter 官方文件](https://www.google.com/search?q=Jupyter+documentation)
- [JupyterLab 使用指南](https://www.google.com/search?q=JupyterLab+tutorial)
