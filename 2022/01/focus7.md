# 深度學習的關鍵突破

## 導言

從 2006 年到 2022 年，深度學習經歷了從復興到爆發的歷程。本文回顧這段歷程中的關鍵突破。

## 2006：深度信念網路

Geoffrey Hinton 在 2006 年發表了《A Fast Learning Algorithm for Deep Belief Nets》，提出逐層預訓練的方法：

1. 使用受限波茲曼機（RBM）逐層無監督預訓練
2. 使用反向傳播進行微調

這項工作被視為深度學習復興的起點。

## 2012：ImageNet 時刻

Alex Krizhevsky、Ilya Sutskever 和 Geoffrey Hinton 在 2012 年 ImageNet 競賽中憑藉 AlexNet 取得了驚人的成績：

- Top-5 錯誤率：15.3%（第二名為 26.2%）
- 5 個卷積層 + 3 個全連接層
- ReLU 啟用函數
- Dropout 正則化
- GPU 加速訓練

```
2012 年前：手工特徵 + SVM
      SIFT 特徵 → 編碼 → SVM 分類
      錯誤率約 26%

2012 年後：端到端深度學習
      原始像素 → CNN → 分類
      錯誤率 15.3%
```

### 成功的三大要素

1. **大數據**：ImageNet 資料集有 1400 萬張圖像
2. **GPU 運算**：NVIDIA GTX 580 將訓練時間從數週縮短到數天
3. **新技術**：ReLU、Dropout、資料增強

## 2013-2014：擴散與多樣化

- **Word2Vec**（Mikolov 等）：詞嵌入的突破
- **GAN**（Goodfellow 等）：生成對抗網路
- **Seq2Seq**（Sutskever 等）：序列到序列學習
- **Adam 優化器**（Kingma 等）：自適應學習率

## 2015：殘差網路

ResNet 由 Kaiming He 等人在微軟研究院提出：

- 152 層網路（是 VGG 的 20+ 倍深）
- ImageNet Top-5 錯誤率 3.57%（超越人類水準）
- 殘差連接解決梯度消失

```python
class ResidualBlock:
    def forward(self, x):
        return self.layers(x) + x  # 殘差連接
```

## 2017：Transformer

Vaswani 等人在《Attention Is All You Need》中提出 Transformer：

- 完全基於注意力機制
- 拋棄了 RNN 和 CNN 的遞迴結構
- 支援大規模平行運算
- BLEU 分數在機器翻譯上達到新高

```python
def attention(Q, K, V):
    scores = Q @ K.T / sqrt(d_k)
    weights = softmax(scores)
    return weights @ V
```

## 2018-2020：預訓練時代

### BERT（2018）

Google 提出 BERT（Bidirectional Encoder Representations from Transformers）：
- 雙向上下文理解
- 遮蔽語言模型預訓練
- 在 11 個 NLP 任務上達到 SOTA

### GPT 系列

- **GPT-1**（2018）：117M 參數，生成式預訓練
- **GPT-2**（2019）：1.5B 參數，生成品質飛躍
- **GPT-3**（2020）：175B 參數，少樣本學習

## 2021-2022：規模化與多模態

- **DALL-E**：文字到圖像生成
- **CLIP**：圖文對比學習
- **AlphaFold 2**：蛋白質結構預測
- **Stable Diffusion**：開源文字到圖像

## 關鍵突破時間線

```
2006 Hinton 深度信念網路
    │
2012 AlexNet ImageNet 突破
    │
2014 GAN, Adam, Seq2Seq
    │
2015 ResNet, BatchNorm
    │
2017 Transformer
    │
2018 BERT, GPT-1
    │
2020 GPT-3 (175B)
    │
2022 InstructGPT (RLHF)
    │
    ▼
當代：大型語言模型、多模態 AI
```

## 持續的趨勢

1. **規模定律（Scaling Laws）**：模型效能隨參數、資料、運算量的增加而提升
2. **自監督學習**：減少對標註資料的依賴
3. **多模態融合**：文字、圖像、音訊、影片的統一建模
4. **對齊訓練**：RLHF、指令微調使 AI 更符合人類意圖

---

## 延伸閱讀

- [Hinton 2006 深度信念網路](https://www.google.com/search?q=Hinton+2006+deep+belief+nets)
- [AlexNet 2012](https://www.google.com/search?q=AlexNet+ImageNet+2012)
- [Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+2017)
- [GPT-3 論文](https://www.google.com/search?q=GPT-3+Language+Models+are+Few+Shot+Learners)

*本篇文章為「AI 程式人雜誌 2022 年 1 月號」歷史回顧系列之一。*
