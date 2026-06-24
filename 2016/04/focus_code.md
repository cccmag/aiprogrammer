# 附加：函數式程式實作

## 程式碼範例說明

本期的主題是函數式程式設計，我們特別準備了多個語言的範例程式，展示函數式程式設計的核心概念。

## 目錄結構

```
_code/
├── haskell/
│   ├── lambda.hs        # Lambda Calculus 解釋器
│   ├── higher_order.hs  # 高階函式範例
│   └── monad.hs         # Monad 基本概念
├── clojure/
│   ├── core.clj         # Clojure 基礎
│   ├── sequences.clj    # 序列抽象
│   └── agents.clj       # Agent 並發模型
├── scala/
│   ├── HigherOrder.scala  # 高階函式
│   ├── PatternMatch.scala # 模式匹配
│   └── Actors.scala       # Actor 模型
├── python/
│   ├── functional.py     # Python 函式式特性
│   ├── higher_order.py   # 高階函式
│   ├── closures.py      # 閉包
│   └── memoization.py   # 記憶化
└── test.sh              # 測試腳本
```

## Haskell 範例

### Lambda Calculus 解釋器

```haskell
-- lambda.hs - 簡化的 Lambda Calculus 解釋器

data Expr
    = Var String
    | Lam String Expr
    | App Expr Expr
    deriving (Show, Eq)

-- 自由變數
freeVars :: Expr -> [String]
freeVars (Var x) = [x]
freeVars (Lam x e) = filter (/= x) (freeVars e)
freeVars (App e1 e2) = freeVars e1 ++ freeVars e2

-- 替換（beta 歸約的關鍵）
subst :: String -> Expr -> Expr -> Expr
subst x replacement (Var y)
    | x == y    = replacement
    | otherwise = Var y
subst x replacement (Lam y e)
    | x == y    = Lam y e
    | y `elem` freeVars replacement = Lam y e  -- 避免捕捉
    | otherwise = Lam y (subst x replacement e)
subst x replacement (App e1 e2) = App (subst x replacement e1)
                                          (subst x replacement e2)

-- 單步歸約（call-by-name）
step :: Expr -> Maybe Expr
step (App (Lam x e1) e2) = Just (subst x e2 e1)
step (App e1 e2) = case step e1 of
    Just e1' -> Just (App e1' e2)
    Nothing -> case step e2 of
        Just e2' -> Just (App e1 e2')
        Nothing -> Nothing
step (Lam x e) = case step e of
    Just e' -> Just (Lam x e')
    Nothing -> Nothing
step _ = Nothing

-- 完全歸約
reduce :: Expr -> Expr
reduce e = case step e of
    Just e' -> reduce e'
    Nothing -> e

-- 測試
-- (\x. \y. x) (\z. z)  應該歸約為 \y. \z. z
test :: Expr
test = App (Lam "x" (Lam "y" (Var "x"))) (Lam "z" (Var "z"))
```

### 高階函式範例

```haskell
-- higher_order.hs - 高階函式示範

-- Compose：組合兩個函式
compose :: (b -> c) -> (a -> b) -> (a -> c)
compose f g x = f (g x)

-- Curry 和 Uncurry
curry' :: ((a, b) -> c) -> (a -> b -> c)
curry' f x y = f (x, y)

uncurry' :: (a -> b -> c) -> ((a, b) -> c)
uncurry' f (x, y) = f x y

-- Flip：交換參數順序
flip' :: (a -> b -> c) -> (b -> a -> c)
flip' f y x = f x y

-- 永續資料結構：列表
data PersistentList a = Nil | Cons a (PersistentList a)
    deriving (Show, Eq)

push :: a -> PersistentList a -> PersistentList a
push x xs = Cons x xs

pop :: PersistentList a -> Maybe (a, PersistentList a)
pop Nil = Nothing
pop (Cons x xs) = Just (x, xs)

-- Tree 範例
data Tree a = Empty | Node a (Tree a) (Tree a)
    deriving (Show, Eq)

mapTree :: (a -> b) -> Tree a -> Tree b
mapTree _ Empty = Empty
mapTree f (Node x left right) =
    Node (f x) (mapTree f left) (mapTree f right)

foldTree :: (a -> b -> b -> b) -> b -> Tree a -> b
foldTree _ z Empty = z
foldTree f z (Node x left right) =
    f x (foldTree f z left) (foldTree f z right)
```

## Clojure 範例

### 序列抽象

```clojure
;; sequences.clj - Clojure 序列抽象示範

;; 序列函式 vs Java Collection 方法
;; Clojure 的序列抽象是通用的

;; 使用序列函式處理多種資料類型
(defn process [coll]
  (->> coll
       (filter odd?)          ; 奇數
       (map inc)              ; 加 1
       (reduce +)))           ; 總和

(process [1 2 3 4 5])         ; => 9
(process '(1 2 3 4 5))        ; => 9
(process #{1 2 3 4 5})        ; => 9
(process {:a 1 :b 2 :c 3})    ; => 6 (處理 values)

;; 無限序列
(defn fibonacci []
  (let [fibs (fn [a b]
               (cons a (lazy-seq (fibs b (+ a b)))))]
    (fibs 0 1)))

;; 只取需要的部分
(take 10 (fibonacci))         ; => (0 1 1 2 3 5 8 13 21 34)

;; 序列的惰性求值
(def large-sequence
  (range 1000000))

(take 10 large-sequence)      ; 不會真的產生全部元素
```

### Agent 並發模型

```clojure
;; agents.clj - Agent 並發模型

;; 建立 Agent
(def log-agent (agent []))

;; 非同步發送 action
(send log-agent conj "User login")
(send log-agent conj "User viewed page")
(send log-agent conj "User clicked button")

;; 等待並讀取狀態
(println @log-agent)

;; 錯誤處理
(def error-agent (agent 0))

;; 發生錯誤時的處理
(send error-agent (fn [state]
                     (if (> state 5)
                       (throw (Exception. "Too many errors!"))
                       (inc state))))

;; 監聽錯誤
(add-watch error-agent :error-log
           (fn [_ _ _ error]
             (println "Error:" error)))

;; STM 事務
(def account-a (ref 1000))
(def account-b (ref 1000))

;; 在事務中進行轉帳
(dosync
  (alter account-a - 100)
  (alter account-b + 100))

;; 驗證結果
@account-a  ; => 900
@account-b  ; => 1100
```

## Python 範例

### 函數式程式設計工具

```python
# functional.py - Python 函數式工具

from functools import reduce, lru_cache, partial
from operator import add, mul
from typing import Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')

# 自訂 compose（Python 3.9+可直接使用 functools.reduce）
def compose(*functions: Callable) -> Callable:
    """由右到左組合函式"""
    def inner(x):
        result = x
        for f in reversed(functions):
            result = f(result)
        return result
    return inner

# Pipeline 運算子（使用 dataclass 模擬）
from dataclasses import dataclass

@dataclass
class Pipe:
    value: any

    def then(self, f):
        if callable(f):
            return Pipe(f(self.value))
        return Pipe(f)

    def __radd__(self, other):
        return Pipe(other).then(self.value)

# Currying
def curried_map(f: Callable[[T], U]) -> Callable[[list], list]:
    return lambda lst: list(map(f, lst))

def curried_filter(pred: Callable[[T], bool]) -> Callable[[list], list]:
    return lambda lst: list(filter(pred, lst))

# 範例
square = curried_map(lambda x: x ** 2)
evens = curried_filter(lambda x: x % 2 == 0)

result = square(evens(range(10)))
print(result)  # [0, 16, 36, 64]
```

### 閉包與記憶化

```python
# closures.py - 閉包與記憶化

def make_memoize():
    """工廠函式：創建帶有獨立 cache 的 memoize"""
    cache = {}

    def memoize(func):
        def wrapper(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        wrapper.cache = cache  # 暴露 cache 供檢查
        return wrapper

    return memoize

# 使用工廠函式
memoize = make_memoize()

@memoize
def fibonacci(n):
    """具有封閉 cache 的記憶化費伯那契"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# 測試
print(fibonacci(100))  # 快速返回

# 閉包工廠：參數化行為
def make_validator(pattern, error_msg):
    import re
    compiled = re.compile(pattern)

    def validate(value):
        if not compiled.match(str(value)):
            raise ValueError(error_msg)
        return value

    return validate

# 建立具體驗證器
validate_email = make_validator(
    r'^[\w\.-]+@[\w\.-]+\.\w+$',
    'Invalid email address'
)
validate_phone = make_validator(
    r'^\d{3}-\d{4}$',
    'Invalid phone format (XXX-XXXX)'
)

# 測試
print(validate_email("user@example.com"))  # user@example.com
```

## Scala 範例

### 高階函式與模式匹配

```scala
// HigherOrder.scala - Scala 高階函式

object HigherOrder extends App {

  // 高階函式：接受函式參數
  def applyTwice(f: Int => Int, x: Int): Int = f(f(x))

  // 匿名函式
  val double = (x: Int) => x * 2
  val inc = (x: Int) => x + 1

  println(applyTwice(double, 5))  // 20
  println(applyTwice(inc, 5))     // 7

  // 柯里化（Currying）
  def curriedSum(x: Int)(y: Int): Int = x + y
  val addFive = curriedSum(5) _
  println(addFive(3))  // 8

  // 部分應用
  def log(level: String, message: String): Unit =
    println(s"[$level] $message")

  val errorLog = log("ERROR", _: String)
  errorLog("Something went wrong")

  //  collection 高階函式
  val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

  // map, filter, reduce
  val result = numbers
    .filter(_ % 2 == 0)       // 偶數
    .map(x => x * x)          // 平方
    .reduce(_ + _)            // 總和

  println(result)  // 220

  // 模式匹配
  def describe(x: Any): String = x match {
    case 1 => "one"
    case s: String => s"String of length ${s.length}"
    case List(_, _*) => "a list"
    case m: Map[_, _] => s"map with ${m.size} entries"
    case _ => "something else"
  }

  println(describe(42))
  println(describe("hello"))
  println(describe(List(1, 2, 3)))
}
```

### Actor 模型

```scala
// Actors.scala - Akka Actor 示範

import akka.actor._

case class Greet(name: String)
case class GreetBack(message: String)

class HelloActor extends Actor {
  def receive = {
    case Greet(name) =>
      println(s"Hello, $name!")
      sender() ! GreetBack(s"Hello, $name!")

    case GreetBack(message) =>
      println(s"Received: $message")

    case _ =>
      println("Unknown message")
  }
}

object ActorDemo extends App {
  // 建立 Actor 系統
  val system = ActorSystem("HelloSystem")

  // 建立 Actor
  val helloActor = system.actorOf(Props[HelloActor], name = "hello")

  // 發送訊息
  helloActor ! Greet("World")
  helloActor ! Greet("Scala")

  // 等待處理，然後關閉系統
  Thread.sleep(1000)
  system.terminate()
}
```

## 執行測試

請參考 `test.sh` 來執行各語言的範例。

```bash
# 執行所有測試
cd _code
./test.sh

# 單獨執行 Python 範例
python3 python/functional.py
python3 python/closures.py

# 執行 Haskell 範例（需要 GHC）
ghc haskell/lambda.hs && ./lambda
```

## 延伸閱讀

- [Google 搜尋：functional programming basics](https://www.google.com/search?q=functional+programming+basics)
- [Google 搜尋：Haskell tutorial](https://www.google.com/search?q=Haskell+tutorial)
- [Google 搜尋：Clojure getting started](https://www.google.com/search?q=Clojure+getting+started)
- [Google 搜尋：Scala functional programming](https://www.google.com/search?q=Scala+functional+programming)
- [Google 搜尋：RxJS tutorial](https://www.google.com/search?q=RxJS+tutorial)