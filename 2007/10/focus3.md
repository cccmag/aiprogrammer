# 雲端與網格運算：從網格到雲端

## 網格運算的起源

網格運算（Grid Computing）起源於 1990 年代，主要用於科學研究。

### 網格運算的特點

```bash
# 網格運算的特性
# - 分散式資源聚合
# - 志願者計算
# - 科學和工程應用
# - 類似虛擬超級電腦
```

### 著名的網格計算專案

```
網格計算專案：
───────────────
SETI@home   - 搜尋外星智慧
Climateprediction.net - 氣候模擬
Folding@home - 蛋白質折疊
Berkeley Open Infrastructure for Network Computing (BOINC)
```

## 從網格到雲端

### 比較

```
網格 vs 雲端：
──────────────────────────────────────────────────────────
特性          網格運算              雲端運算
──────────────────────────────────────────────────────────
目標          志願者貢獻資源        商業化服務
資源類型      異構分散資源          標準化資料中心
管理          去中心化             中央化管理
使用案例      科學研究              商務應用
計費          通常免費             按使用量計費
彈性          有限                 高度彈性
──────────────────────────────────────────────────────────
```

### 轉變的關鍵

```python
# 網格運算的限制
# 1. 缺乏標準化
# 2. 可靠性問題
# 3. 安全問題
# 4. 缺乏商業支援

# 雲端運算的優勢
# 1. 標準化 API
# 2. 高可靠性
# 3. 企業級安全
# 4. 專業支援
```

## Hadoop 與雲端

### Hadoop 的起源

```java
// Google 三大論文
// 2003: Google File System (GFS)
// 2004: MapReduce
// 2005: BigTable

// Nutch 專案（後來成為 Hadoop）
// 2006: Hadoop 從 Nutch 分離出來
// 2007: Hadoop 0.16, 支援 HDFS
```

### Hadoop 與雲端運算

```python
# Hadoop 可以在雲端上運行
# Amazon EMR（Elastic MapReduce）
# 使用 Hadoop 分析 S3 中的資料

# EMR 範例
emr = boto.connect_emr()
jobflow = emr.run_jobflow(
    name='My Analysis',
    ami_version='2.0',
    instance_type='m1.small',
    ec2_keyname='my-key',
    keep_alive=True,
    num_instances=5
)
```

## 結語

雲端運算繼承了網格運算的分散式計算理念，但提供了更商業化、標準化、彈性的解決方案。從志願者計算到商業雲端服務，這是分散式運算的自然演化。

---

## 延伸閱讀

- [grid+computing+to+cloud+computing](https://www.google.com/search?q=grid+computing+to+cloud+computing)

---