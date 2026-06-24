# 程式碼說明 — ML 框架基礎展示腳本

## 功能概述

`_code/ml_demo.py` 展示了三大機器學習框架（TensorFlow、PyTorch、JAX）的基礎概念。此腳本可在沒有 GPU 的環境中執行，專注於展示框架的語法與概念。

## demo() 函數說明

### 1. NumPy 基礎
展示 NumPy 的基本操作，說明所有框架的 API 都與 NumPy 相容。

### 2. 自動微分概念
說明梯度計算是如何運作的，這是深度學習框架的核心功能。

### 3. 簡單神經網路
展示如何用 NumPy 實現一個極簡的神經網路前饋傳播。

### 4. 框架檢測
嘗試匯入各框架，顯示系統中安裝了哪些框架。

## 執行方式

```bash
cd _code
python3 ml_demo.py
```

或使用測試腳本：

```bash
cd _code
bash test.sh
```

## 輸出範例

```
============================================================
機器學習框架基礎展示
============================================================

[1] NumPy 基礎
    陣列建立：shape (3, 3)
    矩陣乘法結果：shape (3, 3)

[2] 自動微分概念
    函式 f(x) = x^2 在 x=3 的梯度：6

[3] 簡單神經網路
    前饋傳播完成（純 NumPy 實現）

[4] 框架檢測
    NumPy: 1.18.1
    (TensorFlow/PyTorch/JAX 需要單獨安裝)

============================================================
展示完成
============================================================
```

## 安裝框架

```bash
# TensorFlow
pip install tensorflow==2.1

# PyTorch
pip install torch torchvision

# JAX
pip install jax jaxlib
```

## 參考資源

- https://www.google.com/search?q=TensorFlow+PyTorch+JAX+installation+tutorial+2020
- https://www.google.com/search?q=NumPy+neural+network+from+scratch+Python+2020