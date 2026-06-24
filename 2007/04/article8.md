# 電腦視覺的新標準：ImageNet 與深度學習

## 前言

2007 年，Fei-Fei Li 啟動了 ImageNet 計畫。這是一個影響深遠的決定——ImageNet 最終成為深度學習革命的催化劑。

## ImageNet 的創建

### 大規模視覺資料集的需求

2007 年，大多數視覺辨識研究使用的資料集規模很小：

```
早期視覺資料集：
─────────────────
資料集         影像數量    類別數
──────────────────────────────
Caltech 101    9,146       101
Caltech 256    30,607      256
PASCAL VOC     語義分割     20
──────────────────────────────
```

### ImageNet 的規模

ImageNet 的目標是「更多影像、更多類別」：

```
ImageNet 規模（2009 年）：
─────────────────────────
項目                數量
──────────────────────────
總影像數            14,197,122
總類別數            21,841
WordNet 同義集      21,841
手動標注影像        約 1,000,000
候選影像            ~5,000 每類別
──────────────────────────
```

## ImageNet 的技術貢獻

### WordNet 層級結構

ImageNet 類別按照 WordNet 語義層級組織：

```
ImageNet 層級範例：
─────────────────────
實體
 └─ 物體
     └─ 天然物體
         └─ 動物
             └─ 脊椎動物
                 └─ 哺乳動物
                     └─ 食肉動物
                         └─ 犬科
                             ├─ 狼
                             ├─ 狐狸
                             └─ 狗
```

### 群眾外包標注

大規模標注需要群眾外包：

```python
# Amazon Mechanical Turk 標注任務
turk_task = {
    "title": "影像分類標注",
    "description": "請選擇影像中物體的類別",
    "reward": 0.05,
    "images": image_urls,
    "categories": categories
}
```

## 對深度學習的影響

### ILSVRC 競賽

2010 年開始的 ImageNet Large Scale Visual Recognition Challenge (ILSVRC)：

```
ILSVRC 錯誤率變化：
─────────────────────────────
年份    方法          Top-5 錯誤率
──────────────────────────────
2010    人工特征+SVM    28%
2011    特效工程        26%
2012    AlexNet        16.4%
2014    VGG/GoogLeNet  7%
2015    ResNet         3.6%
──────────────────────────────
```

## 結語

ImageNet 的故事告訴我們：**資料，有時比演算法更重要**。2007 年開始的這個計畫，最終成為深度學習革命的催化劑之一。

---

## 延伸閱讀

- [ImageNet+history+Fei-Fei+Li](https://www.google.com/search?q=ImageNet+history+Fei-Fei+Li)
- [ImageNet+large+scale+visual+recognition](https://www.google.com/search?q=ImageNet+large+scale+visual+recognition)

---