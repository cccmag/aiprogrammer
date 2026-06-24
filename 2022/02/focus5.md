# 多 GPU 訓練策略

## 資料平行與模型平行

### 為什麼需要多 GPU 訓練

大型語言模型的參數量已經從數億成長到數千億。GPT-3 有 1750 億參數，PaLM 更達到 5400 億參數。這樣的大模型即使使用最大的單一 GPU（如 A100 80GB）也無法完整載入。更不用說單一 GPU 的訓練時間可能長達數月。因此，多 GPU 訓練從選項變成了剛需。

### Data Parallelism（資料平行）

資料平行是最直觀的多 GPU 策略。每個 GPU 儲存一份完整的模型副本，但處理不同的批次資料：

1. 主 GPU 廣播模型參數到所有 GPU
2. 每個 GPU 在自己的資料分片上執行前向和反向傳播
3. 所有 GPU 的梯度透過 all-reduce 通訊進行平均
4. 每個 GPU 用平均梯度更新自己的參數

資料平行的優勢在於簡單，但缺點也很明顯：當模型大到無法放入單一 GPU 記憶體時，資料平行就失效了。

PyTorch 中的實作：

```python
model = MyModel().cuda()
model = torch.nn.DataParallel(model, device_ids=[0,1,2,3])
# 或使用 DistributedDataParallel（推薦）
```

### Model Parallelism（模型平行）

模型平行將模型的不同層分配給不同的 GPU，解決了模型過大無法放入單一 GPU 的問題：

```python
class PipelineModel(nn.Module):
    def __init__(self):
        self.layer1 = nn.Linear(1024, 2048).cuda(0)
        self.layer2 = nn.Linear(2048, 4096).cuda(1)
        self.layer3 = nn.Linear(4096, 1024).cuda(2)
    def forward(self, x):
        x = self.layer1(x.cuda(0))
        x = self.layer2(x.cuda(1))
        x = self.layer3(x.cuda(2))
        return x
```

### Pipeline Parallelism（管線平行）

管線平行是模型平行的進化版本，引入管線排程來提高 GPU 利用率：

```
GPU0: Layer1 → microbatch 0 → Layer1 → microbatch 1 → ...
GPU1:                     → Layer2 → microbatch 0 → ...
GPU2:                                    → Layer3 → microbatch 0 → ...
```

管線平行存在「氣泡效應」：在管線填充和排空階段，部分 GPU 處於空閒。Google 的 GPipe 和 Microsoft 的 PipeDream 提出了不同的排程策略來最小化氣泡開銷。

### Tensor Parallelism（張量平行）

張量平行將單一層的計算拆分到多個 GPU。例如，對於線性層 Y = XW，我們可以將權重矩陣 W 按列分割到不同 GPU，各自部分計算之後再透過 all-reduce 合併結果。

NVIDIA 的 Megatron-LM 框架將張量平行與管線平行結合，成功訓練了 530B 參數的 Megatron-Turing NLG 模型。

### NCCL 通訊協定

多 GPU 訓練的核心瓶頸通常是 GPU 間通訊而非計算。NCCL（NVIDIA Collective Communications Library）提供了最佳化的集合通訊原語：

- **All-Reduce**：所有 GPU 的梯度求平均，用於資料平行
- **All-Gather**：收集所有 GPU 的資料，用於張量平行
- **Reduce-Scatter**：分散式 reduce，用於節省頻寬

NCCL 支援多種通訊後端：NVLink（GPU 間直接互連）、PCIe、InfiniBand、RoCE。在 DGX 等專業系統中，GPU 透過 NVSwitch 全互連，all-reduce 頻寬可達 600 GB/s。

### 策略選擇指南

選擇多 GPU 訓練策略需要考慮：

- **模型大小 vs GPU 記憶體**：模型能塞入單 GPU 就使用資料平行
- **通訊頻寬**：高頻寬（NVLink）環境適合張量平行
- **批次大小限制**：大模型配合梯度累積可實現有效大 batch
- **開發成本**：資料平行最簡單，張量平行開發成本最高

### 延伸閱讀

- [NCCL Documentation](https://www.google.com/search?q=NVIDIA+NCCL+documentation)
- [Megatron-LM: Training Large Models](https://www.google.com/search?q=Megatron-LM+training+large+models)
- [PyTorch Distributed Training](https://www.google.com/search?q=PyTorch+distributed+data+parallel)
