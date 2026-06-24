# 邊緣裝置上的多模態模型

## 前言

將多模態 AI 部署到邊緣裝置（手機、IoT、嵌入式系統）面臨著模型大小、推論速度與功耗的嚴峻挑戰。本文將介紹如何在資源受限的裝置上執行多模態模型，包括模型壓縮、量化、以及邊緣優化技術。

---

## 一、邊緣裝置的挑戰

邊緣裝置的資源限制：

| 資源 | 手機 | Raspberry Pi | 微控制器 |
|------|------|-------------|---------|
| RAM | 4-12 GB | 1-8 GB | 256 KB - 1 MB |
| 儲存 | 64-512 GB | 16-256 GB | 1-16 MB |
| GPU | 有（專用） | 無/弱 | 無 |
| 功耗 | 3-8 W | 2-5 W | 0.01-0.1 W |

## 二、模型量化

量化是減少模型大小和加速推論最有效的方法。將 FP32 權重轉換為 INT8：

```python
import torch

def quantize_model(model, calib_loader):
    """靜態量化：需要校準資料集"""
    model.eval()
    model.qconfig = torch.ao.quantization.get_default_qconfig("qnnpack")
    model = torch.ao.quantization.prepare(model, inplace=False)

    # 校準：跑數個 batch 來觀察 activation 分布
    with torch.no_grad():
        for images, _ in calib_loader:
            model(images)

    model = torch.ao.quantization.convert(model, inplace=False)
    return model

# 量化前後的大小對比
def model_size(model):
    param_size = sum(p.numel() * p.element_size() for p in model.parameters())
    return param_size / (1024 ** 2)  # MB

float_model = CLIPWrapper()
print(f"FP32 模型大小: {model_size(float_model):.2f} MB")

int8_model = quantize_model(float_model, calib_loader)
print(f"INT8 模型大小: {model_size(int8_model):.2f} MB")
```

## 三、ONNX Runtime 部署

ONNX Runtime 提供跨平台的優化推論引擎：

```python
import onnx
import onnxruntime as ort
import numpy as np

def export_to_onnx(model, dummy_input, onnx_path="model.onnx"):
    torch.onnx.export(
        model, dummy_input, onnx_path,
        input_names=["input"],
        output_names=["embedding"],
        dynamic_axes={"input": {0: "batch_size"}},
        opset_version=17,
    )
    print(f"Exported to {onnx_path}")

def run_onnx_inference(onnx_path, input_data):
    session = ort.InferenceSession(
        onnx_path,
        providers=["CPUExecutionProvider"]
    )
    input_name = session.get_inputs()[0].name
    output = session.run(None, {input_name: input_data})
    return output[0]

# 邊緣裝置上的推論
onnx_model = "clip_text_encoder.onnx"
text_embedding = run_onnx_inference(onnx_model, np.array(tokenized_text))
```

## 四、TFLite 與行動裝置

TensorFlow Lite 針對行動裝置進行了深度優化：

```python
import tensorflow as tf

def convert_to_tflite(keras_model, tflite_path="model.tflite"):
    converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_types = [tf.float16]
    converter.representative_dataset = representative_dataset

    tflite_model = converter.convert()
    with open(tflite_path, "wb") as f:
        f.write(tflite_model)

# Android 端使用
class MobileMultiModal:
    def __init__(self, model_path):
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def embed_text(self, text):
        # 文字前處理 + 推論
        input_data = self.preprocess_text(text)
        self.interpreter.set_tensor(self.input_details[0]["index"], input_data)
        self.interpreter.invoke()
        return self.interpreter.get_tensor(self.output_details[0]["index"])
```

## 五、模型蒸餾

用小模型（學生）學習大模型（教師）的行為：

```python
class DistillationLoss:
    def __init__(self, temperature=4.0, alpha=0.5):
        self.temperature = temperature
        self.alpha = alpha

    def __call__(self, student_logits, teacher_logits, labels):
        # 軟目標損失（蒸餾）
        soft_targets = F.softmax(teacher_logits / self.temperature, dim=1)
        student_soft = F.log_softmax(student_logits / self.temperature, dim=1)
        distill_loss = F.kl_div(student_soft, soft_targets, reduction="batchmean")
        distill_loss *= self.temperature ** 2

        # 硬目標損失
        hard_loss = F.cross_entropy(student_logits, labels)

        return self.alpha * distill_loss + (1 - self.alpha) * hard_loss

def distill_multimodal(teacher, student, dataloader, epochs=10):
    optimizer = torch.optim.Adam(student.parameters(), lr=1e-4)
    criterion = DistillationLoss()

    for epoch in range(epochs):
        for batch in dataloader:
            images, texts, labels = batch
            with torch.no_grad():
                t_out = teacher(images, texts)
            s_out = student(images, texts)
            loss = criterion(s_out, t_out, labels)
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```

## 六、Edge AI 框架比較

| 框架 | 支援平台 | 量化支援 | 硬體加速 |
|------|---------|---------|---------|
| ONNX Runtime | Linux, Windows, macOS, iOS, Android | INT8, FP16 | CPU, GPU, NPU |
| TensorFlow Lite | Android, iOS, Linux | INT8, FP16 | GPU, NNAPI |
| Core ML | iOS, macOS | FP16, INT8 | Apple Neural Engine |
| ExecuTorch | iOS, Android | INT8, FP16 | CPU, GPU, NPU |

---

## 結語

邊緣多模態 AI 正在從理論走向實用。憑藉量化、蒸餾和硬體加速技術，即使在手機上也能即時運作 CLIP 等級的多模態模型。未來的 edge AI 將進一步整合 NPU 硬體加速和更高效的架構，讓多模態 AI 無所不在。

---

**參考資料**

- ONNX Runtime：https://onnxruntime.ai/
- TensorFlow Lite：https://www.tensorflow.org/lite
- 模型量化技術：https://www.google.com/search?q=model+quantization+int8+edge+AI
- ExecuTorch：https://pytorch.org/executorch/
