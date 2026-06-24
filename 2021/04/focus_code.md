# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/data_tools.py`，展示 Python 資料科學工具鏈的核心功能。包含 NumPy 向量化操作、pandas DataFrame 處理、以及簡單的資料處理流程。程式碼無需額外依赖，僅使用 Python 標準庫和 NumPy、pandas。

## 程式結構

### NumPy 基礎

展示向量建立、形状操作、索引、切片等基礎功能。`create_sample_data()` 函數創建示範用的NumPy 陣列，支援不同形狀和資料類型。`numpy_operations()` 展示向量化和廣播的基本用法。

### pandas DataFrame 處理

展示 DataFrame 的建立、常見操作、分組聚合等。`pandas_operations()` 函數演示典型資料處理流程：讀取資料、清洗、轉換、聚合。`grouped_aggregation()` 展示 groupby 的各種聚合方式。

### 資料處理流程

`process_data_pipeline()` 整合以上概念，實現一個簡單的 ETL 流程：從原始資料提取、轉換為所需格式、載入（此處為返回）。這個模式可扩展至真實的資料流水線。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 data_tools.py`。`demo()` 函式展示完整流程：創建資料、處理、聚合，驗證各元件的正確運作。

## 參考資源

- NumPy 官方教程：https://www.google.com/search?q=numpy+tutorial+beginners
- Pandas 官方教程：https://www.google.com/search?q=pandas+tutorial+data+analysis