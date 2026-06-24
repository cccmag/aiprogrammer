# 程式實作：mini-dl — 從零開始的深度學習框架

## 簡介

本實作展示如何用 Rust 從零建構一個迷你深度學習框架，包含張量運算、神經網路層、自動微分（手動實作梯度）、SGD 最佳化器，以及在螺旋資料集上訓練分類模型。完整程式碼在 `_code/src/lib.rs`。

## 核心元件

### 1. 張量（Tensor）

張量是多維陣列的基礎資料結構：

```rust
pub struct TensorData {
    pub data: Vec<f32>,
    pub shape: Vec<usize>,
    pub grad: Option<Vec<f32>>,
}
```

使用 `Rc<RefCell<TensorData>>` 實現共享所有權，方便計算圖的建構。

### 2. 基本運算

我們實作了完整的矩陣運算：

```rust
pub fn matmul(a: &SharedTensor, b: &SharedTensor) -> SharedTensor { ... }
pub fn add(a: &SharedTensor, b: &SharedTensor) -> SharedTensor { ... }
pub fn relu(t: &SharedTensor) -> SharedTensor { ... }
pub fn softmax(t: &SharedTensor) -> SharedTensor { ... }
```

`add` 支援 broadcasting，允許 (n, d) 與 (1, d) 形狀相加。

### 3. 神經網路層

```rust
pub struct Linear {
    pub w: SharedTensor,   // 權重 (in_features x out_features)
    pub b: SharedTensor,   // 偏置 (1 x out_features)
}

impl Linear {
    pub fn forward(&self, x: &SharedTensor) -> SharedTensor {
        let z = matmul(x, &self.w);
        add(&z, &self.b)
    }
}
```

### 4. 損失函數

交叉熵損失結合 softmax：

```rust
pub fn cross_entropy_loss(pred: &SharedTensor, target: &SharedTensor) -> SharedTensor {
    // -sum(target * log(pred)) / n
}
```

### 5. 最佳化器

```rust
pub struct SGD {
    params: Vec<SharedTensor>,
    lr: f32,
}

impl SGD {
    pub fn step(&self, grads: &[Vec<f32>]) {
        for (param, grad) in self.params.iter().zip(grads.iter()) {
            let mut param = param.borrow_mut();
            for i in 0..param.data.len() {
                param.data[i] -= self.lr * grad[i];
            }
        }
    }
}
```

### 6. 反向傳播（手動梯度）

```rust
pub fn backward_two_layer(
    x, h, a, l1, l2, logits, target,
) -> [Vec<f32>; 4] {
    // 1. softmax 輸出
    // 2. dL/dlogits = (softmax - target) / n
    // 3. dL/dw2 = a^T @ dL/dlogits
    // 4. dL/da = dL/dlogits @ w2^T
    // 5. dL/dh = dL/da * (h > 0)  （ReLU 反向）
    // 6. dL/dw1 = x^T @ dL/dh
    // 7. 回傳 [dw1, db1, dw2, db2]
}
```

## 訓練流程

### 螺旋資料集

我們生成三類螺旋資料作為分類任務：

```rust
let (x, y) = make_spiral_data(100);
// x shape: (300, 2), y shape: (300, 3)  — one-hot encoding
```

### 模型與訓練

```rust
let l1 = Linear::new(2, 32);
let l2 = Linear::new(32, 3);
let sgd = SGD::new(vec![l1.w, l1.b, l2.w, l2.b], 0.5);

for epoch in 0..1000 {
    let (h, a, logits, loss) = forward_two_layer(&x, &l1, &l2, &y);
    let grads = backward_two_layer(&x, &h, &a, &l1, &l2, &logits, &y);
    sgd.step(&grads);
}
```

## 執行結果

```
epoch   0  loss=1.100  acc=33.7%
epoch 500  loss=1.056  acc=48.3%
epoch 999  loss=1.015  acc=48.0%
```

對於 2 層網路 + 32 隱藏單元 + SGD 的簡單組合，在 3 類別螺旋資料上達到 ~48% 準確率（隨機基準為 33%）。

## 與 Candle/Burn 的對比

| 特性 | mini-dl | Candle | Burn |
|------|---------|--------|------|
| 自動微分 | 手動 | 自動 | 自動 |
| GPU 支援 | ❌ | CUDA/Metal | WGPU |
| 型別安全 | 無 | Shape 檢查 | Shape 檢查 |
| 程式碼行數 | ~500 | ~50K | ~100K |

## 延伸練習

1. **加入 BatchNorm**：實作 Batch Normalization 層及其梯度
2. **加入 Dropout**：實作訓練/推論模式切換
3. **多層網路**：支援任意數量的隱藏層
4. **自動微分**：實作真正的計算圖與反向傳播（如 `autograd`）
5. **GPU 支援**：接入 wgpu 計算著色器加速張量運算

## 執行與測試

```bash
cd _code
cargo build
cargo test    # 8 個測試全部通過
cargo run     # 訓練 1000 個 epoch
```
