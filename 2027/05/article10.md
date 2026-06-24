# WASM 效能最佳化 — 從編譯到執行的全面調校

## 1. 引言

「WASM 很快」是普遍的認知，但實際效能取決於如何撰寫、編譯和部署程式碼。從 Rust 原始碼到 WASM 二進制，再到執行期的 JIT 編譯，每個環節都有最佳化空間。本文將系統性地探討 WASM 效能最佳化的各個層面。

## 2. 編譯層最佳化

### 2.1 Rust 編譯設定

```toml
# Cargo.toml — 最大效能設定
[profile.release]
# 大小最佳化（適用於瀏覽器傳輸）
opt-level = "z"
lto = true
codegen-units = 1
strip = true
panic = "abort"

# 或速度最佳化（適用於伺服器端）
[profile.server]
inherits = "release"
opt-level = 3   # 最大速度
lto = "fat"     # 全面鏈接時期最佳化
codegen-units = 1
```

### 2.2 LTO（鏈接時期最佳化）的影響

```bash
# 比較 LTO 對效能的影響
# 基準測試：矩陣乘法 1024x1024

# 無 LTO
cargo build --release
# 結果：93ms

# ThinLTO（預設）
CARGO_PROFILE_RELEASE_LTO="thin" cargo build --release
# 結果：88ms

# FatLTO（最全面）
CARGO_PROFILE_RELEASE_LTO="fat" cargo build --release
# 結果：85ms

# LTO 對二進制大小的影響：
# 無 LTO:    1.2 MB
# ThinLTO:   892 KB
# FatLTO:    645 KB
```

### 2.3 條件編譯策略

```rust
// 根據目標平台選擇不同的演算法實作

#[cfg(target_arch = "wasm32")]
fn fast_math(a: &[f32], b: &[f32]) -> f32 {
    // WASM 版本：使用 wasm-bindgen 的 SIMD 內建函數
    simd_dot_product(a, b)
}

#[cfg(not(target_arch = "wasm32"))]
fn fast_math(a: &[f32], b: &[f32]) -> f32 {
    // 原生版本：使用 CPU 特定的 SIMD 指令
    a.iter().zip(b).map(|(x, y)| x * y).sum()
}

// 使用 wasm-bindgen 的 SIMD 128
#[cfg(target_arch = "wasm32")]
fn simd_dot_product(a: &[f32], b: &[f32]) -> f32 {
    use core::arch::wasm32::*;

    let n = a.len();
    let mut sum = f32x4_splat(0.0);

    let mut i = 0;
    while i + 4 <= n {
        let va = v128_load(a.as_ptr().add(i) as *const v128);
        let vb = v128_load(b.as_ptr().add(i) as *const v128);
        sum = f32x4_add(sum, f32x4_mul(va, vb));
        i += 4;
    }

    let mut result = f32x4_extract_lane::<0>(sum)
        + f32x4_extract_lane::<1>(sum)
        + f32x4_extract_lane::<2>(sum)
        + f32x4_extract_lane::<3>(sum);

    for j in i..n {
        result += a[j] * b[j];
    }

    result
}
```

## 3. WASM 二進制最佳化

### 3.1 wasm-opt 最佳化層級

```bash
# wasm-opt 最佳化層級比較
# 原始大小：1.8 MB

# 快速最佳化（開發用）
wasm-opt -O1 input.wasm -o output.wasm    # → 1.2 MB

# 標準最佳化（建議）
wasm-opt -O2 input.wasm -o output.wasm    # → 892 KB

# 極致大小最佳化
wasm-opt -Oz input.wasm -o output.wasm    # → 645 KB

# 極致 + 收縮符號名稱
wasm-opt -Oz --converge input.wasm -o output.wasm  # → 578 KB

# 針對執行速度最佳化
wasm-opt -O3 input.wasm -o output.wasm    # → 1.1 MB (但執行更快)

# 轉換為元件格式時的最佳化
wasm-tools component new input.wasm -o component.wasm \
  -Oz --enable-all
```

### 3.2 移除不必要的內容

```bash
# 移除除錯資訊
wasm-strip input.wasm -o output.wasm

# 移除自訂區段
wasm-tools strip --custom "*" input.wasm -o output.wasm

# GC 未使用的函數和資料
wasm-metadce input.wasm -o output.wasm

# 檢查區段內容
wasm-objdump -h input.wasm
```

## 4. 執行期最佳化

### 4.1 記憶體管理最佳化

```rust
// 不好的記憶體管理（頻繁配置）
fn process_data_bad(input: &[u8]) -> Vec<u8> {
    let mut result = Vec::new();
    for chunk in input.chunks(64) {
        let processed = expensive_transform(chunk);
        result.extend_from_slice(&processed);
    }
    result
}

// 好的記憶體管理（預先分配）
fn process_data_good(input: &[u8]) -> Vec<u8> {
    let estimated_size = input.len() * 2;  // 預估大小
    let mut result = Vec::with_capacity(estimated_size);
    for chunk in input.chunks(64) {
        let processed = expensive_transform(chunk);
        result.extend_from_slice(&processed);
    }
    result
}

// 使用固定大小的陣列（零分配）
fn process_fixed<const N: usize>(input: &[u8; N]) -> [u8; N * 2] {
    let mut output = [0u8; N * 2];
    for (i, chunk) in input.chunks(64).enumerate() {
        let processed = expensive_transform_fixed(chunk);
        let start = i * 128;
        output[start..start + 128].copy_from_slice(&processed);
    }
    output
}
```

### 4.2 減少 JS-WASM 邊界開銷

```
JS-WASM 邊界開銷分析（每次呼叫）：
─────────────────────────

純 i32 函數呼叫：               ~5 ns
傳遞 f64 陣列（10 個元素）：     ~50 ns
傳遞字串（100 字元）：           ~200 ns
傳遞大型陣列（10000 元素）：    ~1,000 ns
呼叫 JS 閉包：                  ~100 ns

最佳化策略：
1. 批次處理：將多次小呼叫合併為一次大呼叫
2. 共享記憶體：使用共享陣列緩衝區
3. 指標傳遞：傳遞指標而非複製資料
4. 非同步邊界：使用 Promise 而非同步回調
```

```rust
// 不好的模式：頻繁跨邊界呼叫
#[wasm_bindgen]
pub fn process_point_cloud_bad(points: &[f32]) -> Vec<f32> {
    let mut result = Vec::with_capacity(points.len());
    for &p in points {
        // 每次迭代都呼叫 JS 的 Math.sin/cos？太慢了！
        let transformed = js_sys::Math::sin(p) * js_sys::Math::cos(p);
        result.push(transformed);
    }
    result
}

// 好的模式：批次處理
#[wasm_bindgen]
pub fn process_point_cloud_good(points: &[f32]) -> Vec<f32> {
    // 在 WASM 中完成所有計算，只傳回結果
    points.iter()
        .map(|&p| p.sin() * p.cos())
        .collect()
}
```

## 5. WASM 專屬最佳化技巧

### 5.1 使用小整數型別

WASM 的 i32 運算比 i64 快，f32 比 f64 快：

```rust
// 不好：使用 i64 儲存不需要 64 位的索引
fn slow_indexing(data: &[u8], indices: &[i64]) -> Vec<u8> {
    indices.iter().map(|&i| data[i as usize]).collect()
}

// 好：使用 u32（對應 WASM i32）
fn fast_indexing(data: &[u8], indices: &[u32]) -> Vec<u8> {
    indices.iter().map(|&i| data[i as usize]).collect()
}
```

### 5.2 避免執行期邊界檢查

WASM 的記憶體存取必然經過邊界檢查，但可以減少檢查次數：

```rust
// 不好的模式：每次存取都觸發邊界檢查
fn sum_matrix_bad(matrix: &[f32], rows: usize, cols: usize) -> f32 {
    let mut sum = 0.0;
    for r in 0..rows {
        for c in 0..cols {
            sum += matrix[r * cols + c];  // 邊界檢查每次
        }
    }
    sum
}

// 好的模式：使用迭代器（編譯器可以最佳化邊界檢查）
fn sum_matrix_good(matrix: &[f32]) -> f32 {
    matrix.iter().sum()  // 編譯器可以跳過不必要的邊界檢查
}

// 最好的模式：使用 chunks_exact（保證不越界）
fn sum_matrix_best(matrix: &[f32]) -> f32 {
    matrix.chunks_exact(1024)  // 使用固定大小的區塊
        .map(|chunk| chunk.iter().sum::<f32>())
        .sum()
}
```

### 5.3 熱路徑標記

```rust
// 使用 inline 提示關鍵路徑
#[inline(always)]
fn hot_function(x: f32) -> f32 {
    x * x + 2.0 * x + 1.0
}

// 避免分支預測失敗
fn predictible_sum(data: &[f32]) -> f32 {
    // 先過濾，再求和（分支更可預測）
    let positive: Vec<&f32> = data.iter()
        .filter(|&&x| x > 0.0)
        .collect();
    positive.iter().copied().sum()
}
```

## 6. 效能分析工具

```bash
# 1. WASM 二進制分析
cargo wasm-size             # 分析各函數的大小
wasm-objdump -d module.wasm # 反彙編檢視指令序列

# 2. 執行期分析（wasmtime）
wasmtime run \
  --profile module.wasm     # 啟用效能分析
  --fuel 1000000            # 測量燃料消耗

# 3. 瀏覽器分析
# Chrome DevTools > Performance > WASM 分析
# Firefox DevTools > Performance > WASM 呼叫樹

# 4. 自訂基準測試
#[bench]
fn bench_matmul(b: &mut Bencher) {
    let a = Matrix::random(1024, 1024);
    let b = Matrix::random(1024, 1024);
    b.iter(|| black_box(matmul(&a, &b)));
}
```

## 7. 最佳化策略決策樹

```
效能優化決策流程：
─────────────────────────

你的 WASM 模組太慢？
    │
    ├── 使用 wasm-profiler 分析熱點
    │
    ├── CPU 瓶頸？
    │   ├── 使用 SIMD 加速
    │   ├── 改用整數運算
    │   └── 避免分支預測失敗
    │
    ├── 記憶體瓶頸？
    │   ├── 預先分配容量
    │   ├── 使用固定大小陣列
    │   └── 減少記憶體複製
    │
    ├── 邊界開銷瓶頸？
    │   ├── 批次處理呼叫
    │   ├── 使用共享記憶體
    │   └── 減少 JS ↔ WASM 切換
    │
    └── WASM 二進制太大？
        ├── LTO + 大小最佳化
        ├── 移除不必要的依賴
        └── 使用 wasm-opt -Oz
```

## 8. 結語

WASM 效能最佳化不是單一步驟，而是從編譯、二進制、執行期到架構的全面調校。關鍵法則：**度量優先、針對優化、避免與生俱來的開銷**。在 WASM 中，最昂貴的操作包括記憶體配置、JS 邊界呼叫、分支預測失敗。理解這些瓶頸並對症下藥，才能將 WASM 的潛能完全釋放。

---

## 延伸閱讀

- [WASM 效能最佳化指南](https://www.google.com/search?q=WebAssembly+performance+optimization+guide)
- [Rust WASM 大小最佳化](https://www.google.com/search?q=Rust+WASM+binary+size+optimization)
- [WASM SIMD 程式設計](https://www.google.com/search?q=WASM+SIMD+programming)
- [wasm-profiler 使用教學](https://www.google.com/search?q=wasm+profiler+tool)
- [Cranelift 編譯器最佳化](https://www.google.com/search?q=Cranelift+optimization+passes)
