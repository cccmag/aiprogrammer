# MapReduce 程式開發實戰

## WordCount 範例詳解

WordCount 是 MapReduce 的 Hello World 程式，計算文字檔案中每個單字出現的次數。

### 完整程式碼

```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import java.io.IOException;
import java.util.StringTokenizer;

public class WordCount {

    // Mapper 類別
    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private static final IntWritable one = new IntWritable(1);
        private Text word = new Text();

        @Override
        protected void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    // Reducer 類別
    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        @Override
        protected void reduce(Text key, Iterable<IntWritable> values,
                              Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    // 主程式
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();

        if (otherArgs.length != 2) {
            System.err.println("Usage: wordcount <input> <output>");
            System.exit(2);
        }

        Job job = new Job(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(otherArgs[0]));
        FileOutputFormat.setOutputPath(job, new Path(otherArgs[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

## Mapper 實作

### 输入格式

Mapper 的輸入是鍵值對：

```java
// key: 行偏移量（可忽略）
// value: 該行文字
public void map(Object key, Text value, Context context)
```

### 自訂 Mapper

```java
public static class MyMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
    private final IntWritable one = new IntWritable(1);
    private Text word = new Text();

    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        // 處理每一行文字
        String line = value.toString();
        // ...
    }
}
```

### 輸出型別

Mapper 輸出必須符合 Job 設定：

```java
// 設定 Mapper 輸出型別
job.setMapOutputKeyClass(Text.class);
job.setMapOutputValueClass(IntWritable.class);
```

## Reducer 實作

### Reduce 函數

```java
public static class MyReducer
        extends Reducer<Text, IntWritable, Text, IntWritable> {

    @Override
    protected void reduce(Text key, Iterable<IntWritable> values, Context context)
            throws IOException, InterruptedException {
        // key: 單字
        // values: 出現次數的疊代器
        int sum = 0;
        for (IntWritable val : values) {
            sum += val.get();
        }
        context.write(key, new IntWritable(sum));
    }
}
```

### 多個 Reduce

可以設定多個 Reduce 任務：

```java
job.setNumReduceTasks(4);
```

這會將輸出分為 4 個分割區。

## Combiner 函數

Combiner 是在 Map 端進行的局部彙總，可以減少網路傳輸：

```java
// 使用 Reducer 作為 Combiner
job.setCombinerClass(IntSumReducer.class);
```

### 使用時機

Combiner 適用於：
- 支援交換律和結合律的操作（如 sum、count）
- max、min 等

不適用於：
- average（需要全部值才能計算）
- median

## Partitioner 實作

自訂 Partitioner 控制資料分割：

```java
public class MyPartitioner extends Partitioner<Text, IntWritable> {
    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        String word = key.toString();
        if (word.startsWith("a")) return 0;
        if (word.startsWith("b")) return 1;
        if (word.startsWith("c")) return 2;
        return 3;
    }
}

// 設定 Partitioner
job.setPartitionerClass(MyPartitioner.class);
```

## 執行 Job

### 本地執行

```bash
# 編譯
javac -classpath $HADOOP_HOME/hadoop-core-0.18.0.jar WordCount.java

# 打包
jar cf wc.jar WordCount*.class

# 執行
hadoop jar wc.jar WordCount input.txt output
```

### 叢集執行

```bash
# 複製輸入到 HDFS
hadoop fs -put local_input /user/hduser/input

# 執行
hadoop jar wc.jar WordCount /user/hduser/input /user/hduser/output

# 檢視結果
hadoop fs -cat /user/hduser/output/part-r-00000
```

## 偵錯技巧

### 檢視日誌

```bash
# 追蹤 TaskTracker 日誌
tail -f $HADOOP_HOME/logs/hadoop-hduser-tasktracker-*.log

# 追蹤 JobTracker 日誌
tail -f $HADOOP_HOME/logs/hadoop-hduser-jobtracker-*.log
```

### 本地執行模式

使用本機檔案系統而非 HDFS：

```java
Configuration conf = new Configuration();
conf.set("fs.default.name", "file:///");
conf.set("mapred.job.tracker", "local");
```

### 單機 MapReduce

```bash
hadoop jar wc.jar WordCount -files local_input.txt file:///output
```

### 常見錯誤

| 錯誤 | 解決方案 |
|------|----------|
| ClassNotFoundException | 確認 JAR 包含所有依賴 |
| NoSuchFileException | 檢查 HDFS 路徑是否正確 |
| OutOfMemoryError | 增加 reducer 記憶體 |

## 進階範例：倒排索引

```java
public class InvertedIndex {

    public static class Map extends Mapper<LongWritable, Text, Text, Text> {
        @Override
        protected void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {
            String[] fields = value.toString().split("\t");
            String url = fields[0];
            String content = fields[1];

            for (String word : content.split("\\s+")) {
                context.write(new Text(word), new Text(url));
            }
        }
    }

    public static class Reduce extends Reducer<Text, Text, Text, Text> {
        @Override
        protected void reduce(Text word, Iterable<Text> urls, Context context)
                throws IOException, InterruptedException {
            StringBuilder sb = new StringBuilder();
            for (Text url : urls) {
                if (sb.length() > 0) sb.append(",");
                sb.append(url.toString());
            }
            context.write(word, new Text(sb.toString()));
        }
    }
}
```

## 效能優化

### 輸入分割

```java
// 設定分割大小
FileInputFormat.setMaxInputSplitSize(job, 256 * 1024 * 1024);
FileInputFormat.setMinInputSplitSize(job, 64 * 1024 * 1024);
```

### 壓縮輸出

```java
// 中間結果壓縮
conf.set("mapred.compress.map.output", "true");
conf.set("mapred.map.output.compression.codec", "org.apache.hadoop.io.compress.GzipCodec");

// 最終輸出壓縮
FileOutputFormat.setCompressOutput(job, true);
FileOutputFormat.setOutputCompressorClass(job, GzipCodec.class);
```

### 使用 Combiner

```java
job.setCombinerClass(MyReducer.class);
```

## 結論

MapReduce 程式開發的核心是正確實作 Mapper 和 Reducer。理解資料流、分割、排序和 combiner 的工作原理，才能編寫高效的 MapReduce 程式。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [HDFS 分散式檔案系統](focus2.md)
- [Hadoop+WordCount+example](https://www.google.com/search?q=Hadoop+WordCount+example)