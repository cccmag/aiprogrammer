# 主題一：Python 發展歷史與生態

## Python 的起源

Python 誕生於 1989 年的聖誕節，由荷蘭程式設計師 Guido van Rossum 創造。Guido 當時在荷蘭的 CWI（Centrum Wiskunde & Informatica）工作，想要開發一種易於閱讀和編寫的腳本語言。

Python 這個名字來自於英國喜劇團體 Monty Python，而非蛇。這反映了 Guido 的幽默感。

## 版本演進

### Python 1.x（1991-2000）

- Python 1.0 於 1991 年發布
- 包含函式程式設計特性：map、filter、reduce
- 早期的物件導向支援

### Python 2.x（2000-2010）

- Python 2.0 於 2000 年發布
- 引入垃圾回收機制（Garbage Collection）
- Unicode 支援改進
- 2006 年 Python 2.5 引入 with 語句
- 2008 年 Python 2.6 開始為 Python 3 做準備

### Python 3.x（2008-至今）

- Python 3.0 於 2008 年發布，這是一個破壞性改變的版本
- print 成為函式（`print()` 而非 `print`）
- 預設使用 Unicode 字串
- 去除了一些冗餘語法

**重要版本時間線**：
- Python 3.0：2008 年 12 月
- Python 3.2：2011 年 2 月
- Python 3.3：2012 年 9 月
- Python 3.4：2014 年 3 月
- Python 3.5：2015 年 9 月（預計）

## Python 2 vs Python 3

Python 3 引入了一些破壞性變更：

```python
# Python 2
print "Hello"  # 陳述式形式

# Python 3
print("Hello")  # 函式形式

# Python 2
x = raw_input()  # 回傳 str
x = input()  # 回傳 eval

# Python 3
x = input()  # 回傳 str，直接替換 raw_input
```

## 2015 年的生態狀況

### Python 2.7 仍是主流

儘管 Python 3 已經發布多年，2015 年時 Python 2.7 仍是大多數專案的首選。原因包括：
- 大量現有程式碼基於 Python 2
- 某些重要庫尚未完全支援 Python 3
- 遷移成本

### Python 3  adoption 加速

隨著 Python 3.4 的發布和更多庫支援 Python 3，越來越多的新專案開始採用 Python 3。

## Python 標準庫

Python 的標準庫非常豐富：

```python
import os          # 作業系統介面
import sys         # 系統相關參數
import json        # JSON 處理
import re          # 正規表達式
import datetime    # 日期時間
import collections # 容器資料型態
import itertools   # 迭代工具
import functools   # 函式工具
import random      # 隨機數
import math        # 數學函式
import csv         # CSV 處理
import urllib      # URL 處理
import sqlite3     # SQLite 資料庫
```

## 第三方庫生態

### pip 和 PyPI

pip 是 Python 的套件管理器，PyPI（Python Package Index）是 Python 第三方庫的主仓库。

```bash
# 安裝套件
pip install requests

# 列出已安裝的套件
pip list

# 顯示套件資訊
pip show requests
```

### 熱門套件

**Web 開發**：
- Django：全功能 Web 框架
- Flask：輕量級 Web 框架
- Pyramid：靈活的中型框架
- Bottle：極簡單框架

**資料科學**：
- NumPy：數值計算基礎
- SciPy：科學計算
- Pandas：資料分析
- Matplotlib：資料視覺化

**機器學習**：
- scikit-learn：機器學習工具
- TensorFlow：深度學習框架（2015 年 11 月發布）
- Theano：深度學習框架
- Keras：高級 Neural Networks API

## Python 社群

### PSF（Python Software Foundation）

Python 軟體基金會成立於 2001 年，致力於推廣和保護 Python 語言。

### 會議和活動

- PyCon US：美國 Python 會議
- EuroPython：歐洲 Python 會議
- PyCon APAC：亞太區 Python 會議
- 各地的 Python Meetup

## 應用領域

Python 廣泛應用於：
- Web 和網際網路開發
- 教育和教學
- 科學和數值計算
- 資料分析
- 機器學習和 AI
- 自動化腳本和系統管理
- 遊戲開發
- 桌面應用程式

Python 的多樣性和靈活性使其成為最受歡迎的程式語言之一。