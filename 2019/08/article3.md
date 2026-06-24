# React 16.9：Concurrent Mode 接近完成

## 前言

React 16.9 於 2019 年 7 月正式發布。這個版本標誌著 Concurrent Mode 接近完成，為未來的 React 17 打下基礎。

## Concurrent Mode 的意義

### 什麼是 Concurrent Mode？

Concurrent Mode 是 React 的一組新功能，允許 React 同時準備多個 UI 版本：

```jsx
// Concurrent Mode 的特性
// 1. 可中斷的渲染
// 2. 優先級調度
// 3. Suspense for data fetching
```

### 優先級調度

```
高優先級更新：用戶輸入、點擊
低優先級更新：資料獲取、列表渲染
```

---

## 新的 Hooks

### useEffect 的非同步 cleanup

```jsx
useEffect(() => {
    let cancelled = false;
    fetchData().then(data => {
        if (!cancelled) {
            setData(data);
        }
    });
    return () => { cancelled = true; };
}, []);
```

---

## 結語

React 16.9 為未來的 Concurrent Mode 鋪平了道路，React 的未來令人期待。

---

**延伸閱讀**

- [React 16.9](https://www.google.com/search?q=React+16.9+release+notes)
- [Concurrent Mode](https://www.google.com/search?q=React+concurrent+mode)