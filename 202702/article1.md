# Rust 中的零成本抽象與遊戲效能優化

## 零成本抽象原則

Rust 的核心設計哲學之一是「零成本抽象」（Zero-Cost Abstractions）：你不需要為了使用高階語言特性而付出執行期效能代價。這對遊戲開發至關重要——遊戲迴圈每幀只有 16ms（60 FPS），任何額外開銷都會直接影響幀率。

## Iterator：無開銷的序列操作

在 C++ 或 C# 中，使用迭代器可能涉及虛擬函式呼叫和堆積分配。Rust 的迭代器透過單態化（monomorphization）在編譯期展開為與手寫迴圈完全相同的機器碼：

```rust
// 高階寫法 — 編譯器展開為高效 SIMD 向量化程式碼
let speeds: Vec<f32> = enemies
    .iter()
    .map(|e| e.velocity.length())
    .filter(|&s| s > 0.0)
    .collect();

// 等價的低階手寫迴圈 — 編譯器產生的機器碼與上方完全相同
let mut speeds = Vec::with_capacity(enemies.len());
for e in enemies {
    let s = e.velocity.length();
    if s > 0.0 {
        speeds.push(s);
    }
}
```

## 閉包與泛型：編譯期展開

Rust 的閉包是編譯時展開的匿名結構體，不是堆積分配的函式指標：

```rust
fn apply_to_all<T, F>(items: &mut [T], mut f: F)
where
    F: FnMut(&mut T),
{
    for item in items {
        f(item);
    }
}

// 使用 inline 閉包 — 編譯器會內聯
apply_to_all(&mut enemies, |e| {
    e.health -= 10;
    e.state = EnemyState::Hurt;
});
```

編譯器為每組 `(T, F)` 組合產生獨立實體（單態化），消除虛擬分派和間接呼叫。

## 遊戲迴圈的效能關鍵

### 快取區域性（Cache Locality）

ECS 架構的核心優勢來自於資料佈局。將所有 `Position` 元件連續儲存在陣列中，而非分散在堆積上：

```rust
// 好的資料佈局 — 連續記憶體，CPU 快取友好
struct Positions {
    xs: Vec<f32>,
    ys: Vec<f32>,
}

// 不理想的資料佈局 — 指標追逐，快取缺失
struct BadEntity {
    x: f32,
    y: f32,
    // 其他不相關的資料...
}
```

### 分配模式（Allocation Patterns）

遊戲迴圈中不應該做堆積分配：

```rust
struct PhysicsSystem;

impl PhysicsSystem {
    fn update(&self, dt: f32) {
        // 緩衝區複用，避免每幀分配
        thread_local! {
            static BUFFER: std::cell::RefCell<Vec<f32>> =
                const { std::cell::RefCell::new(Vec::new()) };
        }
        BUFFER.with(|buf| {
            let mut buf = buf.borrow_mut();
            buf.clear();
            // 使用 buf 儲存中間結果
        });
    }
}
```

### SIMD 自動向量化

Rust 編譯器（LLVM 後端）會自動對簡單的數值迴圈進行 SIMD 向量化：

```rust
#[repr(C)]
struct Vec4(f32, f32, f32, f32);

// LLVM 會將這個迴圈自動向量化為 SSE/AVX 指令
fn normalize_all(vecs: &mut [Vec4]) {
    for v in vecs {
        let len_sq = v.0 * v.0 + v.1 * v.1 + v.2 * v.2 + v.3 * v.3;
        let inv_len = 1.0 / len_sq.sqrt();
        v.0 *= inv_len;
        v.1 *= inv_len;
        v.2 *= inv_len;
        v.3 *= inv_len;
    }
}
```

需要更精細控制時，可以使用 `core::simd`（穩定中）或 `packed_simd` crate。

## 效能分析工具

| 工具 | 用途 | 平台 |
|------|------|------|
| `perf` | CPU 取樣分析 | Linux |
| `flamegraph` | 火焰圖視覺化 | 跨平台 |
| `tracy` | 幀率分析 | 跨平台 |
| `cargo asm` | 檢視生成的組合語言 | 跨平台 |

## 關鍵建議

1. 使用 `criterion` crate 進行微基準測試，確保抽象不會帶來意外開銷
2. 在熱路徑（hot path）預分配緩衝區，使用 `Vec::with_capacity`
3. 優先使用 `#[derive(Clone, Copy)]` 小型型別，減少指標追逐
4. 利用 `cargo asm` 檢查關鍵函式的編譯產出

## 延伸閱讀

- [Rust 零成本抽象官方說明](https://www.google.com/search?q=Rust+zero-cost+abstractions)
- [遊戲引擎中的資料導向設計](https://www.google.com/search?q=data-oriented+design+game+engine)
- [LLVM 自動向量化文檔](https://www.google.com/search?q=LLVM+auto-vectorization)
