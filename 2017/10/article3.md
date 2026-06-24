# WebAssembly 正式成為 W3C 標準

## 前言

2017 年 10 月，W3C 正式宣佈 WebAssembly 成為官方標準。這個低層級的位元組碼格式可以在瀏覽器中以接近原生的速度執行代碼，為 Web 效能開闢了新時代。

## WebAssembly 概述

WebAssembly（簡稱 WASM）是一種為高效執行而設計的新式瀏覽器位元組碼格式。它提供了：
- 近乎原生的執行速度
- 記憶體安全執行環境
- 多語言支援（C/C++、Rust、Go 等）

```rust
// Rust 程式碼可以編譯為 WebAssembly
#[no_mangle]
pub extern "C" fn add(a: i32, b: i32) -> i32 {
    a + b
}
```

## 效能優勢

```
┌─────────────────────────────────────────────────────────┐
│            JavaScript vs WebAssembly 效能對比            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  任務            JavaScript      WebAssembly            │
│  ─────────────────────────────────────────────────     │
│  影像處理        基准           10-30x 提升             │
│  密碼學          基准           5-15x 提升              │
│  資料壓縮        基准           5-20x 提升              │
│  物理模擬        基准           3-10x 提升              │
│  AI 推論        基准           3-8x 提升               │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 與 JavaScript 的互操作

```javascript
// 載入 WebAssembly 模組
WebAssembly.instantiateStreaming(fetch('module.wasm'))
    .then(result => {
        const { add, process_data } = result.instance.exports;
        console.log(add(1, 2));  // 3
    });
```

## 應用場景

- **遊戲**：Unity 和 Unreal 遊戲可以透過 WASM 在瀏覽器執行
- **影片處理**：FFmpeg 的 WebAssembly 版本可以在瀏覽器中進行影片轉檔
- **AI 推論**：輕量級模型可以在瀏覽器中運行

## 未來展望

WASM 的標準化為邊緣運算和客戶端 AI 開闢了新可能。

---

**延伸閱讀**

- [WebAssembly Official Site](https://www.google.com/search?q=WebAssembly+official+website)
- [WASM Tutorial](https://www.google.com/search?q=WebAssembly+tutorial+2017)