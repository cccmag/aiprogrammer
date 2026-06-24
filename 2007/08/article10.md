# 資料探勘：WEKA 機器學習工具

WEKA (Waikato Environment for Knowledge Analysis) 是紐西蘭 Waikato 大學開發的開源機器學習和資料探勘工具。

## WEKA 功能

```java
// WEKA Java API
import weka.core.Instances;
import weka.classifiers.trees.J48;
import weka.classifiers.Evaluation;

// 載入資料
Instances data = new Instances(new BufferedReader(new FileReader("data.arff")));
data.setClassIndex(data.numAttributes() - 1);

// 建立分類器
J48 tree = new J48();
tree.buildClassifier(data);

// 評估
Evaluation eval = new Evaluation(data);
eval.crossValidateModel(tree, data, 10, new Random(1));

System.out.println(eval.toSummaryString());
```

## 預處理

```java
// WEKA 濾波器
import weka.filters.unsupervised.attribute.Normalize;
import weka.filters.unsupervised.attribute.Discretize;

// 標準化
Normalize normalize = new Normalize();
normalize.setInputFormat(data);
Instances normalizedData = Filter.useFilter(data, normalize);

// 離散化
Discretize discretize = new Discretize();
discretize.setInputFormat(data);
Instances discretizedData = Filter.useFilter(data, discretize);
```

## 結語

WEKA 為資料探勘研究提供了完整的工具集。

---

*延伸閱讀：[WEKA 官方網站](https://developers.google.com/search/?q=weka+official)*