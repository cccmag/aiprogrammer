# Python 生態：2017 年回顧

## 前言

Python 在 2017 年繼續保持作為 AI 和資料科學領域首選語言的地位。讓我們回顧這一年 Python 生態的重要發展。

## 2017 年重要發布

```python
# Python 版本時間線

# Python 3.6 (2016年12月)
# - f-strings
# - 數字分隔符
# - 安全的OrderedDict

# Python 3.7 (2018年6月)
# - async/await 改進
# - Data Classes
# - 效能提升

# Python 3.6.5 (2017年3月)
# - 穩定性修復
```

## 深度學習框架

```python
# 主要框架相容 Python 3.6

# TensorFlow 1.4 (2017年10月)
import tensorflow as tf
print(f"TensorFlow: {tf.__version__}")

# PyTorch 0.3 (2017年10月)
import torch
print(f"PyTorch: {torch.__version__}")

# Keras 2.1 (2017年9月)
import keras
print(f"Keras: {keras.__version__}")
```

## 資料科學庫

```python
# NumPy 1.13 (2017年6月)
# - Broadcasting 改進
# - 更好的效能

# Pandas 0.21 (2017年10月)
# - 更新的視覺化
# - 更好的字串處理

# Scikit-learn 0.19 (2017年8月)
# - 新演算法
# - 效能優化

# Matplotlib 2.0 (2017年1月)
# - 預設色彩地圖
# - 更好的樣式
```

## 環境管理

```bash
# pip 升級
pip install --upgrade pip

# conda 環境
conda create -n myenv python=3.6
conda activate myenv

# 常用套件安裝
pip install numpy pandas scikit-learn matplotlib tensorflow keras torch
```

## Jupyter 生态

```python
# Jupyter Notebook 5.0 (2017年6月)
# - 更好的 Markdown 支援
# - 捷徑自訂

# JupyterLab (beta)
# - 增強的介面
# - 多視窗支援
```

## 2017 年 Python 應用

```
┌─────────────────────────────────────────────────────────┐
│              2017 年 Python AI 應用                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  機器學習:                                            │
│  - scikit-learn 0.19                                  │
│  - XGBoost, LightGBM                                  │
│                                                         │
│  深度學習:                                            │
│  - TensorFlow, PyTorch, Keras                         │
│  - 預訓練模型庫                                       │
│                                                         │
│  資料處理:                                            │
│  - Pandas, Dask                                       │
│  - Vaex, Modin                                        │
│                                                         │
│  部署:                                               │
│  - Flask, Django                                       │
│  - Docker, Kubernetes                                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 2018 年展望

Python 3.7 預計帶來：
- 更快啟動速度
- 更好的 async/await
- Data Classes 標準化

---

**延伸閱讀**

- [Python Official Website](https://www.google.com/search?q=Python+official)
- [Python 3.6 Release Notes](https://www.google.com/search?q=Python+3.6+release+notes)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*