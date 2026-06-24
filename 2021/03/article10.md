# 邊緣 GPU 部署

## NVIDIA Jetson 系列

| 型號 | GPU | AI 效能 |
|------|-----|--------|
| Jetson Nano | 128-core | 0.5 TFLOPS |
| Jetson Xavier NX | 384-core | 21 TFLOPS |
| Jetson AGX Xavier | 512-core | 32 TFLOPS |

## JetPack SDK

```bash
# 安裝 JetPack
sdkmanager --install "jetpack-4.6"
```

## 部署流程

```python
import torch

# TorchScript 導出
model.eval()
example = torch.randn(1, 3, 224, 224)
traced = torch.jit.trace(model, example)

# 優化
optimized = torch.utils.mobile_optimizer.optimize_for_mobile(traced)
optimized.save('model_lite.pt')
```

## 效能優化

```python
# 量化
model quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear}, dtype=torch.qint8
)
```

## 即時推論

```cpp
// TensorRT 推論
#include <NvInfer.h>

void runInference(float* input, float* output) {
    // 建立 Engine
    // 執行推論
}
```

---

## 延伸閱讀

- [Jetson+官方網站](https://www.google.com/search?q=NVIDIA+Jetson+embedded)
- [TensorRT+部署](https://www.google.com/search?q=TensorRT+deployment)
- [邊緣AI+部署案例](https://www.google.com/search?q=edge+AI+deployment+examples)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*