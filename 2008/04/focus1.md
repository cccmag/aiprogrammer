# MapReduce 分散式運算模型

## 分散式運算的起源

Google 在 2004 年發表了 MapReduce 論文，提出了一個用於處理大規模資料集的程式設計模型。MapReduce 的核心思想是「分而治之」——將大規模運算任務分解為多個可並行處理的子任務。

### MapReduce 的基本概念

MapReduce 程式設計模型包含兩個主要階段：

1. **Map 階段**：將輸入資料轉換為鍵值對（Key-Value pairs）
2. **Reduce 階段**：將具有相同鍵的值聚合在一起進行處理

```
輸入 → Map → 中間鍵值對 → Shuffle & Sort → Reduce → 輸出
```

## Map 和 Reduce 函數

### Map 函數

Map 函數接受輸入鍵值對，產生一組中間隔鍵值對：

```java
map(K1, V1) → List(K2, V2)
```

例如，在 WordCount 範例中：
- 輸入：(行號, "hello world hello")
- 輸出：[("hello", 1), ("world", 1), ("hello", 1)]

### Reduce 函數

Reduce 函數接收具有相同鍵的所有值，產生輸出鍵值對：

```java
reduce(K2, List(V2)) → List(V3)
```

例如，在 WordCount 範例中：
- 輸入：("hello", [1, 1])
- 輸出：("hello", 2)

## Hadoop 中的 MapReduce

### Mapper 和 Reducer 介面

在 Hadoop 中，開發者需要實作 Mapper 和 Reducer 類別：

```java
public class MyMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    @Override
    protected void map(LongWritable key, Text value, Context context) {
        // 處理每一筆記錄
    }
}

public class MyReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context) {
        // 彙總具有相同鍵的值
    }
}
```

### 驅動程式

驅動程式負責設定 Job 的相關參數：

```java
Job job = new Job();
job.setJobName("WordCount");
job.setJarByClass(WordCount.class);
job.setMapperClass(Map.class);
job.setReducerClass(Reduce.class);
job.setOutputKeyClass(Text.class);
job.setOutputValueClass(IntWritable.class);
FileInputFormat.addInputPath(job, new Path(input));
FileOutputFormat.setOutputPath(job, new Path(output));
job.waitForCompletion(true);
```

## Shuffle 和 Sort

Shuffle 是 MapReduce 中最複雜的部分，負責將 Map 輸出傳輸到對應的 Reduce：

### Map 端

1. Map 輸出寫入記憶體緩衝區
2. 緩衝區達到閾值時，進行局部排序
3. 分區（Partition）決定每條記錄送往哪個 Reduce
4. 可能使用 Combiner 進行局部彙總

### Reduce 端

1. 從多個 Map 節點拉取屬於該分區的資料
2. 合併來自不同 Map 的輸出
3. 按照鍵進行排序
4. 將相同鍵的值分組

## 分割（Partitioning）

分割決定每條記錄由哪個 Reduce 處理：

```java
public class MyPartitioner extends Partitioner<Text, IntWritable> {
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        // 使用鍵的雜湊值決定分割
        return Math.abs(key.hashCode() % numPartitions);
    }
}
```

預設使用 HashPartitioner，確保相同鍵的記錄送往同一個 Reduce。

##  combiners

Combiner 是在 Map 端進行的局部彙總，可以減少網路傳輸量：

```java
job.setCombinerClass(Reduce.class);
```

注意：Combiner 必須符合結合律和交換律，因為它可能被執行多次。

## 錯誤處理與容錯

Hadoop 設計用於在commodity hardware 上運行，因此必須處理各種故障：

### 任務失敗

- Map 或 Reduce 任務失敗時，JobTracker 會自動重新排程
- 任務可以 speculatively re-execute，避免少數慢節點拖累整體進度

### 節點故障

- DataNode 向 NameNode 發送心跳
- 節點故障時，NameNode 偵測到複製數不足，會自動重建副本

### 任務追蹤

- TaskTracker 定期向 JobTracker 報告進度
- JobTracker 維護所有任務的狀態

## 效能優化技巧

### 避免小檔案

大量小檔案會增加 NameNode 負擔。使用 SequenceFile 或 CombineFileInputFormat 合併小檔案。

### 選擇適當的區塊大小

預設 64MB 的區塊大小需要根據資料特性調整：

| 資料特性 | 建議區塊大小 |
|---------|-------------|
| 小檔案多 | 32MB 或更小 |
| 大檔案 | 128MB 或更大 |

### 使用壓縮

在中間結果和最終輸出使用壓縮：

```java
FileOutputFormat.setCompressOutput(job, true);
job.setOutputFormatClass(SequenceFileOutputFormat.class);
```

## 應用場景

MapReduce 適用於各類大規模資料處理：

| 應用 | 說明 |
|------|------|
| 日誌分析 | 處理點擊流、伺服器日誌 |
| 文字處理 | WordCount、倒排索引 |
| 機器學習 | 訓練資料预处理、特徵擷取 |
| 資料探勘 | 关聯規則、分類、集群 |

## 結論

MapReduce 提供了簡單但強大的分散式運算模型。其「一次寫入、多次讀取」的設計非常適合大規模批次處理。理解 Map 和 Reduce 的抽象，以及 Shuffle 過程的優化，是掌握 Hadoop 開發的關鍵。

---

**延伸閱讀**

- [Hadoop 程式開發實戰](focus4.md)
- [HDFS 分散式檔案系統](focus2.md)
- [Google+MapReduce+paper](https://www.google.com/search?q=Google+MapReduce+paper)