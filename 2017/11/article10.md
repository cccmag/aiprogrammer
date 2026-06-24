# Facebook 開源 Caffe2：跨平台深度學習

## 前言

Caffe2 於 2017 年 4 月由 Facebook 開源，是一個強調便攜性和效能的深度學習框架。

## Caffe2 的設計理念

### 輕量級

Caffe2 的核心非常精簡，適合邊緣部署。

### 跨平台

```python
# 可以在不同平台執行相同程式碼
# 支援：
# - CPU
# - GPU (CUDA)
# - Mobile (iOS, Android)
# - Embedded devices
```

### 高效能

Caffe2 優化了記憶體使用和計算效率：

```python
import caffe2.python.predictor.predictor_exporter as pe

# 模型最佳化
model_proto = pe.prepare_model_devices(model_net)
# 自動選擇最佳執行設備
```

## 預訓練模型庫

Caffe2 Model Zoo 提供了豐富的預訓練模型：

```python
# 下載預訓練模型
from caffe2.python import workspace

# MobileNet
workspace.ReadNetBlob("mobilenet")

# ResNet
workspace.ReadNetBlob("resnet50")
```

## 與 PyTorch 的整合

2017 年底，Facebook 宣佈將 Caffe2 和 PyTorch 整合，最終在 PyTorch 1.0 中實現：

```
Caffe2: 優秀的部署能力
    +              → PyTorch 1.0
PyTorch: 靈活的開發體驗
```

## Caffe2 的特點

| 特性 | 說明 |
|------|------|
| 輕量級 | 核心簡單，部署方便 |
| 跨平台 | iOS, Android, 嵌入式 |
| 高效能 | 記憶體優化，計算效率高 |
| 生態 | 豐富的預訓練模型 |

## 應用場景

### 行動端推論

```python
# 在 iOS 上執行
import caffe2.python.predictor.predictor_session as ps

session = ps.PredictorSession(model_proto)
output = session.run([input_blob])
```

### 邊緣運算

Caffe2 的輕量級設計使其非常適合邊緣 AI 應用。

## 技術架構

```
┌─────────────────────────────────────────────────────────┐
│              Caffe2 架構                                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Python API (教練、實驗)                               │
│       │                                                 │
│  Caffe2 Proto (模型定義)                               │
│       │                                                 │
│  Caffe2 Core (C++ 實作)                                │
│       │                                                 │
│  ├─ CPU Implementation                                │
│  ├─ CUDA Implementation                               │
│  └─ Metal Implementation (iOS)                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 對 AI 部署的影響

Caffe2 的開源推動了深度學習模型部署的發展：

1. **統一的部署流程**：訓練到部署的一致性
2. **跨平台支援**：一次訓練，多平台部署
3. **效能最佳化**：適合生產環境

## 後續發展

Caffe2 與 PyTorch 的整合在 2018 年完成，形成了今天的 PyTorch 生態：

```python
# PyTorch 導出到 Caffe2
import torch.onnx

model = torchvision.models.resnet18(pretrained=True)
torch.onnx.export(model, dummy_input, "resnet18.onnx")

# ONNX 格式可以在 Caffe2 中執行
```

---

**延伸閱讀**

- [Caffe2 GitHub](https://www.google.com/search?q=Caffe2+GitHub+Facebook)
- [Caffe2 Model Zoo](https://www.google.com/search?q=Caffe2+model+zoo)
- [ONNX](https://www.google.com/search?q=ONNX+Facebook+Microsoft)

---

*本篇文章為「AI 程式人雜誌 2017 年 11 月號」AI 相關文章之一。*