# 深度學習框架的演進

## Theano → TensorFlow → PyTorch → JAX：計算圖的四個世代（2007-2026）

### 從 Theano 開始

2007 年，蒙特婁大學的 Yoshua Bengio 團隊發布了 **Theano**——第一個 Python 深度學習框架。Theano 的貢獻不在於效能（它在多數任務上比手寫 C 慢），而在於它引入了**符號計算圖（symbolic computation graph）**的概念：

```python
# Theano 的靜態計算圖範例
import theano.tensor as T

x = T.matrix('x')          # 符號變數
y = T.matrix('y')
z = T.dot(x, y)            # 建構計算圖
f = theano.function([x, y], z)  # 編譯成 GPU 程式
result = f([[1,2]], [[3],[4]])  # 執行
```

這種「先建圖、後執行」的模式稱為**靜態計算圖（static graph）**。優點是編譯器可以進行完整的圖層級最佳化（算子融合、記憶體規劃）；缺點是除錯困難（無法在圖建構時使用 Python 的 `print`）。

### TensorFlow 與靜態圖的全盛期

2015 年，Google 發布了 **TensorFlow**。它繼承了 Theano 的靜態圖設計，但加入了分散式訓練、TensorBoard 可視化、和行動端部署。TensorFlow 1.x 的核心抽象是：

```
Python 前端 → 建構 GraphDef (protobuf)
                  ↓
C++ 執行期 → Session::Run() 執行計算圖
                  ↓
GPU 後端 (CUDA kernel) / CPU 後端 (Eigen)
```

靜態圖的代價是 API 的笨重。開發者需要區分「圖建構階段」和「執行階段」，這在研究中造成了巨大的摩擦。

### PyTorch 的動態圖革命

2016 年，Facebook（現 Meta）的 Adam Paszke 團隊發布了 **PyTorch 0.1**。它的核心設計是**動態計算圖（dynamic graph / define-by-run）**：

```python
# PyTorch 的動態圖：每次前向都重新建構計算圖
x = torch.randn(10, 784)
w = torch.randn(784, 128, requires_grad=True)
h = x.mm(w).clamp(min=0)  # 執行時即建構圖
```

動態圖的優勢顯而易見：
- **可以 debug**：用 Python 的 `pdb` 直接中斷、檢查中間張量
- **控制流自然整合**：`if`、`for` 迴圈不需要特殊的 `tf.cond()` 或 `tf.while_loop()`
- **動態形狀**：RNN 的變長序列無需 padding hack

PyTorch 的動態圖並非沒有代價——每次前向都要重新建構計算圖，這在重複的訓練循環中造成了可觀的開銷。但 PyTorch 團隊用 Eager Mode + TorchScript 的雙軌策略解決了這個問題：研究階段用 Eager，部署階段用 TorchScript（靜態圖）加速。

### JAX：函數式微分的新範式

2018 年，Google 發布了 **JAX**。它不是一個框架，而是一個「可微分數值運算的編譯器」。JAX 的核心是 `grad()`、`jit()`、`vmap()`、`pmap()` 四個轉換器：

```python
import jax.numpy as jnp
from jax import grad, jit

def f(x): return jnp.sin(x).sum()
df = jit(grad(f))  # 先自動微分、再 JIT 編譯
print(df(3.0))     # cos(3.0) ≈ -0.9899
```

JAX 的設計哲學是**函數式**：張量是不可變的，沒有副作用，沒有可變狀態。這讓 JIT 編譯器（XLA）可以進行積極的算子融合和記憶體最佳化。JAX 在語言模型訓練中的效能已經超越了 PyTorch。

### Rust 框架的定位

在最成熟的框架被 Python + C++ 統治的背景下，為什麼 Rust 框架還有機會？

| 框架 | 創建年份 | 後端 | 特色 |
|------|---------|------|------|
| **Candle** | 2022 | CUDA/Metal/CPU | Hugging Face 開發，支援 Llama、Whisper |
| **Burn** | 2023 | CUDA/Metal/WGPU/CPU | 多後端、型別安全、自動微分 |
| **dfdx** | 2022 | CUDA/CPU | 型別層級的形狀檢查（const generics） |
| **tract** | 2018 | CPU | 推論引擎、ONNX 支援、無 std 相容 |

Rust 框架的三個核心優勢：

1. **無 Python 執行期**：Candle 可以在嵌入式裝置上執行，不需要安裝 Python 或 PyTorch
2. **型別安全的形狀**：Burn 和 dfdx 在編譯期檢查張量形狀，消滅維度不匹配的 runtime 錯誤
3. **交叉編譯**：Rust 的交叉編譯生態讓 AI 模型可以直接部署在 ARM 嵌入式裝置上

### 為什麼現在是 Rust AI 框架的時機

有三個趨勢在 2024-2026 年間交會：

- **邊緣 AI 爆發**：LLM 需要在本機執行，Candle 可以取代 Python 堆疊
- **WebGPU 成熟**：Burn 可以編譯到 WebGPU，讓 AI 模型在瀏覽器中執行
- **AI 輔助開發**：LLM 可以自動生成 Rust 算子和 kernel 程式碼，大幅降低開發門檻

Rust 不會取代 Python——Python 的生態和靈活性無可取代。但 Rust 會成為 AI 基礎設施層的關鍵語言：推論引擎、邊緣裝置、效能關鍵路徑——這些領域 Rust 的優勢是壓倒性的。

---

**下一步**：[張量運算：核心資料結構的設計](focus2.md)

## 延伸閱讀

- [Theano: A Python framework for fast computation](https://www.google.com/search?q=Theano+deep+learning+framework)
- [TensorFlow to PyTorch migration](https://www.google.com/search?q=TensorFlow+vs+PyTorch+comparison)
- [JAX: Autograd and XLA](https://www.google.com/search?q=JAX+autograd+XLA+Google)
- [Candle: Minimalist ML for Rust](https://www.google.com/search?q=Candle+Rust+ML+framework+HuggingFace)
- [Burn: Rust deep learning framework](https://www.google.com/search?q=Burn+Rust+deep+learning+framework)
