# 跨語言 WASM 互通性

## 1. 引言

WebAssembly 的一個獨特優勢是「一次編譯，到處執行」——但這裡的「到處」不僅指不同平台，也指不同語言。Rust、C、Go、AssemblyScript 都可以編譯到 WASM，並在同一個應用中協作。本文探討這些語言在 WASM 生態中的互通性。

## 2. 各語言 WASM 編譯對比

### 2.1 Rust

Rust 是 WASM 生態的領導者，擁有最完善的工具鏈：

```rust
// Rust → WASM（最成熟的方案）
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn compute(data: &[f64]) -> f64 {
    data.iter().sum()
}
```

**優點**：無 GC、小體積、強型別、完善的工具鏈
**缺點**：wasm-bindgen 增加橋接開銷

### 2.2 C/C++

C 語言可以透過 Emscripten 或 clang 直接編譯到 WASM：

```c
// C → WASM（透過 Emscripten）
#include <emscripten.h>

EMSCRIPTEN_KEEPALIVE
double compute(double* data, int len) {
    double sum = 0;
    for (int i = 0; i < len; i++) {
        sum += data[i];
    }
    return sum;
}
```

**優點**：最成熟的 WASM 編譯器支援、最小的二進位體積
**缺點**：記憶體安全需人工保證、工具鏈較 Rust 複雜

### 2.3 Go

Go 語言從 1.11 版開始支援 WASM：

```go
// Go → WASM
package main

import "syscall/js"

func compute(this js.Value, args []js.Value) any {
    data := args[0]
    sum := 0.0
    for i := 0; i < data.Length(); i++ {
        sum += data.Index(i).Float()
    }
    return sum
}

func main() {
    js.Global().Set("goCompute", js.FuncOf(compute))
    select {}
}
```

**優點**：熟悉的語法、良好的並發支援
**缺點**：二進位體積大（~2MB 起）、需要捆綁 Go 執行期

### 2.4 AssemblyScript

AssemblyScript 是 TypeScript 的子集，專為 WASM 設計：

```typescript
// AssemblyScript → WASM
export function compute(data: Float64Array): f64 {
    let sum: f64 = 0.0;
    for (let i = 0; i < data.length; i++) {
        sum += data[i];
    }
    return sum;
}
```

**優點**：JavaScript 開發者友好、編譯速度快、型別安全
**缺點**：生態較小、GC 開銷、不適合複雜資料結構

### 2.5 對比總結

| 特性 | Rust | C/C++ | Go | AssemblyScript |
|------|------|-------|-----|---------------|
| WASM 二進位大小（hello world） | ~5 KB | ~2 KB | ~2 MB | ~8 KB |
| GC 需求 | 無 | 無 | 有 | 有 |
| 工具鏈成熟度 | 極佳 | 佳 | 可 | 佳 |
| 語言學習曲線 | 陡 | 中 | 低 | 極低 |
| 記憶體安全 | 編譯器保證 | 人工管理 | GC | GC |
| 非同步支援 | 完善 | 有限 | 完善 | 佳 |

## 3. ABI 相容性與邊界設計

### 3.1 WASM 的 ABI 約定

WASM 本身只定義了數值型別的傳遞。字串、陣列、結構體等高階型別需要二進位檔案之間約定序列化格式：

```
WASM ABI 傳遞方式
├── 數值（i32、i64、f32、f64）→ 直接傳遞
├── 字串 → 寫入線性記憶體，傳遞（指標，長度）
├── 陣列 → 寫入線性記憶體，傳遞（指標，長度）
└── 結構體 → 序列化為位元組陣列（Canonical ABI 或自訂格式）
```

### 3.2 元件模型解決 ABI 問題

元件模型透過 Canonical ABI 標準化跨語言型別轉換：

```wit
// WIT 介面定義（語言無關）
interface math {
    add: func(a: s32, b: s32) -> s32;
    compute: func(data: list<float64>) -> float64;
}
```

Canonical ABI 自動處理記憶體配置和型別轉換，開發者無需關心底層 ABI 細節。

## 4. 共用記憶體策略

### 4.1 序列化協定

不同語言模組之間可以透過標準序列化格式交換資料：

```rust
// Rust 端：使用 MessagePack 序列化
use rmp_serde::Serializer;
use serde::Serialize;

#[wasm_bindgen]
pub fn process_data(input: &[u8]) -> Vec<u8> {
    // 反序列化輸入（來自其他 WASM 模組）
    let data: InputStruct = rmp_serde::from_slice(input).unwrap();

    // 處理
    let result = /* ... */;

    // 序列化輸出
    let mut buf = Vec::new();
    result.serialize(&mut Serializer::new(&mut buf)).unwrap();
    buf
}
```

```go
// Go 端：同樣使用 MessagePack
package main

import (
    "github.com/vmihailenco/msgpack/v5"
)

//export processData
func processData(inputPtr uint32, inputLen uint32) (uint32, uint32) {
    input := readMemory(inputPtr, inputLen)
    var data InputStruct
    msgpack.Unmarshal(input, &data)
    // 處理... 
    output, _ := msgpack.Marshal(result)
    return writeMemory(output)
}
```

### 4.2 零複製傳遞

對高效能場景，可以直接在線性記憶體中操作：

```rust
// Rust 匯出函式，透過指標操作共用記憶體
#[wasm_bindgen]
pub fn process_shared(ptr: *mut f64, len: usize) {
    let slice = unsafe { std::slice::from_raw_parts_mut(ptr, len) };
    for val in slice.iter_mut() {
        *val = (*val).sqrt();
    }
}
```

## 5. 多語言協作案例

假設一個邊緣應用需要：認證（Rust）、資料處理（C）、日誌記錄（AssemblyScript）。

```wit
// 服務介面
interface auth-service {
    authenticate: func(token: string) -> result<string, string>;
}

interface data-processor {
    process: func(data: list<u8>) -> list<u8>;
}

interface logger {
    log: func(level: string, message: string);
}

world edge-app {
    import auth-service;
    import data-processor;
    import logger;
    export run: func(request: string) -> string;
}
```

每個語言實作自己負責的介面，透過 `wasm-tools compose` 組合：

```bash
wasm-tools compose -o combined.wasm \
    auth-rust.wasm \
    data-c.wasm \
    logger-as.wasm \
    orchestrator.wasm
```

## 6. 結語

WebAssembly 的跨語言互通性是其最大的優勢之一。不同的語言有各自的取捨——Rust 適合高效能計算、C 適合既有程式碼遷移、Go 適合並發處理、AssemblyScript 適合快速原型開發。透過元件模型的 WIT 介面和 Canonical ABI，這些語言可以在同一個 WASM 應用中無縫協作。

---

## 延伸閱讀

- [WASM 跨語言互通指南](https://www.google.com/search?q=WebAssembly+cross-language+interoperability)
- [Canonical ABI 規範](https://www.google.com/search?q=Canonical+ABI+WebAssembly)
- [Rust vs Go vs C WASM 比較](https://www.google.com/search?q=Rust+Go+C+WebAssembly+comparison)
- [AssemblyScript 官方文件](https://www.google.com/search?q=AssemblyScript+documentation)
