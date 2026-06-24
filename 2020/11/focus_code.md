# MapReduce 實作：簡化版 MapReduce 框架

## 前言

MapReduce 是分散式處理大規模數據的經典程式模型。本篇文章將帶來一個簡化版的 MapReduce 實作，幫助讀者理解其核心概念。

---

## 原始碼

完整的 Python 實作請參考：[_code/mapreduce.py](_code/mapreduce.py)

```python
#!/usr/bin/env python3
"""簡化版 MapReduce 框架"""

from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Any
import multiprocessing as mp

def map_wrapper(args):
    """包裝 map 函數以支援 multiprocessing"""
    map_func, key_values = args
    results = []
    for key, value in key_values:
        for result in map_func(key, value):
            results.append(result)
    return results

def shuffle_and_sort(mapped_results: List[Tuple]) -> Dict:
    """將 map 輸出按 key 分組並排序"""
    grouped = defaultdict(list)
    for key, value in mapped_results:
        grouped[key].append(value)
    return dict(grouped)

def reduce_wrapper(args):
    """包裝 reduce 函數以支援 multiprocessing"""
    reduce_func, key, values = args
    return (key, reduce_func(key, values))

def map_reduce(
    data: List[Any],
    map_func: Callable,
    reduce_func: Callable,
    num_workers: int = 4
) -> List[Tuple]:
    """
    簡化版 MapReduce
    
    參數：
    - data: 輸入資料
    - map_func: Map 函數，接受 (key, value) 返回 [(key, value)] 的列表
    - reduce_func: Reduce 函數，接受 (key, values) 返回 (key, result)
    - num_workers: 並行 worker 數量
    
    返回：
    - List[Tuple]: 最終結果
    """
    print(f"MapReduce 開始處理，{len(data)} 條資料，{num_workers} 個 worker")
    
    # Step 1: Map 階段
    print("Map 階段...")
    with mp.Pool(num_workers) as pool:
        chunk_size = max(1, len(data) // num_workers)
        chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
        
        # 每個 chunk 呼叫 map_func
        map_results = []
        for chunk in chunks:
            for item in chunk:
                map_results.extend(map_func(None, item))
    
    # Step 2: Shuffle 階段
    print("Shuffle 階段...")
    shuffled = shuffle_and_sort(map_results)
    print(f"  {len(shuffled)} 個唯一的 key")
    
    # Step 3: Reduce 階段
    print("Reduce 階段...")
    results = []
    for key, values in shuffled.items():
        result = reduce_func(key, values)
        results.append(result)
    
    return results

def demo():
    print("=" * 60)
    print("MapReduce 實作演示")
    print("=" * 60)

    # 測試資料：文檔集合
    documents = [
        "hello world",
        "hello python",
        "world of programming",
        "python is great",
        "hello everyone"
    ]

    # Map 函數
    def word_count_map(key, doc):
        for word in doc.split():
            yield (word.lower(), 1)
    
    # Reduce 函數
    def word_count_reduce(word, counts):
        return (word, sum(counts))
    
    # 執行 MapReduce
    result = map_reduce(
        documents,
        map_func=word_count_map,
        reduce_func=word_count_reduce,
        num_workers=2
    )
    
    print("\n結果：")
    for word, count in sorted(result):
        print(f"  {word}: {count}")

    print("\n" + "=" * 60)
    print("MapReduce 演示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()
```

---

## MapReduce 執行流程

```
MapReduce 流程：
────────────────────────────────

輸入: ["hello world", "hello python", ...]
                │
                ▼
        ┌───────────────┐
        │     Map       │
        │  平行執行     │
        └───────┬───────┘
                │
                ▼
        [("hello", 1), ("world", 1), ("hello", 1), ...]
                │
                ▼
        ┌───────────────┐
        │   Shuffle     │
        │ 分組排序       │
        └───────┬───────┘
                │
                ▼
        {"hello": [1, 1, 1], "world": [1, 1], ...}
                │
                ▼
        ┌───────────────┐
        │    Reduce     │
        │  平行執行     │
        └───────┬───────┘
                │
                ▼
        [("hello", 3), ("world", 2), ("python", 2), ...]
```

## 進階功能

### 自定義 Combiner

```python
# Combiner 是本地的 Reduce，可以在 Map 節點先進行一次聚合
# 減少網路傳輸的資料量

def word_count_combiner(word, counts):
    """在 Map 節點進行的局部聚合"""
    return (word, sum(counts))
```

### 分割與並行

```python
# 分割輸入資料
def split_input(data, num_splits):
    chunk_size = len(data) // num_splits
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
```

## 延伸閱讀

- [MapReduce 論文](https://www.google.com/search?q=MapReduce+Google+2004+paper)
- [Hadoop MapReduce](https://www.google.com/search?q=Hadoop+MapReduce+tutorial)
- [分散式計算概念](https://www.google.com/search?q=distributed+computing+MapReduce)

---

*本期程式實作到此結束。*