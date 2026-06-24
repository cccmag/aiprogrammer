# 詞彙化與位置編碼

## 詞彙化（Tokenization）

### 傳統方法的問題

- **Word-level**：詞彙量龐大，OOV 問題嚴重
- **Character-level**：序列過長，語義資訊不足

### BPE（Byte Pair Encoding）

BPE 是一種常見的子詞分割方法：

```
步驟：
1. 初始化詞彙表為所有單字符
2. 統計相鄰 pair 的頻率
3. 合併最高頻率的 pair
4. 重複直到達到目標詞彙量
```

優點：
- 平衡詞彙量與語義完整性
- 能處理未登錄詞

### WordPiece 與 SentencePiece

- **WordPiece**：基於機率的分割，用於 BERT
- **SentencePiece**：將空白也視為一種 token

## 位置編碼（Positional Encoding）

### 為何需要位置編碼？

Transformer 的自注意力機制是位置無關的，但序列順序對語義很重要。

### 解決方案：正弦/餘弦位置編碼

```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

優點：
- 可以推廣到任意長度
- 為每個位置提供唯一編碼

### 其他位置編碼方案

- **相對位置編碼**：關注相對距離
- **旋轉位置編碼（RoPE）**：更高效的表示
- **學習式位置編碼**：端到端學習

---

## 延伸閱讀

- [BPE+演算法詳解](https://www.google.com/search?q=byte+pair+encoding+algorithm)
- [位置編碼比較](https://www.google.com/search?q=positional+encoding+transformer)
- [WordPiece+vs+BPE](https://www.google.com/search?q=wordpiece+vs+bpe+tokenization)

*本篇文章為「AI 程式人雜誌 2021 年 1 月號」精選文章。*