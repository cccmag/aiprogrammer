#!/usr/bin/env python3
"""簡化版 MapReduce 框架"""

from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Any

def shuffle_and_sort(mapped_results: List[Tuple]) -> Dict:
    grouped = defaultdict(list)
    for key, value in mapped_results:
        grouped[key].append(value)
    return dict(grouped)

def map_reduce(
    data: List[Any],
    map_func: Callable,
    reduce_func: Callable,
) -> List[Tuple]:
    print(f"MapReduce 開始處理，{len(data)} 條資料")
    
    print("Map 階段...")
    map_results = []
    for item in data:
        for result in map_func(None, item):
            map_results.append(result)
    
    print("Shuffle 階段...")
    shuffled = shuffle_and_sort(map_results)
    print(f"  {len(shuffled)} 個唯一的 key")
    
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

    documents = [
        "hello world",
        "hello python",
        "world of programming",
        "python is great",
        "hello everyone"
    ]

    def word_count_map(key, doc):
        for word in doc.split():
            yield (word.lower(), 1)
    
    def word_count_reduce(word, counts):
        return (word, sum(counts))
    
    result = map_reduce(documents, word_count_map, word_count_reduce)
    
    print("\n結果：")
    for word, count in sorted(result):
        print(f"  {word}: {count}")

    print("\n" + "=" * 60)
    print("MapReduce 演示完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()