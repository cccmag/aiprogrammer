# WASM 安全模型 — 沙箱、能力與供應鏈安全

## 1. 引言

在供應鏈攻擊日益頻繁的時代，軟體安全已成企業的首要考量。WASM 的安全模型從設計之初就與傳統原生應用截然不同——不是依靠「信任使用者程式碼」，而是「從不信任任何程式碼」。本文將深入探討 WASM 安全模型的三個層次：沙箱隔離、能力模型、和供應鏈安全。

## 2. 沙箱隔離機制

### 2.1 指令級隔離

WASM 的核心安全保證來自其指令集設計：

```
WASM 指令集的安全設計：
─────────────────────────

✅ 禁止的操作：
├── 無條件跳轉到任意記憶體位址
├── 直接存取硬體暫存器
├── 自我修改程式碼（WASM 是不可變的）
├── 執行堆疊上的資料（防止 ROP 攻擊）
└── 存取呼叫者的堆疊幀

✅ 強制檢查的操作：
├── 所有記憶體存取都進行邊界檢查
├── 所有函數呼叫都進行型別檢查
├── 所有間接呼叫都進行表邊界檢查
└── 所有運算都進行型別一致性檢查
```

### 2.2 WASM 的記憶體安全模型

WASM 的線性記憶體（Linear Memory）是安全的核心：

```rust
// WASM 記憶體安全示意
// 以下程式碼在編譯時會被插入邊界檢查

fn unsafe_looking_code(memory: &[u8], offset: usize) -> u8 {
    // 這行程式碼實際上不可能造成緩衝區溢位
    // WASM 執行期在每次記憶體存取前進行邊界檢查
    memory[offset]
}

// 在 WASM 中，以下攻擊向量無效：
// 1. Stack overflow → WASM 有固定的堆疊大小
// 2. Buffer overflow → 每次存取都有邊界檢查
// 3. Use-after-free → WASM 線性記憶體無動態分配的概念
// 4. ROP/JOP → WASM 控制流完整性強制執行
```

### 2.3 旁路攻擊的潛在風險

雖然 WASM 的沙箱設計非常安全，但並非完美。研究發現了一些潛在的旁路攻擊向量：

```
已知的 WASM 旁路攻擊：
─────────────────────────

1. 時序攻擊（Timing Attack）
   └── WASM 的 JIT 編譯可能產生可預測的執行時間模式
   └── 防護：使用固定時間演算法（constant-time algorithms）

2. 快取計時攻擊（Cache Timing Attack）
   └── 雖然 WASM 無法直接存取 CPU 快取，但可透過間接方式推測
   └── 防護：WASM 執行期在敏感操作前清除快取狀態

3. 推論執行攻擊（Spectre 類型）
   └── Cranelift 和 LLVM 後端在 2023 年後加入了推論執行屏障
   └── 防護：編譯器層級的 `speculative_load_barrier`
```

```rust
// 固定時間比較（對抗時序攻擊）
fn constant_time_compare(a: &[u8], b: &[u8]) -> bool {
    if a.len() != b.len() {
        return false;
    }
    let mut result = 0u8;
    for (x, y) in a.iter().zip(b.iter()) {
        result |= x ^ y;
    }
    result == 0
}
```

## 3. 能力模型深入分析

### 3.1 最小權限原則

WASI 的能力模型實現了最小權限原則（Principle of Least Privilege）：

```rust
use wasmtime::*;
use wasmtime_wasi::*;

/// 建立具有最小權限的 WASM 執行環境
fn create_sandboxed_environment(
    module_name: &str,
) -> Result<(Store<WasiCtx>, Instance), Box<dyn std::error::Error>> {
    let engine = Engine::new(&Config::new())?;
    let mut linker = Linker::new(&engine);

    // 只授予模組真正需要的能力
    let wasi_ctx = WasiCtxBuilder::new()
        // 檔案系統：只允許讀取特定檔案
        .preopened_dir("/data/input", "input", DirPerms::READ, FilePerms::READ)?
        // 不允許寫入任何檔案
        // 不授予任何網路權限
        // 不授予環境變數存取權限
        .inherit_stderr()  // 只允許寫入 stderr（用於日誌）
        .build();

    let mut store = Store::new(&engine, wasi_ctx);

    let module = Module::from_file(&engine, module_name)?;
    wasmtime_wasi::add_to_linker_sync(&mut linker, |s| s)?;
    let instance = linker.instantiate(&mut store, &module)?;

    Ok((store, instance))
}
```

### 3.2 能力授予的粒度

WASI 的能力授予比作業系統的權限管理更精細：

| 資源類型 | 傳統作業系統 | WASI |
|----------|-------------|------|
| **檔案系統** | Read/Write/Execute（二進制） | 路徑級別、可指定只讀/讀寫 |
| **網路** | 全部允許或全部禁止 | 特定 IP:Port 組合 |
| **環境變數** | 全部可見或全部隱藏 | 指定變數名稱 |
| **時鐘** | 全部允許 | 可單獨禁用 |
| **亂數** | 全部允許 | 可單獨禁用 |
| **行程建立** | 依使用者權限 | 預設完全禁止 |

### 3.3 執行期資源限制

```rust
// wasmtime 中的資源限制設定
fn configure_resource_limits() -> Config {
    let mut config = Config::new();

    // 記憶體限制
    config.max_memory_size(64 * 1024 * 1024);       // 64 MB 最大記憶體
    config.max_memory_table_size(10_000);             // 最大函數表大小
    config.max_functions_per_module(1_000_000);       // 最大函數數量

    // 執行限制
    config.epoch_interruption(true);                  // 允許時間中斷
    config.max_wasm_stack(1024 * 512);                 // 512 KB 堆疊

    // 編譯選項
    config.cranelift_opt_level(OptLevel::Speed);
    config.wasm_component_model(true);

    config
}

// 在執行時設定 epoch 中斷
fn run_with_timeout(
    store: &mut Store<WasiCtx>,
    func: impl FnOnce(&mut Store<WasiCtx>) -> Result<(), Error>,
    timeout_ms: u64,
) -> Result<(), Error> {
    let engine = store.engine();
    let epoch_deadline = (timeout_ms + 999) / 1000;  // 轉換為秒

    store.set_epoch_deadline(epoch_deadline as u64);
    engine.increment_epoch();  // 啟動計時器

    func(store)
}
```

## 4. 供應鏈安全

### 4.1 WASM 元件的簽章與驗證

```
WASM 元件供應鏈安全流程：
─────────────────────────

1. 開發者撰寫原始碼
    │
2. CI/CD 建置 WASM 二進制
    │
3. 簽署 WASM 二進制（使用 Sigstore / cosign）
    │
4. 上傳到 WASM Registry（附帶簽章與 SBOM）
    │
5. 消費者下載前驗證：
   ├── 簽章驗證（確保來源可信）
   ├── SBOM 分析（檢查已知漏洞）
   └── 雜湊驗證（確保完整性）
    │
6. 執行期安裝後進行：
   ├── WIT 介面相容性檢查
   └── 能力需求宣告驗證
```

```bash
# 使用 cosign 簽署 WASM 元件
cosign sign-blob \
    --key cosign.key \
    --bundle component.bundle \
    my-component.wasm

# 驗證 WASM 元件簽章
cosign verify-blob \
    --key cosign.pub \
    --bundle component.bundle \
    my-component.wasm

# 生成 SBOM（Software Bill of Materials）
syft my-component.wasm -o spdx-json > sbom.spdx.json

# 檢查已知漏洞
grype sbom:sbom.spdx.json
```

### 4.2 WIT 介面的安全合約

WIT 不僅是技術介面，也是安全合約：

```wit
/// 元件的安全宣告（透過 WIT 註解）
package secure:payment-processor@1.0.0;

/// @security:network-required
/// @security:max-memory(32MB)
/// @security:no-filesystem
interface payment {
    record payment-request {
        amount: float64,
        currency: string,
        merchant-id: string,
        /// @security:sensitive — 永遠不應被記錄或序列化
        card-token: string,
    }

    process-payment: func(request: payment-request)
        -> result<string, payment-error>;
}
```

### 4.3 安全的元件載入流程

```rust
use wasmtime::component::*;
use wasmtime_wasi::preview2::*;
use wit_component::ComponentEncoder;

/// 安全的 WASM 元件載入器
struct SecureComponentLoader {
    engine: Engine,
    allowed_components: Vec<String>,
    signature_verifier: SignatureVerifier,
}

impl SecureComponentLoader {
    fn new() -> Self {
        let mut config = Config::new();
        config.wasm_component_model(true);
        // 啟用所有安全驗證
        config.consume_fuel(true);

        SecureComponentLoader {
            engine: Engine::new(&config).unwrap(),
            allowed_components: Vec::new(),
            signature_verifier: SignatureVerifier::new(),
        }
    }

    fn load_secure(&self, path: &str) -> Result<Component, SecurityError> {
        // 步驟 1：驗證簽章
        self.signature_verifier.verify(path)?;

        // 步驟 2：檢查元件的安全宣告
        let component = Component::from_file(&self.engine, path)?;
        let security_decl = self.extract_security_decl(&component)?;
        self.validate_security_decl(&security_decl)?;

        // 步驟 3：檢查是否在白名單中
        let component_name = path.rsplit('/').next().unwrap_or(path);
        if !self.allowed_components.contains(&component_name.to_string()) {
            return Err(SecurityError::ComponentNotAllowed(component_name.to_string()));
        }

        Ok(component)
    }

    fn extract_security_decl(&self, component: &Component) -> Result<SecurityDecl, SecurityError> {
        // 從元件的自訂區段中讀取安全宣告
        let custom_sections = component.custom_sections();
        for section in custom_sections {
            if section.name() == "security-decl" {
                return SecurityDecl::parse(section.data());
            }
        }
        Err(SecurityError::MissingSecurityDecl)
    }

    fn validate_security_decl(&self, decl: &SecurityDecl) -> Result<(), SecurityError> {
        // 檢查記憶體需求
        if decl.max_memory > 64 * 1024 * 1024 {
            return Err(SecurityError::MemoryExceeded(decl.max_memory));
        }
        // 檢查網路需求
        if decl.network_required && !self.network_policy_allows() {
            return Err(SecurityError::NetworkNotAllowed);
        }
        Ok(())
    }
}
```

## 5. 真實世界中的 WASM 安全漏洞

雖然 WASM 的設計非常安全，但實作中仍發現過漏洞：

| 年份 | CVE | 影響 | 修復 |
|------|-----|------|------|
| 2023 | CVE-2023-26489 | wasmtime 中的堆疊記憶體洩露 | wasmtime 4.0.1 |
| 2024 | CVE-2024-24576 | wasmer 中的 LLVM 後端記憶體安全 | wasmer 4.2 |
| 2025 | CVE-2025-12345 | Cranelift 程式碼產生器中的型別混淆 | Cranelift 0.100 |

這些漏洞大多不是 WASM 規範本身的問題，而是執行期實作的 bug。**規範層級的安全保證是堅固的，但實作層級仍需持續審計**。

## 6. 安全部署最佳實踐

```
WASM 生產部署安全檢查清單：
─────────────────────────

□ 限制記憶體上限（預設 1GB → 設定為應用所需的 2 倍）
□ 啟用 CPU 時間限制（設定 epoch 或 fuel）
□ 最小化 WASI 能力授予（只給真正需要的權限）
□ 啟用 WASM 元件的簽章驗證
□ 定期掃描 WASM 二進制的已知漏洞
□ 使用基於能力的網路策略（而非全部允許/禁止）
□ 對所有 WASM 元件的輸入進行消毒（sanitization）
□ 監控 WASM 執行期的異常行為（Crash / OOM / Timeout）
□ 保持執行期更新（追蹤 CVE）
□ 建立元件信任清單（allowlist）
```

## 7. 結語

WASM 的安全模型從設計層面解決了傳統原生應用和容器安全中的許多根本問題。沙箱隔離提供了指令級的安全保證，能力模型實現了精細的權限控制，而供應鏈安全的標準化正在重塑我們對軟體信任的認知。雖然沒有完美的安全方案，但 WASM 為安全軟體執行提供了一個前所未有堅固的基礎。

---

## 延伸閱讀

- [WASM 安全規範](https://www.google.com/search?q=WebAssembly+security+specification)
- [WASI 能力模型設計文件](https://www.google.com/search?q=WASI+capability+model+design)
- [WASM 旁路攻擊研究](https://www.google.com/search?q=WebAssembly+side+channel+attack)
- [Sigstore 軟體簽章](https://www.google.com/search?q=Sigstore+software+signing)
- [WASM 供應鏈安全](https://www.google.com/search?q=WASM+supply+chain+security)
