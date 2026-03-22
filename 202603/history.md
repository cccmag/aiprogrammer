# 歷史回顧

## Lambda Calculus 與 Functional Programming 的發展歷程

### 引言

在程式設計的浩瀚星空中，有一個概念雖然誕生於近百年前，卻持續影響著當代最先進的技術——這就是 Lambda Calculus。從 1936 年 Alonzo Church 的數學理論，到今日大語言模型的核心架構，函式程式設計的思想貫穿了整個計算機科學的發展史。本期歷史回顧將帶領讀者穿梭時空，探索這段迷人的技術演進之旅。

我們將深入探討這條從數學基礎到現代 AI 的思想脈絡，揭示那些看似抽象的概念如何塑造了我們今天所使用的每一種程式語言。

---

## 第一章：數學基礎（1920s-1930s）

### 1.1 計算的本質問題

在 1920 年代，數學界正面臨一場深刻的危機。David Hilbert 在 1900 年提出的 23 個數學問題中，第二個問題涉及到算術公理的一致性證明。這個問題看似簡單，卻引發了對「計算」本質的深刻思考。

什麼是計算？什麼可以被計算？什麼不能被計算？這些問題困擾著一代又一代的數學家。直覺告訴我們，整數加法可以被計算，求解方程式可以被計算，但有些問題——如停機問題——似乎本質上是不可解決的。但「直覺」不夠嚴謹，數學家需要一個精確的定義來描述「可計算性」。

### 1.2 Kurt Gödel 與不完全性定理

1931 年，Kurt Gödel 發表了震驚數學界的不完全性定理。這些定理證明了任何足夠強大的公理系統都存在無法證明或否定的命題。更具體地說，Gödel 發明了「Gödel 編碼」技術，將數學陳述式轉換為自然數，反之亦然。

這個編碼思想極大地啟發了後來的計算理論。如果數學陳述式可以被編碼為數字，那麼函式——從輸入到輸出的映射——也可以被編碼。這為後來的通用可計算函式概念奠定了基礎。

Gödel 與他的學生 Hermann Weyl 有過一段著名的對話。Weyl 說：「什麼是計算？這是一個哲學問題。」Gödel 回應：「你可以在有限步驟內完成的任何操作。」這句話雖然直覺，卻不夠精確——直到後來的三位巨人登場。

### 1.3 Alonzo Church 與 λ 演算的誕生

Alonzo Church（1903-1995）是美國數學家，畢業於普林斯頓大學，並在那裡度過了大半學術生涯。1936 年，Church 發表了論文《An Unsolvable Problem of Elementary Number Theory》，首次提出了 λ 演算（Lambda Calculus）。

λ 演算的核心思想極為簡潔：

**語法規則**：
```
變數：x, y, z, ...
抽象：λx.M（其中 M 是表達式，x 是變數）
應用：M N（其中 M 和 N 都是表達式）
括號：(M)
```

**化簡規則**（β-規約）：
```
(λx.M) N → M[x := N]
```

這就是全部。僅僅這三條語法規則和一條化簡規則，就構成了一個完整的計算系統。

讓我們看一些具體例子：

```lambda
-- 恆等函式
λx.x

-- 應用恆等函式
(λx.x) y
→ y

-- 應用於另一個函式
(λx.x) (λz.z)
→ (λz.z)

-- 柯里化：接受兩個參數的函式
λx.λy.x+y

-- 應用於第一個參數
(λx.λy.x+y) 5
→ λy.5+y

-- 再應用於第二個參數
(λx.λy.x+y) 5 3
→ λy.5+y 3
→ 5+3
→ 8
```

這個系統的威力在於：任何可計算函式都可以用 λ 演算表示。Church 提出了著名的「Church  thesis」：

> **Church 論題**：一個函式是直覺可計算的，當且僅當它是 λ 可定義的。

### 1.4 Alan Turing 與圖靈機

幾乎在同一時期，大洋彼岸的英國劍橋大學，Alan Turing（1912-1954）也在思考同一個問題。1936 年，Turing 發表了論文《On Computable Numbers, with an Application to the Entscheidungsproblem》，提出了圖靈機的概念。

圖靈機的設計極為直覺：

```
┌─────────────────────────────────────────────┐
│                  圖靈機模型                  │
├─────────────────────────────────────────────┤
│                                             │
│    ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐     │
│    │ □ │  │ 0 │  │ 1 │  │ 1 │  │ □ │ ... │
│    └───┘  └───┘  └───┘  └───┘  └───┘     │
│      ↑                                      │
│   讀寫頭                                      │
│                                             │
│  狀態：q0                                    │
│  轉移函式：δ(q0, 0) = (q1, 1, R)           │
│                                             │
└─────────────────────────────────────────────┘
```

圖靈機由以下部分組成：
- 一條無限長的紙帶，被分割成格子
- 一個讀寫頭，可以在紙帶上移動
- 一組有限的狀態
- 一個轉移函式，定義在每個狀態和每個符號下的行為

Turing 的天才之處在於，他證明了這個簡單的機器可以模擬任何計算過程。整數加法、乘法、因數分解——圖靈機都能完成。

### 1.5 Church-Turing 論題

1936 年至 1937 年間，一個重要的發現震驚了數學界：Church 的 λ 演算和 Turing 的圖靈機是等價的！

這意味著：
- 任何可以用 λ 演算計算的函式，也可以用圖靈機計算
- 任何可以用圖靈機計算的函式，也可以用 λ 演算表示

Church-Turing 論題（現在通常這樣稱呼）聲稱：

> **Church-Turing 論題**：可直覺計算的函式 = 可 λ 定義的函式 = 可圖靈機計算的函式

這個論題不是定理——它是一個關於「直覺可計算性」的哲學聲明。但它已經成為計算理論的基石。

### 1.6 Gödel 的疑惑

值得一提的是，Kurt Gödel 最初對 Church 的 λ 演算持懷疑態度。在 Gödel 的一般不完全性定理證明中，他使用了「原始遞迴函式」和「一般遞迴函式」的概念。

Gödel 認為 λ 演算不夠精確，特別是關於「什麼是函式」的定義。他偏好自己提出的「一般遞迴函式」概念——這是基於遞迴方程式的定義方式。

後來，Church 和 Stephen Kleene 證明了這三種定義方式是等價的。Gödel 最終接受了這個結論，但對 λ 演算本身的哲學基礎仍有保留。

---

## 第二章：Lisp 的誕生（1950s-1960s）

### 2.1 人工智慧的夢想

1956 年夏天，在達特茅斯學院舉行了一次歷史性的會議。這次會議汇集了 John McCarthy、Marvin Minsky、Claude Shannon、Herbert Simon 等科學家。會議的主題是：「人工智慧」。

這次會議標誌著 AI 作為一門獨立學科的誕生。而 John McCarthy，正是這門新學科的命名者。

McCarthy 1927 年出生於波士頓，父親是一位發明家，母親是鋼琴家。他從小就展現出對數學和邏輯的天賦。在加州理工學院獲得數學博士學位後，他來到了 MIT。

McCarthy 的願景是：創造一種能夠進行自動推理的機器。為了實現這個目標，他需要一種語言，一種能夠方便地表示符號和進行符號運算的語言。

### 2.2 符號處理的需求

當時的程式語言（如 FORTRAN）專注於數值計算。但 AI 需要處理的不是數字，而是符號：邏輯表達式、語法樹、知識表示。這些都需要一種新的抽象。

McCarthy 在 1958 年發表了論文《Recursive Functions of Symbolic Expressions and Their Computation by Machine》。這篇論文描述了一種新的程式語言的設計——Lisp。

論文中，McCarthy 展示了如何使用 λ 演算的思想來處理符號。他引入了 S-表達式（S-expression）來統一表示程式和資料：

```lisp
; S-表達式例子
; 數字
42

; 符號
foo

; 列表
(1 2 3)

; 巢狀列表
((a b) (c d))

; 程式也是資料
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))
```

McCarthy 在論文中證明，Lisp 可以用來計算任何可計算函式。事實上，他展示了 Lisp 解釋器本身可以用 Lisp 編寫——這是元程式設計的早期例子。

### 2.3 Steve Russell 與第一個 Lisp 解釋器

McCarthy 的論文最初只是理論性的。他描述了 Lisp 的語法和語義，但沒有實際實現。

然而，他的學生 Steve Russell 讀了論文後，做了一件改變歷史的事情：他實際實現了 Lisp 解釋器。

Russell 後來回憶道：

> 「我記得 McCarthy 在黑板上寫下了eval 的定義。我想，哦，這實際上不難實現。把這個函式翻譯成機器碼就行了。」

於是，在 1959 年，世界上第一個 Lisp 解釋器誕生了。當 Russell 向 McCarthy 展示這個工作成果時，McCarthy 驚訝地說：

> 「我從沒想過有人會真的這樣做。」

這個小故事揭示了一個深刻的真理：理論和實踐之間往往隔著一條鴻溝，而有時候，學生比老師更敢於實踐。

### 2.4 Lisp 的核心概念

Lisp 雖然誕生於六十多年前，但其核心概念至今仍影響深遠：

#### 2.4.1 同像性（Homoiconicity）

Lisp 的程式和資料使用相同的表示形式——S-表達式。這意味著「程式是資料，資料是程式」。

```lisp
; 這是一個列表
(1 2 3)

; 這是一個加法程式
(+ 1 2)

; 我們可以將列表當作程式執行
(eval (list '+ 1 2))  ; 返回 3

; 我們可以將程式當作列表操作
(car '(+ 1 2))  ; 返回 +
(cdr '(+ 1 2))  ; 返回 (1 2)
```

這種特性稱為「同像性」，使得 Lisp 可以輕鬆地操作和生成自己的程式碼。

#### 2.4.2 條件表達式

McCarthy 發明的條件表達式是 Lisp 的另一個創新：

```lisp
(cond 
  (p1 e1)
  (p2 e2)
  ...
  (t en))
```

這是 if-then-else 的前身。McCarthy 的天才之處在於，他意識到條件表達式可以完全用函式定義：

```lisp
(cond (p1 e1) (p2 e2) ... (t en))
= 
(if p1 e1 (if p2 e2 ... en))
```

#### 2.4.3 垃圾回收

早期的 Lisp 實現使用引用計數，但這有循環引用的問題。1960 年，MIT 的 Collins 和 Minsky 開發了第一個真正的垃圾回收器——標記-清除演算法。

這項技術後來成為幾乎所有現代程式語言的標準特性。

#### 2.4.4 閉包（Closure）

Lisp 引入了閉包的概念——攜帶其詞法環境的函式：

```lisp
(defun make-counter ()
  (let ((count 0))
    (lambda ()
      (setf count (+ count 1))
      count)))

(defvar c1 (make-counter))
(defvar c2 (make-counter))

(funcall c1)  ; 返回 1
(funcall c1)  ; 返回 2
(funcall c2)  ; 返回 1（獨立的計數器）
```

閉包是 FP 中最重要的概念之一，至今仍在無數語言中使用。

### 2.5 Lisp 的方言時代

1960 年代後，Lisp 衍生出無數方言：

| 方言 | 年份 | 發明者/機構 | 特點 |
|------|------|-------------|------|
| Lisp 1.5 | 1962 | MIT | 最早的標準版本 |
| Maclisp | 1966 | MIT | 預言機上的 Lisp |
| Interlisp | 1967 | BBN | 包含 IDE |
| Scheme | 1975 | MIT | 簡潔的 Lisp 方言 |
| Common Lisp | 1984 | 委員會 | 統一標準 |
| Clojure | 2007 | Rich Hickey | JVM 上的現代 Lisp |

每一個方言都有其特點和應用場景。但總體來說，Lisp 的影響力遠超過了它的使用人數。

### 2.6 Paul Graham 與「Greenspun 第十條規則」

2003 年，程式設計師 Paul Graham 在他的文章中寫道：

> 「任何足夠複雜的 C 或 Fortran 程式都包含一個臨時的、非正式的、拙劣的、執行緩慢的、只有部分完成的 Lisp 實現。」

這被稱為「Greenspun 第十條規則」——這是一個關於語言設計的深刻洞察。

為什麼會這樣？因為 Lisp 的抽象能力太強了。當你需要處理複雜的問題時，你會不自覺地發明某種 Lisp-like 的 DSL。

---

## 第三章：類型理論與 ML 的崛起（1970s-1980s）

### 3.1 Robin Milner 與 Edinburgh LCF

1970 年代，蘇格蘭愛丁堡大學成為函式程式設計研究的重鎮。Robin Milner 是這個領域的核心人物。

Milner（1944-2010）是英國計算機科學家，後來成為劍橋大學教授，並獲得了計算機領域的最高榮譽——圖靈獎（1996 年）。

Milner 的主要貢獻之一是發明了 ML（Meta-Language）語言。這個語言是 Edinburgh LCF（Logic for Computable Functions）專案的一部分，設計用於輔助定理證明。

### 3.2 LCF 的目標：機械化定理證明

LCF 專案的目標是建立一個可以輔助數學定理證明的系統。這個系統需要：
- 一種可以表示數學陳述的語言
- 一種可以進行推理的機制
- 一種可以驗證證明正確性的方法

Milner 意識到，一個強大的型別系統對於這樣的系統至關重要。於是，他在設計 ML 時引入了革命性的 **Hindley-Milner 型別推論**。

### 3.3 Hindley-Milner 型別系統

這個型別系統是 Donald Hindley（1969）和 Robin Milner（1978）獨立發現的。它的核心思想是：**程式員不需要標註每一個型別，編譯器可以自動推斷。**

讓我們看看這個系統有多強大：

```ml
(* 簡單的類型推論 *)
let id x = x;;          (* 'a -> 'a，任意類型的恆等函式 *)

(* 多態函式 *)
let rec length l =      (* 'a list -> int *)
  match l with
  | [] -> 0
  | _::t -> 1 + length t;;

(* 自動推斷泛型 *)
let fst (a, b) = a;;    (* ('a * 'b) -> 'a *)

(* 高階函式 *)
let rec map f l =       (* ('a -> 'b) -> 'a list -> 'b list *)
  match l with
  | [] -> []
  | h::t -> f h :: map f t;;
```

Hindley-Milner 系統的核心是**結構化型別推論**：

```ml
(* 推論過程 *)
(* 輸入：let add x y = x + y *)
(* 步驟1：假設 x : α, y : β, result : γ *)
(* 步驟2：+ 運算子要求 α = int, β = int, γ = int *)
(* 步驟3：推斷 add : int -> int -> int *)
```

這個系統的優雅之處在於：它是**完整且sound的**——所有可推斷的型別都是正確的，且所有正確的型別都可以被推斷（在一個足夠強的系統中）。

### 3.4 ML 的其他創新

ML 還帶來了其他重要的概念：

#### 3.4.1 模式匹配

```ml
(* 模式匹配：表達式的強大解構能力 *)
let rec fib n = match n with
  | 0 -> 0
  | 1 -> 1
  | _ -> fib (n-1) + fib (n-2);;

(* 代數資料類型 *)
type tree = 
  | Leaf of int
  | Node of tree * tree;;

let rec sum = function
  | Leaf n -> n
  | Node (l, r) -> sum l + sum r;;
```

#### 3.4.2 異常處理

```ml
exception Not_found;;

let rec find pred lst = match lst with
  | [] -> raise Not_found
  | x::_ when pred x -> x
  | _::t -> find pred t;;

(* 使用 *)
try find (fun x -> x > 10) [1;2;3] with
  | Not_found -> 0;;
```

#### 3.4.3 模組系統

ML 的模組系統是至今最複雜的之一：

```ml
(* 簽名 *)
module type STACK = sig
  type 'a t
  val empty : 'a t
  val push : 'a -> 'a t -> 'a t
  val pop : 'a t -> 'a * 'a t
  val is_empty : 'a t -> bool
end;;

(* 結構 *)
module ListStack : STACK = struct
  type 'a t = 'a list
  let empty = []
  let push x s = x::s
  let pop = function
    | [] -> failwith "empty"
    | x::s -> (x, s)
  let is_empty = function [] -> true | _ -> false
end;;
```

### 3.5 ML 的後裔

ML 的設計影響深遠，催生了多個重要的語言：

| 語言 | 年份 | 機構/作者 | 特點 |
|------|------|----------|------|
| Standard ML | 1983 | LCF 團隊 | 學術標準 |
| OCaml | 1996 | INRIA | 物件+函式 |
| F# | 2005 | Microsoft | .NET 平台 |
| Elm | 2012 | Evan Czaplicki | 前端 FRP |
| Rust | 2015 | Mozilla | 系統+安全 |

---

## 第四章：純函式與惰性求值（1980s-1990s）

### 4.1 David Turner 與 SASL、Kiev、Kashmir

在英國，David Turner 是另一位重要的函式程式設計先驅。他在 1970 年代和 1980 年代設計了一系列純函式語言：

- **SASL**（1972）：St. Andrews Static Language
- **Kiev**（1980）：早期惰性求值語言
- **Miranda**（1985）：純函式語言的先驅

Miranda 的設計極為優雅，它展示了「純函式」程式設計的威力：

```miranda
-- Miranda 是純函式的：沒有副作用
-- 每個函式都是數學意義上的函式

-- 列表是語言的核心結構
factorial n = product [1..n]

-- 列表推導（後來啟發了 Python）
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

### 4.2 惰性求值的美學

惰性求值（Lazy Evaluation）是 Turner 的核心貢獻。其思想是：**只在需要結果時才計算表達式。**

這帶來了驚人的能力：

```miranda
-- 定義一個無限列表
naturals = [1..]  -- 1, 2, 3, 4, ...

-- 但我們可以取它的前10個元素
take 10 naturals  -- [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

-- 質數篩選
primes = sieve [2..]
  where sieve (p:xs) = p : sieve [n | n <- xs; n mod p /= 0]

take 20 primes  -- [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, ...]
```

惰性求值帶來的概念：
- ** thunk**：延遲計算的表示
- **記憶化**：每個 thunk 只計算一次
- **流式處理**：處理無限資料結構

### 4.3 Haskell 的誕生

1987 年，一群研究者決定在 Miranda 的基礎上創建一個新的標準函式語言。這個語言以 Haskell Brooks Curry 命名——他是數理邏輯的先驅。

1990 年，Haskell 1.0 規範發布。此後，這個語言經歷了多次修訂：

| 版本 | 年份 | 主要變化 |
|------|------|---------|
| Haskell 1.0 | 1990 | 初始版本 |
| Haskell 98 | 1999 | 第一個穩定標準 |
| Haskell 2010 | 2010 | 最新 ISO 標準 |
| GHC 擴展 | 至今 | 豐富的語言擴展 |

### 4.4 Haskell 的核心特性

Haskell 是迄今為止最純粹的函式語言之一：

```haskell
-- Haskell 是純函式的：沒有副作用
-- 這段程式碼總是返回相同的結果
add :: Int -> Int -> Int
add x y = x + y

-- 惰性求值：只在需要時計算
fibs :: [Integer]
fibs = 0 : 1 : zipWith (+) fibs (tail fibs)

-- 無限列表的優雅處理
take 10 fibs  -- [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

-- 列表推導
pythagorean :: [(Int, Int, Int)]
pythagorean = [(a,b,c) | c <- [1..], 
                          a <- [1..c], 
                          b <- [a..c],
                          a*a + b*b == c*c]
```

### 4.5 Monads：處理副作用的革命

Haskell 最重要的創新是 **Monads**——這是一種用純函式處理副作用的抽象。

在純函式語言中，如何處理 I/O、狀態、異常等副作用？Haskell 的答案是：將副作用封裝在 Monad 中。

```haskell
-- IO Monad：用於處理輸入輸出
main :: IO ()
main = do
  putStrLn "What is your name?"
  name <- getLine
  putStrLn $ "Hello, " ++ name ++ "!"

-- Maybe Monad：處理可能失敗的操作
safeDiv :: Int -> Int -> Maybe Int
safeDiv _ 0 = Nothing
safeDiv x y = Just (x `div` y)

-- 使用 do 語法糖
divide :: Int -> Int -> Maybe Int
divide x y = do
  a <- safeDiv x y
  b <- safeDiv a 2
  return b

-- State Monad：處理有狀態的計算
type Stack = [Int]

pop :: State Stack Int
pop = state $ (x:xs) -> (x, xs)

push :: Int -> State Stack ()
push x = state $ xs -> ((), x:xs)
```

Monads 的數學定義（對程式員來說）：

```haskell
class Monad m where
  (>>=)  :: m a -> (a -> m b) -> m b    -- bind
  return :: a -> m a                      -- unit
  (>>)   :: m a -> m b -> m b            -- sequence

-- 三個定律：
-- 1. return a >>= f  ≡  f a
-- 2. m >>= return   ≡  m
-- 3. (m >>= f) >>= g  ≡  m >>= (\x -> f x >>= g)
```

Monads 的影響極為深遠。這個概念後來出現在：
- JavaScript 的 Promise
- Python 的 list comprehension 和 asyncio
- Scala 的 for comprehension
- Rust 的 Result 和 Option

---

## 第五章：主流語言的函式化（2000s-2010s）

### 5.1 函式概念的普及

經過半個世紀的發展，函式程式設計的概念終於開始滲透到主流語言中。這一趨勢在 2000 年代加速，2010 年代達到高峰。

### 5.2 C# 與 LINQ

2007 年，微軟在 .NET 3.5 中引入了 LINQ（Language Integrated Query）。這是函式程式設計進入主流企業語言的里程碑。

```csharp
// LINQ 使用函式風格的查詢
var result = orders
    .Where(o => o.Total > 1000)          // filter
    .OrderBy(o => o.Date)               // sort
    .Select(o => new { o.Id, o.Total }); // map

// 查詢語法（更接近 SQL）
var result = from o in orders
             where o.Total > 1000
             orderby o.Date
             select new { o.Id, o.Total };

// 延遲執行
var query = orders.Where(o => o.Total > 1000);
orders.Add(new Order { Total = 2000 });
foreach (var o in query)  // 這裡才真正執行
    Console.WriteLine(o);

// 立即執行
var list = orders.Where(o => o.Total > 1000).ToList();
```

LINQ 的設計直接受到了 Haskell 的列表推導和查詢語法啟發。

### 5.3 Java 8 與 Stream API

2014 年，Java 8 發布。這是 Java 自 1995 年诞生以来最大的一次更新，而核心改變就是函式支援。

```java
// Stream API：處理集合的函式風格
List<String> result = orders.stream()
    .filter(o -> o.getTotal() > 1000)    // 過濾
    .sorted(Comparator.comparing(Order::getDate))  // 排序
    .map(Order::getId)                   // 轉換
    .collect(Collectors.toList());       // 收集結果

// 方法參照
List<String> names = users.stream()
    .map(User::getName)                  // 方法參照
    .collect(Collectors.toList());

// 平行流（自動並行化）
double average = orders.parallelStream()
    .mapToDouble(Order::getTotal)
    .average()
    .orElse(0.0);

// reduce：聚合操作
int sum = numbers.stream()
    .reduce(0, Integer::sum);

//  Optional：處理可能為空的值
String name = user
    .map(User::getAddress)
    .map(Address::getCity)
    .orElse("Unknown");
```

### 5.4 Python 的函式特性

Python 雖然不是純函式語言，但早早引入了多種函式概念：

```python
# Lambda 表達式
square = lambda x: x ** 2
add = lambda x, y: x + y

# map, filter, reduce
numbers = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
total = reduce(lambda x, y: x + y, numbers)

# 列表推導（受 Haskell 啟發）
squares = [x ** 2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]

# 生成器（惰性求值）
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fibs = fibonacci()
first_10 = [next(fibs) for _ in range(10)]

# 裝飾器（高階函式）
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time() - start}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

### 5.5 JavaScript 的函式復興

JavaScript 從一開始就內建函式特性，但 ES6（2015）帶來了革命性的改變：

```javascript
// 箭頭函式
const square = x => x ** 2;
const add = (x, y) => x + y;

// 解構賦值
const { name, age } = user;
const [first, ...rest] = array;

// 展開運算子
const combined = [...arr1, ...arr2];
const merged = { ...obj1, ...obj2 };

//  async/await（Promise 的語法糖）
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// 函式組成
const compose = (...fns) => x => fns.reduceRight((v, f) => f(v), x);
const pipe = (...fns) => x => fns.reduce((v, f) => f(v), x);

const processData = pipe(
    filter(x => x > 0),
    map(x => x * 2),
    reduce((a, b) => a + b, 0)
);
```

### 5.6 React 與函式元件

2013 年，Facebook 開源了 React。這個庫將函式程式設計的概念帶入了前端開發：

```jsx
// 函式元件（無狀態）
function UserProfile({ user, onLogout }) {
    return (
        <div className="profile">
            <h1>{user.name}</h1>
            <img src={user.avatar} alt={user.name} />
            <button onClick={onLogout}>登出</button>
        </div>
    );
}

// Hooks：狀態的函式式管理
function Counter() {
    const [count, setCount] = useState(0);
    
    const increment = useCallback(() => {
        setCount(c => c + 1);
    }, []);
    
    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={increment}>+1</button>
        </div>
    );
}

// useMemo 和 useCallback：效能優化
const sortedList = useMemo(
    () => items.slice().sort(),
    [items]
);

// Context：純函式依賴注入
const ThemeContext = createContext('light');

function App() {
    return (
        <ThemeContext.Provider value="dark">
            <Toolbar />
        </ThemeContext.Provider>
    );
}

function Toolbar() {
    const theme = useContext(ThemeContext);
    return <div className={theme}>...</div>;
}
```

---

## 第六章：Rust 與現代系統程式設計（2010s-2020s）

### 6.1 Rust 的誕生

2006 年，Graydon Hoare 開始開發 Rust。這是一個旨在提供 C++ 的效能和控制力的語言，同時確保記憶體安全。

Rust 的設計深受函式程式設計影響：

```rust
// 模式匹配
match value {
    Some(x) => println!("{}", x),
    None => println!("nothing"),
}

// 不可變所有權（預設）
let x = 5;
let y = x;  // x 被移動到 y
// println!("{}", x);  // 錯誤！x 已不再有效

// 借用檢查器
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// 閉包
let add = |x, y| x + y;
let numbers = vec![1, 2, 3, 4, 5];
let sum: i32 = numbers.iter().map(|x| x * 2).sum();

// Option 和 Result
fn divide(a: f64, b: f64) -> Option<f64> {
    if b == 0.0 { None } else { Some(a / b) }
}

fn read_file(path: &str) -> Result<String, io::Error> {
    fs::read_to_string(path)
}
```

### 6.2 Iterator 與函式 combinator

Rust 的 Iterator 是函式程式設計的完美體現：

```rust
// 鏈式呼叫
let result: i32 = (1..1000)
    .filter(|x| x % 3 == 0 || x % 5 == 0)
    .map(|x| x * x)
    .sum();

// 迭代器是惰性的
let iter = (1..1000).map(|x| x * x);  // 什麼都沒計算
let first_five: Vec<_> = iter.take(5).collect();  // 這裡才計算

// 自定義迭代器
struct Counter {
    count: u32,
}

impl Iterator for Counter {
    type Item = u32;
    
    fn next(&mut self) -> Option<Self::Item> {
        self.count += 1;
        Some(self.count)
    }
}
```

---

## 第七章：Lambda Calculus 在現代 AI 中的重生（2010s-2020s）

### 7.1 深度學習的函式視角

2012 年，AlexNet 在 ImageNet 競賽中取得突破性成果，標誌著深度學習時代的來臨。從那時起，我們可以從一個獨特的角度看待深度學習：

**神經網路本質上是一個巨大的複合函式。**

```python
# 深度學習模型就是函式組合
# 輸入 -> 線性層 -> 激活函式 -> 線性層 -> 激活函式 -> ... -> 輸出

class NeuralNetwork(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(784, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        return self.layers(x)

# 這就是一個巨大的函式
# f(x) = W3 * ReLU(W2 * ReLU(W1 * x + b1) + b2) + b3
```

### 7.2 Transformer 架構與注意力機制

2017 年，Google 發表了革命性的論文《Attention Is All You Need》。這個 Transformer 架構現在是幾乎所有大型語言模型的基礎。

讓我們從函式程式設計的角度理解 Transformer：

```python
# Transformer 的核心：注意力機制
# 這本質上是一個高階函式

def attention(query, keys, values):
    """
    注意力機制的函式視角：
    - query: 查詢函式（我們想要查什麼）
    - keys: 鍵（每個位置的標識）
    - values: 值（每個位置的內容）
    
    輸出是 values 的加权和，權重由 query 和 keys 的相似度決定
    """
    # 計算相似度（點積）
    scores = torch.matmul(query, keys.transpose(-2, -1))
    
    # 標準化
    scores = scores / math.sqrt(keys.size(-1))
    
    # Softmax 權重
    weights = F.softmax(scores, dim=-1)
    
    # 加權求和
    return torch.matmul(weights, values)

# 多頭注意力：並行的多個注意力函式
class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # 四個線性變換（函式）
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # 線性變換（函式應用）
        Q = self.W_q(query)
        K = self.W_k(key)
        V = self.W_v(value)
        
        # 分頭（函式的分割）
        Q = Q.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        K = K.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        V = V.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
        
        # 並行注意力計算（map）
        x, _ = attention(Q, K, V)
        
        # 合併頭（函式的合併）
        x = x.transpose(1, 2).contiguous().view(batch_size, -1, self.num_heads * self.d_k)
        
        return self.W_o(x)
```

### 7.3 函式 API 與模型建構

現代深度學習框架提供了函式式的模型建構 API：

```python
# PyTorch 的函式式 API
model = nn.Sequential(
    nn.Conv2d(3, 64, 3, padding=1),
    nn.ReLU(),
    nn.MaxPool2d(2, 2),
    nn.Conv2d(64, 128, 3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((1, 1)),
    nn.Flatten(),
    nn.Linear(128, 10)
)

# Keras Functional API
inputs = tf.keras.Input(shape=(28, 28, 1))
x = layers.Conv2D(32, 3, activation='relu')(inputs)
x = layers.MaxPooling2D(2)(x)
x = layers.GlobalAveragePooling2D()(x)
outputs = layers.Dense(10)(x)
model = tf.keras.Model(inputs, outputs)

# JAX：純函式_transform
@jax.jit
@jax.grad
def loss(params, x, y):
    pred = model(params, x)
    return cross_entropy_loss(pred, y)
```

### 7.4 AI Agent 與函式呼叫

2023 年後，AI Agent 成為熱門話題。其核心思想是：讓 AI 模型呼叫外部工具和函式。這正是 Lambda Calculus「應用」概念的現代詮釋。

```python
# AI Agent 呼叫外部函式
class Agent:
    def __init__(self, llm, tools):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
    
    async def execute(self, query: str):
        # LLM 規劃並選擇工具
        plan = await self.llm.plan(query, available_tools=list(self.tools.keys()))
        
        results = []
        for step in plan:
            tool_name = step["tool"]
            params = step["parameters"]
            
            # 函式應用
            if tool_name in self.tools:
                result = await self.tools[tool_name].call(**params)
                results.append(result)
            else:
                raise ValueError(f"Unknown tool: {tool_name}")
        
        # 最終響應
        return await self.llm.synthesize(query, results)

# 工具定義
@tool
def calculate_route(origin: str, destination: str) -> dict:
    """計算兩地之間的路線"""
    return {"distance": "200km", "duration": "2h30m", "route": [...]}

@tool  
def search_database(query: str, filters: dict = None) -> list:
    """搜尋資料庫"""
    return db.search(query, filters)
```

### 7.5 向量化與函式抽象

在深度學習中，向量化是將函式應用於整個資料結構的過程：

```python
import numpy as np

# 傳統方式：迴圈
def add_matrices_slow(A, B):
    C = np.zeros_like(A)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i, j] = A[i, j] + B[i, j]
    return C

# 向量化方式：函式應用於整個結構
def add_matrices_fast(A, B):
    return A + B  # NumPy 的廣播機制

# 更複雜的例子
def normalize(images):
    # 將 normalize 函式應用於所有圖片
    return (images - images.mean(axis=(1, 2), keepdims=True)) / images.std(axis=(1, 2), keepdims=True)
```

---

## 第八章：結論與展望

### 8.1 從理論到實踐的旅程

從 1936 年 Church 提出 λ 演算，到 2026 年的今天，我們走過了漫長的旅程。

| 年份 | 里程碑 |
|------|--------|
| 1936 | λ 演算和圖靈機誕生 |
| 1958 | Lisp 的誕生 |
| 1978 | Hindley-Milner 型別推論 |
| 1985 | Miranda 純函式語言 |
| 1990 | Haskell 規範發布 |
| 2007 | LINQ 進入 C# |
| 2012 | AlexNet 開啟深度學習時代 |
| 2014 | Java 8 引入 Stream API |
| 2017 | Transformer 架構誕生 |
| 2023-26 | AI Agent 的興起 |

### 8.2 永恆的主題

在這九十年裡，核心概念幾乎沒有改變：

- **抽象**：用函式封裝計算
- **組合**：用小構件建構大系統
- **求值**：何時以及如何計算表達式
- **型別**：如何確保計算的正確性

這些主題在每一代新技術中都煥發新生。

### 8.3 未來的方向

- **AI 程式設計**：AI 正在學習如何撰寫和理解函式
- **形式化驗證**：借助 AI 證明程式的正確性
- **新範式**：量子計算、機率程式設計等新範式正在興起

Lambda Calculus 告訴我們：複雜的計算可以歸約為少數簡單的規則——抽象、應用、替換。這些規則不僅是數學真理，更是計算思維的精髓。

在這個 AI 迅速發展的時代，讓我們牢記這些基本概念。因為無論技術如何變遷，抽象和組合的威力永遠不會過時。

---

## 延伸閱讀

- [Church 1936 Lambda Calculus](https://www.google.com/search?q=Church+Lambda+Calculus+1936)
- [McCarthy 1960 Lisp](https://www.google.com/search?q=McCarthy+Lisp+1960+Recursive+Functions)
- [Hudak 1989 Functional Programming](https://www.google.com/search?q=Hudak+Functional+Programming+languages)
- [Vaswani 2017 Attention Is All You Need](https://www.google.com/search?q=Attention+Is+All+You+Need+Transformer)

---

*本期歷史回顧到此結束。下期我們將回顧另一個影響深遠的主題，敬請期待。*
