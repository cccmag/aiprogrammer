# GPT 系列：從 GPT 到 GPT-3

## 自回歸語言建模的演进

### 歷史回顧

| 模型 | 時間 | 參數 | 主要創新 |
|------|------|------|---------|
| GPT-1 | 2018 | 1.17 億 | 預訓練 + 微調 |
| GPT-2 | 2019 | 15 億 | 無需微調 |
| GPT-3 | 2020 | 1750 億 | Few-shot Learning |

---

## GPT-1 (2018)

### 核心思想

使用左到右的 Transformer 解碼器進行語言建模：

```
P(output | input) = Product P(w_t | w_{<t})
```

### 預訓練 + 微調

GPT-1 展示了可以通過大規模預訓練，然後在特定任務上微調來達到良好效果。

---

## GPT-2 (2019)

### 規模提升

GPT-2 的參數量是 GPT-1 的 10 倍以上（15 億 vs 1.17 億）。

### 無需微調

GPT-2 展示了：
- 在大量資料上預訓練後
- 可以直接處理各種任務
- 透過任務描述（Prompt）來引導

### 爭議與開放

OpenAI 最初以「太危險」為由延遲發布完整模型，後來還是開源了。

---

## GPT-3 (2020)

### 規模的突破

1750 億參數——迄今為止最大的語言模型之一。

### Few-shot Learning

GPT-3 的核心創新是極強的少樣本學習能力：

```
Input:
Translate to French:
Dog -> chien
Cat -> chat
Bird -> [模型輸出]
```

### 與 BERT 的對比

| 方面 | BERT | GPT-3 |
|------|------|-------|
| 架構 | Encoder-only | Decoder-only |
| 注意力 | 雙向 | 單向（左到右） |
| 預訓練目標 | MLM + NSP | 語言建模 |
| 微調方式 | 任務特定微調 | Few-shot |
| 規模 | 3.4 億 | 1750 億 |

---

## 兩種預訓練範式的比較

### Encoder-only (BERT 系列)

**優勢**：
- 雙向上下文感知
- 適合理解任務（分類、抽取）

**劣勢**：
- 不能自然生成文字
- 需要微調

### Decoder-only (GPT 系列)

**優勢**：
- 適合生成任務
- 強大的少樣本能力

**劣勢**：
- 單向注意力
- 生成效率較低

---

## GPT-3 的能力展示

### 文字生成

```python
prompt = "Once upon a time in a distant land"
output = gpt3.generate(prompt, max_tokens=100)
```

### 程式碼生成

```python
prompt = "Write a Python function to calculate fibonacci"
output = gpt3.generate(prompt)
```

### 翻譯

```python
prompt = "Translate English to French: Hello ->"
output = gpt3.generate(prompt)
```

---

## 為何 GPT-3 如此強大？

### 1. 規模

1750 億參數提供了足够的容量來學習：
- 語法結構
- 世界知識
- 任務模式

### 2. 多樣化的訓練資料

45 TB 的互聯網文本，涵蓋幾乎所有領域。

### 3. In-context Learning

模型學會從輸入的少量範例中推斷任務。

---

**下一步**：[T5：Text-to-Text Transfer Transformer](focus4.md)

## 延伸閱讀

- [GPT+series+language+model](https://www.google.com/search?q=OpenAI+GPT+language+model+series)
- [GPT-3+175B+parameters+2020](https://www.google.com/search?q=GPT-3+175B+parameters+2020)
- [decoder+vs+encoder+transformer](https://www.google.com/search?q=decoder+vs+encoder+transformer+language+model)