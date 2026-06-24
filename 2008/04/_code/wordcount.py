#!/usr/bin/env python3
"""WordCount 示範 - 計算文字中每個單字出現的次數"""

def word_count(text):
    """計算文字中每個單字出現的次數"""
    words = text.lower().split()
    counts = {}
    for word in words:
        word = ''.join(c for c in word if c.isalnum())
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts

def demo():
    """示範函數"""
    text = """
    hello world hello
    python programming is great
    hello hadoop mapreduce
    big data processing with hadoop
    python java c++
    """

    print("=" * 50)
    print("WordCount 示範 - Hadoop MapReduce 概念展示")
    print("=" * 50)
    print("\n輸入文字:")
    print(text)

    result = word_count(text)

    print("\n單字計數結果:")
    print("-" * 30)
    for word, count in sorted(result.items(), key=lambda x: -x[1]):
        print(f"  {word}: {count}")

    print("\n" + "=" * 50)
    print("這模擬了 MapReduce 的工作流程：")
    print("Map: 將文字分割為 (word, 1) 鍵值對")
    print("Shuffle: 按鍵排序並合併")
    print("Reduce: 將相同鍵的值相加")
    print("=" * 50)

if __name__ == "__main__":
    demo()