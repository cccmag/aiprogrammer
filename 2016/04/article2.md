# Clojure 開發大資料處理系統

## Clojure 的大資料生態

Clojure 作為 JVM 語言，可以無縫使用 Java 生態中的大資料工具，如 Hadoop、Spark 和 Kafka。結合 Clojure 的函式式特性，使得大資料處理既高效又優雅。

## 使用 Spark 的 Clojure 包

`sparkling` 是 Clojure 的 Spark 包：

```clojure
(ns myapp.spark
  (:require [sparkling.core :as spark]
            [sparkling.function :as func]))

;; 建立 Spark 上下文
(def sc (spark/spark-context "local[*]" "myapp"))

;; 讀取資料
(def lines (spark/text-file sc "hdfs://data/logs/*.txt"))

;; 處理：計算每個單字出現次數
(def word-counts
  (->> lines
       (spark/flat-map (func/flat-map-fn
                        #(clojure.string/split % #"\s+")))
       (spark/map-to-pair (func/map-to-pair-fn
                           #(spark/tuple (clojure.string/lower-case %) 1)))
       (spark/reduce-by-key +)))

;; 輸出結果
(->> word-counts
     (spark/collect)
     (run! println))
```

## Kafka 串流處理

使用 `jackdaw` 進行 Kafka 串流處理：

```clojure
(ns myapp.kafka
  (:require [jackdaw.serdes :as serdes]
            [jackdaw.streams :as streams]))

;; 定義拓撲
(def topology
  (streams/topology
   {:input-topic [(streams/source :input)]
    :output-topic (streams/sink :output)}

   (fn [builder]
     (-> builder
         (streams/stream :input-topic)
         (streams/map-values deserializer)
         (streams/filter #(< (:price %) 100))
         (streams/map-values serializer)
         (streams/to :output-topic)))))

;; 啟動 streams
(def kafka-config {:bootstrap-servers "localhost:9092"})
(def streams-instance (streams/kafka-streams topology kafka-config))

(streams/start streams-instance)
```

## 高效的並行處理

Clojure 的核心序列抽象天然適合大資料處理：

```clojure
;; 平行映射（使用 reducers）
(require '[clojure.core.reducers :as r])

;; 處理大型集合，自動利用多核心
(def results
  (into []
        (r/map expensive-computation
               (r/filter valid? large-dataset)))
```

## 案例：金融異常偵測

某金融機構使用 Clojure 建構即時欺詐偵測系統：

- 使用 Kafka 攝入交易串流
- 使用 Spark Streaming 分析交易模式
- 使用 Clojure 的 STM 確保狀態一致性
- 毫秒級延遲，處理數萬筆交易/秒

## 延伸閱讀

- [Google 搜尋：Clojure big data processing](https://www.google.com/search?q=Clojure+big+data+processing)
- [Google 搜尋：Sparkling Clojure Spark](https://www.google.com/search?q=sparkling+Clojure+Spark)