# PyTorch GPU 加速實戰

## 從 CPU 程式到 GPU 加速的實際轉換

### 基本轉換：.cuda() 與 .to()

在 PyTorch 中，將 CPU 程式轉換為 GPU 加速最簡單的方式是將 tensor 和模型移至 GPU：

```python
import torch

# CPU 程式
x = torch.randn(1000, 1000)
y = torch.randn(1000, 1000)
z = x @ y  # CPU 計算

# GPU 加速
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
x_gpu = x.to(device)
y_gpu = y.to(device)
z_gpu = x_gpu @ y_gpu  # GPU 計算
```

對於模型：

```python
model = MyNeuralNetwork()
model.to(device)  # 所有參數移至 GPU

inputs = inputs.to(device)
labels = labels.to(device)
outputs = model(inputs)  # 在 GPU 上執行 forward
```

### 最小化 CPU-GPU 資料傳輸

PyTorch GPU 程式設計最重要的效能原則：**盡量減少 .cpu() 和 .cuda() 的調用次數**。每次資料傳輸都會通過 PCIe，產生數微秒的延遲和多個 GB/s 的頻寬消耗。

正確做法：在訓練或推理過程中，所有資料始終在 GPU 上：

```python
# 不好的做法：每次迭代都傳輸資料
for epoch in range(10):
    for batch in dataloader:
        inputs = batch["image"].cuda()  # 每次拷貝
        labels = batch["label"].cuda()
        outputs = model(inputs)

# 好的做法：在 DataLoader 中搬移到 GPU
class CUDADataLoader:
    def __init__(self, dataloader, device):
        self.dataloader = dataloader
        self.device = device
    def __iter__(self):
        for batch in self.dataloader:
            yield {k: v.to(self.device) for k, v in batch.items()}
```

### 使用 DataLoader 的 num_workers

DataLoader 的 num_workers 參數可以平行載入資料：

```python
dataloader = DataLoader(dataset, batch_size=64,
                        num_workers=4,    # 4 個子程序平行載入
                        pin_memory=True)  # 使用 pinned memory 加速傳輸
```

pin_memory=True 讓主機記憶體頁面鎖定，使 GPU 可以透過 DMA 直接訪問，加速 CPU→GPU 的傳輸。

### 混合精度訓練

使用 torch.cuda.amp 的 autocast 和 GradScaler：

```python
scaler = torch.cuda.amp.GradScaler()

for batch in dataloader:
    with torch.cuda.amp.autocast():
        outputs = model(inputs)
        loss = criterion(outputs, labels)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
    optimizer.zero_grad()
```

### 使用 torch.jit.script 和 torch.compile

PyTorch 2.0 引入的 torch.compile 可以將模型編譯為最佳化的 GPU Kernel：

```python
model = MyModel().cuda()
model = torch.compile(model)  # 編譯優化

for batch in dataloader:
    outputs = model(inputs)  # 使用編譯後的 kernel
```

### 實戰效能檢查清單

- [ ] tensor 和 model 都在同一 device 上？
- [ ] 資料傳輸僅發生在 epoch 邊界？
- [ ] DataLoader 使用 num_workers？
- [ ] 使用了 pin_memory=True？
- [ ] batch size 足夠大（利用 GPU 平行度）？
- [ ] 使用了非同步 CUDA stream？
- [ ] 監控 GPU 利用率（nvidia-smi）？

### 延伸閱讀

- [PyTorch CUDA Semantics](https://www.google.com/search?q=PyTorch+CUDA+semantics)
- [PyTorch Performance Tuning](https://www.google.com/search?q=PyTorch+GPU+performance+tuning)
