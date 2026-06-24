# PyTorch Mobile

## 安裝

```bash
# Android
pip install torch torchvision

# iOS 需要從原始碼編譯（2020 年初複雜度較高）
```

## 模型準備

```python
import torch
import torchvision.models as models

# 訓練或載入模型
model = models.mobilenet_v2(pretrained=True)
model.eval()

# 追蹤模型
example_input = torch.rand(1, 3, 224, 224)
traced_model = torch.jit.trace(model, example_input)

# 儲存
traced_model.save('mobilenet_v2.pt')
```

## Android 部署

```kotlin
// MainActivity.kt
import org.pytorch.MobileModule

class MainActivity : AppCompatActivity() {
    private lateinit var module: MobileModule

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        module = MobileModule.loadFromFile("mobilenet_v2.pt")
    }

    fun predict(image: Tensor) {
        val output = module.forward(IValue.from(image))
        // 處理輸出
    }
}
```

## 預處理

```kotlin
// 使用 Android TorchVision
import org.pytorch.torchvision.TensorOps

val bitmap = MediaStore.Images.Media.getBitmap(contentResolver, uri)
val tensor = TensorOps.bitmapToNormalizedFloat32Tensor(bitmap, Device.CPU)
```

## iOS Swift API（基本）

```swift
// 2020 年初 Swift API 仍在發展
// 需要從原始碼編譯 libtorch

import TorchMobile

let module = try MobileModule.loadModel(atPath: "mobilenet_v2.pt")
let inputTensor = Tensor(copying: imageData)
let output = try module.forward(inputTensor)
```

## 效能優化

```python
# 模型量化
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear: torch.nn.quantized.DynamicLinear}
)
quantized_model.eval()

# 追蹤量化後模型
example_input = torch.rand(1, 3, 224, 224)
quantized_traced = torch.jit.trace(quantized_model, example_input)
quantized_traced.save('mobilenet_v2_quantized.pt')
```

## 與 TensorFlow Lite 比較

| 特性 | TF Lite | PyTorch Mobile |
|------|---------|----------------|
| Android 支援 | 完善 | 基本支援 |
| iOS 支援 | 完善 | 需要編譯 |
| API 穩定性 | 穩定 | 演進中 |
| 模型大小 | 較小 | 較大 |

## 建議

2020 年初，PyTorch Mobile 仍在快速發展中。如果主要需要 Android 部署，TensorFlow Lite 仍是更穩定的選擇。

## 參考資源

- https://www.google.com/search?q=PyTorch+Mobile+Android+deployment+tutorial+2020
- https://www.google.com/search?q=PyTorch+Mobile+iOS+Swift+API+2020
- https://www.google.com/search?q=PyTorch+Mobile+quantization+optimization+2020