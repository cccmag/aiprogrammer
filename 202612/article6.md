# AI 輔助 WASM 模組優化

## 1. 引言

2026 年，AI 輔助程式碼生成已經成為開發者的日常工具。對於 Rust+WASM 開發，LLM（大型語言模型）不僅可以生成初始程式碼，更可以在編譯設定、效能最佳化、體積控制等方面提供專業建議。

## 2. LLM 生成 WASM 友好的 Rust 程式碼

### 2.1 提示工程策略

要讓 LLM 生成對 WASM 友好的 Rust 程式碼，提示中需要包含以下關鍵資訊：

```
請用 Rust 實作一個高效能的 WASM 模組，遵循以下規則：
1. 使用 #[wasm_bindgen] 匯出所有公開函式
2. 避免使用 std::io 和 std::thread（WASM 不支援）
3. 使用 &[u8] 或 &[f32] 傳遞大量資料（避免 Vec 複製）
4. 批次處理，減少邊界跨越次數
5. 不要使用 println!，改用 wasm_bindgen 的 console::log!
```

### 2.2 案例：LLM 生成影像處理 WASM

以下是由 Claude 6 生成的 WASM 友善程式碼：

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn fast_blur(pixels: &[u8], width: u32, height: u32, radius: u32) -> Vec<u8> {
    let mut output = pixels.to_vec();
    let r = radius as usize;

    for y in 0..height as usize {
        for x in 0..width as usize {
            let mut sum_r = 0u32;
            let mut sum_g = 0u32;
            let mut sum_b = 0u32;
            let mut count = 0u32;

            for dy in 0..=r {
                for dx in 0..=r {
                    let nx = x.wrapping_add(dx).min(width as usize - 1);
                    let ny = y.wrapping_add(dy).min(height as usize - 1);
                    let idx = (ny * width as usize + nx) * 4;
                    sum_r += pixels[idx] as u32;
                    sum_g += pixels[idx + 1] as u32;
                    sum_b += pixels[idx + 2] as u32;
                    count += 1;
                }
            }

            let idx = (y * width as usize + x) * 4;
            output[idx] = (sum_r / count) as u8;
            output[idx + 1] = (sum_g / count) as u8;
            output[idx + 2] = (sum_b / count) as u8;
        }
    }

    output
}
```

LLM 自動應用了以下 WASM 最佳實踐：
- 使用 `&[u8]` 而非 `Vec<u8>` 作為輸入參數
- 使用 `wrapping_add` 避免溢出檢查
- 批次處理整個影像資料
- 最小化邊界跨越

## 3. AI 自動化編譯設定

### 3.1 智慧化 Cargo.toml 設定

AI 可以根據專案需求自動生成最優的 `Cargo.toml` 設定：

```toml
[package]
name = "wasm-processor"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib"]

[dependencies]
wasm-bindgen = "0.2"

[profile.release]
opt-level = "s"    # AI 建議：size 最佳化
lto = true         # 編譯時連結最佳化
codegen-units = 1  # 單一編譯單元（體積更小）
strip = true       # 移除除錯符號
panic = "abort"    # 中止而非展開（體積更小）
```

### 3.2 自動化 wasm-opt 設定

AI 可以根據目標場景選擇最佳的最佳化策略：

| 場景 | 建議選項 | 目標 |
|------|---------|------|
| 網頁載入 | `-Oz` | 最小體積 |
| 邊緣運算 | `-O3` | 最大效能 |
| 遊戲 | `-O3 --enable-simd` | 啟用 SIMD |
| 嵌入式 | `-Oz --strip-debug` | 極小體積 |

## 4. WASM 二進位體積分析

### 4.1 使用 twiggy 分析體積

```bash
# 安裝體積分析工具
cargo install twiggy

# 分析 WASM 二進位
twiggy top pkg/wasm_processor_bg.wasm
twiggy dominators pkg/wasm_processor_bg.wasm
```

### 4.2 AI 驅動的體積建議

AI 可以分析 twiggy 輸出並提供具體建議：

```
分析結果：您 WASM 模組中 40% 的體積來自 serde 序列化，
25% 來自 regex crate。

建議：
1. 如非必要，使用手動序列化替代 serde（節省 ~30KB）
2. 考慮用簡單的字串處理替代 regex（節省 ~50KB）
3. 啟用 lto = true 和 opt-level = "s" 可再節省 ~15%
```

## 5. 效能 Profiling 與 AI 分析

### 5.1 瀏覽器 Profiling

使用 Chrome DevTools 的 Performance 面板和 WASM profiling：

```javascript
// 手動標記 WASM 函式呼叫
performance.mark('wasm-start');
const result = wasm.process(data);
performance.mark('wasm-end');
performance.measure('WASM Processing', 'wasm-start', 'wasm-end');
```

### 5.2 AI 分析效能瓶頸

LLM 可以分析 profiling 結果並定位瓶頸：

```
效能分析結果：
- `process_pixels` 耗時 35ms（佔總時間 70%）
- `memory_copy` 耗時 10ms（佔總時間 20%）
- 其餘函式耗時 5ms

建議：
1. process_pixels 中的邊界檢查可以使用 debug_assert! 替代
   assert!，在 release 中消除開銷
2. memory_copy 可以考慮傳遞指標而非複製資料
3. 合併多次小陣列操作為一次大陣列操作
```

## 6. AI 輔助安全分析

AI 還可以自動分析 WASM 模組的潛在安全問題：

```rust
// AI 檢測到的潛在問題
#[wasm_bindgen]
pub fn unsafe_process(ptr: *mut u8, len: usize) {
    // ⚠️ 裸指標操作：無邊界檢查
    // 建議：使用 &mut [u8] 而非 *mut u8
    for i in 0..len {
        unsafe {
            *ptr.add(i) = 0;
        }
    }
}
```

AI 修正建議：

```rust
#[wasm_bindgen]
pub fn safe_process(data: &mut [u8]) {
    // ✅ 有邊界檢查的安全版本
    for byte in data.iter_mut() {
        *byte = 0;
    }
}
```

## 7. 結語

AI 輔助開發對 Rust+WASM 開發者的生產力提升是顯著的。從初始程式碼生成、編譯設定最佳化、體積控制、到效能分析與安全審查，LLM 可以在每一個環節提供有價值的協助。關鍵是開發者需要了解 WASM 的基本原理，才能準確評估和應用 AI 的建議。

---

## 延伸閱讀

- [Claude 6 WASM 分析能力](https://www.google.com/search?q=Claude+6+WebAssembly+analysis)
- [twiggy WASM 體積分析](https://www.google.com/search?q=twiggy+WebAssembly+size+profiler)
- [wasm-opt 最佳化選項](https://www.google.com/search?q=wasm-opt+optimization+options)
- [LLM 輔助 Rust 開發最佳實踐](https://www.google.com/search?q=LLM+assisted+Rust+development)
