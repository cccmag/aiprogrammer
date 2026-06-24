# 電腦視覺發展

## 前言

電腦視覺（Computer Vision）是讓電腦能夠「看見」和理解影像的科學。2008 年時，傳統電腦視覺方法仍是主流，深度學習尚未在這個領域取得突破。

## 電腦視覺的基本任務

### 主要任務類型

```python
cv_tasks = {
    "影像分類": "辨識影像中的主要物件類別",
    "物體偵測": "找出影像中所有物件的位置",
    "語義分割": "對每個像素分類",
    "實例分割": "區分同類別的不同個體",
    "人臉偵測": "找出人臉的位置",
    "姿勢估計": "預測人體關鍵點"
}
```

### 傳統方法 vs 深度學習

```python
# 2008 年的技術對比

traditional_methods = {
    "特徵提取": "手動設計（SIFT, HOG）",
    "分類器": "SVM, AdaBoost, Random Forest",
    "優勢": "計算量小、可解釋性強",
    "劣勢": "難以處理複雜場景、泛化能力有限"
}

deep_learning = {
    "特徵學習": "自動學習層次化特徵",
    "分類器": "類神經網路端到端訓練",
    "優勢": "處理複雜場景能力強",
    "劣勢": "需要大量標註資料和計算資源"
}
```

## SIFT 特徵

### 尺度不變特徵轉換

David Lowe 在 1999 年發表的 SIFT 是最重要的電腦視覺演算法之一：

```python
sift_algorithm = {
    "發明者": "David Lowe",
    "年份": "1999",
    "全名": "Scale-Invariant Feature Transform",
    "特點": "對尺度、旋轉、亮度保持不變"
}
```

### SIFT 的步驟

```python
sift_steps = {
    "1. 尺度空間極值偵測": "在不同尺度尋找興趣點",
    "2. 興趣點定位": "精確確定位置和尺度",
    "3. 方向指定": "為每個興趣點指定方向",
    "4. 特徵描述子": "計算周圍區域的梯度方向直方圖"
}
```

### SIFT 描述子

```python
# SIFT 描述子的結構

sift_descriptor = {
    "梯度計算": "計算 16x16 區域內的梯度",
    "方向分配": "將 360 度分為 8 個方向區間",
    "形成向量": "4x4 區塊，每區塊 8 方向 = 128 維向量",
    "標準化": "對向量進行 L2 正規化"
}
```

## HOG 特徵

### 方向梯度直方圖

```python
# Navneet Dalal 和 Bill Triggs 在 2005 年提出

hog_features = {
    "全名": "Histogram of Oriented Gradients",
    "應用": "人臉偵測、行人偵測",
    "核心思想": "區域內的梯度方向分佈可以描述形狀"
}
```

### HOG 計算流程

```python
hog_calculation = {
    "1. 正規化": "對影像進行 gamma 正規化",
    "2. 梯度計算": "計算每個像素的梯度",
    "3. 細胞區塊": "將影像分為小區塊",
    "4. 直方圖": "每個細胞內計算梯度方向直方圖",
    "5. 區塊正規化": "相鄰細胞組成區塊後正規化"
}
```

## Haar 特徵

### 特徵選擇

```python
# Viola-Jones 人臉偵測使用的特徵

haar_features = {
    "類型": [
        "邊緣特徵（上下、左右）",
        "線條特徵（中心周圍）",
        "對角線特徵"
    ],
    "計算": "白色區域總和 - 黑色區域總和",
    "效率": "使用積分影像快速計算"
}
```

### 積分影像

```python
# 快速計算影像區域總和的方法

integral_image = {
    "定義": "每個位置的積分值等於左上角所有像素的總和",
    "好處": "任何大小的矩形區域都可以 O(1) 計算",
    "公式": "ii(x,y) = i(x,y) + ii(x-1,y) + ii(x,y-1) - ii(x-1,y-1)"
}
```

## 傳統物體偵測

### 滑動視窗方法

```python
# 傳統物體偵測的流程

sliding_window = {
    "1. 產生候選框": "不同位置和尺度的視窗",
    "2. 特徵提取": "對每個視窗提取 HOG/SIFT",
    "3. 分類": "使用 SVM 等分類器判斷是否包含物體",
    "4. 非極大值抑制": "合併重疊的偵測結果"
}
```

### DPM 方法

```python
# Deformable Part Models (Felzenszwalb et al., 2008)

dpm_method = {
    "發明者": "Felzenszwalb, McAllester, Ramanan",
    "概念": "每個物體由多個部件組成",
    "優勢": "對形變有一定的容忍度"
}
```

## 人臉偵測

### Viola-Jones 框架

2001 年 Viola 和 Jones 發表的即時人臉偵測框架是該領域的重大突破：

```python
viola_jones = {
    "貢獻": "第一個可在 CPU 上即時執行的人臉偵測器",
    "核心技術": [
        "Haar-like 特徵",
        "積分影像",
        "AdaBoost 分類器",
        "級聯分類器"
    ]
}
```

### 級聯分類器

```python
# 將多個分類器串聯，快速排除非人臉區域

cascade_classifier = {
    "結構": "多個強分類器串聯",
    "前面的分類器": "簡單，快速，盡可能排除負樣本",
    "後面的分類器": "複雜，準確，確認最終結果",
    "好處": "大多數負樣本在前幾層就被排除"
}
```

## 影像分類

### Bag of Visual Words

```python
# 借鑒文字分類的概念

bag_of_words = {
    "1. 特徵偵測": "使用 SIFT 等偵測興趣點",
    "2. 描述子計算": "計算每個興趣點的描述子",
    "3. 視覺詞典": "對所有描述子進行集群，建 Vocabulary",
    "4. 向量化": "計算每張影像中各視覺詞的頻率",
    "5. 分類": "使用 SVM 等分類器"
}
```

### 空間金字塔匹配

```python
# 加入空間資訊

spatial_pyramid = {
    "概念": "將影像分為多尺度區塊",
    "方法": "在每個尺度統計視覺詞直方圖",
    "好處": "捕捉空間佈局資訊"
}
```

## 資料集

### 2008 年的主要資料集

```python
datasets_2008 = {
    "Caltech 101": "101 類別影像，每類約 40-800 張",
    "Caltech 256": "256 類別，更具挑戰性",
    "PASCAL VOC": "20 類別，每年競賽",
    "LabelMe": "開放標註的影像資料庫"
}
```

### ImageNet 即將到來

```python
imagenet_intro = {
    "年份": "2009 年正式啟動",
    "規模": "1400 萬張影像，2 萬多類別",
    "影響": "成為影像分類的標準基準",
    "競賽": "ILSVRC 競賽（2010 年起）"
}
```

## 挑戰

### 困難場景

```python
challenges = {
    "照明變化": "光線明暗改變影響",
    "視角變化": "不同角度看到不同樣子",
    "遮擋": "物體被部分遮擋",
    "尺度變化": "同物體有不同大小",
    "類內差異": "同類物體差異可能很大"
}
```

### 維度災難

```python
# 處理高維度特徵的問題

curse_of_dimensionality = {
    "問題": "維度越高，需要的訓練樣本越多",
    "解決": "降維（PCA）、特徵選擇"
}
```

## 未來展望

### 深度學習的來臨

```python
# 2008 年後的發展

deep_learning_future = {
    "2012": "AlexNet 在 ImageNet 取得突破",
    "2013": "ZFNet、OverFeat",
    "2014": "VGG、GoogleNet",
    "2015": "ResNet 残差網路"
}
```

### 傳統方法的價值

```python
# 即使深度學習普及，傳統方法仍有價值

traditional_value = {
    "特徵可視化": "理解深度網路學到了什麼",
    "混合方法": "傳統特徵 + 深度學習",
    "理論基礎": "為電腦視覺提供理論框架"
}
```

---

**延伸閱讀**

- [Computer vision history](https://www.google.com/search?q=computer+vision+history)
- [SIFT+feature+extraction](https://www.google.com/search?q=SIFT+feature+extraction)
- [HOG+features+human+detection](https://www.google.com/search?q=HOG+features+human+detection)