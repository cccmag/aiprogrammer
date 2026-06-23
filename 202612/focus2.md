# wasm-bindgen 與 DOM

## 繫結生成、型別橋接、事件處理（2018-2026）

### 前言

WebAssembly 本身無法直接操作 DOM。wasm-bindgen 的誕生（2018 年）徹底改變了這個局面——它提供了一個高效、型別安全的橋樑，讓 Rust 可以像操作原生 DOM 一樣自然。

### 繫結生成機制

wasm-bindgen 透過 proc-macro `#[wasm_bindgen]` 在編譯時分析函式簽名，自動生成三類程式碼：

1. **型別轉換程式碼**：將 Rust 的數值、字串、陣列轉換為 JavaScript 可理解的型別
2. **記憶體管理程式碼**：在線性記憶體中分配和釋放 Rust 物件
3. **生命週期管理程式碼**：確保 Rust 物件在 JavaScript 持有參照期間不會被釋放

```rust
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

### 型別橋接

wasm-bindgen 提供了完整的型別映射：

| Rust | JavaScript | 傳遞方式 |
|------|-----------|---------|
| `i32`/`u32`/`f64` | `number` | 直接傳值 |
| `String` | `string` | 線性記憶體複製 |
| `Vec<T>` | `Array` | 線性記憶體複製 |
| `JsValue` | `any` | 外部參照（不轉換） |

### web-sys 與 js-sys

wasm-bindgen 生態的核心 crate：

```rust
use web_sys::{console, Document, HtmlElement};

fn setup_page() -> Result<(), JsValue> {
    let document = web_sys::window().unwrap().document().unwrap();
    let body = document.body().unwrap();

    let div = document.create_element("div")?;
    div.set_inner_html("<h1>Hello from Rust WASM!</h1>");
    body.append_child(&div)?;

    console::log_1(&"Page setup complete".into());
    Ok(())
}
```

### 事件處理

透過 `Closure` 類型將 Rust 閉包傳遞給事件監聽器：

```rust
use wasm_bindgen::closure::Closure;

let handler = Closure::<dyn Fn(MouseEvent)>::new(|event| {
    console::log_1(&"Clicked!".into());
});

element.add_event_listener_with_callback("click", handler.as_ref().unchecked_ref())?;
handler.forget(); // 防止 GC 回收
```

### 效能考量

每次跨越 WASM 邊界的呼叫都有開銷。最佳實踐是：在 WASM 中批次計算，將結果以資料形式傳回 JS。

### 小結

wasm-bindgen 極大地降低了 Rust+WASM 的開發門檻。它讓 Rust 開發者可以直接使用 Web API，同時保持 WASM 的效能優勢。web-sys 和 js-sys 提供了完整的 Web API 覆蓋。

---

**下一步**：[效能關鍵應用](focus3.md)

## 延伸閱讀

- [wasm-bindgen 指南](https://www.google.com/search?q=wasm-bindgen+guide)
- [web-sys API](https://www.google.com/search?q=web-sys+API)
- [Closure 文件](https://www.google.com/search?q=wasm-bindgen+closure)
