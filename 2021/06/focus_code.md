# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/distributed.py`，展示分散式訓練的核心概念和簡化實現。包含資料平行、模型分片、梯度 checkpointing 等核心概念的教學實現。程式碼使用純 Python 和 NumPy，幫助讀者建立分散式訓練的直覺。

## 元件說明

### `AllReduce`

實現簡化的 Ring-AllReduce 演算法。每個節點與兩個鄰居交換資料，最終所有節點獲得相同的總和平均值。這是分散式訓練中梯度同步的核心操作。

### `GradientCheckpointing`

實現梯度 checkpointing 的概念。保存部分活化值，在 backward 時重新計算節省記憶體。這個概念演示了計算換記憶體的策略。

### `ZeROStage1` 模擬

展示 ZeRO Stage 1 的核心思想：將優化器狀態分片到不同節點。每個節點只保存 1/N 的優化器狀態，大幅減少記憶體使用。

### 分散式資料處理

模擬資料分發和聚合的過程。展示如何將資料分割到多個節點，以及如何收集和處理來自多個節點的結果。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 distributed.py`。`demo()` 函式展示完整流程：初始化節點、資料分割、平行計算、梯度同步，驗證各步驟的正確運作。

## 參考資源

- Distributed Training Concepts：https://www.google.com/search?q=distributed+training+concepts+tutorial
- DeepSpeed Examples：https://www.google.com/search?q=DeepSpeed+examples+GitHub