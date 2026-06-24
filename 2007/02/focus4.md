# Mashup 與開放 API

## 前言

Mashup 是 Web 2.0 時代的代表性應用形態。將多個來源的內容和服務組合在一起，創造出全新的價值。

## Mashup 的定義

### 什麼是 Mashup

```
┌────────────────────────────────────────────────────────┐
│              Mashup 的概念                            │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Mashup = 混合 + 應用                                  │
│                                                        │
│  將兩個或多個來源的內容/服務                           │
│  組合在一起，創造新的應用                               │
│                                                        │
│  範例：                                               │
│  - Google Maps + 房屋租金 → 房屋地圖                  │
│  - Google Maps + 犯罪資料 → 治安地圖                  │
│  - Amazon + Facebook → 推薦好友買過的商品             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Google Maps API 的成功

### 開放 API 的先驅

```javascript
// Google Maps API 範例
var map = new GMap2(document.getElementById("map"));
map.setCenter(new GLatLng(25.0330, 121.5654), 13);

var marker = new GMarker(new GLatLng(25.0330, 121.5654));
map.addOverlay(marker);
```

### 經典 Mashup

```
┌────────────────────────────────────────────────────────┐
│          經典 Google Maps Mashup                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  HousingMaps.com：                                    │
│  - Craigslist 房租 + Google Maps                      │
│  - 第一個著名的商業 Mashup                            │
│                                                        │
│  Chicago Crime：                                      │
│  - 犯罪資料 + 地圖                                    │
│  - 可視化犯罪熱點                                     │
│                                                        │
│  WikiMapia：                                          │
│  - Wikipedia + 地圖                                  │
│  - 协作式地圖編輯                                     │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 開放 API 的商業模式

### 為何要開放 API

```python
# 開放 API 的動機
API_OPEN_REASONS = {
    "擴大生態": "吸引開發者建立應用",
    "創新加速": "汇集更多創意",
    "品牌推廣": "透過應用接觸用戶",
    "資料價值": "資料產生網路效應"
}
```

### API 經濟

```
┌────────────────────────────────────────────────────────┐
│              API 經濟模型                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  按量付費：                                           │
│  - AWS、Google Cloud                                 │
│  - 免費額度 + 超用收費                                │
│                                                        │
│  免費 + 付費分層：                                    │
│  - Twitter API、GitHub API                           │
│  - 基本功能免費，高級功能付費                          │
│                                                        │
│  開發者補貼：                                          │
│  - Facebook 早期補貼開發者                            │
│  - 建立生態系                                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Mashup 技術棧

### 2007 年的 Mashup 技術

```javascript
// 典型 Mashup 架構
var MASHUP_STACK = {
    "前端": "HTML + CSS + JavaScript (jQuery)",
    "地圖": "Google Maps API / Yahoo! Maps",
    "資料": "Yahoo! Pipes / 公開 API",
    "托管": "Amazon S3 / Google App Engine"
};
```

## 結論

Mashup 展示了 Web 2.0 時代「組合式創新」的力量。開放 API 讓任何人都能站在巨人的肩膀上，創造新的價值。

---

## 延伸閱讀

- [Google Maps API 歷史](https://www.google.com/search?q=Google+Maps+API+history)
- [Mashup 應用](https://www.google.com/search?q=Mashup+applications+2007)

---

*本篇文章為「AI 程式人雜誌 2007 年 2 月號」本期焦點系列文章。*