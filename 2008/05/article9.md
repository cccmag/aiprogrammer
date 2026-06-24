# 自然語言處理的統計方法

## N-gram 模型

```python
# Bigram 模型
def bigram(sentence):
    words = sentence.split()
    return [(words[i], words[i+1]) for i in range(len(words)-1)]
```

## 應用

- 語音辨識
- 機器翻譯

## 結論

統計方法主導了 NLP 領域數十年。

---

**延伸閱讀**

- [NLP+statistical+methods](https://www.google.com/search?q=statistical+NLP+methods)