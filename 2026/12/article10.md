# WebAssembly 安全模型

## 1. 引言

安全是 WebAssembly 的核心設計目標之一。從最初在瀏覽器中安全執行第三方程式碼，到邊緣運算中的多租戶隔離，安全模型貫穿了 WASM 架構的每一個層面。本文探討 WASM 的沙箱隔離機制、能力模型、潛在的旁路攻擊風險、以及安全部署的最佳實踐。

## 2. WASM 沙箱隔離機制

### 2.1 線性記憶體隔離

每個 WASM 模組實例擁有獨立的線性記憶體空間，無法直接存取其他模組或主機程序的記憶體：

```
WASM 實例 A         WASM 實例 B       主機程序
┌──────────┐      ┌──────────┐      ┌──────────┐
│ 線性記憶體 │      │ 線性記憶體 │      │ 原生記憶體 │
│ (0-1MB)  │      │ (0-2MB)  │      │ (0-16GB) │
└──────────┘      └──────────┘      └──────────┘
     │                  │                │
     └──────────────────┴────────────────┘
          無法互相存取，也無法存取主機記憶體
```

WASM 的記憶體隔離是「沙箱中的沙箱」——即使在同一個程序內執行，不同 WASM 實例之間也完全隔離。

### 2.2 控制流完整性

WASM 的二進位格式是型別安全的。所有間接呼叫（`call_indirect`）都會在執行期進行型別檢查：

```wasm
;; 間接呼叫前的型別檢查
;; 如果函式簽名不匹配，會觸發 trap
call_indirect (type $sig)  ;; 型別 $sig 必須與目標函式匹配
```

這防止了傳統 C/C++ 中常見的 vtable 劫持和間接呼叫攻擊。

### 2.3 無未定義行為

WASM 規範明確定義了所有指令的行為。沒有 C/C++ 中的未定義行為：

| 操作 | C/C++ 行為 | WASM 行為 |
|------|-----------|----------|
| 整數除以零 | 未定義 | 觸發 trap |
| 陣列越界存取 | 未定義（可能成功） | 觸發 trap |
| 懸置指標解參照 | 未定義 | WASM 中無法建立懸置指標（無指標算術） |
| 堆疊溢位 | 未定義 | 觸發 trap |

## 3. 能力模型（Capability Model）

### 3.1 WASI 的能力模型

WASI 採用基於能力的存取控制。不同於傳統的安全模型（如 Unix 的 user/group），WASI 的每個資源存取都需要明確的能力宣告：

```rust
// WASI 模組的權限宣告（執行期由宿主授予）
// 沒有宣告的能力，模組無法存取

// 不需要任何特殊能力
fn pure_computation(x: i32) -> i32 { x + 1 }

// 需要檔案系統能力
fn read_file(path: &str) -> Vec<u8> {
    // 只有在宿主授予 --dir 權限時才能執行
    std::fs::read(path).unwrap()
}

// 需要網路能力
fn fetch_url(url: &str) -> String {
    // 只有在宿主授予網路權限時才能執行
    reqwest::blocking::get(url).unwrap().text().unwrap()
}
```

在 wasmtime 中授予能力：

```bash
# 只授予特定目錄的唯讀存取
wasmtime --dir /data/input:ro app.wasm

# 授予網路存取
wasmtime --tcplisten 0.0.0.0:8080 server.wasm
```

### 3.2 精細權限控制

WASI 的能力模型支援比容器更精細的權限控制：

| 資源類型 | Unix 權限 | 容器 Docker | WASI wasmtime |
|---------|----------|------------|---------------|
| 檔案系統 | 粗粒度（user/group/other） | volume mount（整目錄） | 精細到每個目錄 + 讀寫控制 |
| 網路 | 全部或無 | 全部或無 | 精細到每個位址 + 連接埠 |
| 環境變數 | 全部 | 全部或清單 | 精細到每個變數 |
| 系統時間 | 無法限制 | 無法限制 | 可限制時鐘存取 |

## 4. 旁路攻擊與防護

### 4.1 時序攻擊（Timing Attack）

WASM 無法完全消除時序攻擊的風險，因為底層硬體的時序差異仍然存在：

```rust
// 潛在的時序攻擊漏洞：比較時間取決於資料內容
fn insecure_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() { return false; }
    for i in 0..a.len() {
        if a[i] != b[i] { return false; } // ⚠️ 提前返回揭示比較位置
    }
    true
}

// 安全的常數時間比較
fn secure_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() { return false; }
    let mut result = 0u8;
    for i in 0..a.len() {
        result |= a[i] ^ b[i]; // 無論如何都遍歷整個陣列
    }
    result == 0
}
```

### 4.2 推測執行攻擊（Spectre）

WASM 在瀏覽器中仍然可能受到推測執行攻擊的影響。瀏覽器廠商透過在 WASM 執行期加入 `fence` 指令來緩解：

```javascript
// 瀏覽器自動在 WASM 邊界插入序列化指令
// 開發者無需手動處理
const result = wasmInstance.exports.process(data);
```

### 4.3 記憶體側信道

WASM 的線性記憶體操作可能被用於建立隱蔽通道：

```rust
// ⚠️ 不安全的記憶體存取模式（可能被用於建立側信道）
fn covert_channel(bit: bool) {
    // 根據 bit 的值存取不同的記憶體位址
    // 攻擊者可以透過測量 cache miss 來推斷 bit 的值
    unsafe { MEMORY[if bit { 0x1000 } else { 0x2000 }] }
}
```

緩解措施：避免在 WASM 中執行對時序敏感的密碼學操作，或使用專用的常數時間密碼學庫。

## 5. 安全部署最佳實踐

### 5.1 最小權限原則

```bash
# ❌ 不安全：授予過多權限
wasmtime --dir / app.wasm

# ✅ 安全：只授予必要權限
wasmtime --dir /data/input:ro --dir /data/output app.wasm
```

### 5.2 WASM 模組簽名

使用內容可尋址（content-addressable）機制驗證 WASM 模組的完整性：

```bash
# 產生模組雜湊
sha256sum app.wasm > app.wasm.sha256

# 執行前驗證雜湊
if sha256sum -c app.wasm.sha256; then
    wasmtime app.wasm
else
    echo "WASM module integrity check failed!"
    exit 1
fi
```

### 5.3 執行期安全設定

```rust
// wasmtime 的安全設定
use wasmtime::{Config, Engine, Store, Module};

let mut config = Config::new();
config.wasm_multi_value(true);
config.wasm_bulk_memory(true);

// 限制 WASM 記憶體大小
config.max_memory_size(10 * 1024 * 1024); // 10 MB

// 限制 WASM 的 CPU 資源
config.max_wasm_stack(1024 * 1024); // 1 MB stack

let engine = Engine::new(&config)?;
```

## 6. 安全威脅模型對比

| 威脅 | WASM 是否可防禦 | 說明 |
|------|---------------|------|
| 緩衝區溢位 | ✅ 完全防禦 | 記憶體邊界由 WASM 執行期強制檢查 |
| 釋放後使用 | ✅ 完全防禦 | WASM 中無指標算術 |
| 型別混淆 | ✅ 完全防禦 | WASM 二進位是型別安全的 |
| 程式碼注入 | ✅ 部份防禦 | 無法注入原生程式碼，但可載入惡意 WASM 模組 |
| 時序攻擊 | ⚠️ 有限防禦 | 需要開發者撰寫常數時間程式碼 |
| 推測執行 | ⚠️ 有限防禦 | 依賴瀏覽器 vendor 的緩解措施 |
| 社交工程 | ❌ 無法防禦 | WASM 無法防止使用者的被騙行為 |

## 7. 結語

WebAssembly 提供了現代執行環境中最強的沙箱隔離之一。它的線性記憶體模型、型別安全的二進位格式、和能力導向的權限控制，從架構層面消除了整個類別的安全漏洞。對於旁路攻擊，WASM 無法完全免疫，但透過常數時間程式碼和執行期緩解措施，可以將風險降到最低。在邊緣運算場景中，WASM 的安全模型特別適合多租戶環境和第三方程式碼執行。

---

## 延伸閱讀

- [WebAssembly 安全規範](https://www.google.com/search?q=WebAssembly+security+specification)
- [WASI 能力模型](https://www.google.com/search?q=WASI+capability+model)
- [WASM 旁路攻擊研究](https://www.google.com/search?q=WebAssembly+side+channel+attacks)
- [wasmtime 安全設定](https://www.google.com/search?q=wasmtime+security+configuration)
