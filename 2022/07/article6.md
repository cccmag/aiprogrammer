# 去重與模糊比對

## 大規模語料庫的去重演算法實戰

### 為什麼需要去重

在 Common Crawl 的資料中，約有 10-20% 的內容是重複的。重複內容會導致訓練偏差、計算浪費、評估失真等問題。

### 精確去重

對於完全相同的文本，使用雜湊函數是最快的方法：

```python
import hashlib

def exact_dedup(documents):
    seen = set()
    unique = []
    for doc in documents:
        h = hashlib.md5(doc.encode('utf-8')).hexdigest()
        if h not in seen:
            seen.add(h)
            unique.append(doc)
    return unique
```

### 近似去重

網路上的重複內容很少完全一致。同一篇文章被不同網站轉載時，會加入不同的廣告或修改部分文字。這時需要近似去重技術。

**MinHash：**
用於估計集合相似度，廣泛應用於大規模去重：

```python
def minhash_signature(text, num_hashes=100):
    shingles = {hash(text[i:i+5]) for i in range(len(text)-5)}
    return [min(h ^ i for h in shingles) for i in range(num_hashes)]
```

**SimHash：**
Google 使用的去重演算法，將文本轉換為固定長度指紋，透過漢明距離判斷相似度：

```python
def simhash(text, bits=64):
    v = [0] * bits
    for word in text.split():
        h = hash(word)
        for i in range(bits):
            v[i] += 1 if h & (1 << i) else -1
    return sum((1 << i) for i in range(bits) if v[i] > 0)
```

### 行級去重

C4 語料庫使用的方法：如果一行出現在多個文件中，該行很可能是廣告或導覽列，應移除。

```python
from collections import Counter

def line_level_dedup(documents):
    counts = Counter()
    for doc in documents:
        for line in set(doc.split('\n')):
            counts[line.strip()] += 1
    return ['\n'.join(line for line in doc.split('\n')
            if counts.get(line.strip(), 0) <= 1) for doc in documents]
```

### 實務建議

大規模去重應遵循分而治之原則：先精確去重，再近似去重，最後行級去重。使用 Spark 或 Ray 進行分布式處理。相似度閾值通常設為 0.7-0.9。

---

## 延伸閱讀

- [MinHash 演算法詳解](https://www.google.com/search?q=MinHash+algorithm+explained)
- [SimHash Google 去重演算法](https://www.google.com/search?q=SimHash+Google+near+duplicate+detection)
- [C4 資料集去重策略](https://www.google.com/search?q=C4+dataset+deduplication+strategy)
