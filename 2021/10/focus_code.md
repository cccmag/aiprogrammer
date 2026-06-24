# 程式碼說明 — focus_code.md

## 概述

本期範例程式碼位於 `_code/testing.py`，展示 Python 測試的核心概念和工具實現。涵蓋單元測試、Mock、Fixtures 等測試基礎概念的簡化實現。程式碼使用純 Python，幫助讀者建立測試思維。

## 元件說明

### `TestRunner`

實現簡化的單元測試執行框架。收集測試方法、執行測試、計算通過/失敗數量。這展示了 pytest 等框架的基本原理。

### `AssertFunctions`

收集常用的斷言函式：`assert_equal`、`assert_true`、`assert_false`、`assert_raises`。這些是測試框架的基礎構造。

### `SimpleMock`

實現簡化的 Mock 物件。支援屬性訪問、返回值設置、呼叫計數追蹤。展示 Mock 的基本概念。

### `FixtureStore`

展示 Fixture 的管理機制：scope 控制生命週期、依賴解析、清理回呼。這是 pytest Fixtures 的核心概念模擬。

## 執行程式

```bash
cd _code
bash test.sh
```

`test.sh` 使用 `set -x` 顯示執行過程並呼叫 `python3 testing.py`。`demo()` 函式展示完整流程：單元測試執行、Mock 使用、Fixture 管理，驗證測試工具的正確運作。

## 參考資源

- pytest 官方文件：https://www.google.com/search?q=pytest+documentation
- Python unittest 文件：https://www.google.com/search?q=Python+unittest+documentation
- Hypothesis 屬性測試：https://www.google.com/search?q=Hypothesis+property+based+testing