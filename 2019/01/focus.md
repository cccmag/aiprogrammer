# 主題總覽：Python 3.7 生態系

Python 3.7 于 2018 年 6 月發布，經過半年的發展，在 2019 年 1 月已成為新專案的首選版本。本期的主題是幫助讀者系統性地掌握 Python 3.7 的核心特性，這些特性對日常開發與資料科學工作都有重要影響。

## 為什麼要關注 Python 3.7？

Python 3.7 帶來了多項重大改進，特別是對非同步程式設計、型別安全與程式碼簡潔性的提升。這些改進使得 Python 更適合建構大型、複雜的應用程式，特別是在資料科學與機器學習領域。

## 核心特性地圖

### 1. asyncio 非同步程式設計
Python 3.7 強化了 asyncio 模組，使得非同步程式設計更加直覺。包括 asyncio.create_task()、asyncio.current_task() 等新 API，讓併發程式的撰寫更加簡單。

### 2. Type Hints 型態提示
Python 3.7 的型態提示更加成熟，配合 mypy、Pyright 等工具，可以在開發早期發現型別錯誤。這對於大型專案與團隊協作特別有價值。

### 3. Dataclasses 資料類別
Python 3.7 引入的@dataclass 裝飾器大幅簡化了資料類別的建立過程。自動生成的 __init__、__repr__、__eq__ 等方法減少了樣板程式碼。

### 4. 效能改進
Python 3.7 在啟動速度與執行效率上都有提升。 Faster CPython（PEP 587）計畫也在此時醞釀，預計為 Python 3.8 帶來更大幅度的效能改進。

## 學習路徑

建議依序閱讀 focus1 到 focus7，了解 Python 3.7 的完整生態系。article1 到 article5 聚焦於 Python 特性，article6 到 article10 則探討 Python 在機器學習領域的應用。

## 本期結構

- focus1–7：Python 3.7 核心特性深度解析
- article1–5：非同步程式設計與型態系統
- article6–10：Python 機器學習工具鏈
- _code/python37_features.py：Python 3.7 特性展示腳本

## 參考資源

- https://www.google.com/search?q=Python+3.7+features+asyncio+dataclass+type+hints+2019
- https://www.google.com/search?q=Python+3.7+performance+improvements+2019+ecosystem
- https://www.google.com/search?q=Python+3.7+migration+guide+from+3.6+new+features