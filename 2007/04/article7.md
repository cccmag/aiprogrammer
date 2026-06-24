# 機器翻譯新突破：統計翻譯模型的進展

## 前言

2007 年，機器翻譯領域正在經歷一場革命——從規則基礎的翻譯系統，到統計翻譯模型的轉變。

## 從規則到統計

### 傳統計翻譯（PBMT）

傳統的機器翻譯基於語言學規則：

```python
# 規則基礎翻譯
rules = [
    (['the', 'N'], ['the', 'N']),  # 英文保持
    (['V', 'the', 'N'], ['the', 'N', 'V']),  # 日文語序
]
```

### 統計機器翻譯（SMT）

2000 年代中期，IBM 提出的統計翻譯模型開始流行：

```python
# 簡化的統計翻譯
def translate(sentence, model, alignments):
    # 分詞
    words = sentence.split()

    # 翻譯每個詞
    translated = []
    for word in words:
        # 找到最可能的翻譯
        best = max(model[word], key=lambda x: x['probability'])
        translated.append(best['translation'])

    # 重新排序
    return reorder(translated, alignments)
```

## 翻譯模型的組成

```
統計機器翻譯模型：
─────────────────────
翻譯模型 P(e|f)    - 給定外語句子，找出最可能的翻譯
語言模型 P(e)      - 確保譯文流暢
解碼器             - 搜索最佳譯文
重排序模型         - 處理語序差異
```

## 主要進展

### 片語式翻譯

2005-2007 年，片語式翻譯（Phrase-based SMT）成為主流：

```python
# 片語翻譯
phrases = [
    ("我想", "I want"),
    ("去日本", "to go to Japan"),
    ("旅遊", "travel"),
]

# 翻譯
input_phrase = "我想去日本旅遊"
translations = match_phrases(input_phrase, phrases)
# ["I want", "to go to Japan", "travel"]
```

### 對齊模型

IBM 模型提供了語言對齊的數學框架：

```python
# IBM Model 1：簡化對齊
def alignment_model1(english, french, theta):
    log_prob = 0
    for e in english:
        # 對齊到任意外語詞
        probs = [theta[(e, f)] for f in french]
        log_prob += math.log(sum(probs))
    return log_prob
```

## 結語

統計機器翻譯的興起，標誌著 NLP 領域的「資料驅動」轉變。不再依賴人工編寫規則，而是從大量雙語語料中學習翻譯模式。

這種方法的限制——片語對齊的局限、缺乏語義理解——最終在 2016 年被神經網路翻譯（GNMT）克服。

---

## 延伸閱讀

- [Statistical+machine+translation+2007](https://www.google.com/search?q=Statistical+machine+translation+2007)
- [IBM+translation+models+phrase-based](https://www.google.com/search?q=IBM+translation+models+phrase-based)

---