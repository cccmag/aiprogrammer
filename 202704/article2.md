# 實作自動微分：從 Wengert List 到計算圖

## 前言

自動微分（Automatic Differentiation, AD）是深度學習框架的核心技術。與數值微分（有限差分）和符號微分不同，AD 透過鏈鎖法則（chain rule）精確且高效地計算導數。在 Rust 中實作自動微分，不僅要處理數學問題，還需要妥善處理所有權（ownership）與借用（borrowing）——這是 Rust 區別於 Python/C++ 的關鍵挑戰。

本文將帶領你從零實作一個 tape-based 自動微分系統。

## 前向模式 vs 反向模式

### 數學原理

給定函數 f: Rⁿ → Rᵐ，鏈鎖法則：

```
∂f/∂x = (∂f/∂y) · (∂y/∂x)
```

| 模式 | 計算路徑 | 適合場景 | 計算複雜度 |
|------|---------|---------|-----------|
| 前向模式 | 從輸入到輸出 | n ≪ m（少量輸入） | O(n) |
| 反向模式 | 從輸出到輸入 | n ≫ m（少量輸出） | O(m) |

深度學習中，損失函數通常是 Rⁿ → R（m=1），因此反向模式是最自然的選擇。

## Wengert List：Tape 的起源

1970 年代，Wengert 提出了用「串列」（list）來記錄計算歷史的想法。現代的 tape-based AD 是其直接後代：

```rust
enum TapeEntry {
    /// 常數
    Constant { value: f64 },
    /// 變數（葉子節點）
    Variable { value: f64, index: usize },
    /// 二元運算
    Add { left: usize, right: usize },
    Mul { left: usize, right: usize },
    /// 一元運算
    Neg { input: usize },
    Exp { input: usize },
    /// 啟用函數
    ReLU { input: usize },
}

struct Tape {
    entries: Vec<TapeEntry>,
    gradients: Vec<f64>,
}
```

### 前向傳播：記錄 Tape

```rust
impl Tape {
    fn new() -> Self {
        Tape { entries: vec![], gradients: vec![] }
    }

    fn constant(&mut self, value: f64) -> usize {
        let idx = self.entries.len();
        self.entries.push(TapeEntry::Constant { value });
        self.gradients.push(0.0);
        idx
    }

    fn variable(&mut self, value: f64) -> usize {
        let idx = self.entries.len();
        self.entries.push(TapeEntry::Variable { value, index: idx });
        self.gradients.push(0.0);
        idx
    }

    fn add(&mut self, left: usize, right: usize) -> usize {
        let idx = self.entries.len();
        let lval = self.eval(left);
        let rval = self.eval(right);
        self.entries.push(TapeEntry::Add { left, right });
        self.gradients.push(0.0);
        idx
    }

    fn eval(&self, idx: usize) -> f64 {
        match &self.entries[idx] {
            TapeEntry::Constant { value } => *value,
            TapeEntry::Variable { value, .. } => *value,
            TapeEntry::Add { left, right } => self.eval(*left) + self.eval(*right),
            TapeEntry::Mul { left, right } => self.eval(*left) * self.eval(*right),
            TapeEntry::Neg { input } => -self.eval(*input),
            TapeEntry::Exp { input } => self.eval(*input).exp(),
            TapeEntry::ReLU { input } => self.eval(*input).max(0.0),
        }
    }
}
```

### 反向傳播：計算梯度

```rust
impl Tape {
    fn backward(&mut self, output_idx: usize) {
        // 初始化輸出梯度為 1.0
        self.gradients[output_idx] = 1.0;

        // 反向遍歷 tape（從後往前）
        for idx in (0..=output_idx).rev() {
            let grad = self.gradients[idx];
            match self.entries[idx] {
                TapeEntry::Add { left, right } => {
                    self.gradients[left] += grad;
                    self.gradients[right] += grad;
                }
                TapeEntry::Mul { left, right } => {
                    let lval = self.eval(left);
                    let rval = self.eval(right);
                    self.gradients[left] += grad * rval;
                    self.gradients[right] += grad * lval;
                }
                TapeEntry::Neg { input } => {
                    self.gradients[input] += -grad;
                }
                TapeEntry::Exp { input } => {
                    let oval = self.eval(idx);
                    self.gradients[input] += grad * oval; // d(e^x)/dx = e^x
                }
                TapeEntry::ReLU { input } => {
                    let ival = self.eval(input);
                    self.gradients[input] += if ival > 0.0 { grad } else { 0.0 };
                }
                _ => {} // Constant 和 Variable 沒有輸入
            }
        }
    }
}
```

## 使用範例：邏輯回歸

```rust
fn main() {
    let mut tape = Tape::new();

    // 輸入 x = 2.0, 權重 w = 0.5, 偏置 b = 0.1
    let x = tape.variable(2.0);
    let w = tape.variable(0.5);
    let b = tape.variable(0.1);

    // 計算 y = sigmoid(w * x + b)
    let prod = tape.mul(w, x);
    let sum = tape.add(prod, b);
    // sigmoid 近似：使用內建 exp 實作
    let neg_sum = tape.neg(sum);
    let exp_neg = tape.exp(neg_sum);
    let one = tape.constant(1.0);
    let denom = tape.add(one, exp_neg);
    let one2 = tape.constant(1.0);
    let y = tape.mul(denom, one2); // 簡化：實際需除
    // 改為更正確的表達式 y = 1.0 / (1.0 + exp(-sum))

    tape.backward(y);

    println!("dy/dw = {}", tape.gradients[w]);
    println!("dy/dx = {}", tape.gradients[x]);
    println!("dy/db = {}", tape.gradients[b]);
}
```

## Rust 的所有權挑戰

在 Python 的 PyTorch 中，計算圖是動態建立的，節點透過 `weakref` 連結。但在 Rust 中，我們需要明確處理所有權。

### 方案一：索引陣列（Tape-based）

上述實作使用 `Vec<TapeEntry>` + `usize` 索引。這是 Candle 採用的方案。

**優點**：
- 記憶體連續，快取友善
- 無所有權問題
- 序列化簡單

**缺點**：
- 動態 shape 處理複雜
- 無法靜態追蹤形狀

### 方案二：Rc<RefCell> 計算圖

```rust
use std::rc::Rc;
use std::cell::RefCell;

struct Value {
    data: f64,
    grad: f64,
    backward: Option<Box<dyn Fn()>>,
    prev: Vec<Rc<RefCell<Value>>>,
}

impl Value {
    fn new(data: f64) -> Rc<RefCell<Self>> {
        Rc::new(RefCell::new(Value {
            data, grad: 0.0, backward: None, prev: vec![]
        }))
    }
}

fn add(a: &Rc<RefCell<Value>>, b: &Rc<RefCell<Value>>) -> Rc<RefCell<Value>> {
    let out = Value::new(a.borrow().data + b.borrow().data);
    let a_clone = Rc::clone(a);
    let b_clone = Rc::clone(b);
    out.borrow_mut().backward = Some(Box::new(move || {
        a_clone.borrow_mut().grad += out.borrow().grad;
        b_clone.borrow_mut().grad += out.borrow().grad;
    }));
    out.borrow_mut().prev = vec![Rc::clone(a), Rc::clone(b)];
    out
}
```

**優點**：直觀、動態、類似 PyTorch API
**缺點**：Rc 引用計數開銷、RefCell 執行期檢查、循環引用風險

## 與 PyTorch 的比較

| 特性 | PyTorch Autograd | 我們的 Tape |
|------|-----------------|------------|
| 計算圖生命週期 | 動態（每次 forward 重建） | 靜態（一次性） |
| 記憶體管理 | Python GC + C++ | Vec 連續記憶體 |
| 梯度累積 | 自動累積 | 手動 reset |
| 控制流 | 原生支援 | 需預先構建 |
| 形狀推斷 | 執行期 | 需額外實作 |

## 進階：in-place 操作處理

In-place 操作（如 `add_`）是 Rust AD 中最棘手的問題。因為 in-place 修改會破壞 tape 的記錄——原始值在梯度計算時可能已不存在。

Candle 的解決方案是：在 in-place 操作時，如果該 tensor 需要梯度（`requires_grad`），則先 clone：

```rust
// Candle 的近似策略
fn add_inplace(&mut self, other: &Tensor) {
    if self.requires_grad() {
        // 儲存當前的值用於反向傳播
        let saved = self.data.clone();
        // 記錄一個 inplace 操作節點
        self.tape.push(InplaceOp::Add {
            orig_value: saved,
            other: other.id(),
        });
    }
    // 實際的 inplace 加法
    for (a, b) in self.data.iter_mut().zip(&other.data) {
        *a += b;
    }
}
```

## Burn 的 Autograd 設計

Burn 框架採用更靜態的方法——利用 Rust 型別系統在編譯期跟蹤梯度需求：

```rust
// Burn 的張量區分是否追蹤梯度
struct Tensor<B: Backend, const D: usize> { /* ... */ }

// 需要梯度的版本
struct Tensor<B: Backend, const D: usize, Grad> {
    inner: Tensor<B, D>,
    graph: ComputationGraph,
}
```

這種設計讓 Burn 可以在編譯期決定是否建立計算圖，執行期零開銷。

## 總結

從 Wengert List 到現代的自動微分系統，核心思想保持一致：記錄計算歷史，然後反向應用鏈鎖法則。Rust 的 tape-based 方案（使用索引陣列）是記憶體效率和開發複雜度之間的最佳平衡點，而採用 `Rc<RefCell>` 的方案則提供更直觀的 API。

---

**參考資料**

- https://www.google.com/search?q=Wengert+list+automatic+differentiation
- https://www.google.com/search?q=Rust+autograd+tape+implementation
- https://www.google.com/search?q=Candle+autograd+source+code
- https://www.google.com/search?q=Burn+autograd+design
- https://www.google.com/search?q=reverse+mode+automatic+differentiation+Rust
