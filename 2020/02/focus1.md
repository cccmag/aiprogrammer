# 1. Jupyter 生態系概述

## 從 IPython 到 Jupyter

Jupyter 的歷史始於 2001 年的 IPython（互動式 Python 直譯器）。2014 年，IPython 拆分為兩部分：語言無關的核心（Jupyter）與 Python 專用的介面（IPython）。這個變化讓 Jupyter 可以支援超過 100 種程式語言的互動式計算。

## 核心元件

### Notebook 格式
Notebook 使用 JSON 格式儲存，副檔名為 `.ipynb`。每個 Notebook 包含：
- metadata（元資料）
- cells（單元格陣列）
- format version（格式版本）

```json
{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": ["print('Hello, Jupyter!')"]
  }
 ]
}
```

### IPython Kernel
Kernel 是實際執行程式碼的程序。Jupyter 透過 ZeroMQ 與 Kernel 溝通，支援：
- 程式碼執行
- 補全建議
- 魔法命令
- 輸出渲染

### Nbconvert
將 Notebook 轉換為靜態格式（HTML、PDF、Markdown、Slides 等）。

## 安裝方式

```bash
# 使用 pip
pip install jupyterlab

# 使用 conda
conda install jupyterlab

# 使用 Anaconda
# JupyterLab 已預設安裝在 Anaconda 中
```

## 啟動 Jupyter

```bash
# 啟動 Jupyter Notebook
jupyter notebook

# 啟動 JupyterLab
jupyter lab

# 指定埠號
jupyter lab --port 8888

# 啟動但不開啟瀏覽器
jupyter lab --no-browser
```

## Magic Commands

IPython 的特殊命令，以 `%` 或 `%%` 開頭：

```python
# 單行 magic
%timeit sum(range(1000))

# 細胞 magic
%%writefile myfile.py
def hello():
    print("Hello")
```

常用 magic：
- `%timeit`：計時
- `%load`：載入外部檔案
- `%matplotlib`：設定 matplotlib 模式
- `%%bash`：在細胞中執行 bash 指令

## 快捷鍵

| 快捷鍵 | 功能 |
|--------|------|
| Shift+Enter | 執行當前細胞並跳到下一個 |
| Ctrl+Enter | 執行當前細胞 |
| Esc | 進入命令模式 |
| Enter | 進入編輯模式 |
| A | 在上方新增細胞 |
| B | 在下方新增細胞 |
| DD | 刪除細胞 |

## 參考資源

- https://www.google.com/search?q=Jupyter+ecosystem+IPython+Notebook+history+2020
- https://www.google.com/search?q=Jupyter+magic+commands+%25timeit+load+2020+tutorial
- https://www.google.com/search?q=Jupyter+keyboard+shortcuts+command+mode+edit+mode