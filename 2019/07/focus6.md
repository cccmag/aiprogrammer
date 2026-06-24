# 雙向 RNN 與堆疊 RNN

## 增強模型的表達能力

在 RNN 的發展過程中，研究者開發了多種技術來增強模型的表達能力。雙向 RNN（Bidirectional RNN）和堆疊 RNN（Stacked RNN）是兩種最基礎且有效的架構改進。

這些技術簡單而強大：
- **雙向 RNN**：利用未來上下文
- **堆疊 RNN**：學習更抽象的表示

---

## 雙向 RNN（BiRNN）

### 問題背景

標準 RNN 的資訊流是單向的：

```
x1 → h1 → h2 → h3 → h4 → h5 → ...
```

這意味著在時間 t 的隱藏狀態只能看到過去的輸入，不能看到未來的上下文。

### 應用場景

哪些任務需要未來上下文？

| 任務 | 為什麼需要未來資訊 |
|------|-------------------|
| 詞性標註 | 要正確標註位置 t 的詞，需要看完整個句子 |
| 命名實體識別 | 實體可能在句子末尾才完整顯現 |
| 語音辨識 | 聲音信號是雙向的 |
| 手寫辨識 | 看完整個筆劃才能判斷 |

### 雙向 RNN 的結構

```
┌─────────────────────────────────────────────────────┐
│              Bidirectional RNN                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│   x1 →  Forward  → h1_f ──────────►               │
│   x2 →  Forward  → h2_f ────────►  ┌──────────┐   │
│   x3 →  Forward  → h3_f ──────► ┌──│ 拼接     │   │
│   x4 →  Forward  → h4_f ───► ┌──├──│ h_t =   │   │
│   x5 →  Forward  → h5_f ─► ┌──┐│  │ [h_t_f;  │   │
│                             │  ││  │  h_t_b]  │   │
│   x1 ← Backward ← h1_b ──► │  │└──│          │   │
│   x2 ← Backward ← h2_b ───► └──┘└──┴──────────┘   │
│   x3 ← Backward ← h3_b ─────►                    │
│   x4 ← Backward ← h4_b ──────►                    │
│   x5 ← Backward ← h5_b ───────►                    │
│                                                     │
│   橙色箭頭：Forward (→)                            │
│   藍色箭頭：Backward (←)                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 前向和後向網路

**前向網路（Forward RNN）**：
```python
h_t_f = forward(x_t, h_{t-1}_f)
# 從左到右計算，利用過去資訊
```

**後向網路（Backward RNN）**：
```python
h_t_b = backward(x_t, h_{t+1}_b)
# 從右到左計算，利用未來資訊
# 實際實現時從序列末尾開始
```

### 隱藏狀態拼接

最終的隱藏狀態是兩個方向的拼接：

```python
h_t = concat([h_t_f, h_t_b])

# 如果使用雙向 LSTM，則拼接兩個方向的 cell 狀態
# c_t = concat([c_t_f, c_t_b])
# h_t = concat([h_t_f, h_t_b])
```

### 雙向 LSTM（BiLSTM）

最常見的配置是使用雙向 LSTM：

```python
# 雙向 LSTM 的 PyTorch 實現
bi_lstm = nn.LSTM(
    input_size=embedding_dim,
    hidden_size=hidden_dim,
    num_layers=1,
    bidirectional=True,
    batch_first=True
)

# 輸出形狀：[batch, seq_len, hidden_dim * 2]
outputs, (hidden, cell) = bi_lstm(input序列)
```

---

## 堆疊 RNN（Stacked RNN）

### 多層 RNN 的思想

堆疊 RNN（也稱為多層 RNN或深層 RNN）將多個 RNN 層疊在一起：

```
┌─────────────────────────────────────────────────────┐
│                  Stacked RNN                        │
├─────────────────────────────────────────────────────┤
│                                                     │
│   輸入:  x1   x2   x3   x4   x5                    │
│          │    │    │    │    │                     │
│          ▼    │    │    │    │                     │
│   Layer1 h1   h2   h3   h4   h5  (第一層)          │
│          │    │    │    │    │                     │
│          ▼    │    │    │    │                     │
│   Layer2 h1'  h2'  h3'  h4'  h5' (第二層)          │
│          │    │    │    │    │                     │
│          ▼    │    │    │    │                     │
│   Layer3 h1''  h2'' h3'' h4'' h5'' (第三層)         │
│                                                     │
│   更高層 = 更抽象的表示                             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 多層 LSTM

```python
# 多層 LSTM 的 PyTorch 實現
stacked_lstm = nn.LSTM(
    input_size=embedding_dim,
    hidden_size=hidden_dim,
    num_layers=3,  # 三層
    batch_first=True
)

# 每層都有獨立的權重
# 更高層捕捉更抽象的特徵
```

### 為什麼多層？

- **第一層**：學習低層特徵（詞彙、語法）
- **第二層**：學習中層特徵（句法結構、語義）
- **第三層**：學習高層特徵（語用、推理）

```
視覺化理解：
┌────────────────────────────────────────────────────┐
│  第三層抽象表示：    ┌────────────────────────┐     │
│                     │  積極/消極 情感         │     │
│                     └────────────────────────┘     │
│  第二層語義表示：    ┌────────────────────────┐     │
│                     │  滿意 不滿 期待 失望    │     │
│                     └────────────────────────┘     │
│  第一層詞彙表示：    ┌────────────────────────┐     │
│                     │ 好 棒 贊 優 差 糟 爛   │     │
│                     └────────────────────────┘     │
└────────────────────────────────────────────────────┘
```

---

## 實用組合：深層雙向 LSTM

最常見的工業應用配置是 **深層雙向 LSTM（Deep BiLSTM）**：

```python
# 4 層雙向 LSTM
model = nn.LSTM(
    input_size=embedding_dim,
    hidden_size=256,
    num_layers=4,
    bidirectional=True,
    batch_first=True,
    dropout=0.3  # 層間 Dropout
)
```

### 效能對比

| 模型 | 參數量 | 訓練時間 | 準確率 |
|------|--------|---------|--------|
| Single LSTM | 2.1M | 1x | 85.2% |
| BiLSTM | 3.8M | 1.2x | 87.5% |
| 2-layer LSTM | 4.2M | 1.5x | 86.8% |
| 2-layer BiLSTM | 7.6M | 1.8x | 89.1% |
| 4-layer BiLSTM | 15.2M | 2.5x | 89.8% |

### 訓練技巧

**1. 梯度裁剪**

深層 RNN 容易梯度爆炸：

```python
# PyTorch 中的梯度裁剪
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
```

**2. 殘差連接**

幫助梯度流動，更容易訓練深層網路：

```python
# 殘差連接
output = layer_norm(x + sublayer(x))
```

**3. 層歸一化**

加速收斂：

```python
# 層歸一化
layer_norm = nn.LayerNorm(hidden_dim)
h = layer_norm(h + sublayer(h))
```

---

## 應用實例：命名實體識別

NER 是展示 BiLSTM 強大的經典任務：

```
輸入：「馬斯克成立了SpaceX公司」

輸出：
  馬斯克 → 人名 (PER)
  成立了 → 動詞 (V)
  SpaceX → 組織名 (ORG)
  公司 → 名詞 (N)
```

### NER 的 BiLSTM 架構

```python
# NER 模型架構
class NERModel(nn.Module):
    def __init__(self):
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.bilstm = nn.LSTM(
            embed_dim, hidden_dim,
            num_layers=2,
            bidirectional=True,
            batch_first=True
        )
        self.fc = nn.Linear(hidden_dim * 2, num_tags)

    def forward(self, x):
        # x: [batch, seq_len]
        embedded = self.embedding(x)  # [batch, seq_len, embed_dim]
        lstm_out, _ = self.bilstm(embedded)  # [batch, seq_len, hidden_dim*2]
        logits = self.fc(lstm_out)  # [batch, seq_len, num_tags]
        return logits
```

### 特徵輸入

NER 的輸入可以使用多種特徵：

1. **詞嵌入**：Word2Vec, GloVe, FastText
2. **字元級嵌入**：捕捉字形態
3. **位置嵌入**：詞在句子中的位置
4. **詞性標註**：POS tags
5. **依存關係**：Dependency parsing

---

## 總結

雙向 RNN 和堆疊 RNN 是兩種基礎但強大的架構改進：

- **雙向 RNN**：允許模型利用未來上下文，對序列標註任務特別有效
- **堆疊 RNN**：通過多層結構學習更抽象的表示

兩者的組合——深層雙向 RNN——是工業應用中的常見選擇，在各種序列標註任務中取得了優秀的效果。

然而，這些架構仍然受到順序計算的限制。Transformer 的出現最終解決了這個問題，使得更深、更寬的模型成為可能。

---

## 延伸閱讀

- [Bidirectional LSTM](https://www.google.com/search?q=bidirectional+LSTM+NER)
- [Stacked RNN deep learning](https://www.google.com/search?q=stacked+RNN+deep+learning)
- [Deep BiLSTM NLP](https://www.google.com/search?q=deep+bidirectional+LSTM+NLP)

---

*本篇文章為「AI 程式人雜誌 2019 年 7 月號」循環神經網路系列之六。*