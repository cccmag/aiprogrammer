# 本期焦點

## Web 2.0 與互聯網革命

### 引言

2007 年，Web 2.0 的概念已經深入人心。這不是一個技術的更新，而是一種思考網路的新方式。Tim O'Reilly 在 2004 年提出的 Web 2.0 概念，正在深刻改變我們使用網路的方式。

從 AJAX 技術的成熟，到社交媒體的崛起；從 Mashup 混搭服務的興起，到開放 API 的普及，Web 2.0 代表了一個以使用者為中心的網路新時代。

在本期內容中，我們將深入探討這場網路革命的各個層面。

---

## 大綱

* [程式：AJAX 技術實作](focus_code.md)
   - XMLHttpRequest 詳解
   - jQuery AJAX 方法
   - JSON 資料交換

1. [Web 2.0 的概念與起源](focus1.md)
   - O'Reilly 的 Web 2.0 七原則
   - 從 Web 1.0 到 Web 2.0
   - 網路平台的轉變

2. [AJAX 技術的成熟](focus2.md)
   - XMLHttpRequest 的故事
   - 非同步交互的優勢
   - 前端框架的繁榮

3. [社交媒體的崛起](focus3.md)
   - YouTube 與影片分享
   - Facebook 的社交圖
   - Twitter 的微型部落格

4. [Mashup 與開放 API](focus4.md)
   - Google Maps API
   - 混搭服務的商業模式
   - 開放平台的興起

5. [部落格與使用者生成內容](focus5.md)
   - 部落格文化
   - Wikipedia 的成功
   - 使用者創作的價值

6. [Firefox 與開源瀏覽器](focus6.md)
   - Mozilla 專案
   - Firefox 的崛起
   - 瀏覽器標準之爭

7. [未來展望：Web 的下一步](focus7.md)
   - HTML 5 的願景
   - 即時 Web
   - 物聯網與 Web

---

## 濃縮回顧

### Web 2.0 七原則

Tim O'Reilly 提出的 Web 2.0 七原則：

```
┌────────────────────────────────────────────────────────┐
│            Web 2.0 七原則                               │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 網路作為平台                                       │
│     └─ 軟體即服務（SaaS）                              │
│                                                        │
│  2. 集體智慧                                           │
│     └─ 利用使用者群體的貢獻                            │
│                                                        │
│  3. 資料是核心                                         │
│     └─ 資料擁有網路效應                                │
│                                                        │
│  4. 軟體的少數定律                                     │
│     └─ 開放取代封閉，少數引導多數                      │
│                                                        │
│  5. 永遠的 Beta                                       │
│     └─ 持續改進，即時部署                              │
│                                                        │
│  6. 粒狀組成                                           │
│     └─ 元件化，可混搭                                  │
│                                                        │
│  7. 豐富的使用者體驗                                   │
│     └─ AJAX、DHTML、RIA                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Web 1.0 vs Web 2.0

```
┌────────────────────────────────────────────────────────┐
│          Web 1.0 vs Web 2.0                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Web 1.0：                                            │
│  - 讀為主                                              │
│  - 大型入口網站                                        │
│  - 靜態內容                                            │
│  - 封閉平台                                            │
│  - 少數內容創作者                                      │
│                                                        │
│  Web 2.0：                                            │
│  - 讀/寫                                              │
│  - 社交網路                                            │
│  - 動態內容                                            │
│  - 開放平台                                            │
│  - 多數內容創作者                                      │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 代表性服務

| 類別 | Web 1.0 | Web 2.0 |
|------|---------|---------|
| 搜尋 | Yahoo 目錄 | Google |
| 百科 | Britannica Online | Wikipedia |
| 內容 | CNN 官方網站 | YouTube |
| 商務 | Amazon 1.0 | Amazon 平台 |
| 社交 | BBS、留言板 | Facebook |
| 軟體 | 授權軟體 | SaaS |

---

## AJAX 的核心技術

### XMLHttpRequest

```javascript
// 原始 XMLHttpRequest 用法
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/data', true);
xhr.onreadystatechange = function() {
    if (xhr.readyState == 4 && xhr.status == 200) {
        var data = JSON.parse(xhr.responseText);
        console.log(data);
    }
};
xhr.send();
```

### jQuery AJAX

```javascript
// jQuery 封裝的 AJAX
$.ajax({
    url: '/api/data',
    type: 'GET',
    dataType: 'json',
    success: function(data) {
        $('#result').html(data.content);
    },
    error: function(xhr) {
        console.error('Error:', xhr.status);
    }
});

// 簡化版本
$.get('/api/data', function(data) {
    $('#result').html(data);
});

$.post('/api/submit', { name: 'John' }, function(response) {
    console.log(response);
});
```

### JSON 資料格式

```javascript
// JSON 替代 XML
// XML
<user>
    <name>John</name>
    <age>30</age>
</user>

// JSON
{
    "name": "John",
    "age": 30
}
```

---

## 社交媒體的興起

### YouTube 的成功

```
┌────────────────────────────────────────────────────────┐
│              YouTube 發展歷程                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  2005 年 2 月：聯合創辦人陳士駿、Steve Chen、         │
│                 Chad Hurley 創立 YouTube              │
│                                                        │
│  2006 年：                                            │
│  - 每日觀看次數突破 1 億                              │
│  -  Google 以 16.5 億美元收購                        │
│                                                        │
│  2007 年：                                            │
│  - 每日上傳影片超過 6 萬                              │
│  -  成為全球最大影片分享平台                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Facebook 的社交圖

Facebook 提出的「社交圖」概念，改變了我們對社交網路的理解：

```javascript
// 社交圖查詢
FB.api('/me/friends', function(response) {
    // 取得所有朋友
    console.log(response.data);
});

// 朋友的動態
FB.api('/me/home', function(response) {
    // 取得動態消息
});
```

---

## 開放 API 的商業模式

### Mashup 範例

```javascript
// Google Maps + Twitter = 地理推文地圖
function displayTweetsOnMap(tweets) {
    tweets.forEach(function(tweet) {
        if (tweet.geo) {
            var marker = new google.maps.Marker({
                position: tweet.geo,
                map: map,
                title: tweet.user.name + ': ' + tweet.text
            });
        }
    });
}
```

### API 經濟

```
┌────────────────────────────────────────────────────────┐
│              API 經濟的興起                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  平台提供 API 吸引開發者：                             │
│  - Twitter API → 大量第三方用戶端                     │
│  - Facebook API → 社交遊戲                           │
│  - Google Maps API → 地圖應用                        │
│  - Amazon API → 電子商務整合                         │
│                                                        │
│  商業模式：                                            │
│  - 付費 API                                            │
│  - 廣告分潤                                            │
│  - 生態系建設                                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 結論

Web 2.0 不僅是技術術語，更是一種思考網路的新範式。它代表著：

- 從封閉到開放
- 從讀到讀/寫
- 從少數創作者到多數創作者
- 從大型入口到社交網路

2007 年是 Web 2.0 概念深入人心的年份，這場革命的影響將持續多年。

---

## 延伸閱讀

- [Web 2.0 概念](focus1.md)
- [AJAX 技術](focus2.md)
- [社交媒體](focus3.md)
- [Mashup](focus4.md)
- [部落格文化](focus5.md)
- [開源瀏覽器](focus6.md)
- [未來展望](focus7.md)

---

*本期焦點到此結束。下期我們將探討程式語言多樣化的主題，敬請期待。*