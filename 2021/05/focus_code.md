# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/dl_theory.py`，使用純 Python 和 NumPy 從頭實作深度學習的核心理論。包含反向傳播、優化器、正則化等核心概念的簡化實現。程式碼以教學為目的，幫助讀者建立從數學到程式的直覺。

## 元件說明

### `sigmoid` 和 `relu` 激活函數

實現兩種常見的激活函數及其導數。sigmoid 將輸入映射到 (0,1)，導數可以用輸出值簡便計算。ReLU 是最常用的激活函數，簡單但高效。

### `compute_loss`

交叉熵損失的實現。對於 one-hot 編碼的標籤和 softmax 輸出，可簡便計算損失值及其梯度。這是分類任務的標準損失函數。

### `backward_pass`

實現完整的三層網路的反向傳播。從輸出層反向計算每層的梯度，展示鏈式法則的實際應用。包含梯度的矩陣形式實現，與框架的自動微分對應。

### 優化器模擬

實現簡化的 SGD 和 Adam 優化器步驟。SGD 展示最簡單的梯度下降。Adam 展示如何維護一二階矩估計並計算自適應學習率。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 dl_theory.py`。`demo()` 函式展示完整流程：初始化網路、向前傳播、向後傳播、參數更新，驗證各步驟的正確運作。

## 參考資源

- Neural Networks from Scratch：https://www.google.com/search?q=neural+network+from+scratch+python
- Deep Learning Theory：https://www.google.com/search?q=deep+learning+theory+fundamentals