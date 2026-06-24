# 效能關鍵應用

## Canvas、WebGL、大量資料、邊界開銷（2019-2026）

### 前言

WASM 在瀏覽器中的核心價值是效能。對於影像處理、資料視覺化、遊戲等應用，WASM 可以比純 JavaScript 快 2-10 倍。但效能增益並非免費——正確的邊界管理和批次策略是關鍵。

### Canvas 2D 加速

Canvas 的像素處理是 WASM 最典型的應用。將 `ImageData` 傳入 WASM 進行批次處理：

```
JavaScript                  Rust WASM
  │                           │
  │ getImageData()            │
  │ ── pixels (Uint8Array) ──→ │
  │                           │ 批次處理
  │ ←── processed (Vec<u8>) ──│
  │                           │
  │ putImageData()            │
```

**效能數據**（1920x1080，M3）：

| 操作 | JS | WASM | 加速比 |
|------|----|------|--------|
| 灰階 | 8ms | 3ms | 2.7x |
| 模糊（3x3） | 45ms | 12ms | 3.8x |
| Sobel 邊緣 | 38ms | 9ms | 4.2x |

### 大量資料視覺化

對數十萬個資料點進行座標轉換和路徑計算：

```rust
#[wasm_bindgen]
pub fn compute_positions(data: &[f64], width: f64, height: f64) -> Vec<f64> {
    // 在 WASM 中批次計算所有座標
    let min = data.iter().cloned().fold(f64::INFINITY, f64::min);
    let max = data.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let range = (max - min).max(1.0);

    data.iter().enumerate().flat_map(|(i, &v)| {
        let x = i as f64 / (data.len() - 1) as f64 * width;
        let y = height - ((v - min) / range * height);
        vec![x, y]
    }).collect()
}
```

### WebGL 整合

WASM 處理幾何變換和物理模擬，JavaScript 負責 WebGL 狀態管理：

```
WASM: 頂點變換、碰撞檢測、粒子模擬
  │
  │ (回傳頂點資料)
  ▼
JS: WebGL buffer binding、draw call
```

### 邊界開銷管理

JS-WASM 邊界呼叫的開銷是真實的。關鍵策略：

1. **批次原則**：合併多次小型呼叫為一次大型呼叫
2. **減少邊界跨越**：讓 WASM 完成完整的計算管線後再回傳
3. **指標傳遞**：對大型資料傳遞指標而非複製
4. **SharedArrayBuffer**：實現真正的零複製共用記憶體

### 小結

WASM 在瀏覽器中的效能優勢在正確的使用模式下非常顯著。關鍵在於理解邊界開銷的本質——WASM 不是用來取代 JavaScript，而是用來加速 JavaScript 不擅長的計算密集型任務。

---

**下一步**：[WASI](focus4.md)

## 延伸閱讀

- [WASM 效能最佳化](https://www.google.com/search?q=WebAssembly+performance+optimization)
- [Canvas + WASM 實戰](https://www.google.com/search?q=Canvas+WebAssembly+tutorial)
- [SharedArrayBuffer WASM](https://www.google.com/search?q=SharedArrayBuffer+WASM)
