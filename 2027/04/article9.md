# AI 測試生成器：自動驗證 DL 框架正確性

## 前言

深度學習框架的正確性至關重要——一個微小的張量運算錯誤可能在反向傳播中被放大，導致模型無法收斂或在生產環境中產生錯誤預測。傳統的單元測試覆蓋率有限，而 Rust 的屬性測試（property-based testing）提供了一個系統性的驗證方案。

本文展示如何使用屬性測試、梯度檢查和隨機測試生成來自動驗證 Rust 深度學習框架的正確性。

## 屬性測試基礎

### 使用 proptest 測試張量運算

```rust
use proptest::prelude::*;

// 生成隨機張量
fn tensor_strategy(rows: usize, cols: usize) -> impl Strategy<Value = Vec<f32>> {
    prop::collection::vec(
        prop::num::f32::ANY, // 任何浮點數
        rows * cols,
    )
}

proptest! {
    #[test]
    fn test_matmul_associativity(
        a in tensor_strategy(4, 4),
        b in tensor_strategy(4, 4),
        c in tensor_strategy(4, 4),
    ) {
        // (A × B) × C == A × (B × C)
        let ab = matmul(&a, &b, 4, 4, 4);
        let ab_c = matmul(&ab, &c, 4, 4, 4);

        let bc = matmul(&b, &c, 4, 4, 4);
        let a_bc = matmul(&a, &bc, 4, 4, 4);

        for (l, r) in ab_c.iter().zip(a_bc.iter()) {
            prop_assert!((l - r).abs() < 1e-5);
        }
    }
}
```

### 代數法則測試

張量運算應滿足的代數法則：

```rust
proptest! {
    // 加法交換律：A + B == B + A
    #[test]
    fn add_commutative(a in tensor_strategy(3, 3), b in tensor_strategy(3, 3)) {
        let ab = add(&a, &b);
        let ba = add(&b, &a);
        for (l, r) in ab.iter().zip(ba.iter()) {
            prop_assert!((l - r).abs() < 1e-6);
        }
    }

    // 加法結合律：(A + B) + C == A + (B + C)
    #[test]
    fn add_associative(
        a in tensor_strategy(2, 4), b in tensor_strategy(2, 4), c in tensor_strategy(2, 4)
    ) {
        let ab_c = add(&add(&a, &b), &c);
        let a_bc = add(&a, &add(&b, &c));
        for (l, r) in ab_c.iter().zip(a_bc.iter()) {
            prop_assert!((l - r).abs() < 1e-6);
        }
    }

    // 分配律：A × (B + C) == A × B + A × C
    #[test]
    fn matmul_distributive(
        a in tensor_strategy(4, 4), b in tensor_strategy(4, 4), c in tensor_strategy(4, 4)
    ) {
        let left = matmul(&a, &add(&b, &c), 4, 4, 4);
        let right = add(
            &matmul(&a, &b, 4, 4, 4),
            &matmul(&a, &c, 4, 4, 4),
        );
        for (l, r) in left.iter().zip(right.iter()) {
            prop_assert!((l - r).abs() < 1e-5);
        }
    }
}
```

## 梯度檢查（Gradient Checking）

### 有限差分近似

梯度檢查是驗證反向傳播正確性的黃金標準。使用有限差分近似計算數值梯度，與分析梯度比較：

```rust
fn numerical_gradient<F>(
    f: F,
    x: &[f32],
    epsilon: f32,
) -> Vec<f32>
where
    F: Fn(&[f32]) -> f32,
{
    let mut grad = vec![0.0; x.len()];
    for i in 0..x.len() {
        let mut x_plus = x.to_vec();
        x_plus[i] += epsilon;
        let mut x_minus = x.to_vec();
        x_minus[i] -= epsilon;

        let f_plus = f(&x_plus);
        let f_minus = f(&x_minus);
        grad[i] = (f_plus - f_minus) / (2.0 * epsilon);
    }
    grad
}
```

### 自動梯度檢查

```rust
struct GradientCheckResult {
    max_relative_error: f32,
    num_passed: usize,
    num_failed: usize,
    threshold: f32,
}

fn check_gradients<F>(
    analytical_grad: &[f32],
    f: F,
    x: &[f32],
    threshold: f32,
) -> GradientCheckResult
where
    F: Fn(&[f32]) -> f32,
{
    let numerical = numerical_gradient(f, x, 1e-5);
    let mut passed = 0;
    let mut failed = 0;
    let mut max_error = 0.0;

    for (a, n) in analytical_grad.iter().zip(numerical.iter()) {
        let denominator = a.abs().max(n.abs()).max(1e-8);
        let relative_error = (a - n).abs() / denominator;
        max_error = max_error.max(relative_error);

        if relative_error < threshold {
            passed += 1;
        } else {
            failed += 1;
        }
    }

    GradientCheckResult {
        max_relative_error: max_error,
        num_passed: passed,
        num_failed: failed,
        threshold,
    }
}

fn test_linear_layer_gradient() {
    // 定義一個簡單的線性層
    let w = vec![0.5, -0.3, 0.8, 0.1]; // 2×2
    let b = vec![0.1, -0.2];
    let x = vec![1.0, 2.0];

    // 前向傳播
    let y = linear_forward(&w, &b, &x, 2, 2);

    // 損失：MSE
    let target = vec![0.5, 0.5];
    let loss = mse_loss(&y, &target);

    // 反向傳播：取得分析梯度
    let (grad_w, grad_b) = linear_backward(&w, &x, &y, &target, 2, 2);

    // 梯度檢查 w.r.t w
    let f = |w: &[f32]| -> f32 {
        let y = linear_forward(w, &b, &x, 2, 2);
        mse_loss(&y, &target)
    };

    let result = check_gradients(&grad_w, f, &w, 1e-4);
    println!("Gradient check results:");
    println!("  Max relative error: {:.2e}", result.max_relative_error);
    println!("  Passed: {}/{}", result.num_passed,
             result.num_passed + result.num_failed);

    assert!(result.max_relative_error < 1e-4);
}
```

### 選擇 epsilon

| epsilon | 截斷誤差 | 捨入誤差 | 建議 |
|---------|---------|---------|------|
| 1e-10 | 很小 | 很大 | 數值不穩定 |
| 1e-7 | 小 | 中等 | 單精度（f32）最佳 |
| 1e-5 | 中等 | 小 | 雙精度（f64）最佳 |
| 1e-3 | 大 | 很小 | 不建議 |

## 隨機測試生成

### 邊界值測試

神經網路運算容易在邊界值出錯：

```rust
fn generate_edge_cases() -> Vec<Vec<f32>> {
    vec![
        vec![],                    // 空張量
        vec![0.0; 100],            // 全零
        vec![1.0; 100],            // 全一
        vec![f32::MAX; 10],        // 極大值
        vec![f32::MIN; 10],        // 極小值
        vec![f32::NAN; 10],        // NaN
        vec![f32::INFINITY; 10],   // 無限大
        vec![1.0, 0.0, -1.0],      // 正負零
        (0..100).map(|i| i as f32).collect(), // 單調遞增
    ]
}

proptest! {
    #[test]
    fn test_relu_stability(
        x in prop::collection::vec(prop::num::f32::ANY, 0..100)
    ) {
        let result = relu(&x);
        // ReLU 輸出應 >= 0
        for &v in &result {
            prop_assert!(v >= -1e-6);
        }
        // 不應產生 NaN
        for &v in &result {
            prop_assert!(!v.is_nan());
        }
    }
}
```

## 與參考框架比較

### PyTorch 參考輸出

最可靠的測試是與 PyTorch 的輸出進行比較：

```rust
fn compare_with_pytorch() {
    use std::process::Command;

    // 1. 使用 Python 產生參考資料
    let python_code = r#"
import torch
import numpy as np

torch.manual_seed(42)
x = torch.randn(4, 4)
w = torch.randn(4, 4, requires_grad=True)
y = (x @ w).relu().sum()
y.backward()

np.save("pytorch_x.npy", x.numpy())
np.save("pytorch_w.npy", w.detach().numpy())
np.save("pytorch_output.npy", (x @ w.detach()).relu().numpy())
np.save("pytorch_grad.npy", w.grad.numpy())
"#;

    std::fs::write("gen_ref.py", python_code).unwrap();
    Command::new("python3").arg("gen_ref.py").status().unwrap();

    // 2. 在 Rust 中載入並比較
    let x = Tensor::load_npy("pytorch_x.npy");
    let w = Tensor::load_npy("pytorch_w.npy");
    let expected_y = Tensor::load_npy("pytorch_output.npy");
    let expected_grad = Tensor::load_npy("pytorch_grad.npy");

    // 在 Candle 中執行相同運算
    let our_y = x.matmul(&w).unwrap().relu().unwrap();
    let diff = (our_y - &expected_y).abs().unwrap().sum_all().unwrap();
    assert!(diff.to_scalar::<f32>() < 1e-5, "Output mismatch: {}", diff);
}
```

### 持續整合中的測試矩陣

```yaml
# .github/workflows/test.yml
test_matrix:
  strategy:
    matrix:
      features: [cpu, cuda, metal]
      dtype: [f32, f16, bf16]
  steps:
    - run: cargo test --features ${{ matrix.features }}
    - run: python3 scripts/gen_reference.py --dtype ${{ matrix.dtype }}
    - run: cargo run --example compare_reference
```

## 自動化測試生成工具

```rust
// 一個自動生成測試用例的系統
struct TestGenerator {
    rng: StdRng,
    shape_generator: Box<dyn Fn(&mut StdRng) -> Vec<usize>>,
}

impl TestGenerator {
    fn new(seed: u64) -> Self {
        TestGenerator {
            rng: StdRng::seed_from_u64(seed),
            shape_generator: Box::new(|rng| {
                let ndim = rng.gen_range(1..=4);
                (0..ndim).map(|_| rng.gen_range(1..=32)).collect()
            }),
        }
    }

    fn generate_binary_op_test(&mut self) -> BinaryOpTest {
        let shape = (self.shape_generator)(&mut self.rng);
        let size: usize = shape.iter().product();

        let a = (0..size).map(|_| self.rng.gen_range(-1.0..1.0)).collect();
        let b = (0..size).map(|_| self.rng.gen_range(-1.0..1.0)).collect();

        // 從可用算子中隨機選擇
        let op = self.rng.gen_range(0..4);
        let op_name = match op {
            0 => "add", 1 => "sub", 2 => "mul", 3 => "div", _ => unreachable!()
        };

        BinaryOpTest { a, b, shape, op_name: op_name.to_string() }
    }
}

// 測試運行器
fn run_generated_tests(num_tests: usize) {
    let mut generator = TestGenerator::new(42);
    let mut all_passed = true;

    for i in 0..num_tests {
        let test = generator.generate_binary_op_test();
        let result = execute_and_verify(&test);
        if !result.passed {
            eprintln!("Test {} FAILED: {} {:?}",
                i, test.op_name, test.shape);
            all_passed = false;
        }
    }

    assert!(all_passed, "Some generated tests failed");
}
```

## 測試覆蓋率分析

| 測試類型 | 發現的錯誤類型 | 典型錯誤率 |
|---------|---------------|-----------|
| 代數法則 | 運算實作錯誤 | 3-5% |
| 梯度檢查 | 反向傳播錯誤 | 10-15% |
| 邊界值測試 | 數值穩定性問題 | 5-8% |
| 跨框架比較 | API 語意差異 | 8-12% |
| 隨機生成 | 邊緣案例 | 2-4% |

## 總結

深度學習框架的正確性驗證需要多層次策略：屬性測試確保代數法則成立，梯度檢查驗證反向傳播的正確性，邊界值測試捕捉數值穩定性問題，而與 PyTorch 的交叉驗證則是最終的背書。

Rust 的 `proptest` 和型別系統讓這套測試策略可以系統性地執行。建議在 CI 中每天執行全套隨機化測試，並在每次 PR 中執行梯度檢查。

---

**參考資料**

- https://www.google.com/search?q=property+based+testing+Rust+proptest
- https://www.google.com/search?q=gradient+checking+finite+difference+deep+learning
- https://www.google.com/search?q=Rust+deep+learning+framework+testing+strategy
- https://www.google.com/search?q=proptest+tensor+operation+testing
- https://www.google.com/search?q=comparing+Rust+DL+output+with+PyTorch
