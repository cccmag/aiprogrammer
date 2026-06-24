# 程式碼說明 — Jupyter 互動式範例腳本

## 功能概述

`_code/jupyter_demo.py` 展示了在純 Python 環境中模擬 Jupyter 互動式輸出的一些基礎功能。此腳本不需要 Jupyter 環境即可執行，用於說明資料視覺化與互動計算的基本概念。

## demo() 函數說明

### 1. 簡單輸出
展示如何在命令列環境中產生類似 Jupyter 的格式化輸出。

### 2. 基礎資料視覺化
使用 matplotlib 在非 Jupyter 環境中生成圖表，說明圖表生成與儲存的原理。

### 3. 互動式模擬
透過簡單的 input() 互動，說明 Jupyter 中 widgets 的基本概念。

## 執行方式

```bash
cd _code
python3 jupyter_demo.py
```

或使用測試腳本：

```bash
cd _code
bash test.sh
```

## 輸出範例

```
============================================================
Jupyter 互動式計算基礎展示
============================================================

[1] 格式化輸出
    資料處理結果：
    - 最大值：100
    - 最小值：1
    - 平均值：50.5

[2] 視覺化資訊
    已生成圖表：histogram.png
    （在非 Jupyter 環境中，圖表將儲存為圖檔）

[3] 互動式模擬
    請輸入一個數值（輸入 'q' 結束）：50
    您輸入的值：50，其平方為：2500
```

## 在實際 Jupyter 中使用

在 Jupyter Notebook/Lab 中：

```python
# 安裝依賴
!pip install matplotlib numpy

# 執行
%matplotlib inline
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
plt.show()
```

## 參考資源

- https://www.google.com/search?q=matplotlib+non+interactive+backend+save+figure+Python+2020
- https://www.google.com/search?q=Jupyter+Notebook+matplotlib+inline+visualization+tutorial