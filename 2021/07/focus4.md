# 主題四：Tokenization 與詞彙化

## BPE、WordPiece、SentencePiece

### 1. 為什麼需要 Tokenization？

在將文字輸入神經網路之前，需要先將文字轉換為數字序列。這個過程稱為 Tokenization（分詞）。

**詞彙化面臨的挑戰**：
- 不同語言的詞邊界定義不同
- 開放詞彙問題：新詞不斷出現
- 罕見詞和未登錄詞（OOV）問題
- 輸入長度與詞彙量的權衡

### 2. 詞粒度分詞

最直觀的方法是基於單詞進行分詞：

```python
def naive_tokenize(text):
    """簡單的空格分詞"""
    return text.lower().split()

def whitespace_tokenizer(text):
    """正則表達式分詞"""
    import re
    return re.findall(r'\w+|[^\s\w]+', text.lower())
```

**問題**：
- 詞彙表過大（英語可達數百萬）
- 嚴重的 OOV 問題
- 無法處理新詞

### 3. Byte Pair Encoding (BPE)

BPE 是一種基於子詞的詞彙化方法，最初用於資料壓縮，後被 GPT 等模型採用：

```python
def learn_bpe(vocab, num_merges):
    """學習 BPE 分詞規則"""
    vocab = {tuple(word.split()): count for word, count in vocab.items()}
    merges = []

    for _ in range(num_merges):
        pairs = get_pair_counts(vocab)
        if not pairs:
            break
        most_common = max(pairs, key=pairs.get)
        merges.append(most_common)
        vocab = merge_vocab(vocab, most_common)

    return merges

def tokenize(text, vocab, merges):
    """使用 BPE 分詞"""
    tokens = list(text)
    for merge in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and (tokens[i], tokens[i+1]) == merge:
                new_tokens.append(tokens[i] + tokens[i+1])
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

**BPE 的優勢**：
- 控制詞彙表大小
- 有效處理罕見詞
- 保留詞根、詞綴等語言資訊

### 4. WordPiece

WordPiece 是 Google 為 BERT 開發的詞彙化方法，與 BPE 类似但略有不同：

**BPE 貪心選擇最高頻的相鄰 token 對**

**WordPiece 選擇使語料庫似然最大化增加的 token 對**

```python
def wordpiece_tokenize(text, vocab, unk_token='[UNK]'):
    """WordPiece 分詞"""
    tokens = []
    start = 0

    while start < len(text):
        end = len(text)
        while start < end and text[start:end] not in vocab:
            end -= 1

        if start == end:
            tokens.append(unk_token)
            start += 1
        else:
            tokens.append(text[start:end])
            start = end

    return tokens
```

### 5. SentencePiece

SentencePiece 是 Google 开发的更加通用的分詞庫，特點包括：

- **無需預先分詞**：直接作用於原始文字
- **統一處理空格**：將空格也視為一種 token
- **支援多種語言**：包括中文、日文等無明確詞邊界的語言

```python
import sentencepiece as spm

# 訓練
spm.SentencePieceTrainer.train(
    input='train.txt',
    model_prefix='m',
    vocab_size=8000,
    character_coverage=1.0,
    model_type='bpe'
)

# 使用
sp = spm.SentencePieceProcessor()
sp.load('m.model')

tokens = sp.encode('今天天氣很好', out_type='int')
text = sp.decode(tokens)
```

### 6. 中文分詞的特殊性

中文等東亞語言没有天然的詞邊界，需要特別處理：

**基於詞典的分詞**：
- 最小正向匹配、雙向最大匹配
- 簡單快速但準確度有限

**基於序列標註的分詞**：
- 將分詞視為每個字元的標註問題
- 使用 CRF 或神經網路

**基於子詞的分詞**：
- 直接使用 BPE/WordPiece
- 適用於中文但詞彙表可能很大

### 7. Tokenization 的最新進展

2021 年，一些新的分詞方法開始受到關注：

**Byte-level BPE**：
- 直接在 byte 層面進行分詞
- 完全避免 OOV 問題
- GPT-2、RoBERTa 採用類似方法

**Subword Regularization**：
- 在訓練時使用機率抽樣進行分詞
- 提高模型的魯棒性

**SentencePiece 的普及**：
- 被越來越多的模型採用
- 統一了不同語言的處理方式

---

## 延伸閱讀

- [BPE 演算法詳解](https://www.google.com/search?q=byte+pair+encoding+subword+tokenization)
- [SentencePiece 论文](https://www.google.com/search?q=sentencepiece+subword+tokenization+google)
- [中文分詞方法](https://www.google.com/search?q=chinese+word+segmentation+methods)