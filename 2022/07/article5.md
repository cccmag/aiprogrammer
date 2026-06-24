# 分詞技術：jieba、spaCy

## 中文與英文分詞工具的使用與比較

### 為什麼需要分詞

分詞是將連續的文字序列分割為最小語義單位的過程。對於英文等使用空白分隔單詞的語言，分詞看似簡單，但實際上子詞分詞（Subword Tokenization）已成為主流。對於中文、日文等沒有詞邊界的語言，分詞是 NLP 管線中的關鍵第一步。

### jieba 中文分詞

jieba 是 Python 生態系中最受歡迎的中文分詞庫，以其速度快、準確率高、易於使用而聞名。

```python
import jieba

text = "我來到北京清華大學"

# 精確模式（預設）
words = list(jieba.cut(text))
# ['我', '來到', '北京', '清華大學']

# 全模式
words = list(jieba.cut(text, cut_all=True))
# ['我', '來到', '北京', '清華', '清華大學', '華大', '大學']

# 搜尋引擎模式
words = list(jieba.cut_for_search(text))
# ['我', '來到', '北京', '清華', '大學', '清華大學']
```

jieba 的核心特性：

- **基於前綴詞典的分詞**：使用前綴詞典實現高效的詞圖掃描
- **HMM 模型**：使用隱馬可夫模型處理未登錄詞
- **自訂詞典**：可以加入領域特定詞彙
- **詞性標註**：支援詞性標註功能

### spaCy 分詞

spaCy 是一個工業級的 NLP 庫，支援多種語言。與 jieba 不同，spaCy 提供的是完整的 NLP 管線，而不僅僅是分詞。

```python
import spacy

# 載入英文模型
nlp_en = spacy.load('en_core_web_sm')
doc = nlp_en("Natural language processing is fascinating.")

for token in doc:
    print(token.text, token.pos_, token.dep_)
# natural ADJ amod
# language NOUN nsubj
# ...

# 載入中文模型
nlp_zh = spacy.load('zh_core_web_sm')
doc = nlp_zh("自然語言處理非常有趣。")

for token in doc:
    print(token.text, token.pos_)
```

spaCy 的優勢在於：

1. **完整的 NLP 管線**：分詞、詞性標註、依存分析、命名實體識別
2. **基於 CNN 或 Transformer 的模型**：使用深度學習提升準確率
3. **與 jieba 的整合**：spaCy 的中文模型底層使用 jieba 進行分詞
4. **高效能**：使用 Cython 實現，速度接近 jieba

### 子詞分詞

現代語言模型使用子詞分詞演算法來處理詞彙問題：

**BPE（Byte-Pair Encoding）：**
將詞彙分解為頻繁出現的子詞單元。例如 "unbelievable" 可能被分為 "un"、"believe"、"able"。

```python
from tokenizers import Tokenizer
from tokenizers.models import BPE

# 使用 Hugging Face tokenizers 庫
tokenizer = Tokenizer(BPE())
```

**WordPiece：**
Google 開發的子詞分詞演算法，用於 BERT 模型。與 BPE 類似，但使用不同合併規則。

**SentencePiece：**
Google 開發的無監督分詞器，支援直接從原始文字學習分詞，不需要預先分詞。

### 分詞工具的選擇指南

| 需求 | 推薦工具 |
|--------|---------|
| 快速中文分詞 | jieba |
| 完整 NLP 管線 | spaCy |
| 子詞分詞 | Hugging Face tokenizers |
| 大規模語料處理 | jieba（速度優先） |
| 學術研究 | spaCy（功能完整） |

### 實務提示

在大規模語料庫建構中，分詞的效率至關重要。對於 TB 級別的中文語料，jieba 的精確模式通常是最佳選擇。如果需要整合到深度學習管線中，使用 Hugging Face 的 tokenizers 庫進行子詞分詞是標準做法。

---

## 延伸閱讀

- [jieba 中文分詞 GitHub](https://www.google.com/search?q=jieba+chinese+text+segmentation+GitHub)
- [spaCy 官方文檔](https://www.google.com/search?q=spaCy+NLP+library+documentation)
- [Hugging Face Tokenizers 庫](https://www.google.com/search?q=huggingface+tokenizers+library)
