# MapReduce 程式設計模式

## 常見模式概述

MapReduce 程式設計有幾個常見模式，每種模式解決特定類型的問題。

## 1. 計數（Counting）

最基本的模式，計算某種事件的發生次數。

### WordCount

```java
public static class Map extends Mapper<LongWritable, Text, Text, IntWritable> {
    private IntWritable one = new IntWritable(1);
    private Text word = new Text();

    public void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {
        for (String token : value.toString().split("\\s+")) {
            word.set(token);
            context.write(word, one);
        }
    }
}
```

### 日期計數

```java
// 計算每日的請求數
public void map(LongWritable key, Text value, Context context) {
    LogEntry entry = parse(value);
    context.write(new Text(entry.date), new IntWritable(1));
}
```

## 2. 过滤（Filtering）

選擇符合條件的記錄。

### 簡單過濾

```java
public void map(LongWritable key, Text value, Context context) {
    Record record = parse(value);
    if (record.amount > 1000) {
        context.write(key, record);
    }
}
```

### 隨機採樣

```java
private Random rand = new Random();

public void map(LongWritable key, Text value, Context context) {
    if (rand.nextDouble() < 0.01) {  // 1% 採樣
        context.write(key, value);
    }
}
```

## 3. 組織（Organization）

重新格式化輸出。

### 鍵值交換

```java
// 交換鍵值對的位置
public void map(LongWritable key, Text value, Context context) {
    String[] fields = value.toString().split(",");
    context.write(new Text(fields[1]), new Text(fields[0]));
}
```

### 嵌套結構

```java
// 將多個欄位組合成一個鍵
public void map(LongWritable key, Text value, Context context) {
    String[] fields = value.toString().split(",");
    String compositeKey = fields[0] + "|" + fields[1];
    context.write(new Text(compositeKey), value);
}
```

## 4. 加入（Join）

合併多個資料來源。

### Map 端 Join

```java
public void map(LongWritable key, Text value, Context context) {
    // 預先載入小表格到記憶體
    String[] fields = value.toString().split(",");
    String userId = fields[0];
    if (userTable.containsKey(userId)) {
        User user = userTable.get(userId);
        context.write(value, new Text(user.name));
    }
}
```

### Reduce 端 Join

```java
public void reduce(Text key, Iterable<Text> values, Context context) {
    List<String> left = new ArrayList<>();
    List<String> right = new ArrayList<>();

    for (Text value : values) {
        if (isLeftSource(value)) left.add(value.toString());
        else right.add(value.toString());
    }

    for (String l : left) {
        for (String r : right) {
            context.write(key, new Text(l + "," + r));
        }
    }
}
```

## 5. 排序（Sorting）

對輸出進行排序。

```java
// 使用自訂排序鍵
public static class SortMapper extends Mapper<LongWritable, Text, IntPair, Text> {
    public void map(LongWritable key, Text value, Context context) {
        String[] fields = value.toString().split(",");
        int sortKey = Integer.parseInt(fields[1]);
        context.write(new IntPair(sortKey, 0), value);
    }
}

// IntPair 需要實現 WritableComparable
public class IntPair implements WritableComparable<IntPair> {
    private int first;
    private int second;

    public int compareTo(IntPair o) {
        if (first != o.first) return first - o.first;
        return second - o.second;
    }
}
```

## 6. 倒排索引（Inverted Index）

建立從詞到文檔的映射。

```java
public void map(LongWritable key, Text value, Context context) {
    String[] terms = value.toString().split("\\s+");
    String docId = extractDocId(key);
    for (String term : terms) {
        context.write(new Text(term), new Text(docId));
    }
}

public void reduce(Text term, Iterable<Text> docIds, Context context) {
    Set<String> uniqueDocs = new HashSet<>();
    for (Text docId : docIds) {
        uniqueDocs.add(docId.toString());
    }
    context.write(term, new Text(String.join(",", uniqueDocs)));
}
```

## 7. 集群（Clustering）

將相似的資料分組。

### K-Means MapReduce

```java
// Map：分配點到最近的質心
public void map(LongWritable key, Text value, Context context) {
    Point p = parsePoint(value);
    Centroid nearest = findNearest(p, centroids);
    context.write(nearest, p);
}

// Reduce：重新計算質心
public void reduce(Centroid key, Iterable<Point> points, Context context) {
    Point newCentroid = computeMean(points);
    context.write(newCentroid, new Text(newCentroid.toString()));
}
```

## 8. 模式匹配（Pattern Matching）

正規表達式匹配。

```java
public void map(LongWritable key, Text value, Context context) {
    String text = value.toString();
    Pattern pattern = Pattern.compile("\\d{3}-\\d{3}-\\d{4}");
    Matcher matcher = pattern.matcher(text);
    while (matcher.find()) {
        context.write(new Text(matcher.group()), new IntWritable(1));
    }
}
```

## 效能考量

### Combiner 的使用

```java
// 使用 Reducer 作為 Combiner
job.setCombinerClass(SumReducer.class);
```

### 減少輸出

```java
// 过滤不需要的輸出
if (shouldOutput(value)) {
    context.write(key, value);
}
```

## 結論

MapReduce 模式為常見的資料處理問題提供了標準化的解決方案。掌握這些模式，可以更快速地開發 MapReduce 應用。

---

**延伸閱讀**

- [MapReduce 分散式運算](focus1.md)
- [Hadoop 程式開發實戰](focus4.md)
- [MapReduce+patterns](https://www.google.com/search?q=MapReduce+programming+patterns)