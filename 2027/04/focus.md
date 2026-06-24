# 本期焦點

## Rust 在 AI 框架開發中的應用 — 從深度學習框架到推論引擎

### 引言

長期以來，深度學習框架的生態被 Python 主導。TensorFlow、PyTorch、JAX——這些框架的 Python 前端只是冰山一角；它們的底層核心（GPU 運算、自動微分、計算圖優化）都是用 C/C++ 編寫的。Python 是膠水，C++ 是引擎。

但 Rust 正在改變這個格局。它的獨特優勢——零成本抽象、所有權保證的記憶體安全、無 GC、以及與 C 平等的 FFI——讓它成為建構 AI 基礎設施的天然選擇。

這不是理論上的推測。Candle（由 Hugging Face 開發）、Burn、dfdx、tract——這些純 Rust 的深度學習框架已經在生產環境中運作。它們不需要 Python 執行期，可以交叉編譯到嵌入式裝置，且能利用 Rust 的型別系統在編譯期檢查張量形狀。

本期將帶領你從張量運算和自動微分的基礎開始，逐步建構出一個完整的 mini 深度學習框架，最後探討 AI 如何幫助我們開發更好的 AI 工具。

---

## 大綱

* [程式：實作 mini-dl — 從零開始的深度學習框架](focus_code.md)
   - 張量（Tensor）資料結構
   - 自動微分（Autograd）
   - 神經網路層（Linear、ReLU、CrossEntropyLoss）
   - 隨機梯度下降（SGD）訓練

1. [深度學習框架的演進（2007-2026）](focus1.md)
   - Theano→TensorFlow→PyTorch→JAX 的歷史
   - 靜態圖 vs 動態圖
   - Rust 框架的定位與優勢

2. [張量運算：核心資料結構的設計（2015-2026）](focus2.md)
   - 張量的記憶體佈局（row-major、strides）
   - 廣播（broadcasting）規則
   - GPU 加速的挑戰

3. [自動微分：反向傳播的實作（1986-2026）](focus3.md)
   - 計算圖與反向模式微分
   - Rust 中所有權與計算圖的交疊
   - 梯度累積與更新

4. [神經網路層與損失函數（2012-2026）](focus4.md)
   - 全連接層、卷積層、循環層
   - 啟用函數（ReLU、Sigmoid、GELU）
   - 交叉熵與均方差損失

5. [模型序列化與部署（2016-2026）](focus5.md)
   - ONNX 格式與 Rust 解析
   - 量化（INT8、FP16）技術
   - 邊緣裝置部署策略

6. [推論引擎最佳化（2018-2026）](focus6.md)
   - 算子融合（operator fusion）
   - 記憶體複用與記憶體規劃
   - 多執行緒推論與批次處理

7. [AI 輔助 AI 框架開發（2024-2026）](focus7.md)
   - LLM 生成算子實作
   - AI 輔助模型架構搜尋（NAS）
   - 自動化測試與效能預測

---

## AI 框架層次

```
應用層 (模型定義、訓練腳本、資料載入)
      │
自動微分 (計算圖、梯度計算、反向傳播)
      │
神經網路層 (Linear、Conv2d、RNN、Loss)
      │
張量運算 (形狀管理、廣播、基本運算)
      │
後端 (CPU / CUDA / Metal / WebGPU)
```

## 濃縮回顧

### 深度學習框架歷史

| 年份 | 框架 | 創新 |
|------|------|------|
| 2007 | Theano | 首個 Python DL 框架，自動微分 |
| 2015 | TensorFlow | Google 的靜態圖框架 |
| 2016 | PyTorch | Facebook 的動態圖框架 |
| 2018 | JAX | Google 的可微分數值運算 |
| 2022 | Candle | Hugging Face 的純 Rust 框架 |
| 2023 | Burn | 純 Rust、多後端 DL 框架 |
| 2025 | Rust 框架成熟 | Candle + Burn 覆蓋 NLP/CV |

### Rust 在 AI 領域的獨特優勢

| 特性 | Rust | Python | C++ |
|------|------|--------|-----|
| 記憶體安全 | 編譯期保證 | GC | 需經驗 |
| 無 Python 執行期 | ✅ | ❌ | ✅ |
| 交叉編譯 | ✅ | ❌ | 部分 |
| 型別安全 | ✅ | 動態 | 部分 |
| 生態成熟度 | 成長中 | 極成熟 | 成熟 |

### 最小訓練循環

我們的 `mini-dl` 框架核心：

```rust
// 定義模型
struct TwoLayerNet {
    l1: Linear,
    l2: Linear,
}

impl TwoLayerNet {
    fn forward(&self, x: &Tensor) -> Tensor {
        let h = self.l1.forward(x).relu();
        self.l2.forward(&h)
    }
}

// 訓練循環
fn train() {
    let model = TwoLayerNet::new(784, 128, 10);
    let optimizer = SGD::new(model.params(), 0.01);

    for epoch in 0..10 {
        let pred = model.forward(&x);
        let loss = cross_entropy_loss(&pred, &y);
        loss.backward();
        optimizer.step();

        println!("epoch {epoch} loss = {:.4}", loss.item());
    }
}
```

### 自動微分的核心

反向模式自動微分透過追蹤計算圖實現：

```rust
struct Tensor {
    data: Vec<f32>,
    shape: Vec<usize>,
    grad: Option<Vec<f32>>,
    // 計算圖節點
    backward_fn: Option<Box<dyn Fn(&mut Tensor)>>,
    children: Vec<Rc<RefCell<Tensor>>>,
}

impl Tensor {
    fn backward(&mut self) {
        // 拓撲排序後反向遍歷計算圖
        // 每個節點呼叫其 backward_fn
    }
}
```

---

**下一步**：[程式實作](focus_code.md) → [深度學習框架的演進](focus1.md)

## 延伸閱讀

- [Candle: Minimalist ML framework for Rust](https://www.google.com/search?q=Candle+Rust+ML+framework)
- [Burn: Rust deep learning framework](https://www.google.com/search?q=Burn+Rust+deep+learning)
- [Automatic Differentiation in Rust](https://www.google.com/search?q=automatic+differentiation+Rust)
- [ONNX Runtime Rust API](https://www.google.com/search?q=ONNX+Runtime+Rust)
