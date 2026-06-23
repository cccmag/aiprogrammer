# 漂移檢測演算法比較

## 前言

資料漂移（Data Drift）與概念漂移（Concept Drift）是 AI 模型在生產環境中效能衰退的兩大主因。本文比較五種主流漂移檢測演算法的原理與適用場景。

---

## 一、演算法詳解

### 1.1 Population Stability Index (PSI)

PSI 是最廣泛使用的漂移指標：

```python
import numpy as np

def psi(reference, production, bins=10):
    ref_hist, _ = np.histogram(reference, bins=bins, range=(0, 1))
    prod_hist, _ = np.histogram(production, bins=bins, range=(0, 1))
    ref_pct = ref_hist / ref_hist.sum()
    prod_pct = prod_hist / prod_hist.sum()
    return np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct))
```

閾值：PSI < 0.1 無漂移，0.1–0.2 需關注，> 0.2 顯著漂移。

### 1.2 Kolmogorov-Smirnov 檢定

比較兩個連續分布的 CDF：

```python
from scipy.stats import ks_2samp
stat, p_value = ks_2samp(reference, production)
```

### 1.3 KL 散度

```python
from scipy.special import kl_div
kl_value = np.sum(kl_div(ref_pdf, prod_pdf))
```

適合偵測罕見事件的漂移。

### 1.4 ADWIN

ADWIN（Adaptive Windowing）是串流場景的經典演算法，無需預設視窗大小：

```python
from river.drift import ADWIN
adwin = ADWIN()
for value in data_stream:
    adwin.update(value)
    if adwin.change_detected:
        adwin.reset()
```

### 1.5 MMD

最大平均差異適合高維 Embedding 資料：

```python
from sklearn.gaussian_process.kernels import RBF

def mmd(x, y, kernel=RBF()):
    k_xx = kernel(x, x).mean()
    k_yy = kernel(y, y).mean()
    k_xy = kernel(x, y).mean()
    return k_xx + k_yy - 2 * k_xy
```

---

## 二、比較總表

| 演算法 | 資料類型 | 靈敏度 | 計算成本 | 串流支援 |
|--------|---------|--------|---------|---------|
| PSI | 離散/連續 | 中 | 低 | 需批次 |
| KS 檢定 | 連續 | 高 | 低 | 需批次 |
| KL 散度 | 機率分布 | 高 | 低 | 需批次 |
| ADWIN | 任意 | 中 | 極低 | 原生 |
| MMD | 高維向量 | 極高 | 高 | 可批次 |

---

## 三、實戰建議

| 場景 | 推薦演算法 |
|------|-----------|
| 表格資料 | PSI + KS |
| Embedding 資料 | MMD |
| 即時串流 | ADWIN |
| 概念漂移 | ADWIN + DDM |

---

## 結語

建議在生產環境中同時運行 2–3 種方法，採用投票機制降低誤報率。

---

## 參考資料

- https://www.google.com/search?q=drift+detection+algorithm+comparison
- https://www.google.com/search?q=PSI+KL+divergence+model+monitoring
- https://www.google.com/search?q=ADWIN+concept+drift+detection
