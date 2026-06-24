# 本期焦點

## 大規模語言模型：從 word2vec 到 GPT

### 引言

語言是人類智慧的基石，讓機器理解語言一直是人工智慧的核心目標。從早期的 n-gram 統計模型，到 word2vec 的詞向量革命，再到 BERT 和 GPT 等預訓練模型，語言模型的演進速度在過去十年中急劇加速。

本期雜誌將帶領讀者回顧這段精彩的技術演進歷程：

- **統計語言模型**：n-gram、平滑技術
- **神經詞嵌入**：Word2vec、GloVe、FastText
- **循環神經網路**：RNN、LSTM、GRU
- **序列到序列**：Seq2Seq、注意力機制
- **預訓練模型**：ELMo、BERT、GPT
- **提示工程與對話 AI**：現代應用的前沿

---

## 大綱

* [程式實作：語言模型入門](focus_code.md)
   - CBOW Word2Vec
   - RNN 語言模型
   - Beam Search 解碼
   - 困惑度計算

1. [語言模型導論：n-gram 到神經網路](focus1.md)
2. [Word2vec 與詞嵌入](focus2.md)
3. [RNN 語言模型](focus3.md)
4. [LSTM 與 GRU 序列建模](focus4.md)
5. [Seq2Seq 與注意力機制](focus5.md)
6. [ELMo、BERT 與雙向編碼](focus6.md)
7. [GPT 系列與生成式預訓練](focus7.md)

---

## 語言模型演進時間線

```
2013    word2vec (Mikolov)
2014    Seq2Seq (Sutskever), GloVe (Pennington)
2015    Attention (Bahdanau), LSTM 文本生成
2017    Transformer (Vaswani), FastText (Bojanowski)
2018    ELMo (Peters), BERT (Devlin), GPT (Radford)
2019    GPT-2, XLNet, RoBERTa
2020    GPT-3 (175B), T5
2021    Codex, DALL-E
2022    PaLM (540B), Chinchilla, OPT
```

### 從表示學習到生成式 AI

語言模型的發展可以分為三個階段：

**第一階段：靜態詞嵌入**。Word2vec 和 GloVe 為每個詞產生固定的向量表示，但無法處理一詞多義的問題。

**第二階段：上下文編碼**。ELMo 和 BERT 使用雙向語言模型，根據上下文動態調整詞表示，大幅提升了自然語言理解的能力。

**第三階段：生成式預訓練**。GPT 系列展示了大型語言模型在 zero-shot 和 few-shot 學習上的驚人能力，打開了生成式 AI 的大門。

---

**下一步**：[程式實作](focus_code.md) → [語言模型導論](focus1.md)

## 延伸閱讀

- [The Illustrated Word2vec](https://www.google.com/search?q=illustrated+word2vec)
- [Attention Is All You Need 解讀](https://www.google.com/search?q=Attention+Is+All+You+Need+explained)
- [BERT 論文詳解](https://www.google.com/search?q=BERT+paper+explained)
- [GPT-3 技術報告](https://www.google.com/search?q=GPT-3+paper+language+models+few+shot+learners)
