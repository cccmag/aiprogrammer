# ClojureScript 與老牌新技術

## ClojureScript 簡介

ClojureScript 是 Clojure 編譯到 JavaScript 的實現，於 2011 年發布。它讓你能用 Clojure 的優雅語法開發前端應用，同時享受函式式程式設計的所有優勢。

## 為何選擇 ClojureScript？

### Lisp 的強大表达能力

ClojureScript 繼承了 Lisp 的簡潔語法：

```clojure
;; ClojureScript
(->> items
     (filter odd?)
     (map inc)
     (reduce +))

;; 等價的 JavaScript
items.filter(x => x % 2 === 1)
     .map(x => x + 1)
     .reduce((acc, x) => acc + x, 0);
```

### 不可變性為預設

ClojureScript 的資料結構預設是不可變的：

```clojure
(def original [1 2 3 4 5])
(def modified (conj original 6))
;; original 仍然是 [1 2 3 4 5]
;; modified 是 [1 2 3 4 5 6]
```

### 強大的巨集系統

Lisp 的巨集允許你在編譯時擴展語法：

```clojure
(defmacro unless [cond & body]
  `(if (not ~cond)
     (do ~@body)))

;; 使用
(unless (= x 0)
  (println "x is not zero"))
```

## 與 React 生態整合

ClojureScript 與 React 完美配合，特別是通過 Reagent 庫：

```clojure
(ns myapp.core
  (:require [reagent.core :as r]))

;; 定義元件（如同純函式）
(defn greeting [props]
  [:div "Hello, " (:name props) "!"])

;; 可變狀態使用 ratom
(defonce app-state (r/atom {:count 0}))

(defn counter []
  [:div
   [:p "Count: " (:count @app-state)]
   [:button {:on-click #(swap! app-state update :count inc)}
    "Increment"]])

;; 渲染
(r/render [counter]
          (.getElementById js/document "app"))
```

## Om：React 的另類實現

Om 是另一個 ClojureScript 的 React 包裝，強調 immutable 資料結構和統一時間軸：

```clojure
(ns myapp.core
  (:require [om.core :as om :include-macros true]
            [om.dom :as dom]))

(def app-state (atom {:count 0}))

(defn counter [app owner]
  (om/component
   (dom/div #js {}
     (dom/h2 nil (str "Count: " (:count app)))
     (dom/button
      #js {:onClick (fn [e] (om/transact! app :count inc))}
      "Click me!"))))

(om/root
 counter
 app-state
 (gdom/appendChild js/document))
```

## Google Closure 優化

ClojureScript 使用 Google Closure Compiler 進行最佳化：

- **死碼消除**：移除未使用的程式碼
- **內聯**：將簡單函式內聯
- **類型推斷**：利用 JSDoc 註解進行優化

## 實際應用

### CircleCI

CircleCI 使用 ClojureScript 建構其儀表板，展現了在大規模應用中的可行性。

### 遊戲開發

ClojureScript 的即時重載和 REPL 驅動開發使其成為遊戲原型開發的理想選擇。

### 資料視覺化

ClojureScript 的資料處理能力使其適合建構複雜的資料視覺化應用。

## 開發工具

- **Figwheel**：熱模組替換，即時更新瀏覽器中的代碼
- **Planck**：ClojureScript 的命令行直譯器
- **CIDER**：Emacs 的 Clojure/ClojureScript IDE

延伸閱讀：
- [Google 搜尋：ClojureScript tutorial](https://www.google.com/search?q=ClojureScript+tutorial)
- [Google 搜尋：Reagent React ClojureScript](https://www.google.com/search?q=Reagent+React+ClojureScript)