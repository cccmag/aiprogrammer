# ML vs 傳統程式設計

## 兩種編程典範的比較

傳統程式設計和機器學習代表了兩種截然不同的解決問題方式。

### 傳統程式設計

傳統程式的核心是「明確規則」。開發者分析問題，設計演算法，用程式碼實現邏輯：

```python
# 傳統方式：手寫規則判斷水果
def classify_fruit(weight, color, texture):
    if color == "red" and weight < 150:
        return "cherry"
    elif color == "yellow" and texture == "smooth":
        return "banana"
    elif color == "orange" and weight > 100:
        return "orange"
    else:
        return "unknown"
```

這種方式在規則明確時非常有效，但有以下限制：
- 規則數量可能爆炸性成長
- 規則之間可能互相矛盾
- 無法處理規則難以定義的問題（如辨識照片中的物體）

### 機器學習方式

機器學習的方式截然不同——開發者不寫規則，而是提供範例：

```python
from sklearn.ensemble import RandomForestClassifier

# 機器學習方式：從資料中學習規則
clf = RandomForestClassifier()
clf.fit(features, labels)  # 特徵和對應的水果名稱

# 學習完成後，模型自己學會了分類規則
prediction = clf.predict(new_fruit_features)
```

## 什麼時候用什麼？

### 傳統程式設計更適合的情況

- **規則明確且穩定**：稅務計算、排序搜尋
- **需要精確保證**：飛控系統、醫療設備
- **邏輯鏈條可追溯**：除錯需要知道「為什麼」
- **資料量不足**：無法收集足夠的訓練資料

### 機器學習更適合的情況

- **規則難以定義**：影像辨識、語音辨識、情感分析
- **模式會變化**：詐騙偵測模式會隨時間演進
- **需要預測**：股價預測、需求預測
- **大規模個人化**：推薦系統

## 混合模式：最佳實務

現代軟體開發中，傳統程式和機器學習通常是互補的：

```
┌──────────────────────────────────────┐
│            應用程式                     │
│  ┌─────────┐    ┌─────────┐          │
│  │傳統程式碼│    │ ML 模型  │          │
│  │ - 路由   │    │ - 預測   │          │
│  │ - 驗證   │    │ - 分類   │          │
│  │ - 流程   │    │ - 推薦   │          │
│  │ - UI    │    │ - 異常檢測│          │
│  └─────────┘    └─────────┘          │
└──────────────────────────────────────┘
```

典型例子：一個垃圾郵件過濾系統
- 傳統程式處理郵件接收、使用者設定、規則過濾
- ML 模型判斷郵件是否為垃圾郵件
- 兩者協同工作

## 思維轉變：從規則到資料

從傳統程式轉向 ML 需要三個關鍵思維轉變：

### 1. 從 if-else 到機率

傳統程式的判斷是布林值（真/假）；ML 的判斷是機率（有 85% 可能是垃圾郵件）。

### 2. 從精確到統計

傳統程式追求 100% 正確；ML 追求高準確率但接受一定錯誤。

### 3. 從手動到自動

傳統程式的手動調參變成了 ML 模型的自動學習。

## 結論

傳統程式設計和機器學習不是二選一的選擇題。聰明的開發者會根據問題特性選擇合適的工具，甚至將兩者結合。在 AI 時代，理解這兩種編程典範的差異和互補性，是每個開發者必備的素養。

---

## 延伸閱讀

- [傳統程式 vs ML 比較](https://www.google.com/search?q=traditional+programming+vs+machine+learning)
- [ML 專案流程](https://www.google.com/search?q=machine+learning+project+workflow)
- [軟體工程結合 ML](https://www.google.com/search?q=ml+in+software+engineering)
