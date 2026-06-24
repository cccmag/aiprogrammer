# Python 2020 年度回顧

## 前言

2020 年對 Python 來說是重要的一年。Python 3.9 發布、Python 2 正式終結、以及社群持續的成長。

## Python 3.9 新特性

```python
# 字典合併運算子
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}
merged = dict1 | dict2  # {"a": 1, "b": 3, "c": 4}
dict1 |= dict2          # 原地合併

# 字串方法增強
"hello world".removeprefix("hello ")  # "world"
"hello world".removesuffix(" world")  # "hello"

# 型別提示泛型
def process(items: list[str]) -> None:
    for item in items:
        print(item)
```

## Python 2 終結

```
Python 2 正式終結（2020年1月1日）：
────────────────────────────────

Python 2.7是最後一個 Python 2 版本

影響：
- 許多庫停止支援 Python 2
- 遷移到 Python 3 的壓力
- 但仍有大量 Python 2 程式碼在執行

統計：
- 2020 年仍有多少 Python 2 程式碼？
- 主要庫的 Python 3 支援情況
```

## Python 流行度

```
Python 在 2020 年：
────────────────────────────────

- 超越 Java，成為第二受歡迎語言
- 在 GitHub 上使用量排名第一
- 持續領導資料科學和 AI 領域
```

## 延伸閱讀

- [Python 3.9 新特性](https://www.google.com/search?q=Python+3.9+new+features)
- [Python 社群動態](https://www.google.com/search?q=Python+community+2020)

---

*本篇文章為「AI 程式人雜誌 2020 年 12 月號」文章集錦之一。*