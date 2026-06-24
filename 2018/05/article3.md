# React 16.3 新生命週期

## 前言

React 16.3 引入了新的生命週期方法，為未來的非同步渲染做準備。

## 新的生命週期

### static getDerivedStateFromProps

```javascript
static getDerivedStateFromProps(props, state) {
  if (props.userID !== state.lastUserID) {
    return { userID: props.userID };
  }
  return null;
}
```

### getSnapshotBeforeUpdate

```javascript
getSnapshotBeforeUpdate(prevProps, prevState) {
  return scrollPosition;
}

componentDidUpdate(prevProps, prevState, snapshot) {
  if (snapshot !== null) {
    scrollTo(snapshot);
  }
}
```

## 淘汰的生命週期

以下生命週期將在 React 17 淘汰：
- componentWillMount
- componentWillReceiveProps
- componentWillUpdate

## 結論

新的生命週期為未來的 Concurrent Mode 做準備。

---

**延伸閱讀**

- [React 官方網站](https://www.google.com/search?q=React+official+site)
- [React 16.3 發布說明](https://www.google.com/search?q=React+16.3+release+notes)