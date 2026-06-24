# 序列到序列模型 (Sequence-to-Sequence)

## 2014 年的突破性架構

2014 年，Sutskever、Vinyals 和 Le 發表了論文《Sequence to Sequence Learning with Neural Networks》，提出了 Sequence-to-Sequence（Seq2Seq）模型。這是 RNN 發展史上的一個重要里程碑，使得 RNN 能夠處理輸入輸出長度不同的複雜任務。

Seq2Seq 的核心思想：**使用兩個 RNN，一個作為編碼器將輸入序列壓縮為固定維度的向量，另一個作為解碼器根據這個向量生成輸出序列**。

---

## Seq2Seq 架構

```
┌─────────────────────────────────────────────────────┐
│              Sequence-to-Sequence 架構               │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入序列:  [x1,  x2,  x3,  x4,  x5]              │
│                │    │    │    │    │               │
│                ▼    ▼    ▼    ▼    ▼               │
│   ┌────────────────────────────────────────┐       │
│   │              Encoder RNN               │       │
│   │                                        │       │
│   │   h1 = f(W*x1 + U*h0)                 │       │
│   │   h2 = f(W*x2 + U*h1)                 │       │
│   │   h3 = f(W*x3 + U*h2)                 │       │
│   │   ...                                  │       │
│   │   h5 = f(W*x5 + U*h4)                 │       │
│   │                                        │       │
│   │   c = h5  (或所有隱藏狀態的組合)       │       │
│   └────────────────────────────────────────┘       │
│                       │                             │
│                       ▼                             │
│   ┌────────────────────────────────────────┐       │
│   │              Decoder RNN               │       │
│   │                                        │       │
│   │   s0 = c  (或 s0 = 0)                  │       │
│   │   s1 = f(W*y0 + U*s0)                  │       │
│   │   y1 = softmax(V*s1)                   │       │
│   │                                        │       │
│   │   s2 = f(W*y1 + U*s1)                  │       │
│   │   y2 = softmax(V*s2)                   │       │
│   │   ...                                  │       │
│   └────────────────────────────────────────┘       │
│                │    │    │    │    │               │
│                ▼    ▼    ▼    ▼    ▼               │
│   輸出序列:   [y1,  y2,  y3,  y4,  y5]             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 編碼器（Encoder）

編碼器的任務：
1. 讀取輸入序列的每個元素
2. 維護一個累積的隱藏狀態
3. 將最後的隱藏狀態（和記憶）作為「語義向量」傳遞給解碼器

### 解碼器（Decoder）

解碼器的工作方式：
1. 以編碼器的輸出作為初始隱藏狀態
2. 接收特殊的 `<START>` token 作為第一個輸入
3. 每個時間步輸出一個元素
4. 直到輸出特殊的 `<END>` token 為止

### 貪心解碼 vs 束搜索

**貪心解碼（Greedy Decoding）**：
- 每個時間步選擇概率最高的單個 token
- 快速但可能陷入局部最優

**束搜索（Beam Search）**：
- 維護 k 個最優候選序列（beam width = k）
- 在每個時間步擴展所有候選，保留總概率最高的 k 個
- 通常能得到更好的翻譯品質

```
Beam Search 示意（k=2）：

Step 1:  "The" (p=0.3)     "A" (p=0.2)
Step 2:  "The cat" (0.18)  "A dog" (0.12)
Step 3:  "The cat sat" (0.12)  "A dog runs" (0.08)
...
最佳: "The cat sat on the mat" (p=0.002)
```

---

## 機器翻譯：Seq2Seq 的經典應用

### 任務描述

機器翻譯是 Seq2Seq 的經典應用場景：

```
輸入（英文）："The cat sat on the mat"
輸出（法文）："Le chat était assis sur le tapis"
```

### 訓練過程

```python
# Seq2Seq 機器翻譯訓練示意
def train_seq2seq(source, target, encoder, decoder):
    # 編碼階段
    encoder_output, encoder_hidden = encoder(source)

    # 解碼階段
    decoder_input = START_TOKEN
    decoder_hidden = encoder_hidden
    loss = 0

    for t in range(len(target)):
        decoder_output, decoder_hidden = decoder(
            decoder_input, decoder_hidden
        )

        # 交叉熵損失
        loss += criterion(decoder_output, target[t])
        decoder_input = target[t]  # 教師強迫

    return loss
```

### 挑戰與解決方案

**挑戰 1：長序列衰減**

當輸入序列很長時，編碼器很難將所有資訊壓縮到單個向量中。

**解決方案**：
- 使用雙向 RNN
- 使用多層 RNN
- 引入注意力機制

**挑戰 2：曝光偏差（Exposure Bias）**

訓練時使用「教師強迫」（Teacher Forcing），但推理時使用自己預測的輸出。兩者分布不一致導致錯誤累積。

**解決方案**：
- Scheduled Sampling
- Professor Forcing
- 注意力機制（緩解依賴）

---

## 聊天機器人：對話系統

### 任務特點

聊天機器人是另一個重要的 Seq2Seq 應用：

```
輸入：你 吃 飯 了 嗎？
輸出：已 經 吃 過 了，謝謝 關心 ！

輸入：今天 天氣 如何？
輸出：今天 天氣 很 不錯，適合 外出 活動。
```

### 對話 vs 翻譯

| 特性 | 機器翻譯 | 聊天機器人 |
|------|----------|-----------|
| 輸入明確性 | 明確 | 可能模糊 |
| 輸出多樣性 | 較少 | 非常多 |
| 評估指標 | BLEU | 人類評估 |
| 安全性 | 重要 | 非常重要 |

### 聊天機器人的挑戰

1. **一致性**：同一問題的不同問法應得到相似回答
2. **多輪對話**：需要維護對話歷史
3. **安全過濾**：防止生成有害內容
4. **人格設定**：保持一致的個性或身份

---

## 文字摘要

### Extractive vs Abstractive

**抽取式摘要（Extractive）**：
- 從原文中選擇重要句子
- 簡單但可能不通順

**生成式摘要（Abstractive）**：
- 生成新的表述方式
- 更靈活但更困難

Seq2Seq 適合生成式摘要：

```
輸入：
"微軟宣佈以 262 億美元收購 LinkedIn。這是微軟史上最大收購案。LinkedIn 將保持獨立營運。雙方預計今年完成交易。"

輸出：
"微軟以 262 億美元收購 LinkedIn，這是微軟史上最大收購。"
```

### Copy Mechanism

摘要任務中的一個重要技術是「複製機制」：

```python
# 複製網路
p_gen = sigmoid(v^T * s_t + u^T * c_t + b)

# 最終詞彙分布 = 原始分布 * (1-p_gen) + 注意力分布 * p_gen
P_final = (1 - p_gen) * P_vocab + p_gen * P_attention
```

這讓模型能夠：
- 從原文複製專有名詞、數字等
- 生成新的表述方式

---

## 影像描述（Image Captioning）

Seq2Seq 還廣泛應用於影像描述生成：

```
┌─────────────────────────────────────────────────────┐
│              影像描述生成架構                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   圖片 ──► CNN ──► 視覺特徵 ──► RNN ──► 描述文字    │
│                             (解碼器)                  │
│                                                     │
│   輸入：「一隻狗在草地上奔跑」                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 訓練流程

1. **視覺特徵提取**：使用預訓練 CNN（如 ResNet）提取圖像特徵
2. **特徵饋入**：將視覺特徵作為 RNN 的初始隱藏狀態
3. **文字生成**：使用 Seq2Seq 生成描述

---

## 總結

Seq2Seq 模型開創了序列到序列學習的新時代，使得 RNN 能夠處理輸入輸出長度不同的複雜任務。

從機器翻譯到聊天機器人，從文字摘要到影像描述，Seq2Seq 架構展現了驚人的靈活性和強大能力。

然而，Seq2Seq 也有其局限性：
1. **瓶頸問題**：固定維度的向量難以表達無限的資訊
2. **順序計算**：無法平行化

這些問題最終由注意力機制和 Transformer 架構得到解決，開啟了深度學習的新篇章。

---

## 延伸閱讀

- [Seq2Seq 原始論文 2014](https://www.google.com/search?q=Sutskever+seq2seq+2014)
- [機器翻譯神經網路](https://www.google.com/search?q=neural+machine+translation+seq2seq)
- [Chatbot seq2seq](https://www.google.com/search?q=seq2seq+chatbot+neural+network)

---

*本篇文章為「AI 程式人雜誌 2019 年 7 月號」循環神經網路系列之四。*