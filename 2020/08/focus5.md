# RoBERTa 與模型最佳化

## Facebook 的改進

### 論文資訊

- **標題**：RoBERTa: A Robustly Optimized BERT Pretraining Approach
- **作者**：Yinhan Liu et al.
- **發布**：2019

---

## RoBERTa 對 BERT 的改進

### 1. 去除 Next Sentence Prediction

RoBERTa 發現 NSP 任務對效能沒有幫助，因此去除了它。

### 2. 動態遮罩

| BERT | RoBERTa |
|------|---------|
| 每個 epoch 使用相同遮罩 | 每個 batch 動態生成新遮罩 |
| 靜態 | 動態 |

```python
# 動態遮罩偽碼
for batch in dataloader:
    masked_batch = apply_dynamic_mask(batch)
    loss = model(masked_batch)
```

### 3. 更長的訓練時間

- 更大的批量（8000 vs 256）
- 更長的訓練步數
- 更大的訓練資料

### 4. 更多訓練資料

RoBERTa 使用了更多樣化的資料來源：
- Books + Wikipedia
- CC-News
- OpenWebText
- Stories

---

## 實驗結果

### GLUE 發展

| 版本 | 發展分數 |
|------|---------|
| BERT-base | 79.6 |
| RoBERTa-base | 82.1 |
| BERT-large | 83.3 |
| RoBERTa-large | 88.5 |

### SQuAD 結果

| 模型 | SQuAD 1.1 | SQuAD 2.0 |
|------|----------|----------|
| BERT-large | 91.3 | 86.2 |
| RoBERTa-large | 94.6 | 89.4 |

---

## 模型最佳化的最佳實踐

### 預訓練階段

1. **大批量 + 小學習率**
   ```python
   optimizer = AdamW(lr=1e-4, weight_decay=0.01)
   scheduler = LinearWarmup(warmup_steps=10000)
   batch_size = 8192  # 越大越好
   ```

2. **資料增強**
   - Back-translation
   - 動態遮罩

3. **長訓練**
   - RoBERTa 訓練超過 500,000 步

### 微調階段

1. **較小的學習率**
   ```python
   lr = 1e-5 to 5e-5  # 預訓練時的 1/100 到 1/10
   ```

2. **Early Stopping**
   - 監控驗證集表現
   - 避免過擬合

3. **任務特定技巧**
   - 較低的溫度
   - 標籤平滑

---

## 其他優化變體

### ALBERT (Google)

**引數共享**：跨層共享注意力權重

**詞典分解**：Embedding 矩陣分解

結果：參數減少但效能略有下降。

### ELECTRA (Google)

**替換 Token 檢測 (RTD)**：
- 不預測遮罩詞
- 而是判斷每個位置是否被替换

優點：每一個位置都在學習（而不只是 15%）。

### DistilBERT (Hugging Face)

**知識蒸餾**：從大模型蒸餾到小模型

- 參數減少 40%
- 保留 97% 效能
- 速度快 60%

---

## 實用建議

### 何時使用哪個模型？

| 場景 | 推薦模型 |
|------|---------|
| 資源受限 | DistilBERT, ALBERT |
| 效能優先 | RoBERTa, ELECTRA |
| 生成任務 | GPT-2, T5 |
| 多語言 | mBERT, XLM-R |

### 開源資源

- Hugging Face Model Hub
- 各大模型的預訓練權重
- 微調教程

---

**下一步**：[Transformer 的變體與改進](focus6.md)

## 延伸閱讀

- [RoBERTa+paper+2019](https://www.google.com/search?q=RoBERTa+robustly+optimized+BERT+paper)
- [model+optimization+transformer+NLP](https://www.google.com/search?q=BERT+RoBERTa+optimization+pretraining+2019)