# React 0.13 發布：全新代碼架構

## 前言

Facebook 發布 React 0.13，引入了重要的架構改進，為未來的 React 生態系奠定基礎。

## React.addons 拆離

```javascript
// 舊版（0.12）
var LinkedStateMixin = React.addons.LinkedStateMixin;

// 新版（0.13）
// 需要單獨安裝 react-addons-linked-state
import LinkedStateMixin from 'react-addons-linked-state';
```

## setState 回調

```javascript
// 0.13 新增 setState 回調
this.setState(
  { count: this.state.count + 1 },
  () => {
    console.log('狀態更新完成', this.state.count);
  }
);
```

## 新的生命周期鉤子

```javascript
class MyComponent extends React.Component {
  componentWillMount() {
    console.log('即將掛載');
  }

  componentDidMount() {
    console.log('已掛載');
  }

  componentWillReceiveProps(nextProps) {
    console.log('將接收新屬性');
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextProps.id !== this.props.id;
  }

  componentWillUpdate(nextProps, nextState) {
    console.log('即將更新');
  }

  componentDidUpdate(prevProps, prevState) {
    console.log('更新完成');
  }

  componentWillUnmount() {
    console.log('即將卸載');
  }
}
```

## 結論

React 0.13 為未來的 React 1.0 奠定了基礎，更清晰的 API 和更好的效能讓 React 生態系更加成熟。

---

## 延伸閱讀

- [React 0.13 發布說明](https://www.google.com/search?q=React+0.13+released+2015)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*