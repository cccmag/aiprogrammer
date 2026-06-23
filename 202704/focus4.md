# 神經網路層與損失函數

## Linear、Conv2d、LSTM、ReLU、GELU、CrossEntropy（2012-2026）

### 全連接層（Linear / Dense）

全連接層是神經網路最基礎的構建模塊。數學上很簡單：y = xWᵀ + b。但實作細節決定了效能：

```rust
struct Linear {
    weight: Tensor,  // 形狀 [out_features, in_features]
    bias: Tensor,    // 形狀 [out_features]
}

impl Linear {
    fn forward(&self, x: &Tensor) -> Tensor {
        // y = x @ Wᵀ + b
        let out = x.matmul(&self.weight.t());  // 矩陣乘法
        out + &self.bias                        // 廣播加法
    }
}
```

矩陣乘法是深度學習的 bread and butter。在 CPU 上，Rust 可以使用 `faer` crate（純 Rust 線性代數函式庫）或 `cblas` 綁定。在 GPU 上，需要使用 CUDA 的 cuBLAS 或 Metal 的 MPS。

### 卷積層（Conv2d）

卷積層在影像處理中至關重要。其核心是 **im2col**（image to column）演算法：將輸入影像的每個卷積視窗展開為矩陣的一列，然後透過 `matmul` 計算：

```rust
struct Conv2d {
    weight: Tensor,  // [out_channels, in_channels, kernel_h, kernel_w]
    bias: Tensor,    // [out_channels]
    stride: usize,
    padding: usize,
}

impl Conv2d {
    fn forward(&self, x: &Tensor) -> Tensor {
        // x 形狀: [batch, in_channels, height, width]
        let cols = im2col(x, self.kernel_size(), self.stride, self.padding);
        // cols 形狀: [out_h * out_w, in_channels * kernel_h * kernel_w]
        let weight_flat = self.weight.view()
            .reshape([self.weight.shape[0], -1]);
        let out = cols.matmul(&weight_flat.t());  // [out_h*out_w, out_channels]
        out.reshape([batch, out_h, out_w, out_channels])
            .permute([0, 3, 1, 2])  // NCHW
    }
}
```

im2col 的優點是演算法簡單（全部歸結為矩陣乘法）；缺點是記憶體膨脹——kernel 大小為 3×3 時，記憶體用量增長約 9 倍。

### 循環層（RNN / LSTM）

RNN 維護一個隱藏狀態，在時間步之間傳遞。LSTM 在此基礎上加入了遺忘閘、輸入閘、輸出閘來解決梯度消失問題：

```rust
struct LSTMCell {
    w_ih: Tensor,  // 輸入到隱藏的權重 [4*hidden, input_size]
    w_hh: Tensor,  // 隱藏到隱藏的權重 [4*hidden, hidden_size]
    bias: Tensor,  // [4*hidden]
}

impl LSTMCell {
    fn forward(&self, x: &Tensor, state: &(Tensor, Tensor))
        -> (Tensor, Tensor)
    {
        let (h, c) = state;
        let gates = x.matmul(&self.w_ih.t())
                  + h.matmul(&self.w_hh.t())
                  + &self.bias;
        // 拆成 i, f, g, o 四個閘門
        let chunks = gates.chunk(4, -1);
        let i = chunks[0].sigmoid();
        let f = chunks[1].sigmoid();
        let g = chunks[2].tanh();
        let o = chunks[3].sigmoid();
        let c_new = f * &c + i * g;
        let h_new = o * c_new.tanh();
        (h_new, c_new)
    }
}
```

### 啟用函數

啟用函數提供非線性變換。以下是四個最常見的啟用函數的 Rust 實作：

```rust
fn relu(x: &Tensor) -> Tensor {
    // max(0, x) — 逐元素比較
    x.maximum(&Tensor::zeros(x.shape()))
}

fn sigmoid(x: &Tensor) -> Tensor {
    // 1 / (1 + e^(-x))
    x.neg().exp().add_scalar(1.0).recip()
}

fn tanh(x: &Tensor) -> Tensor {
    // (e^x - e^(-x)) / (e^x + e^(-x))
    let e_x = x.exp();
    let e_nx = x.neg().exp();
    (e_x - e_nx) / (e_x + e_nx)
}

fn gelu(x: &Tensor) -> Tensor {
    // x * Φ(x), where Φ is the standard normal CDF
    // 近似: 0.5 * x * (1 + tanh(sqrt(2/π) * (x + 0.044715 * x^3)))
    let sqrt_2_pi = (2.0 / std::f32::consts::PI).sqrt();
    let x3 = x.powf(3.0);
    let inner = sqrt_2_pi * (x + 0.044715 * x3);
    0.5 * x * (inner.tanh().add_scalar(1.0))
}
```

GELU 是 GPT 和 BERT 系列模型的標配，因為它提供了更平滑的梯度特性。

### 損失函數

**均方差（MSE Loss）**：

```rust
fn mse_loss(pred: &Tensor, target: &Tensor) -> Tensor {
    let diff = pred - target;
    (diff * diff).mean()  // 所有元素的平均平方誤差
}
```

**交叉熵（CrossEntropy Loss）**：最常用的分類損失。分為 log_softmax 和 nll_loss 兩個步驟：

```rust
fn cross_entropy_loss(logits: &Tensor, targets: &[usize]) -> Tensor {
    // logits 形狀: [batch, num_classes]
    // 1. softmax 的數值穩定版本: logits - max(logits)
    let max_vals = logits.max(-1, true);  // 沿 class 維度取最大值
    let shifted = logits - &max_vals;
    let softmax = shifted.exp() / shifted.exp().sum(-1, true);
    // 2. 只取 target 對應的負對數
    let mut loss = 0.0;
    for (i, &t) in targets.iter().enumerate() {
        loss -= softmax.get([i, t]).ln();
    }
    Tensor::scalar(loss / targets.len() as f32)
}
```

### Rust Trait 設計模式

Rust 的 trait 系統為神經網路層提供了優雅的抽象：

```rust
// 所有層的共同介面
trait Layer {
    fn forward(&self, input: &Tensor) -> Tensor;
    fn params(&self) -> Vec<Rc<RefCell<Tensor>>>;
}

// 啟用函數也是一種 Layer
struct ReLU;
impl Layer for ReLU {
    fn forward(&self, input: &Tensor) -> Tensor {
        input.maximum(&Tensor::zeros(input.shape()))
    }
    fn params(&self) -> Vec<Rc<RefCell<Tensor>>> {
        vec![]  // 啟用函數沒有參數
    }
}

// 序貫模型：層的組合
struct Sequential {
    layers: Vec<Box<dyn Layer>>,
}

impl Layer for Sequential {
    fn forward(&self, input: &Tensor) -> Tensor {
        let mut x = input.clone();
        for layer in &self.layers {
            x = layer.forward(&x);
        }
        x
    }
    fn params(&self) -> Vec<Rc<RefCell<Tensor>>> {
        self.layers.iter().flat_map(|l| l.params()).collect()
    }
}
```

這種模式讓建構模型變得直觀：

```rust
let model = Sequential::new(vec![
    Box::new(Linear::new(784, 128)),
    Box::new(ReLU),
    Box::new(Linear::new(128, 10)),
]);
```

---

**下一步**：[模型序列化與部署](focus5.md)

## 延伸閱讀

- [Deep Learning book — CNN and RNN architectures](https://www.google.com/search?q=CNN+RNN+deep+learning+architecture+explained)
- [GELU activation function](https://www.google.com/search?q=GELU+Gaussian+Error+Linear+Unit+activation)
- [Cross entropy loss for classification](https://www.google.com/search?q=cross+entropy+loss+softmax+classification)
- [Burn module system](https://www.google.com/search?q=Burn+Rust+neural+network+module+layer)
- [Rust trait object for neural networks](https://www.google.com/search?q=Rust+trait+object+neural+network+layer+design)
