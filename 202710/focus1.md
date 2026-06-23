# 從單模態到多模態（2012-2026）

## 深度學習的第一波：單模態革命

2012 年 AlexNet 在 ImageNet 上的突破，開啟了深度學習在電腦視覺領域的黃金時代。但此時的 AI 系統仍然是「單模態」的——模型只能處理一種類型的資料：

- **視覺模型**（2012-2017）：AlexNet、VGG、ResNet 只能看圖片
- **語言模型**（2013-2019）：Word2Vec、LSTM、BERT 只能讀文字
- **語音模型**（2014-2018）：DeepSpeech、WaveNet 只能聽聲音

這些模型的共同點是各自在自己的模態內達到頂尖表現，卻無法跨模態理解。

```
2012-2017 單模態時代：
  ┌─────────┐   ┌─────────┐   ┌─────────┐
  │  Image   │   │  Text   │   │  Audio  │
  │  Model   │   │  Model  │   │  Model  │
  │(ResNet)  │   │ (BERT)  │   │(WaveNet)│
  └─────────┘   └─────────┘   └─────────┘
      ↑              ↑              ↑
   圖片資料        文字資料       音訊資料
```

## 注意力機制與 Transformer 的僭越

2017 年「Attention Is All You Need」帶來了 Transformer 架構。它的核心貢獻不在於某個特定模態的表現，而是提供了一個**通用的序列建模框架**：

- 文字是 token 序列 → Transformer Encoder-Decoder
- 圖片是 patch 序列 → ViT（Vision Transformer, 2020）
- 音訊是 frame 序列 → Speech Transformer

同樣的模型架構可以處理不同的模態，只需要調整輸入的 tokenization 方式：

```python
# Transformer 的核心：模態無關的注意力機制
import math
import numpy as np

def scaled_dot_product_attention(Q, K, V):
    """Q, K, V 可以是任何模態的向量序列"""
    scores = np.dot(Q, K.T) / math.sqrt(Q.shape[-1])
    weights = np.exp(scores) / np.sum(np.exp(scores), axis=-1, keepdims=True)
    return np.dot(weights, V)

# 無論是文字、圖片 patch、音訊 frame：
# Q, K, V 的形狀都是 (seq_len, d_model)
# 注意力機制不在乎「內容是什麼」，只在乎「相關性多高」
```

## 多模態的關鍵轉折點

| 年份 | 里程碑 | 意義 |
|------|--------|------|
| 2012 | AlexNet | 深度學習視覺時代開始 |
| 2017 | Transformer | 統一序列建模架構 |
| 2018 | BERT + GPT | NLP 的預訓練時代 |
| 2020 | ViT | Transformer 統一視覺 |
| 2021 | CLIP | 文字-影像跨模態學習 |
| 2022 | Whisper | 語音統一模型 |
| 2023 | GPT-4V | 商業多模態模型 |
| 2024 | Gemini | 原生多模態架構 |
| 2025 | 統一嵌入模型 | 所有模態共用向量空間 |
| 2026 | 模態無關基礎模型 | 任意輸入任意輸出 |

## 多模態的統一表示

核心問題是：**如何讓不同模態在統一的表示空間中對話？**

```python
def unified_embed(data, modality):
    """所有模態 → token 序列 → 同一向量空間"""
    if modality == "text":    tokens = tokenize(data)
    elif modality == "image": tokens = patchify(data)
    elif modality == "audio": tokens = framify(data)
    return transformer(tokens)  # 輸出在同一向量空間
```

這個「統一嵌入空間」讓跨模態搜尋、理解、生成成為可能。

## 小結

從單模態到多模態的演進，不是簡單地把多個模型拼在一起。真正的突破來自於 Transformer 架構的模態無關性——當所有模態都被轉換為 token 序列，AI 模型就能夠在統一的框架下理解世界的多種面向。

---

**下一步**：[多模態嵌入與對比學習](focus2.md)

## 延伸閱讀

- [Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+paper)
- [An Image is Worth 16x16 Words (ViT)](https://www.google.com/search?q=Vision+Transformer+ViT+paper)
- [CLIP: Learning Transferable Visual Models](https://www.google.com/search?q=CLIP+paper+OpenAI)
