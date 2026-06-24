# 本期焦點

## Transformer 架構深入：從 Attention 到大型預訓練模型

### 引言

2017 年，Google 發表了「Attention is All You Need」論文，提出了 Transformer 架構。這一創新徹底改變了 NLP 領域，並在短短農年內擴展到電腦視覺、音訊處理等多個領域。

本期歷史回顧將帶領讀者深入理解 Transformer 架構的核心组件、各主要變體，以及它如何推動了大型預訓練模型的發展。

---

## 大綱

* [程式：實作簡化的 Transformer](focus_code.md)
   - 從注意力機制到完整架構

1. [Attention is All You Need](focus1.md)
   - Transformer 的誕生
   - 核心設計理念

2. [BERT：雙向 Transformer 的崛起](focus2.md)
   - 雙向注意力的創新
   - Masked Language Model

3. [GPT 系列：從 GPT 到 GPT-3](focus3.md)
   - 自回歸語言建模
   - 規模的突破

4. [T5：Text-to-Text Transfer Transformer](focus4.md)
   - 統一框架
   - 各種 NLP 任務的轉換

5. [RoBERTa 與模型最佳化](focus5.md)
   - 去除下一句預測
   - 動態遮罩

6. [Transformer 的變體與改進](focus6.md)
   - 效率改進
   - 架構創新

7. [未來展望](focus7.md)
   - 規模極限
   - 多模態擴展

---

## 濃縮回顧

### Transformer 的核心

```
輸入 -> 詞嵌入 + 位置編碼
      -> N 層 Encoder（自注意力 + 前饋）
      -> N 層 Decoder（自注意力 + 編碼器-解碼器注意力 + 前饋）
      -> 輸出
```

### 關鍵創新

1. **自注意力機制**：捕捉序列內的長距離依賴
2. **位置編碼**：為序列注入順序資訊
3. **多頭注意力**：從多個角度捕捉關係
4. **殘差連接**：訓練更深層網路

### 家族成員

- **BERT 系列**：Encoder-only，双向
- **GPT 系列**：Decoder-only，自回歸
- **T5**：Encoder-Decoder，Text-to-Text

---

## 結論與展望

Transformer 從 2017 年的一篇論文，發展成為深度學習最重要的架構之一。其影響力遠超 NLP，擴展到視覺、音訊、強化學習等多個領域。

---

## 延伸閱讀

- [Attention is All You Need](focus1.md)
- [BERT](focus2.md)
- [GPT 系列](focus3.md)
- [T5](focus4.md)
- [RoBERTa](focus5.md)
- [Transformer 變體](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將探討電腦視覺的進展，敬請期待。*