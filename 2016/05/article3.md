# JVM 調優實踐

## JVM 記憶體結構

```
堆：
  年輕代：
    Eden 区
    Survivor S0
    Survivor S1
  老年代

非堆：
  方法區
  運行時常量池
  即時編譯的程式碼緩存
```

## 常見 GC 演算法

### Serial GC

單執行緒收集，適合小型應用：

```bash
java -XX:+UseSerialGC MyApp
```

### Parallel GC

多執行緒收集，追求吞吐量：

```bash
java -XX:+UseParallelGC -XX:ParallelGCThreads=4 MyApp
```

### CMS GC

並發標記-清除，低停頓：

```bash
java -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=80 MyApp
```

### G1 GC

分割為多個區域，低停頓時間：

```bash
java -XX:+UseG1GC -XX:MaxGCPauseMillis=200 MyApp
```

## 記憶體配置

```bash
# 初始堆大小
-Xms512m

# 最大堆大小
-Xmx2g

# 年輕代大小
-Xmn256m

# Eden/Survivor 比例
-XX:SurvivorRatio=8
```

## JVM 調優範例

### 計算機器

```bash
java -server \
     -Xms4g -Xmx4g \
     -Xmn2g \
     -XX:+UseG1GC \
     -XX:MaxGCPauseMillis=100 \
     -XX:+ParallelRefProcEnabled \
     MyApplication
```

### 延遲敏感應用

```bash
java -server \
     -Xms2g -Xmx2g \
     -XX:+UseZGC \
     -XX:MaxGCPauseMillis=50 \
     MyApplication
```

## 監控工具

### jstat

```bash
# 查看 GC 統計
jstat -gcutil <pid> 1000
```

### jmap

```bash
# 生成堆 dump
jmap -dump:format=b,file=heap.bin <pid>

# 查看類別統計
jmap -clstats <pid>
```

### jcmd

```bash
# 多種診斷命令
jcmd <pid> VM.flags
jcmd <pid> GC.heap_info
```

延伸閱讀：
- [Google 搜尋：JVM tuning guide](https://www.google.com/search?q=JVM+tuning+guide)
- [Google 搜尋：G1 GC tuning](https://www.google.com/search?q=G1+GC+tuning)