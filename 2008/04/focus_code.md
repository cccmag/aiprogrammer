# Hadoop 程式實作

## WordCount 完整實現

本文件提供 Hadoop MapReduce 程式的詳細說明，包含 WordCount 範例的完整程式碼。

## 環境需求

- Java 6 或更高
- Hadoop 0.18.0
- SSH 環境

## WordCount 程式碼

```java
import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

/**
 * WordCount - 計算文字檔案中每個單字出現的次數
 */
public class WordCount {

    /**
     * Mapper 類別
     * 輸入： (行偏移量, 該行文字)
     * 輸出： (單字, 1)
     */
    public static class TokenizerMapper
            extends Mapper<Object, Text, Text, IntWritable> {

        private final IntWritable one = new IntWritable(1);
        private Text word = new Text();

        @Override
        public void map(Object key, Text value, Context context)
                throws IOException, InterruptedException {
            // 使用空白分割文字
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    /**
     * Reducer 類別
     * 輸入： (單字, [1, 1, 1, ...])
     * 輸出： (單字, 總次數)
     */
    public static class IntSumReducer
            extends Reducer<Text, IntWritable, Text, IntWritable> {

        private IntWritable result = new IntWritable();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context)
                throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = new Job(conf, "word count");

        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

## 編譯與執行

### 編譯

```bash
# 設定環境
export HADOOP_HOME=/path/to/hadoop-0.18.0
export CLASSPATH=$HADOOP_HOME/hadoop-core-0.18.0.jar:$HADOOP_HOME/lib/*

# 編譯
javac -cp $CLASSPATH WordCount.java

# 打包 JAR
jar cf wc.jar WordCount*.class
```

### 執行

```bash
# 複製輸入到 HDFS
hadoop fs -put input.txt /user/hduser/input/

# 執行 Job
hadoop jar wc.jar WordCount /user/hduser/input /user/hduser/output

# 檢視結果
hadoop fs -cat /user/hduser/output/part-r-00000
```

## 進階：自訂 Partitioner

```java
public static class FirstLetterPartitioner
        extends Partitioner<Text, IntWritable> {

    @Override
    public int getPartition(Text key, IntWritable value, int numPartitions) {
        String firstChar = key.toString().substring(0, 1).toUpperCase();
        return (firstChar.hashCode() & Integer.MAX_VALUE) % numPartitions;
    }
}

// 在 main 中設定
job.setPartitionerClass(FirstLetterPartitioner.class);
job.setNumReduceTasks(4);
```

## 進階：鏈式 MapReduce

```java
// 設定多重 Mapper
JobChain jobChain = new JobChain(conf);
jobChain.addMapper(WordCount.class)
        .addMapper(Tokenizer.class)
        .addReducer(SumReducer.class);
```

## 常見錯誤

| 錯誤 | 解決方案 |
|------|----------|
| FileNotFoundException | 確認 HDFS 路徑正確 |
| ClassNotFoundException | 確認 JAR 包含所有類別 |
| OutOfMemoryError | 增加 reducer 記憶體 |
| NullPointerException | 檢查空值處理 |

## 效能建議

1. **使用 Combiner**：減少網路傳輸
2. **壓縮中間結果**：減少 IO
3. **合理設定 Reduce 數**：通常為叢集節點數的 0.9 倍
4. **避免小檔案**：合併後再處理

## 參考資源

- [Apache Hadoop官方網站](https://www.google.com/search?q=Apache+Hadoop+official+site)
- [Hadoop+MapReduce+tutorial](https://www.google.com/search?q=Hadoop+MapReduce+tutorial)