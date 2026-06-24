# 梯度累積與批次大小

## 在 GPU 記憶體限制下實現大規模批次訓練

### 批次大小的重要性

批次大小（batch size）是深度學習訓練中最重要的超參數之一。較大的 batch size 可以：

- 提高 GPU 利用率（一次處理更多資料）
- 減少梯度更新的方差（更穩定的收斂）
- 加速訓練（減少 parameter update 次數）
- 充分利用 Tensor Core 的矩陣乘法能力

然而，batch size 受到 GPU 記憶體的限制。一個 batch 的資料需要儲存：輸入資料、中間激活值、梯度、優化器狀態。對於大型模型，batch size 可能被限制在 2 或 4——遠低於理想的 128 或 256。

### 梯度累積的原理

梯度累積（Gradient Accumulation）是一種在不增加 GPU 記憶體消耗的前提下，實現有效大 batch 訓練的技術。其核心思想非常簡單：

1. 將大 batch 分割為多個 micro-batch
2. 對每個 micro-batch 進行 forward + backward（計算梯度）
3. 累積梯度但不立即更新權重
4. 達到設定的累積步數後，用累積的梯度更新一次權重

```python
# 梯度累積實作
model = MyModel().cuda()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)
accumulation_steps = 8  # 有效的 batch = 8 × micro_batch_size

for epoch in range(num_epochs):
    for step, (inputs, labels) in enumerate(dataloader):
        inputs, labels = inputs.cuda(), labels.cuda()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss = loss / accumulation_steps  # 正規化
        loss.backward()

        if (step + 1) % accumulation_steps == 0:
            optimizer.step()
            optimizer.zero_grad()
```

### 梯度累積與 Batch Normalization

使用梯度累積時需要注意 Batch Normalization 的行為：

- **默認行為**：每個 micro-batch 獨立計算 BN 的 mean 和 variance。累積步數越多，BN 統計量的估計偏差越大
- **解決方法**：使用 SyncBatchNorm（同步批次正規化），在 micro-batch 之間同步 BN 統計量
- **替代方案**：使用 LayerNorm 或 GroupNorm 替代 BatchNorm

```python
model = torch.nn.SyncBatchNorm.convert_sync_batchnorm(model)
```

### 動態批次大小與學習率調整

在梯度累積中，有效批次大小 = micro_batch_size × accumulation_steps。當有效批次大小改變時，學習率也需要相應調整：

- **線性 scaling rule**：有效 batch 大小加倍時，learning rate 也加倍
- **初始 warmup**：大 batch 訓練需要更多的 warmup 步數
- **實際經驗**：從 batch 256 開始，每增加一倍 batch 大小，learning rate 增加約 0.5-1x

### 虛擬批次大小查表

```python
def compute_effective_batch(micro_batch, accum_steps, num_gpus):
    return micro_batch * accum_steps * num_gpus

# 範例配置
configs = [
    # (micro_batch, accum_steps, num_gpus) → effective batch
    (32, 1, 1) → 32
    (32, 4, 1) → 128
    (16, 8, 1) → 128
    (32, 4, 4) → 512   # DDP + gradient accumulation
    (8, 16, 8) → 1024  # extreme case
]
```

### 梯度累積 vs 資料平行

梯度累積和資料平行是兩種可以組合使用的技術：

| 技術 | 記憶體需求 | 有效批次大小 | 通訊成本 |
|-----|-----------|-------------|---------|
| Data Parallel | O(model) per GPU | batch × num_GPU | 每次 step 通訊 |
| Gradient Accumulation | O(model) | batch × accum_steps | 無需通訊 |
| 兩者組合 | O(model) per GPU | batch × num_GPU × accum_steps | 每次 accum step通訊 |

### 實戰建議

1. 優先使用資料平行（DDP），其次考慮梯度累積
2. 從 accumulation_steps = 2 開始測試，逐步增加
3. 監控 GPU 記憶體使用量，調整 micro_batch 大小
4. 使用 gradient clipping 防止大 batch 訓練的梯度爆炸
5. 考慮使用更大的 learning rate + warmup

### 延伸閱讀

- [Gradient Accumulation in PyTorch](https://www.google.com/search?q=PyTorch+gradient+accumulation)
- [Large Batch Training](https://www.google.com/search?q=large+batch+training+deep+learning)
