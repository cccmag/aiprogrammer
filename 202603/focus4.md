# 純函式與惰性求值：Haskell 的誕生（1980s-1990s）

## David Turner 與 SASL、Kiev、Miranda

在英國，David Turner 是另一位重要的函式程式設計先驅。他在 1970 年代和 1980 年代設計了一系列純函式語言：

| 語言 | 年份 | 簡介 |
|------|------|------|
| SASL | 1972 | St. Andrews Static Language |
| Kiev | 1980 | 早期惰性求值語言 |
| Miranda | 1985 | 純函式語言的先驅 |
| Orwell | 1986 | Haskell 的前身之一 |

Turner 的工作為後來的 Haskell 奠定了基礎。

---

## Miranda：純函式語言的先驅

1985 年，Turner 設計了 Miranda 語言。這是第一個真正商業化的純函式語言（不带任何指令式特性）。

### Miranda 的設計哲學

Miranda 的核心思想是：**所有函式都是純函式，沒有副作用**。

```miranda
-- Miranda 是純函式的：沒有賦值語句
-- 每個函式都是數學意義上的函式

-- 函式定義
factorial n = product [1..n]

-- 列表是語言的核心結構
evens = [x | x <- [1..]; x mod 2 = 0]

-- 無限列表（惰性求值）
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- 高階函式
map f [] = []
map f (x:xs) = f x : map f xs

filter p [] = []
filter p (x:xs) = 
  if p x then x : filter p xs 
  else filter p xs
```

### 列表推導

Miranda 的列表推導直接啟發了 Python 和 Haskell：

```miranda
-- 基本列表推導
squares = [x*x | x <- [1..10]]

-- 帶條件的推導
evens = [x | x <- [1..100]; x mod 2 = 0]

-- 巢狀推導
pairs = [(x,y) | x <- [1..3]; y <- [1..3]]

-- 更複雜的例子：質數篩選
primes = sieve [2..]
  where sieve (p:xs) = p : sieve [n | n <- xs; n mod p /= 0]

take 20 primes
-- [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
```

---

## Haskell 的誕生

1987 年，一群研究者決定在 Miranda 的基礎上創建一個新的標準函式語言。這個語言以 Haskell Brooks Curry 命名——他是數理邏輯的先驅，組合子邏輯的創始人。

1990 年，Haskell 1.0 規範發布。

### Haskell 的版本歷史

| 版本 | 年份 | 主要變化 |
|------|------|---------|
| Haskell 1.0 | 1990 | 初始版本 |
| Haskell 1.1 | 1991 | 模組系統 |
| Haskell 1.2 | 1992 | I/O 改進 |
| Haskell 1.4 | 1997 | 最後的 Haskell 98 前版本 |
| Haskell 98 | 1999 | 第一個穩定標準 |
| Haskell 2010 | 2010 | 最新 ISO 標準 |
| GHC 擴展 | 至今 | 豐富的語言擴展 |

---

## Haskell 的核心特性

### 純函式

Haskell 是純函式的：沒有賦值，沒有副作用。

```haskell
-- 這段程式碼總是返回相同的結果
add :: Int -> Int -> Int
add x y = x + y

-- 比較：帶副作用的程式（指令式）
-- doAdd x y = do
--     print x
--     print y
--     return (x + y)  -- 這個函式不純！

-- Haskell 的哲學：將純淨的部分與有副作用的部分分開
```

### 惰性求值

Haskell 使用惰性求值（Lazy Evaluation）：只在需要結果時才計算。

```haskell
-- 定義一個無限列表
naturals :: [Integer]
naturals = [1..]  -- 1, 2, 3, 4, ...

-- 但我們可以取它的前10個元素
take 10 naturals  -- [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

-- 無限費波那契數列
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

take 20 fibs
-- [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181]

-- 質數篩選
primes :: [Integer]
primes = sieve [2..]
  where
    sieve (p:xs) = p : sieve [n | n <- xs, n `mod` p /= 0]

take 20 primes
-- [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
```

### 惰性求值的工作原理

```
┌─────────────────────────────────────────────────────┐
│                  惰性求值示意                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  定義：                                             │
│  fibs = 0 : 1 : zipWith (+) fibs (tail fibs)      │
│                                                     │
│  求值過程：                                         │
│                                                     │
│  take 3 fibs                                       │
│  = take 3 (0 : 1 : zipWith (+) fibs (tail fibs))  │
│  = 0 : take 2 (1 : zipWith (+) fibs (tail fibs)) │
│  = 0 : 1 : take 1 (zipWith (+) fibs (tail fibs)) │
│  = 0 : 1 : take 1 (...)                          │
│  = 0 : 1 : 1 : ...                               │
│                                                     │
│  只有需要的部分被計算！                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Monads：處理副作用的革命

Haskell 最重要的創新是 **Monads**——這是一種用純函式處理副作用的抽象。

### 為什麼需要 Monads？

在純函式語言中，如何處理 I/O、狀態、異常等副作用？Haskell 的答案是：將副作用封裝在 Monad 中。

```haskell
-- IO Monad：用於處理輸入輸出
main :: IO ()
main = do
  putStrLn "What is your name?"
  name <- getLine
  putStrLn $ "Hello, " ++ name ++ "!"

-- 展開後相當於：
main = 
  putStrLn "What is your name?"
    >>= (\_ -> getLine)
    >>= (\name -> putStrLn $ "Hello, " ++ name ++ "!")
```

### Maybe Monad：處理可能失敗的操作

```haskell
-- 安全的除法
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)

-- 使用 do 語法糖
divide :: Int -> Int -> Maybe Int
divide x y = do
  a <- safeDiv x y
  b <- safeDiv a 2
  return b

-- 範例
divide 100 4  -- Just 12
divide 100 0  -- Nothing
divide 100 3  -- Nothing（因為 100/3 = 33.3 不是整數）
```

### State Monad：處理有狀態的計算

```haskell
import Control.Monad.State

-- 定義狀態類型
type Stack = [Int]

-- pop 操作
pop :: State Stack Int
pop = state $ (x:xs) -> (x, xs)

-- push 操作
push :: Int -> State Stack ()
push x = state $ xs -> ((), x:xs)

-- 使用 State Monad
stackOps :: State Stack Int
stackOps = do
  push 10
  push 20
  push 30
  a <- pop
  b <- pop
  return (a + b)

-- 執行
runState stackOps []
-- (50, [10])  -- 返回值 50，剩餘堆棧 [10]
```

### Monad 的數學定義

```haskell
-- Monad 類的定義
class Applicative m => Monad m where
  (>>=)  :: m a -> (a -> m b) -> m b    -- bind
  return :: a -> m a                       -- unit
  (>>)   :: m a -> m b -> m b            -- sequence

-- 三個定律：
-- 1. return a >>= f  ≡  f a                (左單位元)
-- 2. m >>= return   ≡  m                  (右單位元)
-- 3. (m >>= f) >>= g  ≡  m >>= (\x -> f x >>= g)  (結合律)
```

### Monads 的視覺化

```
┌─────────────────────────────────────────────────────┐
│                   Monad 示意                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│    Maybe Monad:                                     │
│                                                     │
│         Just a                                      │
│            │                                        │
│            ▼                                        │
│         ┌──────┐                                   │
│         │ >>= f │                                   │
│         └──────┘                                   │
│            │                                        │
│            ▼                                        │
│    ┌────────────┐                                  │
│    │  f a >>= g │                                  │
│    └────────────┘                                  │
│            │                                        │
│     ┌──────┴──────┐                                │
│     ▼              ▼                               │
│   Just b         Nothing                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Monads 的影響

Monads 的概念影響深遠，後來出現在幾乎所有主流語言中：

| 語言 | Monads 的體現 |
|------|--------------|
| JavaScript | Promise |
| Python | List comprehension, async/await |
| Scala | for comprehension |
| Rust | Result, Option, async/await |
| C# | LINQ, async/await |
| Kotlin | 擴展函式 |

### JavaScript Promise

```javascript
// Promise 是 JavaScript 的 IO Monad
fetch('/api/user')
    .then(user => fetch(`/api/posts/${user.id}`))
    .then(posts => posts.json())
    .then(posts => console.log(posts))
    .catch(error => console.error(error));

// 等價於 Haskell 的 do 語法
// do
//   user <- fetch "/api/user"
//   posts <- fetch (concat ["/api/posts/", user.id])
//   liftIO (print posts)
```

### Rust 的 Result

```rust
use std::fs::File;
use std::io::{self, Read};

fn read_file(path: &str) -> Result<String, io::Error> {
    let mut file = File::open(path)?;  // ? 是 >>= 的語法糖
    let mut contents = String::new();
    file.read_to_string(&mut contents)?;
    Ok(contents)
}

// 使用
fn main() {
    match read_file("config.txt") {
        Ok(contents) => println!("{}", contents),
        Err(e) => eprintln!("Error: {}", e),
    }
}
```

---

## Haskell 的其他特色

### 類別系統（Type Classes）

```haskell
-- 類別定義（類似介面）
class Eq a where
    (==) :: a -> a -> Bool
    (/=) :: a -> a -> Bool

-- 實例實現
instance Eq Bool where
    True == True = True
    False == False = True
    _ == _ = False

-- 派生（自動實現）
data Color = Red | Green | Blue
    deriving (Eq, Show, Read)

-- 多參數類別
class Monad m => MonadError e m | m -> e where
    throwError :: e -> m a
    catchError :: m a -> (e -> m a) -> m a
```

### 列表推導

```haskell
-- 列表推導（列表 Monad 的語法糖）
pythagorean :: [(Int, Int, Int)]
pythagorean = [(a,b,c) | c <- [1..], 
                         a <- [1..c], 
                         b <- [a..c],
                         a*a + b*b == c*c]

-- 查詢風格的列表操作
comprehensive :: [(String, Int)]
comprehensive = 
    [ (name, age) 
    | (name, age) <- people
    , age >= 18
    , "台北" `elem` getCities name
    ]
```

### 應用程式設計（Applicative Programming）

```haskell
-- Applicative 允許在上下文中應用普通函式
Just (+3) <*> Just 4    -- Just 7
Nothing <*> Just 4       -- Nothing
Just (+3) <*> Nothing   -- Nothing

-- 序列化和驗證
validate :: String -> Maybe Int
validate s = do
    guard $ not (null s)
    guard $ all isDigit s
    return $ read s

-- 可選值的多步驟處理
lookupCity :: User -> Maybe City
lookupCity u = do
    addr <- address u
    city <- city addr
    return city
```

---

## 結語：為什麼 Haskell 重要？

Haskell 的價值在於：

1. **理論嚴謹性**：基於 Category Theory 的類型系統
2. **實踐價值**：惰性求值、Monads 等概念已被主流語言採用
3. **語言研究平台**：新概念往往先在 Haskell 中實驗
4. **學術影響**：催生了大量的論文和工具

Haskell 雖然從未成為主流語言，但它的思想已經深刻影響了整個程式設計領域。當你使用 Rust 的 `Result`、Python 的 `async/await`、或 JavaScript 的 `Promise` 時，你正在使用 Haskell 的遺產。

---

## 延伸閱讀

- [Haskell Wiki](https://www.google.com/search?q=Haskell+programming+language)
- [Simon Peyton Jones: Escape from the ivory tower](https://www.google.com/search?q=Simon+Peyton+Jones+Haskell+talk)
- [Learn You a Haskell for Great Good](https://www.google.com/search?q=Learn+You+a+Haskell)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之四。*
