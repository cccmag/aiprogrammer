# 集群計算的商業化：Hadoop 的起源

## 前言

2007 年，Apache Hadoop 正在快速發展，基於 Google 的 MapReduce 和 GFS 論文。

## Hadoop 核心概念

```java
// MapReduce 範例
public class WordCount {
    public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
        public void map(LongWritable key, Text value, Context context) {
            for (String word : value.toString().split()) {
                context.write(new Text(word), new IntWritable(1));
            }
        }
    }

    public static class Reduce extends Reducer<Text, IntWritable, Text, IntWritable> {
        public void reduce(Text key, Iterable<IntWritable> values, Context context) {
            int sum = 0;
            for (IntWritable val : values) sum += val.get();
            context.write(key, new IntWritable(sum));
        }
    }
}
```

## 結語

Hadoop 的興起標誌著大數據時代的開始。

---

## 延伸閱讀

- [Hadoop+MapReduce+2007](https://www.google.com/search?q=Hadoop+MapReduce+2007)

---