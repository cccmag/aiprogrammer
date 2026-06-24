# 自然語言處理概論

## 前言

自然語言處理（Natural Language Processing, NLP）是人工智慧與語言學的交叉領域，專注於讓電腦理解、解讀和生成人類語言。2008 年時，統計方法開始主導 NLP 領域，為日後的深度學習時代奠定基礎。

## NLP 的歷史背景

### 規則方法 vs 統計方法

```python
# NLP 發展的兩個時代

nlp_eras = {
    "規則時代 (1950s-1990s)": {
        "方法": "手動定義語法規則",
        "代表": "Chomsky 句法理論",
        "優點": "可解釋性強",
        "缺點": "難以擴展、覆蓋率低"
    },
    "統計時代 (1990s-現在)": {
        "方法": "從大量資料學習模式",
        "代表": "HMM, CRF, 類神經網路",
        "優點": "覆蓋率高、適應性強",
        "缺點": "需要大量訓練資料"
    }
}
```

### 2008 年的 NLP 現況

2008 年是統計 NLP 的高峰期：

```python
nlp_state_2008 = {
    "主流方法": "統計機器學習",
    "訓練資料": "大量標註語料庫可用",
    "評測基準": "清晰的标准任務和資料集",
    "深度學習": "才剛開始應用，仍是邊緣技術"
}
```

## 核心任務

### 文字分類

```python
# 文字分類是什麼？
# 將文字文件歸類到預定義的類別

text_classification = {
    "任務": "新聞分類、垃圾郵件偵測、情緒分析",
    "輸入": "文字文件",
    "輸出": "類別標籤",
    "方法": ["Naive Bayes", "SVM", "邏輯回歸"]
}

# 範例：新聞分類
news_categories = [
    "政治", "科技", "體育", "娛樂", "財經"
]

# 流程
# 1. 文件轉向量（Bag of Words, TF-IDF）
# 2. 訓練分類器
# 3. 預測新文件類別
```

### 序列標註

```python
# 序列標註：為每個詞語預測一個標籤

sequence_labeling = {
    "詞性標註 (POS Tagging)": {
        "定義": "為每個詞預測其在句子中的詞性",
        "範例": "[John/NNP] [is/VBZ] [tall/JJ]"
    },
    "命名實體辨識 (NER)": {
        "定義": "識別文字中的人名、地名、組織等",
        "範例": "[John/NRP] 住在 [台北/NRL]",
        "應用": "資訊擷取、問答系統"
    }
}

# 常用方法
ner_methods = {
    "HMM": "隱藏馬可夫模型，生成模型",
    "CRF": "條件隨機場，判別模型（當時主流）",
    "類神經網路": "才剛開始使用"
}
```

### 句法分析

```python
# 句法分析：分析句子的文法結構

syntactic_parsing = {
    "類型": {
        " constituency parsing": "短語結構文法",
        " dependency parsing": "依存文法"
    },
    "輸出": " parse tree",
    "應用": ["機器翻譯", "資訊擷取", "問答系統"]
}

# 範例： constituency tree
# (S (NP (DT The) (NN cat))
#    (VP (VBD sat)
#        (PP (IN on)
#            (NP (DT the) (NN mat)))))
```

## 機器翻譯

### 統計機器翻譯

2008 年，統計機器翻譯（SMT）是主流：

```python
# 統計機器翻譯流程

statistical_mt = {
    "1. 平行語料": "雙語對齊文件",
    "2. 詞對齊": "找出對應的詞",
    "3. 翻譯模型": "P(目標|來源)",
    "4. 語言模型": "P(目標語句子)",
    "5. 解碼": "搜尋最佳譯文"
}

# IBM 模型（1990s）
ibm_models = {
    "Model 1": "詞對齊，僅計數",
    "Model 2": "加入對齊位置偏移",
    "Model 3": "加入 fertility",
    "Model 4": "相對位置偏移",
    "Model 5": "其他改進"
}
```

### 為何統計翻譯優於規則翻譯？

```python
# 規則翻譯 vs 統計翻譯

rule_based = {
    "優點": ["可解釋", "精確控制"],
    "缺點": ["需要大量專家知識", "難以處理多樣性", "擴展困難"]
}

statistical = {
    "優點": ["從資料自動學習", "處理多樣性", "持續改進"],
    "缺點": ["需要大量平行語料", "解釋性較差"]
}
```

## 資訊檢索

### 搜尋引擎技術

```python
# 資訊檢索基本概念

information_retrieval = {
    "目標": "從文件集合中找到相關文件",
    "核心問題": "哪些文件與查詢相關？",
    "典型應用": "網頁搜尋、新聞搜尋"
}

# 向量空間模型（Vector Space Model）
vector_space_model = {
    "文件表示": "文件轉為向量（TF-IDF）",
    "查詢表示": "查詢也轉為向量",
    "相似度計算": "餘弦相似度",
    "排序": "按相似度排序結果"
}
```

### PageRank 演算法

```python
# Google 的 PageRank（2008 年核心技術）

pagerank_concept = {
    "假設": "重要的網頁被重要的網頁引用",
    "原理": "隨機漫遊者訪問每個頁面的機率",
    "計算": "疊代計算直到收斂"
}

def pagerank(links, num_iterations=100, damping=0.85):
    n = len(links)
    scores = [1.0 / n] * n

    for _ in range(num_iterations):
        new_scores = [(1 - damping) / n] * n

        for i in range(n):
            for j in links[i]:
                new_scores[j] += damping * scores[i] / len(links[i])

        scores = new_scores

    return scores
```

## 文字探勘與 NLP

### 文件摘要

```python
# 文件摘要技術

text_summarization = {
    "抽取式": {
        "方法": "從原文中抽出重要句子",
        "優點": "簡單，保持原文語法",
        "缺點": "可能不通順"
    },
    "生成式": {
        "方法": "生成新的摘要文字",
        "優點": "更流暢",
        "缺點": "技術困難（2008 年尚未成熟）"
    }
}
```

### 情緒分析

```python
# 情緒分析（Sentiment Analysis）

sentiment_analysis_2008 = {
    "任務層級": {
        "文件層級": "整篇文件的正負傾向",
        "句子層級": "每個句子的傾向",
        "方面層級": "特定方面的評價（價格、品質等）"
    },
    "方法": {
        "基於詞典": "統計正面/負面詞數量",
        "監督學習": "用標註資料訓練分類器",
        "半監督": "少量標註 + 大量未標註"
    }
}
```

## 深度學習的萌芽

### 2008 年的類神經網路 NLP

```python
# 早期類神經網路在 NLP 的應用

neural_nlp_2008 = {
    "應用": [
        "語言模型 (Neural Language Model)",
        "詞向量 (Word Embeddings 早期研究)",
        "淺層網路用於分類"
    ],
    "瓶頸": [
        "計算成本高",
        "訓練資料不足",
        "深度學習技術不成熟"
    ]
}
```

### 詞向量（Word Embeddings）

```python
# 詞向量的概念（2008 年仍是研究階段）

word_embeddings = {
    "概念": "將詞語映射到連續向量空間",
    "優點": "捕捉語義相似性",
    "早期方法": "LSA, LDA",
    "突破方法": "Word2Vec (2013)"
}

# 範例
word_vector_analogy = {
    "範例": "king - man + woman ≈ queen",
    "意義": "向量運算能捕捉語意關係"
}
```

## 常見工具與資源

### 2008 年的 NLP 工具

```python
# 當時可用的工具

nlp_tools_2008 = {
    "NLTK": "Python 自然語言工具包（開放原始碼）",
    "Stanford NLP": "Java 實現的高品質分析器",
    "OpenNLP": "Apache 開源專案",
    "LingPipe": "文字分析工具包"
}

# NLTK 範例
nltk_example = {
    "斷詞": "word_tokenize(text)",
    "詞性標註": "pos_tag(tokens)",
    "命名實體辨識": "ne_chunk(tagged_tokens)",
    "句法分析": "stanford_parser.parse(sentence)"
}
```

### 語料庫

```python
# 常見的 NLP 語料庫（2008）

corpora_2008 = {
    "英文": {
        "Penn Treebank": "句法分析標註",
        "CoNLL": "NER、 chunking 等共享任務",
        "TREC": "資訊檢索評測",
        "Brown Corpus": "標準語料庫"
    },
    "中文": {
        "Sinica Corpus": "中央研究院中文語料庫",
        "LDC Chinese": "多種中文資源"
    }
}
```

## 未來展望

### 預測（2008 年的角度）

```python
# NLP 未來發展預測

nlp_predictions = {
    "短期 (2008-2010)": [
        "統計方法持續主導",
        "更多資源開放",
        "跨語言處理進步"
    ],
    "中期 (2010-2015)": [
        "深度學習開始流行",
        "神經機器翻譯興起",
        "端到端學習普及"
    ],
    "長期 (2015+)": [
        "Transformer 架構出現",
        "大型預訓練模型",
        "大型語言模型興起"
    ]
}
```

---

**延伸閱讀**

- [Natural language processing history](https://www.google.com/search?q=natural+language+processing+history)
- [Statistical+NLP+2008](https://www.google.com/search?q=statistical+NLP+2008)
- [Machine+translation+history](https://www.google.com/search?q=machine+translation+history)