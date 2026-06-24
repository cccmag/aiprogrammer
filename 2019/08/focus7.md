# GPT 與自迴歸模型

## 生成式預訓練的崛起

GPT（Generative Pre-training）是另一個基於 Transformer 的預訓練模型系列。與 BERT 不同，GPT 採用自迴歸（Autoregressive）方式，專注於生成任務。從 GPT 到 GPT-2，展示了大型語言模型的驚人能力。

---

## GPT 與 GPT-2 的發展

### OpenAI 的策略

```
┌─────────────────────────────────────────────────────┐
│           GPT 系列的發展歷程                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│   GPT (2018): 1.17 億參數                          │
│     - 首次提出「生成式預訓練」概念                   │
│     - 12 層 Transformer 解碼器                      │
│     - 單向（從左到右）語言模型                       │
│                                                     │
│   GPT-2 (2019): 15 億參數                          │
│     - 更大的模型和數據                              │
│     - 擔憂安全性，分階段發布                        │
│     - 展示無監督多工能力                            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 自迴歸語言模型

### 與 BERT 的區別

```
BERT (雙向，MLM):

輸入: "The cat sat on the [MASK]"
               ↓
          看到兩邊

輸出: "mat"


GPT (單向，LM):

輸入: "The cat sat on the"
               ↓
          只看到左邊

輸出: "mat"
```

### 數學定義

```python
# 自迴歸語言模型的目標
# P(x) = Π_t P(x_t | x_{<t})

# 最大化似然
def lm_loss(logits, targets):
    # logits: [batch, seq_len, vocab_size]
    # targets: [batch, seq_len]
    return F.cross_entropy(
        logits[:, :-1].reshape(-1, vocab_size),
        targets[:, 1:].reshape(-1)
    )
```

---

## GPT 架構

### Transformer 解碼器

```python
class GPTModel(nn.Module):
    def __init__(self, vocab_size, embed_dim, num_layers, num_heads):
        super().__init__()
        self.tokens = nn.Embedding(vocab_size, embed_dim)
        self.positions = nn.Embedding(max_len, embed_dim)
        self.blocks = nn.ModuleList([
            TransformerBlock(embed_dim, num_heads)
            for _ in range(num_layers)
        ])
        self.ln_f = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size, bias=False)

    def forward(self, x):
        x = self.tokens(x) + self.positions(torch.arange(x.size(1)))
        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.head(x)
```

### GPT 與 GPT-2 的配置

| 配置 | GPT | GPT-2 |
|------|-----|-------|
| 參數量 | 117M | 1.5B |
| 層數 | 12 | 48 |
| 隱藏維度 | 768 | 1600 |
| 注意力頭數 | 12 | 25 |
| 上下文長度 | 512 | 1024 |

---

## 無監督多工能力

### GPT-2 的發現

GPT-2 的一個重要發現是：足夠大的語言模型能夠在零樣本（zero-shot）條件下執行多種任務：

```python
# GPT-2 的 zero-shot 能力

# 翻譯（英語到法語）
prompt = "English: I love you\nFrench:"
# 輸出: "Je t'aime"

# 摘要
prompt = """A neutron star is the collapsed core of a massive supergiant star...
TL;DR:"""
# 輸出: 摘要文字

# 問答
prompt = "What is the capital of France?\nAnswer:"
# 輸出: "Paris"
```

### 實驗結果

| 任務 | 之前的無監督方法 | GPT-2 (zero-shot) |
|------|------------------|-------------------|
| CoQA | - | 55F1 |
| SQuAD | - | 62.2 |
| LAMBADA | 7.7 | 19.2 |

---

## GPT-2 的爭議

### 安全考量

OpenAI 的安全考量引發了廣泛討論：

```
担忧：
1. 假新聞生成
2. 誤導性內容
3. 垃圾郵件
4. 抄襲

OpenAI 的回應：
- 分階段發布
- 持續監測使用情況
- 根據反饋調整策略
```

### 社群反應

- **支持**：安全第一，谨慎是对的
- **质疑**：应该开源，限制反而促进地下发展
- **中立**：需要更多讨论和监管

---

## 生成式預訓練的價值

### 為什麼生成式？

```python
# 生成式預訓練的優勢

adv_generative = {
    "連貫性": "能生成流暢的長文本",
    "創造性": "能用於創意寫作",
    "通用性": "適用於任何生成任務",
    "簡單性": "直觀的訓練目標"
}
```

### 應用場景

```python
# 文字生成
text = gpt2.generate("Once upon a time", max_length=100)

# 對話生成
response = gpt2.generate("User: How are you?\nAssistant:")

# 代码補全
code = gpt2.generate("def quick_sort(arr):")
```

---

## BERT vs GPT

### 架構對比

| 特性 | BERT | GPT-2 |
|------|------|-------|
| 方向 | 雙向 | 單向（從左到右）|
| 預訓練任務 | MLM + NSP | 語言模型 |
| 適用場景 | 理解任務 | 生成任務 |
| 典型應用 | 分類、標註、問答 | 對話、摘要、程式碼 |

### 選擇建議

```
理解任務 → 使用 BERT 或其變體
生成任務 → 使用 GPT 或其變體
兩者兼顧 → 使用 T5、GLM 等Encoder-Decoder 模型
```

---

## 預訓練的影響

### 研究範式的轉變

```
之前：
任務特定訓練 → 需要大量標注數據

現在：
預訓練 + 微調 → 少量數據即可
```

### 對業界的影響

```python
# 預訓練改變了 NLP 的遊戲規則

before_bert = {
    "數據需求": "百萬級標注數據",
    "訓練時間": "數週到數月",
    "專業性": "每個任務需要專家",
    "泛化能力": "限於特定任務"
}

after_bert = {
    "數據需求": "數千到數萬微調數據",
    "訓練時間": "數小時到數天",
    "專業性": "通用的語言理解",
    "泛化能力": "跨任務遷移"
}
```

---

## 總結

GPT 系列展示了自迴歸語言模型的強大能力：

1. **生成能力**：能產生連貫、多樣的文字
2. **零樣本學習**：在未見過的任務上也能表現
3. **規模效應**：更大的模型展現更多能力
4. **安全性討論**：推動 AI 負責任發展

GPT 和 BERT 的成功標誌著預訓練時代的全面到來。

---

## 延伸閱讀

- [GPT Paper](https://www.google.com/search?q=OpenAI+GPT+paper+improving+language)
- [GPT-2 Paper](https://www.google.com/search?q=GPT-2+language+models+are+unsupervised)
- [Language+Model+Pre-training](https://www.google.com/search?q=language+model+pre-training+NLP)

---

*本篇文章為「AI 程式人雜誌 2019 年 8 月號」注意力機制系列之七。*