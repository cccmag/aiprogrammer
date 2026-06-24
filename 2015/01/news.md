# 本月新知

## 2015 年 1 月程式技術動態

### 程式語言與框架

**Node.js 0.12 正式發布**

Node.js 社群於本月發布 0.12 版本，這是 2014 年 io.js 分支後的首次重要更新。Node.js 0.12 帶來了革命性的效能提升：

- **V8 引擎升級**：整合 V8 3.28 版，支援 ES6 更多的特性
- **原生 Promise**：無需 polyfill 即可使用 Promise
- **cluster 模組改進**：支援更多負載平衡策略
- **效能提升**：基準測試顯示 HTTP 吞吐量提升約 40%

```
Node.js 0.12 效能對比：
──────────────────────
請求/秒：0.10 → 0.12：+40%
記憶體使用：減少 15%
啟動時間：加快 25%
```

**npm 2.0 隆重登場**

npm 2.0 帶來了更智慧的依賴管理機制：

- **扁平化依賴樹**：減少磁碟空間占用
- **更嚴格的版本控制**：避免依賴地獄
- **可配置的 scripts**：更靈活的生命週期鉤子
- **離線安裝**：支援本地快取安裝

```bash
# npm 2.0 新增功能
npm install --save-optional  # 可選依賴
npm install --save-dev       # 開發依賴
npm ls                       # 檢視依賴樹
```

### 前端開發

**React 0.13 發布**

Facebook 發布 React 0.13，引入了重大架構變革：

- **React.addons 拆離**：官方附加元件移至獨立套件
- **setState 回調**：更好的狀態管理
- **代碼熱載入**：開發體驗大幅提升

```javascript
// React 0.13 的新写法
class MyComponent extends React.Component {
  handleClick() {
    this.setState({ active: true }, () => {
      console.log('State updated!');
    });
  }
  render() {
    return <button onClick={this.handleClick}>Click</button>;
  }
}
```

**AngularJS 1.4 開發中**

AngularJS 團隊宣布 1.4 版本將引入：
- 更容易的國際化（i18n）支援
- 改進的動畫 API
- 效能優化與記憶體泄漏修復

### JavaScript 標準

**ES6 規範定案準備中**

ECMAScript 6（又稱 ES2015）規範於 2015 年 6 月正式定案，本月是最後的準備階段：

- **Block Scoping**：`let` 和 `const` 關鍵字
- **Arrow Functions**：`=>` 語法糖
- **Classes**：`class` 語法支援
- **Modules**：`import` 和 `export`
- **Promises**：原生 Promise 物件
- **Template Literals**：模板字串

```javascript
// ES6 新特性預覽
const PI = 3.14159;
let name = 'World';

const greet = (name) => `Hello, ${name}!`;

class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return greet(this.name);
  }
}

export default Person;
```

### 開發工具

**Browserify 穩定支援**

Browserify 作為前端模組打包工具持續獲得關注，讓 Node.js 風格的 `require()` 可以跑在瀏覽器中。

**Webpack 1.0 穩定版**

Webpack 1.0 的發布讓前端建置工具更加成熟：
- 支援多種模組格式（CommonJS、AMD、ES6）
- 豐富的 loader 生態系
- 程式碼分割與懶載入

### 設計與使用者體驗

**Google Material Design 全面推廣**

Google 發布 Material Design 設計語言，引領 UI 設計趨勢：

- **層次感**：基於紙張與墨水的視覺隱喻
- **動畫**：有意義的轉場動畫
- **色彩系統**：鮮豔的強調色與中性底色
- **圖示**：統一的網格系統

### 業界動態

- **Facebook 開源更多專案**：Flow、Yarn 等工具相繼開源
- **微軟發布 Visual Studio Code** 預覽版：跨平台輕量級編輯器
- **GitHub 突破 500 萬使用者**：開源運動持續壯大
- **npm 註冊套件數突破 150,000**：JavaScript 生態系蓬勃發展

### 標準與規範

- **HTTP/2 標準進入最後審查階段**：預計 2015 年中正式通過
- **WebSocket 協定廣泛支援**：即時通訊應用更普及
- **W3C 推動 Web Components 標準**：组件化開發的未來

---

*本期新知到此結束。下期我們將深入探討 Node.js 與伺服端 JavaScript 的世界。*