# Google Wave：協作平台的新想像

## 前言

2009 年 5 月，Google 在 Google I/O 大會上發表了 Google Wave，這是一個結合即時通訊、文件和社交網路的新型協作平台。Google Wave 使用 HTML 5 技術，重新定義了網頁應用的可能性。

## Google Wave 是什麼？

### 核心理念

```markdown
Google Wave 的願景：

1. 統一通訊
   - 即時訊息
   - 電子郵件
   - 部落格
   - 社交網路

2. 即時協作
   - 多人在同一檔案上工作
   - 看到每個人的游標
   - 就像在同一個房間

3. 對話為核心
   - 不是「發送訊息」
   - 而是「在 Wave 中新增內容」
   - 對話永遠可見、可回覆
```

### 與傳統工具的比較

```
電子郵件 vs 即時通訊 vs Google Wave：

電子郵件：
- 發送 -> 接收 -> 回覆
- 離線無法編輯
- 附件大小限制

即時通訊：
- 即時聊天
- 無歷史記錄（通常）
- 不適合長篇討論

Google Wave：
- 即時 + 離線無縫切換
- 完整歷史
- 可嵌入多媒體
- 就像文件的對話
```

## 技術架構

### HTML 5 的應用

Google Wave 是 HTML 5 技術的先驅：

```javascript
// 即時通訊 - WebSocket
var wave = new WebSocket('wss://wave.google.com/wave');

wave.onopen = function() {
  wave.send(JSON.stringify({
    type: 'join',
    waveId: 'google.com!wave'
  }));
};

wave.onmessage = function(event) {
  var delta = JSON.parse(event.data);
  updateWavelet(delta);
};

// 離線支援 - Web Storage
if (localStorage) {
  localStorage.setItem('draft', JSON.stringify(wavelet.getState()));
}
```

### 操作轉換（Operational Transformation）

```javascript
// Google Wave 使用 OT 來處理並發編輯

// 使用者 A 的操作
var opA = {
  type: 'insert',
  position: 5,
  text: 'Hello'
};

// 使用者 B 的操作
var opB = {
  type: 'insert',
  position: 3,
  text: 'World'
};

// 轉換操作以保持一致
var transformedOp = transform(opA, opB);

// 結果：「WorldHello」
```

## 主要功能

### 1. 即時共同編輯

```javascript
// Wave 中的共同編輯

// 每個參與者可以看到彼此的游標
wavelet.on('participant_cursor', function(event) {
  var user = event.participantId;
  var position = event.position;
  renderCursor(user, position);
});

// 即時文字同步
wavelet.on('blip_content_changed', function(event) {
  var content = event.content;
  updateDisplay(content);
});
```

### 2. 嵌入式多媒體

```javascript
// 在 Wave 中嵌入各種類型的內容

// 地圖
wave.createBlip({
  type: 'gadget',
  gadget: 'http://wave.google.com/gadgets/map.xml',
  state: {
    center: '台北',
    zoom: 10
  }
});

// 影像
wave.createBlip({
  type: 'image',
  url: 'http://example.com/photo.jpg',
  caption: '團隊照片'
});

// 投票
wave.createBlip({
  type: 'gadget',
  gadget: 'http://wave.google.com/gadgets/poll.xml',
  state: {
    question: '下週開會時間？',
    options: ['週一', '週二', '週三']
  }
});
```

### 3. 機器人（Robots）

```javascript
// Google Wave 機器人

var robot = new Robot('my-robot@appspot.com');

robot.onWaveletJoin = function(wavelet) {
  wavelet.createBlip().append('Hello! 我是翻譯機器人。');
};

robot.onBlipSubmitted = function(blip) {
  var content = blip.getContent();

  // 翻譯內容
  if (content.includes('[translate]')) {
    var translated = translate(content, 'zh', 'en');
    blip.createReply().append(translated);
  }
};
```

### 4. Gadgets

```javascript
// Wave Gadget - 小工具

var gadget = {
  kind: 'http://wave.google.com/tools/gadget',
  state: {
    title: '投票 Gadget',
    votes: {}
  },
  render: function() {
    return '<div class="poll">' +
           '<h3>' + this.state.title + '</h3>' +
           Object.keys(this.state.votes).map(opt =>
             '<button>' + opt + '</button>'
           ).join('') +
           '</div>';
  }
};
```

## Wave 的協議

### Federation Protocol

```markdown
Google Wave Federation：

1. 開放協議
   - 任何人都可以建立 Wave 伺服器
   - 不同的 Wave 服務可以互通

2. 協定設計
   - 類似 email 的分散式設計
   - 使用 XMPP 進行點對點通信

3. 協定棧：
   ┌────────────────────────────┐
   │      Wave Client (JS)      │
   ├────────────────────────────┤
   │      Wave Server           │
   ├────────────────────────────┤
   │      Federation Protocol   │
   ├────────────────────────────┤
   │      XMPP / HTTP           │
   └────────────────────────────┘
```

## 對未來的影響

### Web 應用的啟示

```markdown
Google Wave 展示的 HTML 5 能力：

1. WebSocket
   - 真正的即時通信
   - 雙向通信

2. Canvas
   - 遊戲
   - 圖形編輯

3. 離線應用
   - Web Storage
   - Application Cache

4. Web Workers
   - 後台處理
   - 不阻塞 UI
```

### 協作工具的演進

```
2009 年：Google Wave
     ↓
2010 年：Google+、Facebook 聊天
     ↓
2011 年：Google Docs 整合即時協作
     ↓
2012 年：Slack 诞生
     ↓
2013+ 年：更多即時協作工具興起
```

## 局限與批評

### 2009 年的問題

```markdown
Google Wave 的挑戰：

1. 複雜度
   - 學習曲線陡峭
   - 一般用戶難以理解

2. 效能
   - 即時同步延遲
   - 大量資料傳輸

3. 商業模式
   - 不清楚如何獲利
   - 缺乏明確的價值定位

4. 市場時機
   - 2009 年網路基礎設施不足
   - HTML 5 支援有限
```

## 結語

雖然 Google Wave 在 2012 年被終止，但它展示了 Web 應用的未來方向。即時協作、離線支援、WebSocket 通信——這些概念後來都被整合進了現代的 Web 應用中。

## 延伸閱讀

- [Google Wave 發布](https://www.google.com/search?q=Google+Wave+announcement+2009)
- [Google Wave 技術架構](https://www.google.com/search?q=Google+Wave+technical+architecture)
- [Operational Transformation](https://www.google.com/search?q=Operational+Transformation+algorithm)
- [Google Wave 的影響](https://www.google.com/search?q=Google+Wave+impact+on+web+apps)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*