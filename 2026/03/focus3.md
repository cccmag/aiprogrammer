# 類型理論與 ML：Hindley-Milner 的突破（1970s-1980s）

## Edinburgh LCF 專案

1970 年代，蘇格蘭愛丁堡大學成為函式程式設計研究的重鎮。Robin Milner 是這個領域的核心人物。

Robin Milner（1944-2010）是英國計算機科學家，後來成為劍橋大學教授，並獲得了計算機領域的最高榮譽——圖靈獎（1996 年）。他的獲獎理由是：

> 「對資訊技術的三個重要貢獻：1) ML 語言的設計 2) CCS 理論 3) 通信系統作業系統的理論基礎」

### LCF 的目標：機械化定理證明

LCF 專案的目標是建立一個可以輔助數學定理證明的系統。這個系統需要：

```
┌─────────────────────────────────────────────┐
│           Edinburgh LCF 系統                │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────┐   ┌─────────────┐         │
│  │  邏輯核心    │   │  證明引擎   │         │
│  │  (Inference) │◄──│  (Tactics) │         │
│  └──────┬──────┘   └─────────────┘         │
│         │                                    │
│         ▼                                    │
│  ┌─────────────┐   ┌─────────────┐         │
│  │  形式語義    │   │  策略語言   │         │
│  │  (Semantics)│   │ (Strategy)  │         │
│  └─────────────┘   └─────────────┘         │
│                                             │
└─────────────────────────────────────────────┘
```

LCF 的設計哲學是：**所有證明必須由邏輯核心認可**。這確保了系統的可靠性——即使證明引擎有 bug，也無法產生錯誤的定理。

### 為什麼需要強類型系統？

在這樣一個系統中，強類型系統至關重要：

1. **防止無意義的操作**：如 `true + 1`
2. **捕捉常見錯誤**：如類型不匹配的函式調用
3. **文檔作用**：類型是程式的規格說明

Milner 意識到，一個好的類型系統不應該強迫程式員處處標註類型。於是，他發明了 **Hindley-Milner 型別推論**。

---

## Hindley-Milner 型別系統

這個型別系統是 Donald Hindley（1969）和 Robin Milner（1978）獨立發現的。它的核心思想是：**程式員不需要標註每一個類型，編譯器可以自動推斷。**

### 基本類型

```ml
(* 基本類型 *)
42          : int
3.14        : float
true        : bool
"hello"     : string

(* 函式類型 *)
fun x -> x  : 'a -> 'a
(* 'a 是類型變數，表示「任意類型」 *)
```

### 簡單的類型推論

讓我們看看這個系統有多強大：

```ml
(* 恆等函式：編譯器自動推斷為 'a -> 'a *)
let id x = x

(* 多態函式：自動推斷泛型 *)
let rec length l = 
  match l with
  | [] -> 0
  | _::t -> 1 + length t
(* length : 'a list -> int *)

(* 自動推斷泛型 *)
let fst (a, b) = a
(* fst : ('a * 'b) -> 'a *)

(* 推斷過程 *)
(* 
   let id x = x
   1. 假設 x : α
   2. 返回 x，所以結果類型是 α
   3. 推斷 id : α -> α
   4. 由於 α 是變數，id 是多態的
*)
```

### 高階函式

```ml
(* 高階函式：接收函式作為參數 *)
let rec map f l = 
  match l with
  | [] -> []
  | h::t -> f h :: map f t
(* map : ('a -> 'b) -> 'a list -> 'b list *)

(* 閉包：捕獲環境 *)
let makeadder n = 
  let f x = x + n in
  f
(* makeadder : int -> (int -> int) *)

(* 組合 *)
let compose f g = 
  fun x -> f (g x)
(* compose : ('a -> 'b) -> ('c -> 'a) -> 'c -> 'b *)
```

### 類型推論的數學

Hindley-Milner 推論的核心是**統一（Unification）**演算法：

```ml
(* 統一問題 *)
(* 如果我們知道：*)
(*   id x : α *)
(*   id : β -> γ *)
(* 那麼：α = β 且 γ = α *)

(* 統一演算法 *)
unify(α, β) = 
  if α = β then ok
  if α 是類型變數 then 替換 α 為 β
  if β 是類型變數 then 替換 β 為 α
  if α = (α1 -> α2) 且 β = (β1 -> β2)
     then unify(α1, β1); unify(α2, β2)
  else error
```

### 推論過程示例

```ml
(* 完整推論示例 *)
let rec fold f acc l = 
  match l with
  | [] -> acc
  | h::t -> fold f (f acc h) t

(* 步驟 1: 初始假設 *)
(* fold : α -> β -> γ -> δ *)
(* f : ??? *)
(* acc : ??? *)
(* l : ??? *)

(* 步驟 2: 分析 match 表達式 *)
(* l 的類型是 γ list *)

(* 步驟 3: 遞迴調用 *)
(* fold f (f acc h) t *)
(* f : β -> γ -> β *)
(* acc : β *)
(* h : γ *)

(* 步驟 4: 統一 *)
(* f : β -> γ -> β *)
(* f : (δ -> ε -> δ) *)
(* 推斷 f : ('a -> 'b -> 'a) *)
(* acc : 'a *)
(* h : 'b *)
(* l : 'b list *)

(* 最終結果：*)
(* fold : ('a -> 'b -> 'a) -> 'a -> 'b list -> 'a *)
```

---

## ML 的其他創新

### 模式匹配

```ml
(* 基本模式匹配 *)
let rec fib n = match n with
  | 0 -> 0
  | 1 -> 1
  | _ -> fib (n-1) + fib (n-2)

(* 代數資料類型 *)
type tree = 
  | Leaf of int
  | Node of tree * tree

let rec sum = function
  | Leaf n -> n
  | Node (l, r) -> sum l + sum r

(* 約束模式 *)
let rec destutter = function
  | [] -> []
  | [x] -> [x]
  | x::(y::_ as rest) when x = y -> destutter rest
  | x::rest -> x :: destutter rest
```

### 異常處理

```ml
(* 定義異常 *)
exception Not_found
exception Invalid_input of string

(* 拋出異常 *)
let rec find pred lst = match lst with
  | [] -> raise Not_found
  | x::_ when pred x -> x
  | _::t -> find pred t

(* 處理異常 *)
try 
  find (fun x -> x > 10) [1;2;3]
with
  | Not_found -> 0
  | Invalid_input msg -> 
      print_endline ("Error: " ^ msg);
      -1
```

### 模組系統

ML 的模組系統是至今最複雜的之一：

```ml
(* 簽名（介面）*)
module type STACK = sig
  type 'a t
  
  val empty : 'a t
  val push : 'a -> 'a t -> 'a t
  val pop : 'a t -> 'a * 'a t
  val top : 'a t -> 'a
  val is_empty : 'a t -> bool
end

(* 結構（實現）*)
module ListStack : STACK = struct
  type 'a t = 'a list
  
  let empty = []
  let push x s = x::s
  let pop = function
    | [] -> failwith "empty"
    | x::s -> (x, s)
  let top = function
    | [] -> failwith "empty"
    | x::_ -> x
  let is_empty = function [] -> true | _ -> false
end

(* 函子（參數化模組）*)
module MakeSet (Ord : ORDERED) = struct
  type t = Ord.t
  let compare = Ord.compare
  
  let empty = []
  let add x set = ...
end
```

---

## ML 的後裔

ML 的設計影響深遠，催生了多個重要的語言：

| 語言 | 年份 | 機構/作者 | 特點 |
|------|------|----------|------|
| Standard ML | 1983 | LCF 團隊 | 學術標準 |
| OCaml | 1996 | INRIA | 物件+函式 |
| F# | 2005 | Microsoft | .NET 平台 |
| Elm | 2012 | Evan Czaplicki | 前端 FRP |
| Rust | 2015 | Mozilla | 系統+安全 |

### OCaml：學術與產業的橋樑

OCaml 是 ML 的直系後裔，結合了學術嚴謹性和實用性：

```ocaml
(* 模式匹配 *)
let rec fib = function
  | 0 -> 0
  | 1 -> 1
  | n -> fib (n - 1) + fib (n - 2)

(* 物件系統 *)
class counter = 
  object
    val mutable n = 0
    method inc = n <- n + 1
    method value = n
  end

(* 函式式並發 *)
let async_read file =
  Lwt.bind (Lwt_io.open_read file) (fun chan ->
    Lwt_io.read chan)

(*  GADT *)
type _ typ += 
  | Int : int typ
  | String : string typ
  | List : 'a typ -> 'a list typ
```

### F#：.NET 上的函式語言

F# 將 ML 帶入了 Microsoft 生態系統：

```fsharp
// 類型推論
let add x y = x + y
// add : int -> int -> int

// 記錄類型
type Person = { Name: string; Age: int }

// 序列表達式
let fibs = 
    Seq.unfold (fun (a, b) -> 
        Some(a, (b, a + b))) (0I, 1I)

// 計算表達式（Monads）
let result = async {
    let! data = http.AsyncRequest(url)
    return parse data
}
```

### Rust：ML 的精神繼承者

Rust 繼承了 ML 的許多特性，但應用於系統程式設計：

```rust
// 模式匹配
match value {
    Some(x) => println!("{}", x),
    None => println!("nothing"),
}

// 類型推論
let add = |x: i32, y: i32| -> i32 { x + y };

// 枚舉（代數類型）
enum Result<T, E> {
    Ok(T),
    Err(E),
}

// 閉包
let squares: Vec<i32> = (1..10)
    .map(|x| x * x)
    .collect();
```

---

## 為什麼這一切重要？

### 類型系統的價值

Hindley-Milner 型別系統的價值在於：

1. **安全性**：在編譯時捕捉錯誤
2. **簡潔性**：不需要處處標註類型
3. **表達力**：支援多態和泛型
4. **效率**：編譯器可以生成高效代碼

### 與現代語言的聯繫

幾乎所有現代語言都借鑒了 ML 的特性：

```
ML ──► Haskell ──► Purescript, Idris
  │
  ├─► SML ──► OCaml ──► F#, ReasonML
  │
  ├─► Rust (類型推論、模式匹配、枚舉)
  │
  └─► Swift, Kotlin (類型推論、可選類型)
```

### Haskell 的直接影響

1990 年的 Haskell 語言直接基於 ML 的類型系統，並進一步發展出了類別系統（Type Classes）：

```haskell
-- Haskell 的類別系統（基於 ML 的多態）
class Eq a where
    (==) :: a -> a -> Bool
    (/=) :: a -> a -> Bool

instance Eq Bool where
    True == True = True
    False == False = True
    _ == _ = False
```

---

## 延伸閱讀

- [Robin Milner: A Type-Based Approach to Computer Systems](https://www.google.com/search?q=Robin+Milner+type+based+approach)
- [Hindley 1969 Principal Type-Scheme](https://www.google.com/search?q=Hindley+1969+principal+type+scheme)
- [ML Standard Basis Library](https://www.google.com/search?q=Standard+ML+library)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之三。*
