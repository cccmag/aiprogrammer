# 模型壓縮 for Edge

## 1. 為什麼需要壓縮

邊緣裝置的記憶體與儲存空間極為有限。一個標準的 ResNet50 約 98MB，無法放入大多數 MCU。模型壓縮技術可將模型縮小 10-100 倍，同時盡量維持準確度。

## 2. 三種主流壓縮技術

### 2.1 量化（Quantization）

將 FP32 權重降為 INT8 甚至 INT4，可減少 75%-87% 的模型體積：

```python
import tensorflow as tf
import numpy as np

# 訓練基準模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(64,)),
    tf.keras.layers.Dense(10, activation='softmax')
])

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

def representative_dataset():
    for _ in range(100):
        yield [np.random.randn(1, 64).astype(np.float32)]

converter.representative_dataset = representative_dataset
converter.target_spec.supported_types = [tf.int8]
quantized_model = converter.convert()

print(f'原始大小: {model.count_params() * 4 / 1024:.1f} KB (FP32)')
print(f'量化大小: {len(quantized_model) / 1024:.1f} KB (INT8)')
```

### 2.2 剪枝（Pruning）

移除權重接近零的神經元連接：

```python
import tensorflow_model_optimization as tfmot

pruning_params = {
    'pruning_schedule': tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.3, final_sparsity=0.8,
        begin_step=0, end_step=1000)
}

pruned_model = tfmot.sparsity.keras.prune_low_magnitude(
    model, **pruning_params)
# 訓練後稀疏率可達 80%，壓縮比約 5 倍
```

### 2.3 蒸餾（Knowledge Distillation）

用小模型（學生）學習大模型（教師）的輸出分布：

```python
def distillation_loss(student_logits, teacher_logits, temperature=4.0):
    soft_student = tf.nn.softmax(student_logits / temperature)
    soft_teacher = tf.nn.softmax(teacher_logits / temperature)
    return tf.reduce_mean(
        tf.keras.losses.kld(soft_teacher, soft_student)
    ) * temperature ** 2
```

## 3. 壓縮結果比較

| 方法 | 體積縮減 | 準確度損失 | 適用場景 |
|------|---------|-----------|---------|
| INT8 量化 | 75% | <1% | 通用 |
| 剪枝 80% | 80% | 1-3% | 大型模型 |
| 蒸餾 | 90%+ | 2-5% | 資源極受限 |

## 4. 結語

實務上通常組合使用量化、剪枝與蒸餾。更多資訊請參考 https://www.google.com/search?q=model+compression+edge+device+tutorial
