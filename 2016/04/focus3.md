# 主題三：Clojure — Lisp 的現代傳承

## Lisp 的靈魂

1958 年，John McCarthy 在 MIT 發明了 Lisp（LISt Processing）。作為僅次於 FORTRAN 的第二古老高階語言，Lisp 見證了電腦科學的整個發展歷程。

Lisp 的核心思想極為優雅：

- **代碼即資料（Code is Data）**：Lisp 的語法本身就是一種資料結構（S-表達式）
- **同像性（Homoiconicity）**：程式的結構可以直接被程式操作和轉換
- **元程式設計（Metaprogramming）**：強大的巨集系統讓你擴展語言語法

Clojure 是 Rich Hickey 於 2007 年創造的現代 Lisp 方言，運行在 JVM 之上，專為並發和函式式程式設計而設計。

## 為什麼叫 Clojure？

Rich Hickey 選擇「Clojure」這個名字是因為：

- **C** 代表 **C**ommunity（社群）
- **lojure** 暗示這種語言是 Lisp 的 **clo**sure（閉包）

這完美體現了 Clojure 的設計理念：融合 Lisp 的強大元程式設計能力與 JVM 生態系的豐富庫資源。

## Clojure 的核心原則

### 1. 不可變性為預設

Clojure 的資料結構（list、vector、map、set）預設是不可變的。當你「修改」一個資料結構時，實際上是創建了一個新結構，而原結構保持不變。

```clojure
;; 不可變的 vector
(def original [1 2 3 4 5])

;; 創建新 vector，原 vector 不變
(def added (conj original 6))

;; original 仍然是 [1 2 3 4 5]
;; added 是 [1 2 3 4 5 6]
```

這種設計使得並發程式設計大幅簡化——不需要鎖機制，因為資料從來不會被修改。

### 2. 持久化資料結構

Clojure 的不可變資料結構是**持久化**的——它們保留了之前版本的引用，並透過結構共享（Structural Sharing）高效地創建新版本。

```clojure
;; 結構共享示意
(def v1 [1 2 3 4 5])
(def v2 (assoc v1 2 99))  ;; 只複製變更的部分

;; v1 = [1 2 3 4 5]
;; v2 = [1 2 99 4 5]
;; 共享的部分：1, 以及 4, 5
```

### 3. 軟體事務記憶體（STM）

Clojure 提供軟體事務記憶體（Software Transactional Memory），讓你可以用事務的方式處理並發修改。

```clojure
(def counter (ref 0))

;; 在事務中安全地修改 ref
(dosync
  (alter counter inc)
  (alter counter inc)
  (alter counter inc))

;; counter 的值是 3
```

### 4. Agent

Agent 提供了另一種並發模型——每個 Agent 擁有一個獨立的狀態，透過訊息傳遞進行修改。

```clojure
(def log-agent (agent []))

;; 發送 action 給 agent
(send log-agent conj "User logged in")
(send log-agent conj "User made a purchase")

;; 讀取 agent 當前狀態
@log-agent  ;; => ["User logged in" "User made a purchase"]
```

## Clojure 的序列抽象

Clojure 的核心抽象是**序列（Sequence）**——任何可以被視為有序元素集合的東西都可以使用相同的函式處理。

```clojure
;; 使用序列函式處理各種資料來源
(map inc [1 2 3 4 5])              ;; list: (2 3 4 5 6)
(map inc '(1 2 3 4 5))              ;; lazy seq: (2 3 4 5 6)
(map inc #{1 2 3 4 5})              ;; set: (2 3 4 5 6)
(map inc {:a 1 :b 2 :c 3})         ;; map keys: (:a :b :c)
(map (fn [[k v]] [k (inc v)]) {:a 1 :b 2}) ;; map kv: ([:a 2] [:b 3])
```

## REPL 驅動開發

Clojure 強調互動式開發（Interactive Development）。透過 REPL（Read-Eval-Print Loop），你可以：

- 即時測試程式碼片段
- 逐步構建系統
- 在執行時檢查和修改狀態
- 熱交換程式碼（Hot Code Swapping）

```clojure
;; 啟動 REPL
;; lein repl 或 boot repl

;; 互動式開發
(def my-data {:users []})

;; 隨時檢查狀態
(println my-data)

;; 新增功能
(defn add-user [db user]
  (update db :users conj user))

;; 測試新功能
(def updated-db (add-user my-data {:name "Alice" :email "alice@example.com"}))
```

## ClojureScript：前端開發的新選擇

ClojureScript 是 Clojure 編譯到 JavaScript 的實現，讓你可以用 Clojure 的優雅語法開發前端應用。

```clojure
;; ClojureScript 範例
(ns my-app.core
  (:require [reagent.core :as r]))

(defn greeting []
  [:div "Hello, ClojureScript!"])

(r/render [greeting]
          (.getElementById js/document "app"))
```

ClojureScript 的優勢：

- **不可變性**：使用 Reagent/React 時，狀態管理更加清晰
- **精確的資料操作**：強大的序列函式
- **元程式設計**：強大的巨集系統

## Clojure 在金融科技的應用

Clojure 在金融領域獲得廣泛採用：

- **Jane Street**：使用 OCaml 和 Clojure 的量化交易公司
- **Walmart**：使用 Clojure 處理大規模零售資料
- **Chef**：基礎設施自動化工具，大量使用 Clojure DSL

## 小結

Clojure 繼承了 Lisp 的精髓，同時針對現代計算環境進行了優化。不可變性為預設、軟體事務記憶體、Agent 系統——這些特性使得 Clojure 成為處理並發問題的利器。

下一篇文章中，我們將探討 Scala——另一種運行在 JVM 上的函數式語言，卻走了一條不同的融合之路。