# MapReduce 與 Hadoop：大規模資料處理的先驅

## MapReduce 程式模型

### 基本概念

MapReduce 是一種編程模型，用於處理大規模資料集的並行運算。核心思想是將運算分為兩個階段：Map 和 Reduce：

```
MapReduce 資料流：
────────────────────────────────

輸入資料 ──► Map 階段 ──► Shuffle ──► Reduce 階段 ──► 輸出
                │                          ▲
                ▼                          │
           中間鍵值對                  排序後的
           (Key, Value)               鍵值組
```

### Map 和 Reduce 函數

```python
# Map 函數：將輸入轉換為鍵值對
def map_function(doc):
    """
    輸入：文檔
    輸出：(word, count) 的鍵值對
    """
    words = doc.split()
    return [(word, 1) for word in words]

# Reduce 函數：合併相同鍵的值
def reduce_function(key, values):
    """
    輸入：(word, [1, 1, 1, ...])
    輸出：(word, total_count)
    """
    return (key, sum(values))

# 範例：Word Count
documents = [
    "hello world",
    "hello python",
    "world of programming"
]

# Map 階段
mapped = []
for doc in documents:
    mapped.extend(map_function(doc))

print("Map 輸出:", mapped)
# [('hello', 1), ('world', 1), ('hello', 1), ('python', 1), ('world', 1), ('of', 1), ('programming', 1)]

# 這裡需要 shuffle（按 key 分組）- 實際由框架完成
# 模擬 shuffle 的結果
shuffled = {
    'hello': [1, 1],
    'world': [1, 1],
    'python': [1],
    'of': [1],
    'programming': [1]
}

# Reduce 階段
result = []
for key, values in shuffled.items():
    result.append(reduce_function(key, values))

print("最終結果:", result)
# [('hello', 2), ('world', 2), ('python', 1), ('of', 1), ('programming', 1)]
```

## Hadoop 生態系

### Hadoop 專案結構

```
Hadoop 生態系：
────────────────────────────────

┌─────────────────────────────────────────┐
│              Hadoop 生態系               │
├─────────────────────────────────────────┤
│  MapReduce    │ YARN    │    HDFS       │
│  (運算框架)   │(資源管理)│  (分散式檔案) │
├─────────────────────────────────────────┤
│         Hadoop Common (工具庫)           │
└─────────────────────────────────────────┘

其他相關專案：
- Hive: SQL on Hadoop
- HBase: NoSQL 資料庫
- Pig: 資料流語言
- Sqoop: 資料轉換工具
- Flume: 網頁日誌收集
```

### HDFS 架構

Hadoop Distributed File System 是 Hadoop 的分散式檔案系統：

```
HDFS 架構：
────────────────────────────────

           NameNode (主節點)
           ┌─────────────────┐
           │ 管理檔案系統    │
           │ 元數據         │
           │ 命名空間       │
           └────────┬────────┘
                    │  Metadata RPC
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
   ┌────────┐  ┌────────┐  ┌────────┐
   │DataNode│  │DataNode│  │DataNode│
   │        │  │        │  │        │
   │ Block  │  │ Block  │  │ Block  │
   │  A     │  │  A     │  │  B     │
   │  B     │  │  B     │  │  C     │
   └────────┘  └────────┘  └────────┘
   
特點：
- 資料複製（預設 3 份）
- 資料本地性運算
- 分割容錯
```

### YARN 資源管理器

YARN（Yet Another Resource Negotiator）是 Hadoop 2.0 引入的資源管理框架：

```
YARN 架構：
────────────────────────────────

      ┌───────────────────────────┐
      │     ResourceManager       │
      │  - 資源调度               │
      │  - 應用程式管理器         │
      └───────────┬───────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌────────┐   ┌────────┐    ┌────────┐
│NodeManager│ │NodeManager│  │NodeManager│
│         │   │         │    │         │
│Container│   │Container│    │Container│
└────────┘   └────────┘    └────────┘

YARN 的優勢：
- 資源利用率更高
- 支援多種計算框架
- 更靈活的排程
```

## Hadoop 的實際應用

### Word Count 範例

```python
# Hadoop Word Count（使用 Hadoop Streaming）

# mapper.py
#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    for word in words:
        print(f"{word}\t1")

# reducer.py
#!/usr/bin/env python3
import sys

current_word = None
current_count = 0

for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    count = int(count)
    
    if current_word == word:
        current_count += count
    else:
        if current_word:
            print(f"{current_word}\t{current_count}")
        current_word = word
        current_count = count

if current_word == word:
    print(f"{current_word}\t{current_count}")

# 執行命令
# hadoop jar hadoop-streaming.jar \
#   -input /input \
#   -output /output \
#   -mapper mapper.py \
#   -reducer reducer.py
```

### 分散式 Grep

```python
# mapper.py - 搜尋符合模式的行
import sys
import re

pattern = sys.argv[1]  # 從命令列獲取模式

for line in sys.stdin:
    line = line.strip()
    if re.search(pattern, line):
        print(line)  # 直接輸出（key 為空）

# reducer.py - 保持輸出唯一
seen = set()
for line in sys.stdin:
    line = line.strip()
    if line not in seen:
        seen.add(line)
        print(line)
```

## Hadoop 的局限性

### MapReduce 的缺點

```
Hadoop/MapReduce 的問題：
────────────────────────────────

1. 過度傾例於批次處理
   └── 不適合即時查詢
   
2. 高延遲
   └── 啟動 Task 需要較長時間
   
3. 複雜的 I/O
   └── 中間結果寫入磁片
   
4. 難以表達複雜計算
   └── 迭代演算法效率低
   └── 互動式分析不適合
```

### 為什麼需要 Spark？

```
Spark vs MapReduce：
────────────────────────────────

特性          │ MapReduce  │ Spark
──────────────│────────────│────────
中間結果      │ 磁片       │ 記憶體
延遲         │ 高         │ 低
迭代計算     │ 低效       │ 高效
互動式分析   │ 困難       │ 支援
API 複雜度   │ 高         │ 低
學習曲線     │ 陡峭       │ 較平緩
```

## 延伸閱讀

- [MapReduce 原始論文](https://www.google.com/search?q=MapReduce+Google+2004+paper)
- [Hadoop 官方網站](https://www.google.com/search?q=Apache+Hadoop+official)
- [HDFS 架構指南](https://www.google.com/search?q=HDFS+architecture+guide)
- [YARN 資源管理器](https://www.google.com/search?q=YARN+Hadoop+resource+manager)
- [Hadoop Word Count 教學](https://www.google.com/search?q=Hadoop+Word+Count+tutorial)

---

*本篇文章為「AI 程式人雜誌 2020 年 11 月號」歷史回顧系列之一。*