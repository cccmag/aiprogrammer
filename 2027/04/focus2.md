# 張量運算：核心資料結構的設計

## Row-major、Strides、Broadcasting、GPU 傳輸（2015-2026）

### 張量的記憶體佈局

張量（Tensor）是深度學習中最基本的資料結構——它是多維陣列的一種泛化。但與 NumPy 或 PyTorch 的使用者直覺不同，張量的底層並不存在「多維」；它只是一個連續的 1D 記憶體區塊。

```rust
struct Tensor {
    data: Vec<f32>,       // 連續的一維記憶體
    shape: Vec<usize>,    // 每維的長度
    strides: Vec<usize>,  // 每維的步長（bytes或元素數）
}
```

**Row-major（行主序）**是深度學習框架中最常用的記憶體佈局。對於一個形狀為 `[3, 4]` 的二維張量，元素在記憶體中的排列是：

```
行 0: a[0][0] a[0][1] a[0][2] a[0][3]
行 1: a[1][0] a[1][1] a[1][2] a[1][3]
行 2: a[2][0] a[2][1] a[2][2] a[2][3]
```

對應的 strides（步長）是 `[4, 1]`——維度 0 的步長是 4（跨越一行需要跳過 4 個元素），維度 1 的步長是 1。

**為什麼 strides 很重要？** 因為它讓**視圖（view）**操作零成本。考慮矩陣轉置：如果我們交換 strides 而不複製資料：

```rust
fn transpose(t: &Tensor) -> Tensor {
    let mut new_strides = t.strides.clone();
    new_strides.reverse();  // 交換 strides
    Tensor {
        data: t.data.clone(),  // 注意：不複製資料！
        shape: t.shape.iter().rev().cloned().collect(),
        strides: new_strides,
    }
}
```

這正是 PyTorch 和 NumPy 中 `.T` 的實作方式——O(1) 時間複雜度，不需要複製任何元素。

### 廣播（Broadcasting）規則

廣播是張量運算中最優雅也最容易出 bug 的特性。它的核心規則是：**從最後一維開始比對，維度要嘛相等、要嘛其中一個是 1**。

```
形狀 A: [3, 1, 5]
形狀 B: [   4, 1]    (自動補前面維度: [1, 4, 1])
結果:   [3, 4, 5]
```

在 Rust 中實作廣播的關鍵是 strides 的擴展：

```rust
fn broadcast_to(t: &Tensor, target_shape: &[usize]) -> Tensor {
    let pad = target_shape.len() - t.shape.len();
    let mut new_strides = vec![0usize; pad];
    new_strides.extend(t.strides.iter());

    // 對 target_shape 維度為 1 的條目，strides 設為 0（無需移動指標）
    for (i, (&ts, &ss)) in target_shape.iter()
        .zip(new_strides.iter_mut()).enumerate()
    {
        if ts == 1 { *ss = 0; }
    }

    Tensor {
        data: t.data.clone(),  // 資料不複製！
        shape: target_shape.to_vec(),
        strides: new_strides,
    }
}
```

當 strides 為 0 時，沿該維度的索引不會改變讀取位置——這實現了廣播而不需要展開記憶體。

### GPU 加速的挑戰

將張量運算搬到 GPU 上並不容易，主要挑戰有三個：

**1. 記憶體傳輸瓶頸**

```
PCIe 頻寬 (PCIe 4.0 x16): ~32 GB/s
GPU 記憶體頻寬 (RTX 4090): ~1008 GB/s
CPU 記憶體頻寬: ~50 GB/s
```

每次 CPU ↔ GPU 的資料傳輸都像從「慢速硬碟」讀寫。解決方案是**記憶體池（memory pool）**：在 GPU 上預先分配一大塊記憶體，重複使用。

**2. Kernel Launch 開銷**

在 CUDA 中，啟動一個 kernel（即使什麼都不做）有大約 5-10μs 的開銷。對於小張量的逐元素運算（如 ReLU、加法），這個開銷可能比運算本身還大。解決方案是**算子融合（kernel fusion）**：將多個小運算合併為一個 kernel。

**3. 記憶體配置**

`cudaMalloc` 是同步操作，耗時約 10-100μs。在訓練循環中頻繁分配記憶體會造成嚴重的效能衰退。Candle 和 Burn 都使用**記憶體池**來避免這個問題。

### Rust 中的張量設計考量

純 Rust 張量框架面臨一個根本抉擇：**使用 dyn trait（動態分發）還是 enum dispatch（靜態分發）**？

```rust
// 方式 A：dyn trait（彈性高、有虛函式開銷）
pub trait Backend {
    fn matmul(&self, a: &TensorStorage, b: &TensorStorage) -> TensorStorage;
}
pub struct Tensor<B: Backend + ?Sized> {
    storage: TensorStorage,
    backend: Box<B>,
}

// 方式 B：enum dispatch（靜態、零開銷）
pub enum Device {
    Cpu(CpuBackend),
    Cuda(CudaBackend),
    Metal(MetalBackend),
}
impl Device {
    fn matmul(&self, a: &TensorStorage, b: &TensorStorage) -> TensorStorage {
        match self {
            Device::Cpu(b) => b.matmul(a, b),
            Device::Cuda(b) => b.matmul(a, b),
            Device::Metal(b) => b.matmul(a, b),
        }
    }
}
```

Burn 使用了 trait 和 const generics 的組合，在編譯期確定張量的形狀和後端：

```rust
// Burn 的張量設計（簡化）
pub struct Tensor<B: Backend, const D: usize> {
    pub(crate) primitive: B::TensorPrimitive<D>,
    // D 是維度數——編譯期檢查！
}
```

dfdx 更進一步，使用 const generics 記錄完整的形狀：

```rust
// dfdx：形狀也在型別中
pub struct Tensor2D<const M: usize, const N: usize> {
    data: [f32; M * N],
}
pub fn matmul<const M: usize, const N: usize, const K: usize>(
    a: &Tensor2D<M, K>,
    b: &Tensor2D<K, N>,
) -> Tensor2D<M, N> { ... }
// 維度不匹配 → 編譯錯誤！
```

---

**下一步**：[自動微分：反向傳播的實作](focus3.md)

## 延伸閱讀

- [NumPy broadcasting documentation](https://www.google.com/search?q=NumPy+broadcasting+rules+explained)
- [PyTorch Tensor internals](https://www.google.com/search?q=PyTorch+tensor+strides+internals)
- [CUDA memory management best practices](https://www.google.com/search?q=CUDA+memory+pool+management)
- [Candle tensor implementation](https://www.google.com/search?q=Candle+Rust+tensor+implementation)
- [Burn backend design](https://www.google.com/search?q=Burn+Rust+backend+trait+design)
