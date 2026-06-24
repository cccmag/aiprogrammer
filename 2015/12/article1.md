# React 0.14 新功能解析

## 主要變化

React 0.14 是近年來最大的更新之一：

1. **ReactDOM 分離**：DOM 相關功能獨立
2. **Stateless Functions**：無狀態函數元件
3. **Ref 改進**：更靈活的 ref 處理
4. **Server Rendering**：效能提升

## ReactDOM 分離

```javascript
// 舊版
var React = require('react');

// 新版
var React = require('react');
var ReactDOM = require('react-dom');

ReactDOM.render(<App />, document.getElementById('root'));
```

## 無狀態函數元件

```javascript
// 舊版：需要類別
class HelloMessage extends React.Component {
  render() {
    return <div>Hello {this.props.name}</div>;
  }
}

// 新版：函數
const HelloMessage = (props) => (
  <div>Hello {props.name}</div>
);
```

## Ref 改進

```javascript
// 舊版：字串 ref
<input ref="myInput" />

// 新版：回調 ref
<input ref={(node) => this.myInput = node} />
```

## 小結

React 0.14 為未來的架構優化奠定基礎。

---

## 延伸閱讀

- [React 0.14 Release Notes](https://www.google.com/search?q=React+0.14+release+notes)
- [React Documentation](https://www.google.com/search?q=React+official+documentation)