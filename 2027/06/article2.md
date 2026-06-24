# Tokenization 深入：從 BPE 到 SentencePiece

## 前言

Tokenization 是 NLP 管線的第一步，也是最常被忽略的關鍵環節。所有大型語言模型都依賴 tokenizer 將文字轉換為模型可處理的整數序列。你可能不知道，市面上每一個 LLM 的詞彙表大小與分詞策略，深刻影響著模型的表現：中文 tokenizer 是否能有效分割漢字？程式碼中的縮排與特殊符號是否被妥善處理？這些問題都直接關聯到模型的理解能力。本文將深入探討主流的分詞演算法，從 Byte-Pair Encoding (BPE) 到 SentencePiece，並實作一個簡易的 BPE tokenizer。

## 為什麼需要 Tokenizer？

Tokenization 解決了詞彙表大小的問題。若以字元為單位，序列過長且難以捕捉語義；若以詞為單位，詞彙表會膨脹到數十萬且無法處理未登錄詞（Out-of-Vocabulary）。子詞（subword）分詞是兩者的折衷方案，也是當前 LLM 的標準做法。舉例來說，「Transformer」這個詞可能被分割為「Transform」和「er」兩個子詞，這樣即使模型在訓練時沒看過「Transformer」，也能透過已知的子詞組合來推測其意義。這種靈活性是現代 NLP 系統能夠處理開放詞彙的關鍵。

## Byte-Pair Encoding (BPE)

BPE 最初是資料壓縮演算法，由 Sennrich 等人於 2016 年首次引入 NLP 領域。它的核心概念非常直觀：從字元級別開始，反覆掃描訓練語料，找出最頻繁出現的相鄰符號對，將它們合併為一個新的符號。這個過程不斷重複，直到詞彙表達到預設的大小為止。GPT 系列模型從 GPT-2 開始就使用 BPE 作為分詞演算法，後續的 Llama 系列也沿用此方法。

```python
from collections import Counter
import re

def get_stats(vocab):
    pairs = Counter()
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs

def merge_vocab(pair, vocab):
    new_vocab = {}
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    for word, freq in vocab.items():
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = freq
    return new_vocab

# 範例：從單字頻率表學習 BPE
vocab = {
    "l o w </w>": 5, "l o w e r </w>": 2,
    "n e w e s t </w>": 6, "w i d e s t </w>": 3
}
num_merges = 10
for i in range(num_merges):
    pairs = get_stats(vocab)
    if not pairs:
        break
    best = pairs.most_common(1)[0][0]
    vocab = merge_vocab(best, vocab)
    print(f"合併 {i+1}: {best}")

# 編碼新文字
def bpe_encode(text, merges):
    words = text.split()
    encoded = []
    for word in words:
        symbols = list(word) + ['</w>']
        while len(symbols) > 1:
            pairs = [(symbols[i], symbols[i+1]) for i in range(len(symbols)-1)]
            candidates = [(pair, merges.get(pair, float('inf'))) for pair in pairs]
            best_pair = min(candidates, key=lambda x: x[1])[0]
            if best_pair not in merges:
                break
            symbols = merge_pair(symbols, best_pair)
        encoded.append(' '.join(symbols))
    return encoded
```

## WordPiece

WordPiece 是 BERT 使用的分詞演算法，由 Google 開發。與 BPE 的差異在於：BPE 以頻率為合併依據，WordPiece 則以互資訊（PMI）最大化為目標：

```
Score = freq(pair) / (freq(first) * freq(second))
```

## Unigram Language Model

Unigram 分詞由 SentencePiece 支援，以機率模型為基礎。與 BPE/WordPiece 的貪婪合併不同，Unigram 先建立大量候選子詞，再逐步刪除使 Loss 增加最小的子詞：

```python
# 概念示意：Unigram 的 EM 訓練
def unigram_train(corpus, vocab_size):
    # 1. 建立 Seed 詞彙表（所有可能的子詞）
    # 2. EM 演算法估計每個子詞的機率
    # 3. 移除對 Loss 貢獻最小的子詞
    # 4. 重複直到詞彙表大小符合目標
    pass
```

## SentencePiece

SentencePiece 是 Google 開發的開源 tokenization 工具包，整合了 BPE 與 Unigram 兩種演算法。與傳統 tokenizer 最大的不同是：SentencePiece 將輸入視為 Unicode 字元序列，無須預先分詞（不依賴空格分割）：

```python
# 使用 SentencePiece 訓練 tokenizer
import sentencepiece as spm

spm.SentencePieceTrainer.train(
    input='corpus.txt',
    model_prefix='mymodel',
    vocab_size=32000,
    model_type='bpe',  # 或 'unigram'
    character_coverage=0.9995,
)

sp = spm.SentencePieceProcessor(model_file='mymodel.model')
print(sp.encode("大型語言模型", out_type=str))
# ['▁', '大', '型', '語', '言', '模', '型']
print(sp.encode("大型語言模型", out_type=int))
# [1423, 892, 4561, 278, 312, 5678, 1234]
```

SentencePiece 的「▁」字元代表原始文字中的空格，確保解碼時可還原。

## HuggingFace Tokenizers 函式庫

HuggingFace 的 `tokenizers` 函式庫提供高速實作（Rust 後端）：

```python
from tokenizers import Tokenizer, models, trainers

tokenizer = Tokenizer(models.BPE(unk_token="[UNK]"))
trainer = trainers.BpeTrainer(
    vocab_size=30000,
    special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"]
)

files = ["corpus1.txt", "corpus2.txt"]
tokenizer.train(files, trainer)
tokenizer.save("my_tokenizer.json")

# 使用
output = tokenizer.encode("Transformer 架構")
print(output.tokens)
# ['Transformer', '架', '構']
```

## 特殊 Token 與詞彙管理

現代 LLM 的 tokenizer 包含多種特殊 token：

- `<|begin_of_text|>` / `<|end_of_text|>`：序列邊界
- `<|pad|>`：批次對齊填充
- `<|unk|>`：未知字元
- `<|system|>` / `<|user|>` / `<|assistant|>`：角色標記（Chat 模型）
- `<|tool_call|>`：工具呼叫標記

## 比較與選擇建議

| 方法 | 代表模型 | 優點 | 缺點 |
|------|---------|------|------|
| BPE | GPT-4, Llama 3 | 實作簡單，效率高 | 無法保證可逆性 |
| WordPiece | BERT | 語義分割較佳 | 訓練較慢 |
| Unigram | XLNet, T5 | 詞彙大小可控 | 訓練複雜 |

## 參考資源

- [BPE 原始論文](https://www.google.com/search?q=Neural+Machine+Translation+of+Rare+Words+with+Subword+Units)
- [SentencePiece 官方文件](https://www.google.com/search?q=sentencepiece+github+google)
- [HuggingFace Tokenizers 教學](https://www.google.com/search?q=huggingface+tokenizers+library+tutorial)
