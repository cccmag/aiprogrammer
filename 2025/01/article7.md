# 字典與集合實戰

## 字典的進階特性

### 預設值處理

```python
# 傳統方式
counts = {}
fruits = ["蘋果", "香蕉", "蘋果", "橘子", "香蕉", "蘋果"]

for fruit in fruits:
    if fruit in counts:
        counts[fruit] += 1
    else:
        counts[fruit] = 1

print(counts)  # {'蘋果': 3, '香蕉': 2, '橘子': 1}
```

### 使用 defaultdict

```python
from collections import defaultdict

counts = defaultdict(int)  # 預設值為 0
for fruit in fruits:
    counts[fruit] += 1

print(dict(counts))  # {'蘋果': 3, '香蕉': 2, '橘子': 1}

# 分組
students = [
    ("A班", "Alice"),
    ("B班", "Bob"),
    ("A班", "Charlie"),
    ("B班", "Diana"),
]

groups = defaultdict(list)
for class_name, student in students:
    groups[class_name].append(student)

print(dict(groups))
# {'A班': ['Alice', 'Charlie'], 'B班': ['Bob', 'Diana']}
```

### 使用 Counter

```python
from collections import Counter

# 計數
text = "hello world hello python hello world"
word_counts = Counter(text.split())
print(word_counts)
# Counter({'hello': 3, 'world': 2, 'python': 1})

# 最常見的
print(word_counts.most_common(2))
# [('hello', 3), ('world', 2)]

# 合併計數
counter1 = Counter(['a', 'b', 'a', 'c'])
counter2 = Counter(['b', 'b', 'c', 'd'])
print(counter1 + counter2)  # Counter({'b': 3, 'a': 2, 'c': 2, 'd': 1})
```

## 字典的高階操作

### 字典合併

```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}

# Python 3.9+
merged = d1 | d2
print(merged)  # {'a': 1, 'b': 3, 'c': 4}

# 傳統方式
merged = {**d1, **d2}
print(merged)  # {'a': 1, 'b': 3, 'c': 4}
```

### 巢狀字典的存取

```python
data = {
    "users": {
        "alice": {"age": 25, "city": "台北"},
        "bob": {"age": 30, "city": "高雄"}
    }
}

# 安全存取巢狀資料
city = data.get("users", {}).get("alice", {}).get("city")
print(city)  # 台北
```

## OrderedDict 與排序

```python
from collections import OrderedDict

# Python 3.7+ 中，一般字典已保持插入順序
# OrderedDict 多了順序相關的方法

od = OrderedDict()
od["z"] = 1
od["a"] = 2
od["c"] = 3

# 移動到末尾
od.move_to_end("z")
print(list(od.keys()))  # ['a', 'c', 'z']

# 移動到開頭
od.move_to_end("z", last=False)
print(list(od.keys()))  # ['z', 'a', 'c']
```

## 集合的進階應用

### 集合的數學運算

```python
python_devs = {"Alice", "Bob", "Charlie", "David"}
java_devs = {"Charlie", "David", "Eve", "Frank"}

# 精通 Python 和 Java 的開發者
full_stack = python_devs & java_devs
print(f"兩者都會：{full_stack}")

# 只會 Python 的開發者
only_python = python_devs - java_devs
print(f"只會 Python：{only_python}")

# 至少會一種的開發者
any_skill = python_devs | java_devs
print(f"至少會一種：{any_skill}")

# 剛好只會一種的開發者
exactly_one = python_devs ^ java_devs
print(f"剛好只會一種：{exactly_one}")
```

### 集合用於去重與檢測

```python
# 檢查是否有重複
def has_duplicates(items):
    return len(items) != len(set(items))

print(has_duplicates([1, 2, 3, 4]))     # False
print(has_duplicates([1, 2, 2, 3, 4]))  # True

# 從列表中移除重複並保持順序
def unique_preserve_order(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

print(unique_preserve_order([3, 1, 2, 3, 1, 4, 5, 2]))
# [3, 1, 2, 4, 5]
```

## 實戰：文字分析工具

```python
import re
from collections import Counter, defaultdict

class TextAnalyzer:
    """文字分析工具"""

    def __init__(self, text):
        self.text = text
        self.words = self._tokenize()

    def _tokenize(self):
        """分詞"""
        words = re.findall(r'\b\w+\b', self.text.lower())
        return words

    def word_frequency(self, top_n=10):
        """詞頻統計"""
        return Counter(self.words).most_common(top_n)

    def word_length_distribution(self):
        """單詞長度分布"""
        distribution = defaultdict(int)
        for word in self.words:
            distribution[len(word)] += 1
        return dict(sorted(distribution.items()))

    def unique_words(self):
        """不重複單詞"""
        return set(self.words)

    def common_pairs(self):
        """相鄰詞對"""
        pairs = [f"{self.words[i]} {self.words[i+1]}"
                 for i in range(len(self.words)-1)]
        return Counter(pairs).most_common(5)

text = """
Python is an interpreted high-level general-purpose programming language.
Python's design philosophy emphasizes code readability with its notable use
of significant indentation. Its language constructs and object-oriented
approach aim to help programmers write clear logical code.
"""

analyzer = TextAnalyzer(text)
print("=== 詞頻統計 ===")
for word, count in analyzer.word_frequency(5):
    print(f"{word}: {count}")

print("\n=== 單詞長度分布 ===")
for length, count in analyzer.word_length_distribution().items():
    print(f"長度 {length}: {count} 個")
```

## 小結

字典與集合是 Python 中最實用的資料結構。字典提供了靈活的鍵值對儲存，集合則提供了高效的數學運算。結合 `collections` 模組中的 `defaultdict`、`Counter` 和 `OrderedDict`，你可以簡潔且高效地解決各種資料處理問題。

---

**延伸閱讀**

- [Python collections 模組](https://www.google.com/search?q=Python+collections+module+tutorial)
- [Python 字典技巧](https://www.google.com/search?q=Python+dictionary+tips+and+tricks)
