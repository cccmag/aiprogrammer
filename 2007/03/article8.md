# 分散式計算：Hadoop 的誕生

## 前言

Hadoop 在 2007 年持續發展，成為大資料處理的重要框架。

## MapReduce 範例

```python
# MapReduce 概念
# Map: 處理原始資料
def map_function(line):
    words = line.split()
    return [(word, 1) for word in words]

# Reduce: 汇总結果
def reduce_function(word, counts):
    return (word, sum(counts))

# 偽代碼
# "hello world hello" -> [("hello", 1), ("world", 1), ("hello", 1)]
# reduce("hello", [1, 1]) -> ("hello", 2)
```

## 結論

Hadoop 的分散式運算模式改變了大資料處理的遊戲規則。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」文章集錦系列。*