# Jupyter 環境優化

## Jupyter 環境

Jupyter Notebook/Lab 是資料科學領域的主流開發環境，2019 年初 JupyterLab 1.0 正式發布。

## 安裝與設定

```bash
pip install jupyterlab notebook

# 啟動
jupyter lab
# 或
jupyter notebook
```

## 基本操作

```python
# 神奇的指令
%matplotlib inline
%timeit sum(range(1000))
%who_ls

# Markdown 單元格
# # 標題
# **粗體** *斜體*
# `程式碼`
```

## 視覺化整合

```python
import matplotlib.pyplot as plt
import numpy as np

%matplotlib inline

x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.sin(x))
plt.title('Sin Wave')
plt.show()
```

## 交互式 Widgets

```bash
pip install ipywidgets
```

```python
import ipywidgets as widgets
from IPython.display import display

slider = widgets.IntSlider(min=0, max=100, step=1, value=50)
display(slider)

def on_value_change(change):
    print(f"值變為：{change['new']}")

slider.observe(on_value_change, names='value')
```

## 環境管理

### Jupyter Kernel

```bash
# 列出所有 kernel
jupyter kernelspec list

# 切換 kernel
# Kernel -> Change kernel -> 選擇想要的環境
```

### nbconvert 轉換

```bash
# Notebook 轉換為 HTML
jupyter nbconvert --to html notebook.ipynb

# Notebook 轉換為 Python 腳本
jupyter nbconvert --to python notebook.ipynb

# Notebook 轉換為 PDF（需要 LaTeX）
jupyter nbconvert --to pdf notebook.ipynb
```

## 擴展套件

```bash
pip install jupyter_contrib_nbextensions
jupyter contrib nbextensions install
```

常用擴展：
- Table of Contents（目錄）
- Variable Inspector（變數檢查器）
- Code Folding（程式碼摺疊）
- Autopep8（程式碼格式化）

## 提升效能

### 輸出控制

```python
# 限制輸出長度
pd.set_option('display.max_rows', 10)

# 停用 JIT
%unload_ext numba
```

### 記憶體管理

```python
import gc

# 刪除大型物件
del large_dataframe

# 垃圾回收
gc.collect()
```

## 資料科學範例

```python
import pandas as pd
import numpy as np

# 載入資料
df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

# 基本探索
print(df.head())
print(df.info())
print(df.describe())

# 分組統計
print(df.groupby('species').mean())
```

## 與環境整合

```python
# 顯示環境資訊
import sys
import platform
print(f"Python: {sys.version}")
print(f"Platform: {platform.platform()}")

# 檢查已安裝的關鍵套件
import importlib
packages = ['numpy', 'pandas', 'sklearn', 'matplotlib']
for pkg in packages:
    mod = importlib.import_module(pkg)
    print(f"{pkg}: {mod.__version__}")
```

## 參考資源

- https://www.google.com/search?q=JupyterLab+tutorial+environment+setup+2019
- https://www.google.com/search?q=Jupyter+notebook+tips+tricks+productivity+2019
- https://www.google.com/search?q=Jupyter+widgets+ipywidgets+interactive+visualization+2019