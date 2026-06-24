# 文本預處理管線

## 從原始文字到結構化語料

### 預處理的目標

在完成 HTML 標籤去除和文字清洗後，我們得到的是乾淨但仍是原始的文字。文本預處理的目標是將這些文字轉換為適合機器學習模型處理的結構化格式。這個過程通常包括分句、分詞、標準化等步驟。

### 分句

分句是將連續的文字分割為句子單位的過程。對於英文，句點、問號、感嘆號通常是句子邊界。但需要處理縮寫詞（如 "Dr."、"U.S."）帶來的歧義。

Python 中可以使用 `nltk.tokenize.sent_tokenize`：

```python
from nltk.tokenize import sent_tokenize

text = "Dr. Smith went to Washington. He met with the president."
sentences = sent_tokenize(text)
# ['Dr. Smith went to Washington.', 'He met with the president.']
```

中文分句則相對複雜，因為中文不使用空格分隔單詞。常見的中文分句方法是基於標點符號：

```python
import re

def split_chinese_sentences(text):
    sentences = re.split(r'(?<=[。！？；])', text)
    return [s.strip() for s in sentences if s.strip()]
```

### 分詞

分詞是將句子分割為詞彙或子詞單位的過程。不同語言有不同的分詞策略：

**英文分詞：** 基於空白和標點符號的簡單分割通常已足夠。更先進的方法使用 BPE（Byte-Pair Encoding）或 WordPiece 等子詞分詞演算法。

```python
# 簡單分詞
tokens = text.lower().split()

# 使用 NLTK
from nltk.tokenize import word_tokenize
tokens = word_tokenize(text)

# 使用 spaCy
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(text)
tokens = [token.text for token in doc]
```

**中文分詞：** 中文沒有詞邊界，需要專門的分詞工具。jieba 是最受歡迎的中文分詞庫：

```python
import jieba

text = "自然語言處理是人工智慧的重要分支"
words = list(jieba.cut(text))
# ['自然語言', '處理', '是', '人工智慧', '的', '重要', '分支']
```

### 標準化流程

一個完整的預處理管線可以封裝為以下步驟：

```python
def preprocessing_pipeline(text):
    # 1. 分句
    sentences = sent_tokenize(text)

    # 2. 分詞
    tokenized_sentences = []
    for sent in sentences:
        tokens = word_tokenize(sent.lower())
        # 3. 過濾停用詞
        tokens = [t for t in tokens if t not in stop_words]
        # 4. 詞幹提取（英文）
        tokens = [stemmer.stem(t) for t in tokens]
        tokenized_sentences.append(tokens)

    return tokenized_sentences
```

### 語料格式標準化

為了方便儲存和交換，語料庫通常使用標準化格式：

**JSONL（每行一個 JSON 物件）：**
```json
{"text": "This is a sentence.", "source": "wikipedia", "id": "001"}
{"text": "Another sentence.", "source": "wikipedia", "id": "002"}
```

**Parquet：**
列式儲存格式，支援壓縮和高效查詢，適合大型語料庫。

**Hugging Face Datasets 格式：**
將資料集包裝為 Apache Arrow 格式，支援記憶體映射和懶加載。

### 品質控制閾值

在預處理管線中，可以加入品質檢查步驟，過濾低品質內容：

- **最小句子長度**：過濾少於 10 個字元的句子
- **最大句子長度**：過濾過長的異常行
- **重複率**：過濾重複 n-gram 比例過高的文本
- **字母比例**：過濾非字母字元比例過高的行

---

## 延伸閱讀

- [NLTK 分句與分詞文檔](https://www.google.com/search?q=nltk+sentence+tokenization+documentation)
- [jieba 中文分詞庫](https://www.google.com/search?q=jieba+chinese+text+segmentation)
- [Hugging Face Datasets 格式說明](https://www.google.com/search?q=huggingface+datasets+format+arrow)
