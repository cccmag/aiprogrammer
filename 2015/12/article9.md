# 2015 網頁標準進展

## ECMAScript 2015（ES6）

### 重要里程碑

ES6 在 2015 年正式成為標準：

- **Classes**
- **Arrow Functions**
- **Promises**
- **Modules**
- **Template Literals**

## HTTP/2

### 標準化完成

HTTP/2 在 2015 年正式發布：

| 特性 | HTTP/1.1 | HTTP/2 |
|------|---------|--------|
| 多工 | 無 | 是 |
| Header 壓縮 | 無 | 是 |
| Server Push | 無 | 是 |
| 單一連線 | 否 | 是 |

## Service Workers

### 離線應用

Service Workers 在 2015 年獲得主流瀏覽器支援：

```javascript
// 註冊 Service Worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}

// sw.js
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

## WebAssembly

### 進展

WebAssembly 在 2015 年持續發展：

- **規範制定**：基本完成
- **工具鏈**：Emscripten 支援
- **瀏覽器支援**：Firefox Nightly

## WebGL 2.0

### 新功能

- 更好的效能
- 3D 紋理
- 多渲染目標
- 實例化繪製

## 小結

Web 標準在 2015 年取得了長足進步。

---

## 延伸閱讀

- [ES6 Features](https://www.google.com/search?q=ES6+features+tutorial)
- [HTTP/2 Specification](https://www.google.com/search?q=HTTP2+specification)
- [Service Worker Guide](https://www.google.com/search?q=Service+Worker+tutorial)