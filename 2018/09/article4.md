# 模型蒸餾與壓縮

## 1. 為什麼需要模型壓縮？

大模型（如 ResNet-152，60M 參數）難以部署到邊緣裝置。需要將知識從大模型遷移到小模型。

## 2. 知識蒸餾（Knowledge Distillation）

```python
# 教師模型（複雜）
teacher = ResNet152()

# 學生模型（簡單）
student = ResNet18()

# 軟目標（soft targets）— 教師模型輸出
teacher_probs = F.softmax(teacher(x) / temperature, dim=1)

# 蒸餾損失
distillation_loss = F.kl_div(
    F.log_softmax(student(x) / temperature, dim=1),
    teacher_probs
)
```

## 3. 剪枝（Pruning）

```python
import torch.nn.utils.prune as prune

# 結構化剪枝：移除整個 channel
prune.l1_unstructured(model.fc, name='weight', amount=0.3)
prune.remove(model.fc, 'weight')

# 非結構化剪枝：移除個別權重
for name, module in model.named_modules():
    if 'conv' in name:
        prune.l1_unstructured(module, name='weight', amount=0.3)
```

## 4. 量化（Quantization）

```python
# 動態量化（訓練後）
model_quantized = torch.quantization.quantize_dynamic(
    model, {nn.Linear, nn.Conv2d}, dtype=torch.qint8
)

# 訓練時量化aware訓練
model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
torch.quantization.prepare(model, inplace=True)
# 訓練
torch.quantization.convert(model, inplace=True)
```

## 5. 知識蒸餾與剪枝比較

| 方法 | 原理 | 壓縮比 | 精度損失 |
|------|------|--------|----------|
| 蒸餾 | 訓練小模型模仿大模型 | 2-10x | 中 |
| 剪枝 | 移除不重要權重 | 2-10x | 小 |
| 量化 | 使用低精度表示 | 4x | 小 |
| 知識蒸餾 + 剪枝 | 結合兩者 | 10-20x | 可控 |

## 6. 小結

模型壓縮讓深度學習模型能在邊緣裝置上高效運行。知識蒸餾、剪枝和量化是三種主要方法，可以結合使用。

---

**參考資料**
- [Model Compression Techniques](https://www.google.com/search?q=model+compression+knowledge+distillation+pruning)
- [Model Quantization PyTorch](https://www.google.com/search?q=PyTorch+model+quantization+tutorial+2018)