# 自動微分：反向傳播的實作

## 計算圖、Wengert List、所有權與梯度流（1986-2026）

### 從數學到程式

自動微分（Automatic Differentiation, AD）不是數值微分（有限差分），也不是符號微分（展開表達式）。它基於一個簡單的觀察：**任何可微函數都可以分解為一系列基本運算，每個運算的導數是已知的**。

### 前向模式 vs 反向模式

```rust
// f(x, y) = x * y + sin(x)
// 前向模式：同時計算值和導數
struct Dual {
    val: f32,
    der: f32,
}

impl Dual {
    fn sin(self) -> Dual {
        Dual { val: self.val.sin(), der: self.der * self.val.cos() }
    }
}

impl std::ops::Mul for Dual {
    type Output = Dual;
    fn mul(self, rhs: Dual) -> Dual {
        Dual { val: self.val * rhs.val, der: self.val * rhs.der + self.der * rhs.val }
    }
}

// f(2, 3) 且 df/dx:
let x = Dual { val: 2.0, der: 1.0 };  // der=1 表示對 x 微分
let y = Dual { val: 3.0, der: 0.0 };
let result = x * y + x.sin();
// result.der = f_x(2, 3) = y + cos(x) = 3 + (-0.416) ≈ 2.584
```

前向模式適合**輸入少、輸出多**的場景（如 f: ℝⁿ → ℝᵐ, n ≪ m）。但深度學習中的損失函數是 f: ℝⁿ → ℝ（單一輸出、百萬參數）——反向模式才是正確的選擇。

**反向模式自動微分**（又稱**反向傳播**）分為兩個階段：
1. **前向傳播（forward pass）**：計算每個節點的值，記錄計算軌跡
2. **反向傳播（backward pass）**：從輸出開始，鏈式法則反向傳播梯度

### Wengert List（W 字節碼 / Tape）

Wengert List（又稱 W 表達式、tape、或 Wengert tape）是反向模式 AD 最常用的實作方式。它本質上是一個**線性化的計算軌跡記錄**：

```rust
// 一個簡化的 tape 實作
enum Op {
    Add(usize, usize),     // 結果 = 輸入 a + 輸入 b
    Mul(usize, usize),     // 結果 = 輸入 a * 輸入 b
    Sin(usize),            // 結果 = sin(輸入 a)
    Variable(f32),         // 葉節點：常數或參數
}

struct Tape {
    ops: Vec<Op>,           // 依序記錄的操作
    values: Vec<f32>,       // 每個節點的值（前向時填充）
    grads: Vec<f32>,        // 每個節點的梯度（反向時填充）
}

impl Tape {
    fn forward(&mut self) {
        for (i, op) in self.ops.iter().enumerate() {
            self.values[i] = match op {
                Op::Add(a, b) => self.values[*a] + self.values[*b],
                Op::Mul(a, b) => self.values[*a] * self.values[*b],
                Op::Sin(a) => self.values[*a].sin(),
                Op::Variable(v) => *v,
            };
        }
    }

    fn backward(&mut self) {
        let n = self.ops.len();
        self.grads[n - 1] = 1.0;  // d loss / d loss = 1
        for i in (0..n).rev() {
            match &self.ops[i] {
                Op::Add(a, b) => {
                    self.grads[*a] += self.grads[i];
                    self.grads[*b] += self.grads[i];
                }
                Op::Mul(a, b) => {
                    self.grads[*a] += self.grads[i] * self.values[*b];
                    self.grads[*b] += self.grads[i] * self.values[*a];
                }
                Op::Sin(a) => {
                    self.grads[*a] += self.grads[i] * self.values[*a].cos();
                }
                Op::Variable(_) => {}  // 葉節點：停止
            }
        }
    }
}
```

Tape 的優點是簡潔且可以處理任意控制流（if、while、遞歸）——因為 tape 是實際執行軌跡的記錄，不是靜態分析。缺點是需要儲存所有中間值，記憶體開銷與計算深度成正比。

### Rust 中所有權與計算圖的挑戰

在 Python 的 PyTorch 中，計算圖是一個 DAG（有向無環圖），節點的生命週期由 GC 管理。在 Rust 中，我們沒有 GC——這意味著我們需要明確管理圖節點的共享與回收。

最常見的 Rust 模式是 `Rc<RefCell<T>>`：

```rust
use std::rc::Rc;
use std::cell::RefCell;

struct Tensor {
    data: Vec<f32>,
    grad: Vec<f32>,
    requires_grad: bool,
    // 計算圖相關
    grad_fn: Option<Box<dyn Fn(&mut [f32], &[f32])>>,
    parents: Vec<Rc<RefCell<Tensor>>>,
}

impl Drop for Tensor {
    fn drop(&mut self) {
        // Rc 引用計數自動管理
        // 當所有引用消失時，計算圖子圖自動釋放
    }
}
```

但 `Rc<RefCell<T>>` 不是沒有代價的：
- **執行期開銷**：引用計數的原子操作（`Rc` 非執行緒安全，`Arc` 需要 atomic increment）
- **借用檢查**：`RefCell` 的運行期借用檢查，違反時會 panic
- **循環引用**：雖然計算圖是 DAG（理論上無環），但實現不當仍可能產生循環

Burn 和 Candle 採用了不同的策略。Burn 使用**基於索引的計算圖**——節點不直接持有 parent 引用，而是使用索引陣列：

```rust
// Burn 風格的計算圖（簡化）
struct GraphNode {
    op: Op,
    inputs: Vec<usize>,  // 索引而非指標
    output: usize,       // 輸出張量的索引
}

struct ComputationGraph {
    nodes: Vec<GraphNode>,
    tensors: Vec<TensorData>,
}
```

這種方式完全避免了所有權問題，代價是索引查詢的額外間接性。

### 梯度累積與更新

在實際訓練中，梯度不是反向傳播完就結束了——我們需要將梯度累積起來，然後用優化器更新參數：

```rust
struct SGD {
    params: Vec<Rc<RefCell<Tensor>>>,
    lr: f32,
}

impl SGD {
    fn step(&mut self) {
        for param in &self.params {
            let mut p = param.borrow_mut();
            for i in 0..p.data.len() {
                p.data[i] -= self.lr * p.grad[i];  // w = w - lr * dw
                p.grad[i] = 0.0;  // 梯度清零
            }
        }
    }
}
```

梯度累積模式（gradient accumulation）——在多個 mini-batch 上累積梯度後再更新——在大模型訓練中不可或缺。這在 Rust 中實現起來比 Python 更安全，因為 `RefCell` 的借用規則確保了不會有資料競爭。

---

**下一步**：[神經網路層與損失函數](focus4.md)

## 延伸閱讀

- [Automatic Differentiation in Machine Learning](https://www.google.com/search?q=automatic+differentiation+machine+learning+survey)
- [Wengert List (W expression) explained](https://www.google.com/search?q=Wengert+list+reverse+mode+autodiff)
- [PyTorch autograd mechanics](https://www.google.com/search?q=PyTorch+autograd+computation+graph)
- [Candle autograd implementation](https://www.google.com/search?q=Candle+Rust+autograd+implementation)
- [Rust ownership with computation graphs](https://www.google.com/search?q=Rust+ownership+computation+graph+design)
