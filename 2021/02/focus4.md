# PyTorch Mobile

## 行動裝置部署流程

```
訓練模型（Python）
    ↓
優化模型
    ↓
轉換為 Lite 格式
    ↓
整合到 App
    ↓
部署到裝置
```

## 模型轉換

```python
import torch
from torch.utils.mobile_optimizer import optimize_for_mobile

# 追蹤模型
model = MyModel()
model.eval()
example_input = torch.randn(1, 3, 224, 224)
traced = torch.jit.trace(model, example_input)

# 優化
optimized = optimize_for_mobile(traced)
optimized.save('model_android.pt')
```

## iOS 整合

```swift
import TorchVision

let module = torch.jit.load("model.pt")
let input = torch.rand([1, 3, 224, 224])
let output = module.forward(input)
```

## Android 整合

```kotlin
import org.pytorch.LiteNativePeer

val module = LiteNativePeer.load("model.pt")
val input = torch.rand(longArrayOf(1, 3, 224, 224))
val output = module.forward(input)
```

## 效能優化技巧

### 量化

```python
# 動態量化（簡單）
quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
```

### 資料類型優化

```python
# float16 推理
with torch.cuda.amp.autocast():
    output = model(input)
```

## 支援的操作

PyTorch Mobile 支援大多數常見操作：
- 卷積、池化
- RNN、LSTM、GRU
- Transformer（部分）

---

## 延伸閱讀

- [PyTorch Mobile 官方文檔](https://www.google.com/search?q=PyTorch+Mobile+documentation)
- [iOS+部署教學](https://www.google.com/search?q=PyTorch+Mobile+iOS+tutorial)
- [Android+部署教學](https://www.google.com/search?q=PyTorch+Mobile+Android+tutorial)

*本篇文章為「AI 程式人雜誌 2021 年 2 月號」精選文章。*