# Rust 編譯時元程式設計：從 proc-macro 到 const generics

## 為什麼元程式設計在系統程式設計中重要

系統程式設計長期被視為 C 和 C++ 的領地，但 Rust 正在改變這一切。Rust 不僅帶來記憶體安全，還引入了一套強大的編譯時元程式設計（compile-time metaprogramming）工具，讓開發者能在編譯期間生成、分析和轉換程式碼。

系統程式往往需要處理低階硬體操作、序列化、記憶體佈局等重複性極高的任務。C 語言依賴巨集和 `#ifdef`，但缺乏型別安全且難以除錯。Rust 的元程式設計方案——從 proc-macro 到 const generics——提供了型別安全、可組合、且能在編譯期捕捉錯誤的替代方案。

## proc-macro：最強大的元程式設計工具

proc-macro（程序性巨集）是 Rust 中最靈活的元程式設計機制。與 `#[derive]` 這類宣告式巨集不同，proc-macro 允許開發者編寫任意的 Rust 程式碼來處理 Rust 的抽象語法樹（AST）。

proc-macro 分為三類：自訂 derive 巨集、屬性式巨集、函數式巨集。建立一個 proc-macro 需要在 `Cargo.toml` 中宣告：

```toml
[lib]
proc-macro = true

[dependencies]
syn = { version = "2", features = ["full"] }
quote = "1"
proc-macro2 = "1"
```

`syn` 負責將 Rust 原始碼解析為 AST，`quote` 負責將產生的 TokenStream 序列化回程式碼。這兩個函式庫構成了 proc-macro 生態系的基石。

## 使用 proc-macro 減少樣板程式碼

任何寫過 Rust 的開發者都使用過 `#[derive(Debug, Clone, PartialEq)]`。這就是 proc-macro 最經典的應用。但 proc-macro 的威力遠不止於此。考慮一個序列化場景：

```rust
// 使用者只需要寫：
#[derive(IntoBytes)]
struct Packet {
    id: u32,
    flags: u8,
    payload: [u8; 64],
}

// proc-macro 自動產生：
impl IntoBytes for Packet {
    fn into_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(72);
        bytes.extend_from_slice(&self.id.to_le_bytes());
        bytes.push(self.flags);
        bytes.extend_from_slice(&self.payload);
        bytes
    }
}
```

這不僅節省打字時間，更消除了人為錯誤——欄位順序、大小計算、位元組序處理全部由程式自動生成。

## const generics：編譯時泛型參數

const generics（常數泛型）是 Rust 1.51 引入的功能，允許將整數、布林值或字元等常數值作為泛型參數。這解決了長期以來的痛點：無法用型別表達陣列大小。

```rust
struct Buffer<const N: usize> {
    data: [u8; N],
    len: usize,
}

impl<const N: usize> Buffer<N> {
    fn new() -> Self {
        Buffer { data: [0u8; N], len: 0 }
    }
}

let small = Buffer::<32>::new();
let large = Buffer::<1024>::new();
```

在系統程式設計中，const generics 的應用無所不在：網路協定中的 MTU 大小、音訊處理的取樣緩衝區、嵌入式系統的固定大小陣列——這些都能在型別層級表達。

## const fn：編譯時計算

`const fn` 允許函數在編譯時期執行。隨著 Rust 版本演進，`const fn` 已支援迴圈、條件判斷、泛型等特性：

```rust
const fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 { a } else { gcd(b, a % b) }
}

const COMPUTED: u64 = gcd(48, 18); // 編譯時計算為 6

// 也可以在型別參數中使用：
struct Ratio<const N: u64, const D: u64>;
type Simplified = Ratio<{48 / gcd(48, 18)}, {18 / gcd(48, 18)}>;
```

在系統程式設計中，`const fn` 的價值在於零成本抽象。例如 CRC32 查詢表可在編譯時生成，執行時只需查表：

```rust
const fn build_crc32_table() -> [u32; 256] {
    let mut table = [0u32; 256];
    let mut i = 0;
    while i < 256 {
        let mut crc = i as u32;
        let mut j = 0;
        while j < 8 {
            if crc & 1 == 1 {
                crc = 0xedb88320 ^ (crc >> 1);
            } else {
                crc >>= 1;
            }
            j += 1;
        }
        table[i] = crc;
        i += 1;
    }
    table
}

static CRC32_TABLE: [u32; 256] = build_crc32_table();
```

## 實戰案例：用 proc-macro 實作 MMIO

在嵌入式開發中，MMIO（Memory-Mapped I/O）是最基本的操作模式。手動撰寫 MMIO 訪問程式碼既繁瑣又危險。讓我們用 proc-macro 自動化這個過程：

```rust
#[derive(MMIO)]
#[repr(C)]
struct UARTRegisters {
    #[reg(offset = 0x00)]
    data: Reg<u32>,
    #[reg(offset = 0x04)]
    status: Reg<u32>,
    #[reg(offset = 0x08)]
    control: Reg<u32>,
    #[reg(offset = 0x0C)]
    baud: Reg<u32>,
}

// proc-macro 為每個暫存器產生安全的訪問方法：
impl UARTRegisters {
    pub fn read_data(&self) -> u32 {
        self.read::<u32>(0x00)
    }
    pub fn write_data(&self, value: u32) {
        self.write::<u32>(0x00, value);
    }
    pub fn is_transmit_empty(&self) -> bool {
        self.read::<u32>(0x04) & (1 << 5) != 0
    }
    pub fn enable_transmit(&self) {
        let mut ctrl = self.read::<u32>(0x08);
        ctrl |= 1;
        self.write::<u32>(0x08, ctrl);
    }
}
```

proc-macro 的實作核心使用 `syn` 解析結構體欄位和屬性，再用 `quote` 生成訪問方法：

```rust
#[proc_macro_derive(MMIO, attributes(reg))]
pub fn derive_mmio(input: TokenStream) -> TokenStream {
    let input = parse_macro_input!(input as DeriveInput);
    let struct_data = match &input.data {
        Data::Struct(s) => s,
        _ => panic!("MMIO only supported for structs"),
    };
    let name = &input.ident;

    let expanded = quote! {
        impl MMIO for #name {
            fn read<T>(&self, offset: usize) -> T {
                unsafe { (self as *const Self as *const u8)
                    .add(offset).cast::<T>().read_volatile() }
            }
            fn write<T>(&self, offset: usize, value: T) {
                unsafe { (self as *const Self as *mut u8)
                    .add(offset).cast::<T>().write_volatile(value) }
            }
        }
    };
    expanded.into()
}
```

任何偏移量錯誤、型別不匹配都會在編譯時被捕獲，而非在嵌入式硬體上崩潰。這就是編譯時元程式設計的核心價值。

## 編譯時元程式設計的未來

Rust 的編譯時元程式設計仍在快速演進。幾個值得關注的方向：

**GAT（Generic Associated Types）**：已於 Rust 1.65 穩定，允許 trait 關聯型別擁有泛型參數，讓抽象 factory pattern、lending iterators 等模式成為可能。

**效果泛型（Effect Generics）**：正在設計中的功能，允許函數和型別宣告 `async`、`fallible`、`const` 等「效果」，使 `const fn` 能與泛型程式碼無縫整合。

**編譯時反射**：社群正在討論讓 Rust 具備有限的編譯時反射能力，讓 proc-macro 不需要依賴 `syn` 解析原始碼，而是直接查詢型別資訊。

**更強大的 const generics**：未來可能支援浮點數、字串及更複雜的型別層級計算，進一步模糊編譯期與執行期的界線。

## 結語

從 proc-macro 到 const generics，Rust 提供了一套比其他系統程式語言更安全、更具表達力的編譯時元程式設計工具箱。這些工具不僅減少樣板程式碼，更重要的是將錯誤從執行時移至編譯時，讓「編譯通過即正確」從理想變為現實。

掌握這些工具意味著能編寫更安全、更高效、更可維護的低階程式碼。而這正是 Rust 在系統程式設計領域持續崛起的原因——不是因為它讓困難的事情變簡單，而是因為它讓不可能的事情變得可能。
