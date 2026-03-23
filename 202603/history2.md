# Lisp 的誕生：從理論到實踐（1950s-1960s）

## 人工智慧的夢想

1956 年夏天，在達特茅斯學院舉行了一次歷史性的會議。這次會議汇集了 John McCarthy、Marvin Minsky、Claude Shannon、Herbert Simon 等科學家。會議的主題是：「人工智慧」。

這次會議標誌著 AI 作為一門獨立學科的誕生。而 John McCarthy，正是這門新學科的命名者。

### John McCarthy 的願景

John McCarthy（1927-2011）1927 年出生於波士頓，父親是一位發明家，母親是鋼琴家。他從小就展現出對數學和邏輯的天賦。在加州理工學院獲得數學博士學位後，他來到了 MIT。

McCarthy 的願景是：創造一種能夠進行自動推理的機器。為了實現這個目標，他需要一種語言，一種能夠方便地表示符號和進行符號運算的語言。

> 「我希望電腦能夠像人一樣進行推理，甚至比人更好。」—— John McCarthy

---

## 符號處理的需求

當時的程式語言（如 FORTRAN）專注於數值計算。但 AI 需要處理的不是數字，而是符號：

- 邏輯表達式：`(AND (OR A B) (NOT C))`
- 語法樹：`(S (NP (DT the) (NN dog)) (VP (VBD barked)))`
- 知識表示：`(ISA Canary Bird) (ISA Canary Yellow)`

這些都需要一種新的抽象——這就是 Lisp 的誕生背景。

---

## McCarthy 的論文

McCarthy 在 1958 年發表了論文《Recursive Functions of Symbolic Expressions and Their Computation by Machine》。這篇論文描述了一種新的程式語言的設計——Lisp。

論文中，McCarthy 展示了如何使用 λ 演算的思想來處理符號。他引入了 S-表達式（S-expression）來統一表示程式和資料。

### S-表達式的定義

```lisp
; S-表達式語法
; 原子（Atom）
42          ; 數字原子
foo         ; 符號原子
"string"    ; 字串原子

; 列表（List）
(1 2 3)                    ; 數字列表
(apple banana cherry)       ; 符號列表
((a b) (c d))              ; 巢狀列表
(+ 1 2)                    ; 函式調用也是列表！
```

### S-表達式的遞迴定義

```
S-表達式 ::= 原子 | ( S-表達式 . S-表達式 ) | ( S-表達式序列 )
原子     ::= 數字 | 符號 | 字串
```

---

## Steve Russell 與第一個 Lisp 解釋器

McCarthy 的論文最初只是理論性的。他描述了 Lisp 的語法和語義，但沒有實際實現。

然而，他的學生 Steve Russell 讀了論文後，做了一件改變歷史的事情：他實際實現了 Lisp 解釋器。

### 歷史性的一刻

Russell 後來回憶道：

> 「我記得 McCarthy 在黑板上寫下了 eval 的定義。我想，哦，這實際上不難實現。把這個函式翻譯成機器碼就行了。」

於是，在 1959 年，世界上第一個 Lisp 解釋器誕生了。當 Russell 向 McCarthy 展示這個工作成果時，McCarthy 驚訝地說：

> 「我從沒想過有人會真的這樣做。」

這個小故事揭示了一個深刻的真理：**理論和實踐之間往往隔著一條鴻溝，而有時候，學生比老師更敢於實踐。**

### 原始 Lisp 評估器

Russell 實現的核心是 eval 函式（大幅簡化版）：

```lisp
(defun eval (exp env)
  (cond
    ((numberp exp) exp)
    ((symbolp exp) (lookup exp env))
    ((eq (car exp) 'quote) (cadr exp))
    ((eq (car exp) 'lambda) (list 'closure (cadr exp) (caddr exp) env))
    ((eq (car exp) 'if) (if (eval (cadr exp) env)
                            (eval (caddr exp) env)
                            (eval (cadddr exp) env)))
    (t (apply (eval (car exp) env)
              (mapcar (lambda (arg) (eval arg env)) (cdr exp)))))
```

---

## Lisp 的核心概念

### 同像性（Homoiconicity）

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
(cadr '(+ 1 2)) ; 返回 1

; 程式碼即資料
(defmacro when (test &body body)
  `(if ,test (progn ,@body)))

; 執行時期生成程式碼
(eval `(let ((x 10)) (+ x ,(* 3 4))))
; 返回 22
```

這種特性稱為「同像性」，使得 Lisp 可以輕鬆地操作和生成自己的程式碼。

### 條件表達式

McCarthy 發明的條件表達式是 Lisp 的另一個創新：

```lisp
(cond 
  ((< x 0) 'negative)
  ((= x 0) 'zero)
  ((> x 0) 'positive))

; 這可以翻譯為：
(if (< x 0) 'negative
    (if (= x 0) 'zero
        'positive))
```

### 垃圾回收

早期的 Lisp 實現使用引用計數，但這有循環引用的問題。1960 年，MIT 的 Collins 和 Minsky 開發了第一個真正的垃圾回收器——標記-清除演算法：

```
┌─────────────────────────────────────────────┐
│              標記-清除垃圾回收               │
├─────────────────────────────────────────────┤
│                                             │
│  Phase 1: 標記                              │
│  ┌───┐     ┌───┐     ┌───┐                │
│  │ A │────►│ B │────►│ C │                │
│  └───┘     └───┘     └───┘                │
│    │         │         │                   │
│    ▼         ▼         ▼                   │
│  [root]  [heap]  [heap]                   │
│                                             │
│  Phase 2: 清除                             │
│  ┌───┐     ┌───┐     ┌───┐     ┌───┐     │
│  │ A │────►│ B │     │ C │     │ D │     │
│  └───┘     └───┘     └───┘     └───┘     │
│    │                                         │
│  [live]  [live]  [sweep]  [free]           │
│                                             │
└─────────────────────────────────────────────┘
```

### 閉包（Closure）

Lisp 引入了閉包的概念——攜帶其詞法環境的函式：

```lisp
; 建立一個計數器工廠
(defun make-counter ()
  (let ((count 0))                    ; count 是自由變數
    (lambda ()                         ; 返回一個閉包
      (setf count (+ count 1))
      count)))

; 創建兩個獨立的計數器
(defvar c1 (make-counter))
(defvar c2 (make-counter))

(funcall c1)  ; 返回 1
(funcall c1)  ; 返回 2
(funcall c1)  ; 返回 3
(funcall c2)  ; 返回 1（獨立的計數器！）
(funcall c2)  ; 返回 2
```

閉包是 FP 中最重要的概念之一，至今仍在無數語言中使用。

---

## Lisp 的方言時代

1960 年代後，Lisp 衍生出無數方言：

| 方言 | 年份 | 發明者/機構 | 特點 |
|------|------|-------------|------|
| Lisp 1.5 | 1962 | MIT | 最早的標準版本 |
| Maclisp | 1966 | MIT | 預言機上的 Lisp |
| Interlisp | 1967 | BBN | 包含 IDE |
| Scheme | 1975 | MIT | 簡潔的 Lisp 方言 |
| Common Lisp | 1984 | 委員會 | 統一標準 |
| Clojure | 2007 | Rich Hickey | JVM 上的現代 Lisp |
| Racket | 2010 | PLT | 實驗性語言平台 |

### Scheme 的誕生

1975 年，Guy Steele 和 Gerald Sussman 設計了 Scheme——一個極簡的 Lisp 方言。Scheme 的創新在於：

```scheme
; 詞法作用域（取代動態作用域）
(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

; 尾遞迴優化
(define (factorial n)
  (define (iter n result)
    (if (= n 0)
        result
        (iter (- n 1) (* n result))))
  (iter n 1))

; 延續（Continuation）
(define (search lst target)
  (call/cc
    (lambda (return)
      (for-each
        (lambda (x)
          (if (= x target)
              (return (list 'found x))))
        lst)
      (list 'not-found))))
```

### Common Lisp 的標準化

1984 年，Common Lisp 成為 ANSI 標準。這個標準統一了眾多 Lisp 方言：

```lisp
; 物件系統 CLOS
(defclass person ()
  ((name :initarg :name :accessor name)
   (age  :initarg :age  :accessor age)))

(defmethod greet ((p person))
  (format t "你好，~A！" (name p)))

; 條件系統
(handler-case
    (risky-operation)
  (division-by-zero () 
    (format t "除以零！"))
  (error (e)
    (format t "發生錯誤: ~A" e)))
```

### Clojure：現代 Lisp

2007 年，Rich Hickey 創造了 Clojure——運行在 JVM 上的現代 Lisp：

```clojure
; 不可變資料結構
(def my-map {:name "Alice" :age 30})
(def updated-map (assoc my-map :city "台北"))

; 序列抽象
(->> [1 2 3 4 5]
     (filter even?)
     (map #(* % %))
     (reduce +))  ; => 20

; 并發
(def counter (atom 0))
(swap! counter inc)
(dosync (ref-set shared-ref new-value))
```

---

## Paul Graham 與 Greenspun 第十條規則

2003 年，程式設計師 Paul Graham 在他的文章中寫道：

> 「任何足夠複雜的 C 或 Fortran 程式都包含一個臨時的、非正式的、拙劣的、執行緩慢的、只有部分完成的 Lisp 實現。」

這被稱為「Greenspun 第十條規則」——這是一個關於語言設計的深刻洞察。

### 為什麼會這樣？

因為 Lisp 的抽象能力太強了。當你需要處理複雜的問題時，你會不自覺地發明某種 Lisp-like 的 DSL：

- Python 的列表推導、裝飾器
- Ruby 的元程式設計
- JavaScript 的原型繼承和動態性
- C# 的 LINQ

這些都是「Lisp 的影子」。

---

## Lisp 的遺產

### 對其他語言的影響

| 語言 | 受 Lisp 啟發的特性 |
|------|-------------------|
| Python | 列表推導、裝飾器、eval |
| JavaScript | 函式頭等、閉包、動態性 |
| Ruby | eval、元程式設計、DSL |
| C# | LINQ、lambda |
| Haskell | 惰性求值、列表推導 |
| Java | 泛型、註解（annotation）|

### 當代的 Lisp

Lisp 及其後裔至今仍在廣泛使用：

- **Emacs Lisp**：Emacs 編輯器的擴展語言
- **Scheme**：教學和研究中常用
- **Racket**：程式語言研究平台
- **Clojure**：函式並發編程
- **Common Lisp**：ANSI 標準，工業應用

---

## 結語

Lisp 的故事告訴我們：

1. **理論可以轉化為實踐**：McCarthy 的理論在 Russell 的手中變成了實際可用的工具
2. **簡單的思想可以產生深遠的影響**：六十年前的設計至今仍在影響我們的語言
3. **程式即資料**：這個洞見比以往任何時候都更加重要

當我們使用 Python 的列表推導、JavaScript 的閉包、或 React 的元件時，我們正在延續 Lisp 的遺產。

---

## 延伸閱讀

- [McCarthy 1960: Recursive Functions of Symbolic Expressions](https://www.google.com/search?q=McCarthy+Recursive+Functions+Symbolic+Expressions+1960)
- [Paul Graham: Beating the Averages](https://www.google.com/search?q=Paul+Graham+Beating+the+Averages+Lisp)
- [Graham Conway: The Roots of Lisp](https://www.google.com/search?q=The+Roots+of+Lisp+John+McCarthy)

---

*本篇文章為「AI 程式人雜誌 2026 年 3 月號」歷史回顧系列之二。*
