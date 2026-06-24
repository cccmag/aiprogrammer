# 本期焦點

## Hadoop 與巨量資料處理 — 分散式運算的新時代

### 引言

隨著網路資料量呈指數成長，傳統的資料處理方式已無法勝任。Google 提出了 MapReduce 運算模型，為處理 PB 等級的資料提供了可擴展的解決方案。2008 年，Apache Hadoop 已成為巨量資料處理的主流框架。

本期雜誌將帶您深入了解 Hadoop 的核心概念、架構設計和開發實踐，為迎接巨量資料時代做好準備。

---

## 大綱

* [Hadoop 程式實作](focus_code.md)
   - WordCount 範例
   - MapReduce 程式結構
   - HDFS 檔案操作

1. [MapReduce 分散式運算模型](focus1.md)
   - Map 和 Reduce 函數
   - Mapper 和 Reducer 介面
   - 分散式運算原理

2. [HDFS 分散式檔案系統](focus2.md)
   - NameNode 與 DataNode
   - 區塊複製與容錯
   - 資料本地化

3. [Hadoop 叢集架設與設定](focus3.md)
   - 單機安裝與設定
   - 叢集模式配置
   - 效能調校

4. [MapReduce 程式開發實戰](focus4.md)
   - WordCount 詳解
   - Combiner 和 Partitioner
   - 偵錯技巧

5. [Hive 資料倉儲系統](focus5.md)
   - HiveQL 查詢語言
   - 與 MapReduce 的整合
   - 資料倉儲應用

6. [HBase 即時資料庫](focus6.md)
   - 列導向儲存
   - 即時讀寫特性
   - 與 HDFS 的整合

7. [巨量資料處理的未來趨勢](focus7.md)
   - 即時處理需求
   - 雲端化趨勢
   - 整合分析

---

## 濃縮回顧

### MapReduce 工作流程

```
輸入資料 → Map 階段 → Shuffle → Reduce 階段 → 輸出結果
     ↓           ↓           ↓           ↓
  原始資料    K-V 配對    排序合併    最終彙整
```

### Hadoop 架構

```
┌──────────────────────────────────────┐
│           Hadoop 叢集                  │
├──────────────────────────────────────┤
│  JobTracker          NameNode         │
│  (任務調度)          (元數據管理)       │
├──────────────────────────────────────┤
│  TaskTracker         DataNode         │
│  (任務執行)          (資料儲存)        │
│  × 多個              × 多個            │
└──────────────────────────────────────┘
```

### HDFS 特色

- **大型檔案**：支援 GB 到 TB 等級的檔案
- **高吞吐量**：設計用於一次寫入多次讀取
- **容錯機制**：區塊複製自動恢復

### WordCount 範例

```java
public class WordCount {
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map(LongWritable key, Text value, Context context) {
            for (String word : value.toString().split("\\s+")) {
                context.write(new Text(word), new IntWritable(1));
            }
        }
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context) {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            context.write(key, new IntWritable(sum));
        }
    }
}
```

---

## 結論與展望

Hadoop 開啟了巨量資料處理的新時代。MapReduce 的簡單程式模型掩蓋了複雜的分散式運算細節，讓開發者能夠專注於業務邏輯。

隨著資料量的持續增長，Hadoop 生態系統將持續壯大。Hive、HBase、Pig 等工具的出現，讓不同背景的使用者都能夠受益於巨量資料處理能力。

---

## 延伸閱讀

- [MapReduce 分散式運算](focus1.md)
- [HDFS 分散式檔案系統](focus2.md)
- [Hadoop 程式開發](focus4.md)
- [Hive 資料倉儲](focus5.md)

---

*本期焦點到此結束。下期我們將探討 NoSQL 資料庫的興起，敬請期待。*