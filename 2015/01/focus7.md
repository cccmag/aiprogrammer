# 未來展望：Web Components、ECMAScript 2016+、Progressive Web Apps

## 前言

2015 年是 Web 技術的轉折點。HTML5、ES6、CSS3 為未來十年的 Web 發展奠定了基礎。本篇探討未來的技術方向。

## Web Components 組件化開發

### 核心概念

Web Components 是瀏覽器原生支援的組件化方案：

```
Web Components 三大技術：
─────────────────────────

1. Custom Elements（自訂元素）
   - 定義新的 HTML 標籤
   - <user-card></user-card>

2. Shadow DOM（影子 DOM）
   - 封裝樣式和結構
   - 外部樣式不影響內部

3. HTML Templates（HTML 範本）
   - <template> 標籤
   - 不會渲染的 DOM 片段

4. HTML Imports（HTML 引入）
   - 載入封裝好的元件
```

### Custom Elements

```javascript
// 定義自訂元素
class UserCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    const name = this.getAttribute('name');
    const avatar = this.getAttribute('avatar');

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          display: block;
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 16px;
          max-width: 300px;
        }
        img {
          width: 60px;
          height: 60px;
          border-radius: 50%;
        }
        h3 { margin: 8px 0; }
        p { color: #666; }
      </style>
      <div class="user-card">
        <img src="${avatar}" alt="${name}">
        <h3>${name}</h3>
        <p><slot></slot></p>
      </div>
    `;
  }
}

// 註冊元素
customElements.define('user-card', UserCard);
```

### 使用方式

```html
<!-- 使用自訂元素 -->
<user-card name="王小明" avatar="avatar.jpg">
  資訊工程師，專精 Web 開發
</user-card>

<!-- 支援屬性變更觀察 -->
<script>
  class UserCard extends HTMLElement {
    static get observedAttributes() {
      return ['name', 'avatar'];
    }

    attributeChangedCallback(name, oldValue, newValue) {
      // 屬性變更時自動更新
      this.render();
    }
  }
</script>
```

### Shadow DOM 封裝

```javascript
class Tooltip extends HTMLElement {
  constructor() {
    super();
    // 建立 Shadow DOM
    this.attachShadow({ mode: 'open' });
  }

  connectedCallback() {
    this.render();
  }

  render() {
    const text = this.getAttribute('text') || '';

    this.shadowRoot.innerHTML = `
      <style>
        :host {
          position: relative;
          display: inline-block;
        }
        .tooltip {
          visibility: hidden;
          background: #333;
          color: white;
          padding: 5px 10px;
          border-radius: 4px;
          position: absolute;
          bottom: 100%;
          left: 50%;
          transform: translateX(-50%);
          white-space: nowrap;
        }
        :host(:hover) .tooltip {
          visibility: visible;
        }
      </style>
      <slot></slot>
      <span class="tooltip">${text}</span>
    `;
  }
}

customElements.define('my-tooltip', Tooltip);
```

### HTML Imports（2015 年語法）

```html
<!-- 引入元件 -->
<link rel="import" href="user-card.html">

<!-- 使用 -->
<user-card name="測試"></user-card>
```

## ECMAScript 2016+ 未來展望

### ES2016 (ES7) 新特性

```javascript
// Array.prototype.includes
[1, 2, 3].includes(2);  // true
[1, 2, 3].includes(4);  // false

// 指數運算子
2 ** 3;   // 8
2 ** 4;   // 16
```

### 可能的 ES2017 (ES8) 特性

```javascript
// Async/Await（最終在 ES2017 定案）
async function fetchData() {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error(error);
  }
}

// Object.values / Object.entries
Object.values({ a: 1, b: 2 });  // [1, 2]
Object.entries({ a: 1, b: 2 }); // [['a', 1], ['b', 2]]

// 字串填充
'5'.padStart(3, '0');  // "005"
'5'.padEnd(3, '0');    // "500"
```

### TC39 流程

```
ECMAScript 新特性流程：
───────────────────────
1. Stage 0: Strawman（提案構想）
2. Stage 1: Proposal（正式提案）
3. Stage 2: Draft（草案）
4. Stage 3: Candidate（候選）
5. Stage 4: Finished（完成）

每年發布一次新版本
```

## Progressive Web Apps (PWA)

### 核心特徵

```
PWA 五大核心：
─────────────────

1. 響應式（Responsive）
   - 適合所有設備

2. 離線能力（Offline-capable）
   - Service Worker 實現

3. 類似應用（App-like）
   - 流暢的使用體驗

4. 安全（HTTPS required）
   - 安全傳輸

5. 可發現（Discoverable）
   - 可在搜尋引擎找到
```

### manifest.json

```json
{
  "name": "我的 Web 應用",
  "short_name": "MyApp",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#4A90E2",
  "icons": [
    {
      "src": "icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 安裝横幅

```javascript
let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredPrompt = e;

  // 顯示自訂安裝 UI
  showInstallButton();
});

async function installApp() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response: ${outcome}`);
    deferredPrompt = null;
  }
}
```

## 未來技術趨勢

### 預計 2015-2020 年的發展

```
Web 技術演進時間線：
─────────────────────

2015:
  ✓ ES6 定案
  ✓ HTML5 完成
  ✓ Service Worker 支援

2016:
  → ES2016 (includes, **)
  → PWA 概念成形
  → HTTP/2 普及

2017:
  → ES2017 (async/await)
  → WebAssembly 更成熟
  → CSS Grid 廣泛支援

2018:
  → ES2018 (async iteration)
  → Web Components 成熟
  → PWA 成為標準

2019:
  → ES2019 (optional catch)
  → CSS Houdini
  → PWAs 達到原生體驗
```

### 重要標準化進展

```
未來重要標準：
─────────────────

1. WebAssembly
   - 二進位格式執行
   - 接近原生效能

2. HTTP/2
   - 多工傳輸
   - 伺服器推送

3. WebGL / WebGPU
   - 3D 圖形硬體加速
   - 遊戲與視覺化

4. WebXR
   - VR/AR 體驗
   - 沉浸式網頁

5. Shape Detection
   - 臉部辨識
   - 條碼掃描
```

## 結語

2015 年標誌著 Web 開發新時代的開始。Web Components、ECMAScript 不斷演进、PWA 概念的成形，都預示著 Web 將變得越來越強大。未來的 Web 應用將擁有接近原生應用的體驗，同時保持跨平台的便利性。

---

## 延伸閱讀

- [Web Components 官方說明](https://www.google.com/search?q=Web+Components+custom+elements+Shadow+DOM)
- [PWA 開發指南](https://www.google.com/search?q=Progressive+Web+Apps+tutorial+2015)
- [ES Next 提案](https://www.google.com/search?q=TC39+ECMAScript+proposals+stage)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*