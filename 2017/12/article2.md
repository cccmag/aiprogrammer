# JavaScript 生態：Node.js 與前端框架

## 前言

JavaScript 在 2017 年繼續是 Web 開發的核心語言，Node.js 8 LTS 和前端框架都有重要進展。

## Node.js 8 LTS

```javascript
// Node.js 8 新特性

// 1. async/await 原生支援
async function fetchData() {
    try {
        const response = await fetch('https://api.example.com/data');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

// 2. HTTP/2 支援
const http2 = require('http2');
const fs = require('fs');

const server = http2.createSecureServer({
    key: fs.readFileSync('server-key.pem'),
    cert: fs.readFileSync('server-cert.pem')
});

// 3. N-API (原生模組介面)
const napi = require('./my-native-module');
```

## 前端框架

### React 16

```jsx
// React 16 新特性

// 1. Fragment
function List() {
    return (
        <>
            <li>Item 1</li>
            <li>Item 2</li>
        </>
    );
}

// 2. Portal
const modal = ReactDOM.createPortal(
    <Modal />,
    document.getElementById('modal-root')
);

// 3. Error Boundaries
class ErrorBoundary extends React.Component {
    componentDidCatch(error, info) {
        console.error('Error:', error);
    }

    render() {
        return this.props.children;
    }
}
```

### Vue.js 2.5

```javascript
// Vue.js 2.5 改進

// 更好的 TypeScript 支援
import Vue from 'vue';
import Component from 'vue-class-component';

@Component
export default class MyComponent extends Vue {
    message = 'Hello';

    get reversedMessage() {
        return this.message.split('').reverse().join('');
    }
}
```

## 2017 年前端工具

```
┌─────────────────────────────────────────────────────────┐
│              2017 年前端工具鏈                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  構建工具:                                            │
│  - Webpack 3/4                                        │
│  - Rollup                                             │
│  - Parcel                                            │
│                                                         │
│  預處理器:                                            │
│  - Babel 7 (beta)                                    │
│  - PostCSS                                            │
│  - TypeScript 2.x                                     │
│                                                         │
│  測試:                                               │
│  - Jest 20+                                          │
│  - Cypress                                           │
│  - Puppeteer                                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## AI 在 JavaScript

```javascript
// TensorFlow.js (2018年3月正式發布)
const model = tf.sequential();
model.add(tf.layers.dense({units: 128, activation: 'relu', inputShape: [784]}));
model.add(tf.layers.dense({units: 10, activation: 'softmax'}));

// 訓練
model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
});

await model.fit(xTrain, yTrain, {epochs: 10});
```

---

**延伸閱讀**

- [Node.js Official](https://www.google.com/search?q=Node.js+official)
- [React 16 Blog](https://www.google.com/search?q=React+16+release)

---

*本篇文章為「AI 程式人雜誌 2017 年 12 月號」年終回顧系列之一。*