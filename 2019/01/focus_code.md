# 程式碼說明 — Python 3.7 特性展示

## 功能概述

`_code/python37_features.py` 是一個展示 Python 3.7 核心特性的腳本。包含 dataclass、非同步程式設計、型態提示等範例。

## demo() 函數說明

### 1. dataclass 展示

展示如何使用 `@dataclass` 裝飾器建立資料類別，包括預設值、欄位選項與 frozen 模式。

### 2. asyncio 非同步展示

展示 asyncio 的基本用法，包括 create_task、gather、sleep 等常見操作。

### 3. Type Hints 展示

展示如何為函數與變數添加型態提示，以及使用 typing 模組的常見類型。

### 4. 效能展示

展示 dict 效能改進與字串格式化效能測試。

## 執行方式

```bash
cd _code
python3 python37_features.py
```

或使用測試腳本：

```bash
bash test.sh
```

## 輸出範例

```
============================================================
Python 3.7 特性展示
============================================================

[1] Data Class 展示
Point(x=1.0, y=2.0, label='')
Point 比較: False

[2] Async/Await 展示
開始非同步任務...
Task 1 完成
Task 2 完成
並行結果: ['Task 1 完成', 'Task 2 完成']

[3] Type Hints 展示
學生: Student(name='Bob', age=20, courses=['Math'])

[4] Dict 效能展示
Dict 大小: 10000
插入順序保證: True

============================================================
展示完成
============================================================
```

## 依賴

本腳本使用 Python 3.7 標準函式庫，無需額外安裝。

## 練習題

1. 修改 Point dataclass 加入 frozen=True 並嘗試修改實例
2. 新增一個異步任務並使用 gather 併發執行
3. 為自訂函數添加完整的型態提示

## 參考資源

- https://www.google.com/search?q=Python+dataclass+asyncio+type+hints+tutorial+examples+2019
- https://www.google.com/search?q=Python+3.7+features+demo+script+async+await+dataclass