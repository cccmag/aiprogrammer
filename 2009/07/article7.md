# Facebook 推出人臉辨識功能：臉部偵測技術普及

## 前言

2009 年，Facebook 推出了人臉偵測和標籤建議功能，這是機器學習技術在社交網路上的大規模應用。這個功能引發了隱私權的熱烈討論，也讓更多人接觸到了人工智慧技術。

## 人臉辨識技術的背景

### 技術發展歷程

```
人臉辨識技術發展：

1960s：研究開始
1970s：幾何特徵方法
1980s：模板匹配
1990s：特徵臉（Eigenface）
2000s：局部特徵分析
2009：深度學習興起
```

### 機器學習方法

```python
# 簡化的人臉偵測流程

def detect_faces(image):
    # 1. 載入訓練資料
    positive_examples = load_images('faces/')
    negative_examples = load_images('non_faces/')

    # 2. 提取特徵
    features = []
    for img in positive_examples + negative_examples:
        features.append(extract_haar_features(img))

    # 3. 訓練分類器
    classifier = train_svm(features, labels)

    # 4. 滑動視窗偵測
    detections = []
    for window in sliding_window(image):
        if classifier.predict(window) > threshold:
            detections.append(window)

    # 5. 非極大值抑制
    return non_max_suppression(detections)
```

## Facebook 的實作

### 標籤建議功能

```javascript
// Facebook 使用機器學習來建議照片標籤

// 輸入：上傳的照片
// 輸出：可能的標籤建議

function suggestTags(photo) {
  // 1. 人臉偵測
  var faces = faceDetector.detect(photo);

  // 2. 對每個人臉提取特徵
  var embeddings = faces.map(face =>
    neuralNetwork.extractEmbedding(face)
  );

  // 3. 與已知用戶比對
  var suggestions = embeddings.map(embedding => {
    // 在資料庫中搜尋最相似的人臉
    return findMostSimilarUser(embedding);
  });

  return suggestions;
}
```

### 隱私問題

```markdown
隱私疑慮：

1. 未經同意的臉部資料收集
   - Facebook 在用戶上傳照片時自動偵測人臉
   - 即使不標記，也會分析人臉

2. 資料儲存
   - 人臉特徵被永久儲存
   - 可能被用於其他目的

3. 第三方存取
   - 廣告商可能存取
   - 政府機構可能要求提供

4. 資料遷移
   - 用戶無法輕易導出或刪除
```

## 技術架構

### 深度學習模型

```
人臉辨識系統架構：

┌────────────────────────────────────────┐
│           輸入：照片                    │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│       人臉偵測（Haar Cascades）          │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│     特徵提取（CNN / DeepFace）           │
│     - 128 維度嵌入向量                  │
│     - 去識別化的人臉表示                │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│        比對（向量相似度搜尋）            │
│     - 已知用戶資料庫                    │
│     - K-NN 搜尋                        │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│          輸出：標籤建議                 │
└────────────────────────────────────────┘
```

### 即時處理

```javascript
// 在上傳照片時即時處理
async function processUpload(file) {
  // 1. 壓縮圖片
  var image = await loadImage(file);

  // 2. 偵測人臉
  var faces = await detectFaces(image);

  // 3. 提取嵌入
  var embeddings = faces.map(extractEmbedding);

  // 4. 比對用戶
  for (var embedding of embeddings) {
    var match = await findUserMatch(embedding);
    if (match.confidence > 0.8) {
      suggestTag(match.user);
    }
  }
}
```

## 對社交網路的影響

### 使用者體驗改變

```markdown
正面影響：
+ 更容易標記朋友
+ 組織照片更方便
+ 發現未標記的照片

負面影響：
- 隱私侵犯
- 標籤濫用
- 錯誤識別
```

### 社交媒體的 AI 應用

```
2009 年的社交媒體 AI：

Facebook：
- 人臉偵測
- 標籤建議
- 新聞流排序

Google：
- Google Goggles 影像搜尋
- Picasa 人臉組織

Twitter：
- 圖片識別（有限）
```

## 法律和道德問題

### 2009 年的法律框架

```markdown
各地區的隱私法規：

美國：
- 伊利諾伊州 BIPA（生物特徵資訊隱私法）
- 加州 CCPA
- 聯邦法律不足

歐盟：
- GDPR 當時仍在討論中（2010年生效）
- 嚴格的臉部資料保護

亞洲：
- 日本：個人資訊保護法
- 韓國：資訊通信網路法
```

### 用戶權利

```javascript
// 用戶可以關閉人臉辨識

// 在隱私設定中
settings.faceRecognition = false;

// 刪除已儲存的人臉資料
// （2009年此功能不完善）
```

## 結語

Facebook 的人臉辨識功能是 AI 技術在社交網路上的大規模應用。雖然這個功能帶來了便利，但也引發了對隱私的深刻反思。

## 延伸閱讀

- [Facebook 人臉辨識技術](https://www.google.com/search?q=Facebook+face+recognition+2009)
- [人臉辨識隱私問題](https://www.google.com/search?q=face+recognition+privacy+issues)
- [人臉辨識技術歷史](https://www.google.com/search?q=face+recognition+technology+history)
- [機器學習人臉偵測](https://www.google.com/search?q=machine+learning+face+detection)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*