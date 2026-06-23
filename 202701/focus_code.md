# mini-ml：從零開始的 ML 推論引擎

## 概述

mini-ml 是一個從零實作的純 Rust 推論引擎，沒有任何外部 ML 框架依賴。它展示了張量運算、線性層、激勵函式和前向傳播的核心機制：

1. **張量（Tensor）** — 多維陣列與基本運算（matmul、transpose、add、sum）
2. **激勵函式** — ReLU、Sigmoid、Softmax
3. **線性層（Linear）** — 全連接層的前向傳播
4. **MLP** — 多層感知器的組合與推論
5. **預訓練模型** — 硬編碼權重的 XOR 分類器

## 核心概念

### 1. 張量：ML 的原子

張量是機器學習中最基礎的資料結構——一個多維陣列，搭配形狀（shape）資訊：

```rust
struct Tensor {
    data: Vec<f32>,
    shape: Vec<usize>,
}

impl Tensor {
    fn new(data: Vec<f32>, shape: Vec<usize>) -> Self {
        assert_eq!(data.len(), shape.iter().product());
        Tensor { data, shape }
    }
}
```

矩陣乘法（matmul）是最核心的運算，也是神經網路中計算量最大的部分：

```rust
pub fn matmul(&self, other: &Tensor) -> Tensor {
    let m = self.rows();
    let n = self.cols();
    let p = other.cols();
    let mut data = vec![0.0f32; m * p];
    for i in 0..m {
        for k in 0..n {
            let aik = self.data[i * n + k];
            for j in 0..p {
                data[i * p + j] += aik * other.data[k * p + j];
            }
        }
    }
    Tensor::new(data, vec![m, p])
}
```

### 2. 激勵函式：非線性的來源

單純的線性變換堆疊再多層也還是線性的。激勵函式提供了非線性能力：

```rust
pub fn relu(t: &Tensor) -> Tensor {
    let data = t.data.iter().map(|&x| x.max(0.0)).collect();
    Tensor::new(data, t.shape.clone())
}

pub fn softmax(t: &Tensor) -> Tensor {
    // 將 logits 轉換為機率分佈
    // 每個元素介於 0-1，行總和為 1
}
```

| 函式 | 公式 | 用途 |
|------|------|------|
| ReLU | `max(0, x)` | 隱藏層最常見的激勵函式 |
| Sigmoid | `1 / (1 + e^(-x))` | 二元分類輸出 |
| Softmax | `e^x_i / Σ e^x_j` | 多元分類輸出 |

### 3. 線性層：權重 × 輸入 + 偏置

線性層（全連接層）是神經網路的基本建構塊：

```rust
struct Linear {
    weight: Tensor,  // [out_features, in_features]
    bias: Tensor,    // [out_features]
}

impl Linear {
    fn forward(&self, input: &Tensor) -> Tensor {
        // output = input @ weight.T + bias
        let z = input.matmul(&self.weight.transpose());
        // 加上偏置（廣播到每一行）
        let mut data = Vec::with_capacity(z.data.len());
        for (i, val) in z.data.iter().enumerate() {
            data.push(val + self.bias.data[i % n]);
        }
        Tensor::new(data, z.shape.clone())
    }
}
```

### 4. MLP：多層感知器的推論管線

一個 2 層 MLP 的完整前向傳播：

```rust
struct Mlp {
    fc1: Linear,  // input → hidden
    fc2: Linear,  // hidden → output
}

impl Mlp {
    fn predict(&self, input: &Tensor) -> Tensor {
        let h = relu(&self.fc1.forward(input));
        // 在真實框架中，這裡可能還有 dropout、batch norm 等
        let logits = self.fc2.forward(&h);
        softmax(&logits)
    }
}
```

### 5. XOR 模型：非線性分類的經典案例

XOR（互斥或）問題說明了為什麼神經網路需要隱藏層——單層感知器無法解決 XOR，但加上一層隱藏層就可以了。

mini-ml 內建了一組手算的權重：

| 層 | 形狀 | 功能 |
|------|------|------|
| fc1.weight | [4, 2] | 將 2D 輸入映射到 4D 隱藏空間 |
| fc1.bias | [4] | 四顆隱藏神經元的閾值 |
| fc2.weight | [2, 4] | 從隱藏空間映射到 2 類輸出 |
| fc2.bias | [2] | 輸出偏移 |

推論結果：
```
XOR(0, 0) → 0 (confidence: 73.1%)
XOR(0, 1) → 1 (confidence: 88.1%)
XOR(1, 0) → 1 (confidence: 88.1%)
XOR(1, 1) → 0 (confidence: 73.1%)
```

## 與真實框架的對照

| mini-ml | Candle | Burn | PyTorch |
|---------|--------|------|---------|
| `Tensor::new()` | `Tensor::from_slice()` | `Tensor::from_data()` | `torch.tensor()` |
| `t.matmul(&u)` | `t.matmul(&u)` | `t.matmul(u)` | `t @ u` |
| `softmax(&t)` | `t.softmax()` | `t.softmax()` | `F.softmax(t)` |
| `Linear::forward()` | `Linear::forward()` | `Linear::forward()` | `nn.Linear.forward()` |
| `Mlp::predict()` | `Model::forward()` | `Model::forward()` | `model.forward()` |

## 測試

```
running 12 tests
test tests::test_matmul ... ok
test tests::test_matmul_non_square ... ok
test tests::test_batch_inference ... ok
test tests::test_cross_entropy ... ok
test tests::test_linear_forward ... ok
test tests::test_one_hot ... ok
test tests::test_relu ... ok
test tests::test_sigmoid ... ok
test tests::test_softmax ... ok
test tests::test_tensor_creation ... ok
test tests::test_tensor_sum ... ok
test tests::test_xor_prediction ... ok
test result: ok. 12 passed; 0 failed
```

## mini-ml 教會我們的事

### 1. 張量運算是一切的核心

神經網路說到底就是一連串的張量運算。理解 matmul、transpose 和 broadcast 的實作細節，就掌握了 ML 框架的核心。

### 2. 推論比訓練簡單得多

mini-ml 實作了前向傳播，但沒有反向傳播。這是因為在部署場景中，我們只需要**執行**已經訓練好的模型。Candle、Burn、tract 等框架也是同樣的設計哲學。

### 3. 權重是模型的核心資產

mini-ml 的 XOR 模型權重是手算的硬編碼。在真實世界中，這些權重來自 PyTorch 等框架訓練後匯出的 ONNX 或 safetensors 檔案。Rust 推論引擎的工作就是載入這些權重並高效地執行前向傳播。

### 4. Rust 在 ML 部署中的定位

Python 仍然主導訓練階段。Rust 的優勢在於部署——將訓練好的模型整合到沒有 Python 執行期的生產環境、邊緣裝置或瀏覽器中。

---

## 延伸閱讀

- [完整程式碼](_code/src/lib.rs)
- [Candle 框架](https://www.google.com/search?q=Candle+ML+framework+Rust)
- [Burn 深度學習框架](https://www.google.com/search?q=Burn+deep+learning+Rust)
- [tract ONNX 推論](https://www.google.com/search?q=tract+ONNX+Rust)
- [Neural Networks and Deep Learning](https://www.google.com/search?q=Neural+networks+and+deep+learning+online+book)
