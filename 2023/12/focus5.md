# 程式語言與編譯器

## 2023 年程式語言生態系統回顧

2023 年是程式語言領域充滿變化的一年。Rust 正式進入 Linux 核心，C 語言時隔十年迎來新標準，TypeScript 持續擴張，Mojo 作為 AI 專用語言登場。讓我們一起回顧這些重要發展。

---

## Rust：進入核心的一年

### Linux 核心中的 Rust

2023 年是 Rust 進入 Linux 核心的關鍵一年。雖然 Rust for Linux 專案始於 2021 年，但 2023 年取得了实质性進展：

**6.1 核心**（2022 年 12 月）：最初的 Rust 基礎設施合併。

**6.6 核心**（2023 年 10 月）：第一組 Rust 核心抽象（Rust abstractions）被合併，包括 Arc、RefCount 和異步基礎設施。

**6.7 核心**（2023 年 12 月）：更多的 Rust 驅動器程式碼被合併，包括網路驅動器 NVMe 驅動。

Rust 在核心中的優勢是顯著的：記憶體安全保證可以消除約 70% 的核心漏洞。不過，Rust 核心程式設計仍然面臨工具鏈整合和學習曲線的挑戰。

### Rust 生態擴張

**套件生態**：crates.io 上的套件數從年初的 12 萬成長到年底的 14.5 萬。

**Rust 基金會**：成立了安全關鍵 Rust 聯盟，推動 Rust 在汽車、航空和工業控制等安全關鍵領域的應用。

**就業市場**：Rust 開發者的需求持續增長，被 Stack Overflow 調查評為「最受喜愛的程式語言」第 8 年。

### 關鍵發布

- **Rust 1.70**（6 月）：OnceCell/OnceLock 穩定化
- **Rust 1.71**（7 月）：C-unwind ABI 穩定化
- **Rust 1.72**（8 月）：`.await` 在 `match` 中可用
- **Rust 1.73**（10 月）：Cleanup 恐慌訊息
- **Rust 1.74**（11 月）：Lint 透過 Cargo 配置

---

## C23 標準

2023 年 12 月，國際標準化組織（ISO）正式發布了 C23（ISO/IEC 9899:2024），這是 C 語言自 2011 年以來的第一次重大更新。

### 主要新特性

**`nullptr` 巨集**：引入 `nullptr` 與新的 `nullptr_t` 類型，取代傳統的 `NULL` 巨集。

**`bool` 成為關鍵字**：`bool`、`true`、`false` 不再需要 `<stdbool.h>`。

**`constexpr` 支援**：類似於 C++ 的 `constexpr`，允許編譯時計算。

**`auto` 關鍵字**：從 C++ 引入的類型推導，讓變數宣告更加簡潔。

**`#embed` 預處理器指令**：編譯時直接嵌入二進位檔案內容。

**十進位浮點數**：基於 IEEE 754-2008 的十進位浮點數類型。

### 評估

C23 並不意在讓 C 語言變得「現代」，而是讓 C 更好地服務於其核心場景——系統程式設計和嵌入式開發。新增的特性大多是可選的，不會破壞既有程式碼。

---

## TypeScript 與型別系統

TypeScript 在 2023 年繼續鞏固其作為 JavaScript 超集的地位。

### TypeScript 5.x 系列

- **TypeScript 5.0**（3 月）：裝飾器（decorators）正式標準化，支援 `const` 類型參數
- **TypeScript 5.1**（6 月）：連結類型推導改進，JSX 元素訪問檢查
- **TypeScript 5.2**（8 月）：`using` 宣告和顯式資源管理
- **TypeScript 5.3**（11 月）：匯入屬性，數字分隔符支援

### Flow 的衰落

Meta 在 2023 年宣布將逐步淘汰 Flow，轉向 TypeScript。這結束了 JavaScript 靜態型別檢查工具的多年競爭，TypeScript 成為事實上的標準。

---

## Mojo：AI 專用語言的誕生

2023 年 9 月，Chris Lattner（LLVM 和 Swift 的創造者）創辦的 Modular 公司發布了 Mojo 語言。

### Mojo 的特色

**Python 相容語法**：Mojo 的語法與 Python 高度相似，Python 開發者可以無縫過渡。

**高效能編譯**：基於 MLIR 和 LLVM，Mojo 可以編譯為高效的原生代碼，性能可達 Python 的 35000 倍。

**硬體抽象**：直接在語言層面支援 GPU、TPU 和其他加速器的程式設計。

**所有權系統**：類似 Rust 的所有權模型，但不要求開發者總是顯式管理記憶體。

### 爭議與討論

Mojo 的封閉原始碼策略引發了開源社群的批評。許多開發者對「看起來像 Python 但不同」的語言持觀望態度。儘管如此，Mojo 獲得了 1 億美元的融資，展現了投資者對 AI 專用語言的信心。

---

## 其他語言動態

**Python**：Python 3.12 在 10 月發布，引入了更快的 c-api、更好的錯誤訊息和新的除錯功能。Python 仍然是資料科學和 AI 領域的主導語言。

**Zig**：Zig 0.11 於 5 月發布，專注於改善 C 語言的使用體驗。Zig 在編譯期計算和跨編譯方面的能力受到系統程式設計師的關注。

**Go**：Go 1.21 在 8 月發布，引入了內建的 `log/slog` 結構化日誌、新的 `maps`、`slices` 標準套件，以及向前相容性工具鏈。

**Julia**：Julia 1.9 在 5 月發布，大幅提升首次編譯速度。Julia 在科學計算領域的應用持續增長。

---

## 延伸閱讀

- [Rust for Linux 進展](https://www.google.com/search?q=Rust+Linux+kernel+2023+progress)
- [C23 標準新特性](https://www.google.com/search?q=C23+standard+new+features+2023)
- [Mojo 語言發布](https://www.google.com/search?q=Mojo+programming+language+AI+2023)
- [TypeScript 5.0 發布](https://www.google.com/search?q=TypeScript+5.0+decorators+2023)

---

*本篇文章為「AI 程式人雜誌 2023 年 12 月號」年度回顧系列之五。*
