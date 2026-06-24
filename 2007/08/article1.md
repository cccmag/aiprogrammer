# Firefox 3 Alpha：下一世代瀏覽器

2007 年，Mozilla 正在開發 Firefox 3，代號「Gran Paradiso」。這個版本帶來了革命性的效能提升和豐富的功能改進。

## 主要改進

### Gecko 1.9 渲染引擎

Firefox 3 採用了全新的 Gecko 1.9 渲染引擎，帶來了更好的效能和標準相容性。

### Places 書籤系統

```javascript
// Firefox 3 Places API
PlacesUtils.bookmarks.insert({
    parentGuid: PlacesUtils.bookmarks.toolbarGuid,
    title: "Google",
    url: "https://www.google.com"
});

// 標籤功能
PlacesUtils.tagging.tagURL(url, ["search", "web"]);
```

### 改進的密碼管理

```javascript
// Firefox 3 增強的密碼管理
LoginManager.primaryAuth += "_" + hostname;

// 登入表單自動填寫增強
```

## 結語

Firefox 3 的開發標誌著開放原始碼瀏覽器繼續引領 Web 標準的發展。

---

*延伸閱讀：[Firefox 官方網站](https://developers.google.com/search/?q=firefox+official)*