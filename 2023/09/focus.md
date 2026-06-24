# 本期焦點

## 程式語言理論 (PLT)

### 引言

程式語言理論（Programming Language Theory, PLT）是電腦科學的基礎學科之一，研究程式語言的設計、實作和分析。PLT 不僅是學術研究，更是現代程式語言設計的實用指導——從 Rust 的借用檢查器到 TypeScript 的型別系統，從 Haskell 的 Monad 到 Kotlin 的協程，PLT 的洞見隨處可見。

本期雜誌將帶領讀者探索 PLT 的核心概念。我們從程式語言的設計原則出發，逐步深入到型別系統、λ 演算、閉包、continuation 和程式語意學等主題。每篇文章都力求將理論與實務結合，使用 Python 程式碼展示抽象概念。

### 大綱

* [程式：PLT 範例整合](focus_code.md)
   - λ 演算直譯器（Church numerals、Y combinator）
   - 型別檢查器（簡單型別 λ 演算）
   - 高階函數與組合子
   - Monad 模擬（Maybe、List、Either）

1. [程式語言設計原則](focus1.md)
   - 語法 vs 語意、抽象化機制、正規語法理論

2. [型別系統導論](focus2.md)
   - 型別安全的定義、簡單型別 λ 演算、型別檢查演算法

3. [多型與泛型](focus3.md)
   - 參數多型、特設多型、子型別多型、Rust trait 與 Haskell typeclass

4. [λ 演算與函數式程式設計](focus4.md)
   - Church 編碼、不動點組合子、純函數式程式設計

5. [作用域與閉包](focus5.md)
   - 詞法作用域、動態作用域、閉包的實作、變數捕獲

6. [控制流程與 continuation](focus6.md)
   - CPS 轉換、call/cc、例外處理與協程的理論基礎

7. [程式語意學](focus7.md)
   - 操作語意（小步/大步）、指稱語意、公理語意、Hoare 邏輯

### PLT 的實用價值

PLT 看似抽象，但其概念直接影響每日的程式設計：

- **型別系統**是 TypeScript、Rust、Haskell 的核心——好的型別系統在編譯期就排除大量錯誤
- **閉包**是 JavaScript 和 Python 的關鍵特性——回呼函數、事件處理都依賴閉包
- **Monad** 是函數式 I/O 和錯誤處理的基礎——Rust 的 Result 和 Option 就是 Monad 的實例
- **continuation** 是協程和非同步程式設計的理論來源——async/await 是 continuation 的受限形式
- **程式語意學**提供形式化驗證的理論基礎——用數學保證程式正確性

### 與 AI 開發的關聯

PLT 概念在 AI 開發中也日益重要：

- **型別系統**幫助 LLM 生成的程式碼更可靠
- **程式語意學**為程式碼分析提供理論基礎
- **函數式抽象**讓神經網路架構的設計更具模組性

學習 PLT 不僅是理解語言的「怎麼用」，更是理解語言的「為什麼這樣設計」。這種深度理解讓你在面對新語言或新框架時能更快掌握其精髓。

### 延伸閱讀

- [程式語言設計原則](focus1.md)
- [型別系統導論](focus2.md)
- [多型與泛型](focus3.md)
- [λ 演算與函數式程式設計](focus4.md)
- [作用域與閉包](focus5.md)
- [控制流程與 continuation](focus6.md)
- [程式語意學](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
