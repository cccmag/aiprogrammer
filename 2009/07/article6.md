# Google 發布語音搜尋 API：聲控時代來臨

## 前言

2009 年，Google 發布了語音搜尋 API，讓開發者可以將語音辨識功能整合到網頁應用中。這項技術的開放，標誌著語音介面時代的來臨。

## Google 語音搜尋的技術背景

### 語音辨識的發展

```
語音辨識技術發展：

1950s：基本的數字辨識
1960s：元音識別
1970s：詞彙量增加到數千詞
1980s：隱藏馬爾可夫模型（HMM）
1990s：連續語音辨識
2000s：統計模型和深度學習
2009：Google 雲端語音辨識 API
```

### Google 的優勢

```markdown
Google 語音辨識的優勢：

1. 大規模資料
   - 搜尋查詢作為訓練資料
   - 數十億個語音樣本

2. 機器學習
   - 深層神經網路
   - 持續學習和改進

3. 雲端運算
   - 強大的伺服器處理能力
   - 即時辨識

4. 多語言支援
   - 超過 30 種語言
   - 方言和口音適應
```

## 語音搜尋 API 的功能

### 基本用法

```html
<input type="text" x-webkit-speech />
```

```javascript
// 監聽語音輸入事件
document.querySelector('input').addEventListener('webkitspeechchange', function(e) {
  console.log('辨識結果：', e.results[0][0].transcript);
  console.log('置信度：', e.results[0][0].confidence);
});
```

### 語音辨識屬性

```html
<input type="text"
       x-webkit-speech
       speech="true"
       x-webkit-grammar="builtin:search"
       lang="zh-TW"
/>
```

### JavaScript API

```javascript
var recognition = new webkitSpeechRecognition();

recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'zh-TW';

recognition.onresult = function(event) {
  for (var i = event.resultIndex; i < event.results.length; i++) {
    if (event.results[i].isFinal) {
      console.log('最終結果：', event.results[i][0].transcript);
    } else {
      console.log('臨時結果：', event.results[i][0].transcript);
    }
  }
};

recognition.start();
```

## 語音搜尋的應用場景

### 1. 行動搜尋

```javascript
// 在智慧手機上使用語音搜尋
if ('webkitSpeechRecognition' in window) {
  var recognition = new webkitSpeechRecognition();
  recognition.continuous = false;
  recognition.interimResults = false;

  // 啟動語音辨識
  recognition.start();

  recognition.onresult = function(event) {
    var query = event.results[0][0].transcript;
    window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query);
  };
}
```

### 2. 語音命令

```javascript
var commands = {
  '打開': function() { openApp(); },
  '關閉': function() { closeApp(); },
  '上一頁': function() { history.back(); },
  '下一頁': function() { history.forward(); }
};

recognition.onresult = function(event) {
  var command = event.results[0][0].transcript;
  if (commands[command]) {
    commands[command]();
  }
};
```

### 3. 語音輸入

```html
<textarea id="message"></textarea>

<script>
var textarea = document.getElementById('message');
var recognition = new webkitSpeechRecognition();

recognition.continuous = true;
recognition.interimResults = true;

recognition.onresult = function(event) {
  var transcript = '';
  for (var i = event.resultIndex; i < event.results.length; i++) {
    transcript += event.results[i][0].transcript;
  }
  textarea.value = transcript;
};

textarea.addEventListener('focus', function() {
  recognition.start();
});

textarea.addEventListener('blur', function() {
  recognition.stop();
});
</script>
```

## 技術規格

### 支援的屬性

| 屬性 | 說明 | 範例值 |
|------|------|--------|
| x-webkit-speech | 啟用語音輸入 | (布爾屬性) |
| lang | 辨識語言 | zh-TW, en-US |
| x-webkit-grammar | 語法 | builtin:search |
| maxlength | 最大長度 | 100 |

### 辨識結果結構

```javascript
{
  results: [
    {
      0: {
        transcript: "辨識的文字",
        confidence: 0.95
      },
      isFinal: true
    }
  ]
}
```

## 對未來的影響

### 語音介面的興起

```markdown
語音介面的優勢：

1. 雙手自由
   - 駕駛時
   - 做飯時
   - 運動時

2. 打字速度
   - 每分鐘 150 字
   - 比打字快 3 倍

3. 包容性
   - 視障人士
   - 肢體障礙者
   - 識字能力有限者
```

### 與其他技術的結合

```javascript
// 語音 + AI
// 語音辨識 + 自然語言處理
// 創造更智能的語音介面

var nlp = require('natural');

recognition.onresult = function(event) {
  var transcript = event.results[0][0].transcript;

  // 意圖識別
  if (transcript.includes('天氣')) {
    // 處理天氣查詢
  } else if (transcript.includes('新聞')) {
    // 處理新聞查詢
  } else if (transcript.includes('翻譯')) {
    // 處理翻譯
  }
};
```

## 挑戰與限制

### 2009 年的挑戰

```markdown
語音搜尋的限制：

1. 準確度
   - 背景噪音
   - 多人說話
   - 方言口音

2. 隱私
   - 音訊傳送到伺服器
   - 儲存和處理記錄

3. 網路依賴
   - 需要網路連接
   - 離線無法使用

4. 跨瀏覽器支援
   - 主要 WebKit 支援
   - 其他瀏覽器落後
```

## 結語

Google 語音搜尋 API 的發布，標誌著語音介面進入 Web 開發的時代。雖然 2009 年的技術還有諸多限制，但這開啟了一個新的可能性。

## 延伸閱讀

- [Google 語音搜尋 API](https://www.google.com/search?q=Google+speech+recognition+API+2009)
- [Web Speech API 規格](https://www.google.com/search?q=Web+Speech+API+specification)
- [語音辨識技術歷史](https://www.google.com/search?q=speech+recognition+technology+history)
- [語音介面的未來](https://www.google.com/search?q=future+of+voice+interface)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*