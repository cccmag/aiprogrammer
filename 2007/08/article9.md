# 推薦系統：Apache Mahout 的起源

Apache Mahout 是 Apache 軟體基金會的機器學習庫，2007 年開始開發，旨在建立可擴展的機器學習演算法庫。

## Mahout 的目標

```java
// Mahout 推薦引擎
import org.apache.mahout.cf.taste.impl.model.file.FileDataModel;
import org.apache.mahout.cf.taste.impl.neighborhood.NearestNUserNeighborhood;
import org.apache.mahout.cf.taste.impl.recommender.GenericUserBasedRecommender;
import org.apache.mahout.cf.taste.model.DataModel;
import org.apache.mahout.cf.taste.neighborhood.UserNeighborhood;
import org.apache.mahout.cf.taste.recommender.Recommender;
import org.apache.mahout.cf.taste.recommender.UserBasedRecommender;

// 建立推薦器
DataModel model = new FileDataModel(new File("ratings.csv"));
UserNeighborhood neighborhood = new NearestNUserNeighborhood(10, 0.1, model);
Recommender recommender = new GenericUserBasedRecommender(
    model, neighborhood, new PearsonCorrelationSimilarity(model));
```

## 主要功能

```markdown
# Mahout 提供的演算法：

1. 推薦系統
   - 基於使用者的協同過濾
   - 基於物品的協同過濾
   - SVD 矩陣分解

2. 分群
   - K-means
   - Fuzzy K-means
   - Canopy Clustering

3. 分類
   - 朴素贝叶斯
   - 隨機森林
```

## 結語

Mahout 為大規模機器學習提供了可擴展的解決方案。

---

*延伸閱讀：[Mahout 官方網站](https://developers.google.com/search/?q=apache+mahout)*