# Rust 的起源

## 從個人專案到系統程式語言（2006-2015）

### 一切從電梯故障開始

2006 年，Mozilla 工程師 **Graydon Hoare** 住在溫哥華的一棟高層公寓裡。某天電梯故障，他只好爬了 21 層樓梯——在爬樓梯的過程中，他開始思考現代系統程式語言的問題。

Graydon 在 Mozilla 的主要工作是 Firefox 瀏覽器——一個用 C++ 寫的、超過千萬行程式碼的龐大專案。Firefox 團隊花費了大量時間處理 C++ 的記憶體錯誤：use-after-free、buffer overflow、dangling pointer……這些問題不僅導致瀏覽器崩潰，還帶來了嚴重的安全漏洞。

他的想法很簡單：**能不能設計一種語言，讓編譯器在編譯階段就防止這些錯誤，而不需要犧牲效能？**

### 從 OCaml 到自舉

Graydon 最初用 OCaml 寫了一個編譯器原型——OCaml 的型別系統和模式匹配讓他能快速嘗試不同的設計。2006 年至 2009 年間，Rust 只是一個業餘專案，在 Graydon 的個人時間中緩慢發展。

2010 年，Mozilla 正式贊助了這個專案。原因是：Mozilla 正在開發一個名為 **Servo** 的實驗性瀏覽器引擎——一個用 Rust 寫的、利用現代多核心硬體的平行渲染引擎。Rust 從 Graydon 的個人專案變成了 Mozilla 的戰略投資。

2011 年，Rust 編譯器完成了一個重要里程碑：**自舉**（self-hosting）——Rust 編譯器可以用 Rust 本身編譯了。這證明了 Rust 已經足夠成熟到可以開發編譯器這種複雜的工具。

### 早期的設計探索

2010 年至 2014 年間，Rust 經歷了劇烈的設計變更：

- **Green threading**：最初的 Rust 有自己的輕量執行緒（類似 Go 的 goroutine）。但後來這個設計被移除，Rust 選擇了 OS 執行緒 + 零成本抽象的 async/await
- **Typestate system**：最初的 Rust 有一個複雜的型別狀態系統，後來被簡化為所有權模型
- **Sigils**：Rust 早期版本使用大量的符號（如 `~` 表示堆分配、`@` 表示 GC 指標），最後這些都被替換為更清晰的關鍵字

### Mozilla 的支援

Mozilla 對 Rust 的支援不僅是資金上的，更是戰略上的。Servo 專案提供了 Rust 在大型系統中的實戰驗證。同時，Mozilla 也建立了 **Rust 團隊**——一個由社群驅動的開放治理結構。

2014 年，Rust 的治理模式從 Mozilla 集中管理轉向**核心團隊 + 子團隊**的社群治理。這個轉變確保了 Rust 不會依賴於單一公司的決策。

### Rust 1.0：穩定的承諾

2015 年 5 月 15 日，**Rust 1.0** 正式發布。這不僅是 Rust 的第一個穩定版本，更是一個重要的承諾：**向後相容性**。

Rust 團隊從 1.0 開始就制定了嚴格的向後相容政策：
- 任何在 1.0 上編譯通過的程式碼，在將來的版本中必須繼續編譯通過
- 編譯器不得以向後不相容的方式修改語言
- 新功能通過 Edition 機制引入，不影響舊程式碼

這個承諾至今（2026 年）仍被嚴格遵守。

### 1.0 時期的關鍵設計

Rust 1.0 的核心設計已經與今天的 Rust 非常接近：

```rust
// 所有權與借用
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// Trait 系統
trait Drawable {
    fn draw(&self);
}

// 模式匹配
match x {
    0 => println!("zero"),
    1..=9 => println!("small"),
    _ => println!("large"),
}

// 無條件的記憶體安全
let v = vec![1, 2, 3];
let first = &v[0]; // 編譯器保證不會出現 dangling reference
```

### 歷史的評價

回顧 Rust 的誕生，我們可以看到它的成功並非偶然：

1. **Mozilla 的戰略眼光**：投入資源開發一個沒有短期回報的語言
2. **社群的開放治理**：避免單一公司控制的風險
3. **嚴格的向後相容**：建立開發者的信任
4. **明確的定位**：系統程式語言，不與高階語言競爭

Rust 1.0 的發布標誌著 Rust 從「研究專案」轉變為「生產就緒的語言」。但這只是開始——接下來五年，Rust 將在工具鏈、生態系統和語言功能上繼續快速發展。

---

**下一步**：[所有權模型](focus2.md)

## 延伸閱讀

- [Rust 官方歷史](https://www.google.com/search?q=Rust+programming+language+history)
- [Graydon Hoare 關於 Rust 起源的訪談](https://www.google.com/search?q=Graydon+Hoare+Rust+origin+interview)
- [The Rust Project: From Personal Project to Production](https://www.google.com/search?q=Rust+from+personal+project+to+production)
