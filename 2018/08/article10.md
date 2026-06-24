# PyTorch 生態系工具一覽

## 1. 核心庫

### TorchVision（影像）

```python
from torchvision import models, datasets, transforms

# 模型
resnet = models.resnet18(pretrained=True)

# 資料集
mnist = datasets.MNIST(root='./data')

# 轉換
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])
```

### TorchText（文字）

```python
from torchtext import data, datasets

# 文字欄位
TEXT = data.Field(tokenize='spacy')
LABEL = data.LabelField()

# 內建資料集
train_data, test_data = datasets.SST(root='./data')
```

### TorchAudio（音頻）

```python
import torchaudio

# 載入音頻
waveform, sample_rate = torchaudio.load('audio.wav')

# 轉換
spectrogram = torchaudio.transforms.Spectrogram()(waveform)
```

## 2. 模型壓縮

### Quantization（量化）

```python
# 動態量化
model_quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
```

### Pruning（剪枝）

```python
import torch.nn.utils.prune as prune

# 結構化剪枝
prune.l1_unstructured(model.fc, name='weight', amount=0.3)
prune.remove(model.fc, 'weight')
```

## 3. 視覺化工具

### TensorBoard

```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter('runs/experiment')

for epoch in range(10):
    writer.add_scalar('loss', loss, epoch)
    writer.add_histogram('weights', model.fc.weight, epoch)

writer.close()
```

## 4. 分散式訓練

```python
# 初始化
import torch.distributed as dist

dist.init_process_group(backend='nccl')

# 準備資料
train_sampler = torch.utils.data.distributed.DistributedSampler(train_dataset)

# 包裝模型
model = nn.parallel.DistributedDataParallel(model)
```

## 5. 其他工具

| 工具 | 用途 |
|------|------|
| ignite | 高階訓練幫手 |
| catalyst | 實驗追蹤 |
| PyTorch Geometric | 圖神經網路 |
| PyTorch-BigGraph | 大規模圖嵌入 |
|ParlAI | 對話系統研究平臺 |

## 6. 小結

PyTorch 生態系在 2018 年已相當完整，從資料處理到模型訓練、從視覺化到部署都有成熟工具支援。

---

**參考資料**
- [PyTorch Ecosystem](https://www.google.com/search?q=PyTorch+ecosystem+tools+2018)
- [Awesome PyTorch List](https://www.google.com/search?q=awesome+PyTorch+list+GitHub)