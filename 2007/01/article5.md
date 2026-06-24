# Facebook Platform 開放：社交網路平台化

## 前言

2007 年 5 月 24 日，Facebook 宣布開放 Facebook Platform，讓協力廠商開發者能夠在 Facebook 平台上建立應用程式。這開啟了社交網路平台化的時代。

## Facebook Platform 的發布

### 2007 年的 Facebook

當時的 Facebook 已經擁有超過 2000 萬活躍用戶，並正在快速增長：

```
┌────────────────────────────────────────────────────────┐
│          Facebook Platform 發布背景                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  發布日期：2007 年 5 月 24 日                          │
│                                                        │
│  用戶數量：                                            │
│  - 2007 年 5 月：~2000 萬                             │
│                                                        │
│  開放前的功能：                                        │
│  - 個人頁面                                           │
│  - 塗鴉牆                                             │
│  - 相片分享                                           │
│  - 基本社群功能                                        │
│                                                        │
│  開發者社群：                                          │
│  - 非常想要建立 Facebook 應用                          │
│  - 大量非官方 API 出現                                 │
│  - Facebook 終於回應需求                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## FBML 與 API

### Facebook Markup Language

FBML 是一種允許開發者建立 Facebook 應用的標記語言：

```html
<!-- FBML 範例 -->
<fb:title>My Facebook App</fb:title>

<fb:name uid="12345" useyou="false" />

<fb:profile-pic uid="12345" size="small" />

<fb:if-is-app-user>
  <p>Welcome back!</p>
</fb:if-is-app-user>
```

### Facebook API

```javascript
// Facebook JavaScript API
Facebook.api('/me', function(response) {
  console.log('Hello, ' + response.name);
});

// 发布动态到用户涂鸦墙
Facebook.api('/me/feed', 'post', {
  message: 'Hello from my app!',
  link: 'http://example.com',
  picture: 'http://example.com/image.png',
  name: 'App Name',
  caption: 'Caption text',
  description: 'Description'
});
```

## Social Graph 的概念

### 開放社交圖

Facebook Platform 的核心是「社交圖」的概念：

```
┌────────────────────────────────────────────────────────┐
│              Facebook Social Graph                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│         [User]                                         │
│           │                                            │
│           ├── friends ──→ [User]                     │
│           ├── photos ──→ [Photo]                      │
│           ├── interests ──→ [Page]                    │
│           └── apps ──→ [Application]                 │
│                                                        │
│  透過 API，開發者可以存取這個圖中的元素                 │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### 社交圖範例

```javascript
// 取得用戶的社交圖
FB.api('/me/friends', function(response) {
  response.data.forEach(function(friend) {
    console.log(friend.name);
  });
});

// 取得用戶興趣
FB.api('/me/likes', function(response) {
  response.data.forEach(function(like) {
    console.log(like.name);
  });
});
```

## 第一波 Facebook 應用

### 2007 年的熱門應用

```
┌────────────────────────────────────────────────────────┐
│           早期 Facebook 應用                           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. 心理測驗類                                        │
│     - 「你是哪種動物？」                                │
│     - 「測試你的政治傾向」                              │
│                                                        │
│  2. 禮物類                                            │
│     - Super Wall (送禮物)                             │
│     - 收集虛擬物品                                     │
│                                                        │
│  3. 遊戲類                                            │
│     - 農場類游戲                                       │
│     - IQ 測試                                         │
│                                                        │
│  4. 工具類                                            │
│     - 照片增強                                         │
│     - 行事曆同步                                       │
│                                                        │
│  5. 社群類                                            │
│     - 投票系統                                         │
│     - 活動管理                                         │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## Platform 的商業模式

### 對開發者的吸引力

Facebook Platform 為開發者提供了前所未有的機會：

```python
# Facebook Platform 對開發者的價值
PLATFORM_VALUE = {
    "用戶獲取": "直接接觸 Facebook 用戶",
    "社交驗證": "用戶可以看看朋友在用什麼",
    "病毒式傳播": "easy to share = easy to grow",
    "基礎設施": "無需自建用戶系統",
    "貨幣化": "Virtual Currency ( Credits )"
}
```

### Virtual Currency

Facebook 後來推出的 Credits（虛擬貨幣）系統：

```javascript
// Credits 整合
Facebook.pay({
  method: 'pay',
  action: 'buy_item',
  quantity: 1
}, function(data) {
  if (data['order_id']) {
    // 購買成功
  } else if (data['error_code']) {
    // 錯誤處理
  }
});
```

## 隱私與控制之爭

### Facebook 的「Beacon」爭議

2007 年底，Facebook 推出了 Beacon 功能，自動將用戶在外部網站的活動發布到 Facebook。這引發了嚴重的隱私爭議：

```
┌────────────────────────────────────────────────────────┐
│             Beacon 隱私風波                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  問題：                                                │
│  - 未經明確同意就發布用戶活動                          │
│  - 與外部網站共享用戶資料                              │
│  - 用戶難以完全關閉                                    │
│                                                        │
│  結果：                                                │
│  - 大量用戶反感                                       │
│  - 隱私團體批評                                       │
│  - Facebook 最終修改機制                              │
│  - 教訓：社交功能不能犧牲隱私                          │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 平台化的影響

### 對社交網路的影響

Facebook Platform 的開放象徵著社交網路從「產品」轉變為「平台」：

| 面向 | 封閉模式 | 平台模式 |
|------|----------|----------|
| 應用數量 | 有限 | 指數成長 |
| 創新生態 | 內部創新 | 外部創新 |
| 用戶忠誠 | 對產品忠誠 | 對生態忠誠 |
| 商業模式 | 廣告為主 | 平台費用 |

## 結論

Facebook Platform 的開放，標誌著社交網路平台化時代的來臨。這種模式後來被 Twitter、Instagram 等其他平台借鑒，成為互聯網平台公司的標準策略。

然而，平台化也帶來了新的挑戰：隱私保護、應用審核、使用者資料的控制——這些問題至今仍是社交平台需要面對的核心議題。

---

## 延伸閱讀

- [Facebook Platform 發布](https://www.google.com/search?q=Facebook+Platform+launch+2007)
- [FBML 文件](https://www.google.com/search?q=FBML+Facebook+Markup+Language)
- [Facebook API 歷史](https://www.google.com/search?q=Facebook+API+history)

---

*本篇文章為「AI 程式人雜誌 2007 年 1 月號」文章集錦系列。*