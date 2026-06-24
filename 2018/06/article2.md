# Java 10 新特性

## 前言

Java 10 在 2018 年 3 月發布，帶來了多項新功能。

## 主要新特性

### 區域變量類型推斷（var）

```java
var list = new ArrayList<String>();
var stream = list.stream();
```

### 不可變集合工廠方法

```java
List<Integer> list = List.of(1, 2, 3);
Set<String> set = Set.of("a", "b");
Map<String, Integer> map = Map.of("a", 1, "b", 2);
```

### G1 垃圾回收器改進

效能優化，減少停頓時間。

## 結論

Java 10 是對 Java 語言和平臺的重要更新。

---

**延伸閱讀**

- [Java 10 官方網站](https://www.google.com/search?q=Java+10+official+site)
- [Java 10 新特性](https://www.google.com/search?q=Java+10+new+features)