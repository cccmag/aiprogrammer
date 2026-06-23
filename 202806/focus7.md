# 邊緣裝置推論（2020-2028）

## 為什麼邊緣推論？

將 AI 模型部署在手機、IoT 裝置、嵌入式系統上，而不是雲端。這帶來了三個核心好處：

1. **隱私**：資料不需要離開裝置
2. **延遲**：不需要網路傳輸
3. **離線**：無需網路連線即可使用

## 邊緣裝置的硬體限制

```
雲端 GPU:  A100 80GB, 312 TFLOPS
筆記型電腦: RTX 4090, 82 TFLOPS
手機 NPU:  Apple Neural Engine, 15 TOPS
MCU:       < 1MB SRAM, < 10 MOPS
```

在這樣的限制下，一個 GPT-3 大小的模型（175B 參數）不可能直接部署到邊緣。

## 邊緣推論的關鍵技術

### 模型壓縮鏈

```
原始模型 (FP32, 1GB)
    │
    ▼ 量化
INT8 模型 (250MB)
    │
    ▼ 剪枝
稀疏模型 (100MB)
    │
    ▼ 蒸餾
小模型 (50MB)
    │
    ▼ 編譯
NPU 二進位 (25MB)
```

### 硬體加速器對比

| 加速器 | 裝置 | TOPS | 功耗 |
|--------|------|------|------|
| Apple ANE | iPhone | 15-35 | 1-5W |
| Qualcomm Hexagon | Android | 10-26 | 2-4W |
| Google TPU v4e | Chromebook | 8 | 2W |
| NVIDIA Jetson Orin | 嵌入式 | 200 | 15-75W |
| Arduino Portenta | MCU | 0.6 | 0.1W |

## 邊緣推論框架

```python
# TensorFlow Lite 的邊緣部署流程
import tflite_runtime.interpreter as tflite
import numpy as np

# 載入量化模型
interpreter = tflite.Interpreter(model_path="model_quant.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# 邊緣推論
def edge_inference(input_data):
    # 輸入預處理
    input_data = np.array(input_data, dtype=np.uint8)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    
    # 推論
    interpreter.invoke()
    
    # 輸出後處理
    output = interpreter.get_tensor(output_details[0]['index'])
    return output
```

## 邊緣 LLM 的突破

2024 年，Microsoft Phi-3、Google Gemma 和 Apple OpenELM 等「小型語言模型」的出現改變了邊緣 AI 的格局：

```
Phi-3-mini: 3.8B 參數, 可在 iPhone 上運行
Gemma-2B:   2B 參數, 可在 Android 上運行
OpenELM:    270M-1B 參數, 可在筆電上運行
Llama-3.2:  1B-3B 參數, 支援量化後在邊緣運行
```

## 邊緣推論的未來

到 2028 年，邊緣 AI 將不再是「把雲端模型縮小放到手機上」，而是專為邊緣設計的模型和晶片。神經形態計算（Neuromorphic Computing）和記憶體內計算（In-Memory Computing）將進一步模糊雲端和邊緣的界線。

## 延伸閱讀

- [TensorFlow Lite: On-Device ML](https://www.google.com/search?q=TensorFlow+Lite+on+device+ML+inference)
- [Apple CoreML: On-Device Neural Network](https://www.google.com/search?q=Apple+CoreML+on+device+Neural+Engine)
- [Small Language Models for Edge Devices](https://www.google.com/search?q=small+language+models+Phi+Gemma+edge+deployment)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之七。*
