# 微服務架構的興起

## 前言

微服務是一種將應用拆分為小型、獨立服務的架構模式。

## 單體 vs 微服務

```
單體架構：              微服務架構：
───────────            ────────────
┌─────────────────┐    ┌──────┐ ┌──────┐ ┌──────┐
│                 │    │ User │ │ Order│ │  Pay │
│   全部功能      │    │Service│ │Service│ │Service│
│   在同一程式    │    └──────┘ └──────┘ └──────┘
│                 │         │         │
└─────────────────┘    ┌─────────────────┐
                       │   API Gateway   │
                       └─────────────────┘
```

## Node.js 與微服務

Node.js 的輕量特性非常適合微服務：

- 快速啟動
- 低記憶體占用
- 豐富的 npm 生態系

## 通信方式

```javascript
// 同步（HTTP/REST）
const response = await fetch('http://user-service/users/1');

// 訊息佇列（RabbitMQ/Kafka）
channel.sendToQueue('user.created', Buffer.from(JSON.stringify(user)));
```

---

## 延伸閱讀

- [微服務架構設計](https://www.google.com/search?q=microservices+architecture+Node.js)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*