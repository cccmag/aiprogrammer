# 從 GPT 到 BERT：NLP 的兩條路徑

## 前言

2018-2019 年，NLP 領域見證了兩種主要預訓練範式的崛起：OpenAI 的 GPT 系列和 Google 的 BERT 系列。本篇文章將對比這兩種路徑的異同。

## 架構比較

### GPT：單向語言模型

GPT 使用 Transformer 解碼器，採用從左到右的語言建模：

```
輸入：The cat sat on the
目標：mat

GPT 的計算：
P(mat | The cat sat on the)
只能看到左側上下文
```

### BERT：雙向 Transformer

BERT 使用 Transformer 編碼器，採用 Masked Language Model：

```
輸入：The [MASK] sat on the mat
目標：cat

BERT 的計算：
P(cat | The [MASK] sat on the mat)
可以看到兩側上下文
```

## 預訓練目標

### GPT 的目標

```python
# GPT 的語言建模目標
def gpt_loss(input_ids):
    # 最大化下一個 token 的似然
    for i in range(len(input_ids)):
        loss -= log P(input_ids[i] | input_ids[:i])
    return loss
```

### BERT 的目標

```python
# BERT 的 MLM 目標
def bert_loss(input_ids, mask_positions):
    # 預測被遮蔽的 tokens
    for pos in mask_positions:
        loss -= log P(input_ids[pos] | unmasked_context)
```

## 生成 vs 理解

### GPT 的優勢：生成

GPT 在生成任務上表現更好：

```
GPT 擅長：
- 文字補全
- 創意寫作
- 對話生成
- 程式碼生成
```

### BERT 的優勢：理解

BERT 在理解任務上表現更好：

```
BERT 擅長：
- 文字分類
- 問答
- 自然語言推理
- 命名實體識別
```

## 應用場景的差異

### GPT 的應用

```python
# 文字生成
prompt = "在一個風雨交加的夜晚，"
story = gpt.generate(prompt)

# 對話
context = "User: 你好\nBot:"
response = gpt.generate(context)
```

### BERT 的應用

```python
# 文字分類
outputs = bert_model(input_ids, labels=labels)
loss = outputs.loss

# 問答
outputs = bert_for_qa(input_ids, start_positions, end_positions)
```

## 混合和演進

### 統一模型的出現

一些模型開始結合兩種方法：

```
發展趨勢：
- XLNet：排列語言模型（結合兩者優點）
- RoBERTa：更強的 BERT
- BART：編碼器-解碼器架構
```

### 未來方向

```
未來方向：
- 更大的預訓練
- 更有效的訓練
- 多模態整合
```

## 結論

GPT 和 BERT 代表了 NLP 預訓練的兩條不同路徑。GPT 側重生成，適合文字補全和創意寫作；BERT 側重理解，適合分類和推理任務。兩種方法各有優勢，也促進了 NLP 領域的快速發展。選擇哪種方法應該根據具體的應用場景來決定。

---

**延伸閱讀**

- [GPT+vs+BERT](https://www.google.com/search?q=GPT+vs+BERT+comparison)
- [NLP+pretrained+models](https://www.google.com/search?q=NLP+pretrained+models+2019)
- [language+model+architecture](https://www.google.com/search?q=language+model+architecture+GPT+BERT)