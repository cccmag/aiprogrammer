# 預訓練與資料（2018-2026）

## 預訓練目標

大型語言模型的核心在於預訓練—在大規模無標註資料上學習語言的統計規律。不同架構選擇了不同的預訓練目標：

### MLM — Masked Language Model（BERT, 2018）

隨機遮罩輸入中 15% 的 token，模型需要預測被遮罩的詞：

```
輸入: 我 [MASK] 自然語言處理
目標: 預測 → "愛"
```

BERT 使用雙向上下文，擅長理解任務（分類、NER、QA）。

### CLM — Causal Language Model（GPT, 2018）

從左到右自回歸地預測下一個 token：

```
輸入: 我 愛 自然 → 預測 語言
輸入: 我 愛 自然 語言 → 預測 處理
```

GPT 使用單向上下文，擅長生成任務。

### Seq2Seq — Span Corruption（T5, 2019）

T5 將文字片段替換為特殊哨兵 token，編碼器讀取損壞的文字，解碼器還原原始文字：

```
原始: "深度學習改變了世界"
        └──┘    └────┘
損壞: "深度學習 <X> 了 <Y>"
目標: "<X> 改變 <Y> 世界"
```

## 資料集規模、品質與去重

### 規模的演進

```
Common Crawl (2008-) : 每月 20-30 TB (原始網頁)
The Pile (2020)      : 825 GB (精選高品質)
C4 (2019)            : 750 GB (Common Crawl 清理版)
RedPajama-V2 (2023)  : 30 TB (開源重現 LLaMA 資料)
Dolma (2024)         : 3 TB (OLMo 訓練資料)
FineWeb (2024)       : 15 TB (最佳開源資料集)
```

### 品質過濾管道

```python
def filter_document(text):
    # 1. 語言偵測（只保留目標語言）
    if detect_language(text) != "zh":
        return None
    # 2. 去重（MinHash + LSH）
    if is_near_duplicate(text, existing_set):
        return None
    # 3. 啟發式過濾
    if len(text) < 200:        # 太短
        return None
    if perplexity(text) > 1000:  # 品質太差
        return None
    if is_toxic(text):          # 有毒內容
        return None
    return text
```

2024-2026 年的共識：**資料品質比數量更重要**。使用小量高品質資料訓練的小模型，往往能超越使用大量低品質資料的大模型。

## Tokenization

### BPE（Byte Pair Encoding）

BPE 從字元級別開始，反覆合併最常見的相鄰 token 對：

```
原始: l o w _ l o w e r _ l o w e s t
step 1: l o w → "low" (最常見的對)
step 2: low_ → "low_"
step 3: low_e → "lowe"
step 4: l o w e s t → "lowest"
最終詞彙: ["low", "low_", "lowe", "lowest", "e", "r", ...]
```

### SentencePiece 與 Byte-Level Tokenizer

Google 的 SentencePiece 將整個文字視為 Unicode 字元序列，不依賴空格分割——對中文特別重要：

```
Tokenization 對比：
─────────────────────────
BPE (GPT-2):     "我愛AI" → ["我", "愛", "AI"]
                  (需預先分詞)

SentencePiece:   "我愛AI" → ["我", "愛", "A", "I"]
                  (無需預分詞，純資料驅動)
```

Byte-Level Tokenizer (GPT-4、Claude 3) 進一步將輸入視為 byte 序列，保證任何字元都可表示，詞彙表固定在 100K 左右。

### Rust tokenizers crate

Hugging Face 的 `tokenizers` 庫底層使用 Rust 實作，提供 Python 綁定：

```rust
use tokenizers::tokenizer::{Tokenizer, Model};
use tokenizers::models::bpe::BPE;

fn train_tokenizer(files: &[&str]) -> Tokenizer {
    let mut tokenizer = Tokenizer::new(BPE::default());
    tokenizer.train(files)?;
    tokenizer.save("tokenizer.json", false)?;
    tokenizer
}
```

透過 `tokenizers` crate，可以在 Rust 中直接訓練和執行 tokenizer，獲得遠優於 Python 實作的效能。

---

## 延伸閱讀

- [BERT 預訓練論文](https://www.google.com/search?q=BERT+pre-training+deep+bidirectional+transformers)
- [T5 統一框架](https://www.google.com/search?q=T5+Exploring+the+Limits+of+Transfer+Learning+with+a+Unified+Text-to-Text+Transformer)
- [BPE Tokenization 說明](https://www.google.com/search?q=Byte+Pair+Encoding+tokenization+explained)
- [FineWeb 資料集](https://www.google.com/search?q=FineWeb+decoupled+web+dataset+for+LLM)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
