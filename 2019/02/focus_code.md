# 程式碼說明 — 機器學習基礎展示

## 功能概述

`_code/ml_basics.py` 是一個展示機器學習基礎的腳本。包含監督式學習、非監督式學習、資料预处理等範例。

## demo() 函數說明

### 1. 監督式學習展示

展示分類問題的完整流程，包括資料分割、模型訓練、預測與評估。

### 2. 非監督式學習展示

展示 K-means 聚類與 PCA 降維的基本用法。

### 3. 資料预处理展示

展示 StandardScaler 標準化、訓練/測試分割等操作。

### 4. Pipeline 展示

展示如何使用 Pipeline 將多個步驟串聯。

## 執行方式

```bash
cd _code
python3 ml_basics.py
```

或使用測試腳本：

```bash
bash test.sh
```

## 輸出範例

```
============================================================
機器學習基礎展示
============================================================

[1] 監督式學習 - 分類
資料集大小: 150
訓練集: 120, 測試集: 30
分類報告:
              precision    recall  f1-score   support
      setosa       1.00      1.00      1.00        10
  versicolor       1.00      0.90      0.95        10
   virginica       0.91      1.00      0.95        10

[2] 非監督式學習 - K-means 聚類
集群中心:
[[ 0.663  0.656 ...]
 [ 1.932 -0.023 ...]
 ...]
集群標籤: [0 2 1 1 0 ...]

[3] 資料预处理 - StandardScaler
標準化前均值: [5.84 3.05 3.76 1.20]
標準化後均值: [ 5.84851852e-15 -6.49990848e-16 ...]

[4] Pipeline 展示
Pipeline 訓練集分數: 0.975
Pipeline 測試集分數: 0.967

============================================================
展示完成
============================================================
```

## 依賴

本腳本需要以下套件：
- numpy
- scikit-learn
- matplotlib

安裝方式：
```bash
pip install numpy scikit-learn matplotlib
```

## 練習題

1. 修改 K 值進行 K-means 聚類，觀察集群數量的影響
2. 嘗試不同的分類器（Random Forest、SVM），比較效能
3. 使用不同的 preprocessing 方法（MinMaxScaler）替換 StandardScaler

## 參考資源

- https://www.google.com/search?q=machine+learning+basics+Python+scikit-learn+tutorial+2019
- https://www.google.com/search?q=supervised+unsupervised+learning+example+Python+2019