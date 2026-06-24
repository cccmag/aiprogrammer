# 深度學習的編譯器優化

## 深度學習框架的編譯器技術

深度學習框架需要高效執行大規模矩陣運算。編譯器優化在這裡扮演重要角色。

## TVM：深度學習的編譯器棧

TVM（Tensor Virtual Machine）是專為深度學習設計的編譯器框架：

```python
import tvm
import tvm.te as te

# 定義計算
n = tvm.var("n")
A = te.placeholder((n,), name="A")
B = te.placeholder((n,), name="B")
C = te.compute((n,), lambda i: A[i] + B[i], name="C")

# 排程優化
s = te.create_schedule(C.op)
print(tvm.lower(s, [A, B, C], simple_mode=True))
```

## XLA：TensorFlow 的編譯器

XLA（Accelerated Linear Algebra）將 TensorFlow 圖形編譯為優化的機器碼：

```
TensorFlow 圖
     ↓ [XLA編譯]
優化的 HLO（高階運算）指令
     ↓ [HLO優化]
     ↓ [代碼生成]
優化的機器碼
```

### 啟用 XLA

```python
# TensorFlow 1.x
config = tf.ConfigProto()
config.graph_options.optimizer_options.global_jit_level = tf.OptimizerOptions.ON_1
sess = tf.Session(config=config)

# TensorFlow 2.x（Eager 模式下自動優化）
@tf.function(jit_compile=True)
def fast_matmul(x, y):
    return x @ y
```

## 運算子融合

多個運算子融合為一個，減少記憶體訪問：

```
融合前：
A → Relu → B → Relu → C

融合後：
A → Fuse(Relu + Relu) → C
```

## 記憶體規劃

深度學習編譯器需要規劃暫存器使用：

```python
# 記憶體優化
@tf.function(jit_compile=True)
def optimized_inference(x):
    x = tf.nn.conv2d(x, kernel1)
    x = tf.nn.relu(x)
    x = tf.nn.conv2d(x, kernel2)
    return tf.nn.relu(x)
```

## 自動微分與優化

編譯器可以結合自動微分進行優化：

```python
# 自動微分 + 編譯優化
@tf.function(jit_compile=True)
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = loss_fn(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss
```

## 量化

將浮點數運算量化為定點數：

```python
# INT8 量化
converter = tf.lite.TFLiteConverter.from_saved_model(model_path)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.float16]
quantized_model = converter.convert()
```

## GPU 優化

CUDA 核融合：

```python
# 使用 torch.cuda.jit 優化
@torch.jit.script
def fused_kernel(x, weight, bias):
    return torch.nn.functional.linear(x, weight, bias)
```

延伸閱讀：
- [Google 搜尋：deep learning compiler optimization](https://www.google.com/search?q=deep+learning+compiler+optimization)
- [Google 搜尋：TVM deep learning](https://www.google.com/search?q=TVM+deep+learning)