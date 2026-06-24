# 深度學習框架之戰

## PyTorch 的勝利之年

2022 年是深度學習框架格局發生根本性變化的一年。PyTorch 鞏固了其在研究領域的統治地位，而 TensorFlow 則在被迫追趕。與此同時，JAX 作為第三勢力快速崛起。

## PyTorch 2.0

### 從 1.x 到 2.0

PyTorch 2.0 在 2022 年底發布預覽版，帶來了可能是框架史上最重要的性能提升：

**torch.compile**：一個新的 JIT 編譯器，可以將 PyTorch 程式碼即時編譯為高效的內核程式碼：

```python
import torch

@torch.compile
def train_step(model, data, optimizer):
    predictions = model(data)
    loss = torch.nn.functional.cross_entropy(predictions, data.y)
    loss.backward()
    optimizer.step()
    return loss
```

只需加上 `@torch.compile`，訓練速度就能提升 30%-200%，且不需要修改任何其他程式碼。

### TorchDynamo 的突破

PyTorch 2.0 的核心技術是 TorchDynamo——一個安全的 Python JIT 編譯器。與傳統的 trace-based 方法不同，TorchDynamo 在 Python 位元組碼層級運作，可以捕獲動態計算圖。

`torch.compile` 的三種後端模式：

| 模式 | 描述 | 適合場景 |
|------|------|---------|
| eager | 預設執行模式 | 除錯 |
| reduce-overhead | 減少 CUDA 啟動開銷 | 小批次訓練 |
| max-autotune | 自動調優 | 生產環境 |

## TensorFlow 的轉型

TensorFlow 在 2022 年面臨巨大壓力。Google 在 9 月發布了 TensorFlow 2.11，但焦點已經轉向 JAX。

### TensorFlow 的問題

- **API 複雜性**：多次 API 重構導致社群不滿
- **除錯困難**：靜態圖的除錯體驗遠不如 PyTorch
- **研究社群流失**：頂級會議的論文絕大多數使用 PyTorch
- **生態萎縮**：套件和第三方工具開始優先支援 PyTorch

## JAX 的崛起

JAX 是 Google 開發的數值計算庫，在 2022 年獲得了大量關注：

### JAX 的核心優勢

- **函數式轉換**：`grad()`、`jit()`、`vmap()`、`pmap()` 等函數式 API
- **XLA 編譯**：底層使用 XLA 編譯器，自動最佳化
- **Just-In-Time 編譯**：靜態編譯獲得最佳性能
- **自動批次處理**：`vmap` 自動向量化

```python
import jax
import jax.numpy as jnp

# 自動微分
def f(x):
    return x ** 2 + jnp.sin(x)

grad_f = jax.grad(f)
print(grad_f(3.0))  # 6 + cos(3) ≈ 5.01

# 自動向量化
def single_sample(x, y):
    return jnp.dot(x, y)

batch_dot = jax.vmap(single_sample, in_axes=(0, 0))
```

### Flax / Haiku 生態

JAX 上的深度學習框架生態：

- **Flax**：Google 的官方 JAX 神經網路庫
- **Haiku**：DeepMind 的 JAX 神經網路庫
- **Optax**：最佳化器庫
- **Orbax**：檢查點管理

## 框架使用率變化

根據 2022 年的調查數據，頂級 AI 會議論文中框架使用率的變化：

| 框架 | 2020 | 2021 | 2022 |
|------|------|------|------|
| PyTorch | 42% | 68% | 85% |
| TensorFlow | 51% | 28% | 12% |
| JAX | 2% | 4% | 15% |
| 其他 | 5% | 4% | 3% |

注意：JAX 的 15% 包含基於 JAX 的 Flax/Haiku 等框架。

## 框架選擇建議

- **研究 / Prototype**：PyTorch（社群最大、資源最多）
- **高效能訓練**：JAX / Flax（XLA 優化、自動並行）
- **生產部署**：PyTorch + TorchServe 或 ONNX Runtime
- **邊緣裝置**：TensorFlow Lite（生態成熟）
- **多框架兼容**：ONNX 作為中間格式

## 不需要選邊站

2022 年深度學習框架的趨勢是「互操作性」：

- ONNX 作為統一的中間表示格式
- PyTorch 可以導出到 TensorFlow SavedModel
- JAX 模型可以轉換為 TensorFlow.js
- Hugging Face 已統一支援 PyTorch / TensorFlow / JAX

## 延伸閱讀

- [PyTorch 2.0 博客](https://www.google.com/search?q=PyTorch+2.0+announcement+2022)
- [JAX 官方文檔](https://www.google.com/search?q=JAX+documentation+Google)
- [TensorFlow 2022 回顧](https://www.google.com/search?q=TensorFlow+2022+year+in+review)
- [Flax 框架](https://www.google.com/search?q=Flax+neural+network+library+JAX)
- [ONNX 生態](https://www.google.com/search?q=ONNX+open+standard+AI+models+2022)
