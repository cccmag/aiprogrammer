# 語音辨識的突破：CTC 網路

## 前言

連接時序分類（CTC，Connectionist Temporal Classification）是深度學習在語音辨識領域的重大突破。CTC 使得端到端語音辨識成為可能，大幅簡化了語音辨識系統的設計。

## 語音辨識的挑戰

### 對齊問題

傳統語音辨識需要艱難的時序對齊：

```
輸入語音：40ms × 幀
輸出文字：「你好」

問題：
- 每幀應該對應哪個音素？
- 語速變化如何處理？
- 插入和刪除錯誤如何避免？
```

## CTC 的解決方案

### CTC 的核心思想

CTC 引入了一個特殊的「空白」符號，用於處理輸入輸出的不對齊：

```python
# CTC 的特殊符號
blank = '-'  # 空白符號，不輸出任何字符

# 輸入序列（長度 T）
# 輸出序列（長度 L，通常 L << T）
# CTC 自動學習對齊方式
```

### CTC 損失函數

```python
# CTC 損失
# 最大化正確輸出的概率
# 自動考慮所有可能的對齊方式

import torch

ctc_loss = nn.CTCLoss(blank=0, reduction='mean')
loss = ctc_loss(log_probs, targets, input_lengths, target_lengths)
```

## 經典模型

### Deep Speech

Mozilla 的 Deep Speech 使用 RNN + CTC：

```python
# 網路架構
# 輸入：MFCC 特徵（13-40 維）
# 編碼：多層雙向 RNN
# 解碼：CTC 輸出

# 特點：
# - 端到端訓練
# - 不需要語音知識
# - 支援多種語言
```

### QuartzNet

QuartzNet 採用改進的 CTC 模型：

```python
# 1D 卷積 + CTC
# 更高效的計算
# 更好的效能
```

## 端到端語音辨識的優勢

### 傳統方法 vs CTC

| 特性 | 傳統方法 | CTC/端到端 |
|------|---------|-----------|
| 複雜度 | 高 | 低 |
| 需要語言知識 | 多 | 少 |
| 訓練資料需求 | 中 | 高 |
| 推論速度 | 慢 | 快 |
| 錯誤率 | 中 | 低（大量資料時）|

## 應用場景

- **語音助理**：Siri、Google Assistant、Alexa
- **會議紀錄**：自動生成會議紀錄
- **字幕生成**：影片自動字幕
- **語音輸入**：输入法语音输入

## 結語

CTC 是深度學習在語音辨識領域的重要突破。它簡化了語音辨識系統的設計，使得端到端訓練成為可能。結合深度學習的其他進展，CTC 為現代語音辨識系統奠定了基礎。

---

## 延伸閱讀

- [CTC+語音辨識](https://www.google.com/search?q=CTC+connectionist+temporal+classification+speech)
- [Deep+Speech+Mozilla](https://www.google.com/search?q=Deep+Speech+Mozilla+speech+recognition)
- [端到端+語音辨識](https://www.google.com/search?q=end+to+end+speech+recognition+deep+learning)

---

*本篇文章為「AI 程式人雜誌 2017 年 2 月號」文章系列之一。*