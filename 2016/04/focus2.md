# 主題二：Haskell — 純函式語言的典範

## Haskell 簡史

Haskell 起源於 1987 年，當時一群研究者匯聚於 FPCA（Functional Programming and Computer Architecture）會議，決定創造一個統一的純函式程式語言。經過八年的開發，Haskell 1.0 於 1990 年正式發布。

Haskell 以數學家 Haskell Brooks Curry 命名，他是組合邏輯（Combinatory Logic）的先驅。這個名字極為適切——Haskell 深深根植於數學傳統，將程式視為證明，計算視為推理。

## 純函式的保證

Haskell 最大的特點是**純度（Purety）**——沒有副作用。什麼是副作用？修改全域變數、拋出異常、進行 I/O 操作——這些都是副作用。Haskell 的純函式保證：

- 相同輸入永遠產生相同輸出
- 函式不依賴或修改任何外部狀態
- 程式具有極强的可推斷性和可測試性

當你需要副作用時，Haskell 使用 Monad 來封裝它們。IO Monad 讓你可以編寫有 I/O 的程式，同時保持純函式核心。

```haskell
-- 純函式
factorial :: Integer -> Integer
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- 有副作用的 I/O（使用 IO Monad）
main :: IO ()
main = do
    putStrLn "Enter your name:"
    name <- getLine
    putStrLn ("Hello, " ++ name ++ "!")
```

## 靜態強類型系統

Haskell 採用靜態強類型系統，在編譯時就能發現大多數錯誤。Haskell 的類型推論（Type Inference）極為強大——多數情況下你不需要顯式標注類型，編譯器會自動推斷。

```haskell
-- 編譯器自動推斷：add :: Num a => a -> a -> a
add x y = x + y

-- 顯式類型標注
add :: Int -> Int -> Int
add x y = x + y
```

Haskell 的類型類別（Type Class）是一種強大的抽象機制，類似於其他語言的介面（Interface）：

```haskell
-- 定義類型類別
class Eq a where
    (==) :: a -> a -> Bool
    (/=) :: a -> a -> Bool

-- 為自訂類型實作類型類別
data Color = Red | Green | Blue

instance Eq Color where
    Red == Red = True
    Green == Green = True
    Blue == Blue = True
    _ == _ = False
```

## 惰性求值

Haskell 預設採用惰性求值（Lazy Evaluation）——只有當需要結果時才進行計算。這帶來了強大的表達能力：

```haskell
-- 無限列表：只有需要的部分才會被計算
nats = [1..]  -- 1, 2, 3, 4, ...

-- 前 10 個奇數
odds = [1, 3 ..]
take 10 odds  -- [1,3,5,7,9,11,13,15,17,19]

-- 費伯那契數列
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)
take 20 fibs  -- [0,1,1,2,3,5,8,13,21,34,55,89,144,233,377,610,987,1597,2584,4181]
```

惰性求值使得我们可以優雅地處理無限結構，實現高效的反應式程式。

## 為什麼要學習 Haskell？

### 提升程式設計思維

學習 Haskell 會徹底改變你思考程式的方式。你會學會用數學思維解決問題，將複雜邏輯分解為簡單函式的組合。

### 學術研究與形式驗證

Haskell 在學術界廣泛用於程式語言研究、類型理論研究和形式驗證。許多新語言的概念首先在 Haskell 中實現和測試。

### 金融科技

金融機構採用 Haskell 建構高風險系統。Standard Chartered、Barclays 等公司使用 Haskell 開發交易系統和風險計算引擎。Haskell 的純度和強類型使得系統更難出錯。

### 並行與分散式處理

Haskell 的輕量級執行緒和軟體事務記憶體（Software Transactional Memory）使其適合編寫高效並行程式。

## GHC：主要的 Haskell 編譯器

Glasgow Haskell Compiler（GHC）是 Haskell 最主要和最完整的編譯器：

- **GHCi**：互動式直譯器，方便快速測試想法
- **GHC**：高效 JIT 編譯器
- **Hackage**：Haskell 套件庫，收錄超過 10,000 個套件
- **Stack**：現代 Haskell 專案管理工具

```bash
# 安裝 GHC 和 Stack
# macOS: brew install ghc stack

# 建立新專案
stack new my-project

# 進入 GHCi
stack ghci

# 編譯專案
stack build
```

## Haskell 經典書籍

- **「Learn You a Haskell for Great Good!」**：友善的入門書籍
- **「Real World Haskell」**：實用導向，涵蓋真實專案
- **「Graham Hutton, Programming in Haskell」**：教授 Haskell 基礎
- **「Simon Peyton Jones, Implementation of Functional Languages」**：深入 GHC 內部

## 小結

Haskell 是純函式程式設計的典範，它將數學嚴謹與實際應用完美結合。惰性求值、強類型系統、Monad 抽象——這些概念不僅在 Haskell 中有意義，也影響了整個程式語言生態。

下一篇文章中，我們將探討 Clojure——JVM 上的現代 Lisp，看看函數式程式設計如何在企業環境中大放異彩。