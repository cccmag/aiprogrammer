# 自然語言處理的 Web 介面

## Web Speech API

```javascript
var recognition = new webkitSpeechRecognition();
recognition.onresult = function(event) {
    console.log(event.results[0][0].transcript);
};
recognition.start();
```

## 聊天機器人

```javascript
function sendMessage(text) {
    $.post('/api/chat', { message: text }, function(response) {
        addMessage(response.reply, 'bot');
    });
}
```

## 結論

NLP 讓網頁更加智慧。

---

**延伸閱讀**

- [Web+Speech+API](https://www.google.com/search?q=Web+Speech+API+tutorial)