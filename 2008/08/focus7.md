# YSlow 與效能法則

## Yahoo 效能法則

### 14 條法則

```python
yslow_rules = [
    '1. 減少 HTTP 請求',
    '2. 使用 CDN',
    '3. 添加 Expires 頭',
    '4. Gzip 元件',
    '5. 將 CSS 放在頂部',
    '6. 將 JS 放在底部',
    '7. 避免 CSS 表示式',
    '8. 使用外部 JS 和 CSS',
    '9. 減少 DNS 查詢',
    '10. 精簡 JavaScript',
    '11. 避免重新導向',
    '12. 刪除重複腳本',
    '13. 設定 ETag',
    '14. 讓 Ajax 可快取'
]
```

## 評分系統

### YSlow 等級

```python
grades = {
    'A': '100-90 分，優秀',
    'B': '89-80 分，良好',
    'C': '79-70 分，一般',
    'D': '69-60 分，較差',
    'E': '59-0 分，很差'
}
```

### 評分項目

```python
yslow_components = {
    'ycdn': '使用 CDN',
    'yexpires': 'Expires 頭設定',
    'ycompress': 'Gzip 壓縮',
    'ycsstop': 'CSS 在頂部',
    'yjsbottom': 'JS 在底部',
    'yexpressions': 'CSS 表示式',
    'yexternal': '外部資源',
    'ydns': 'DNS 查詢次數',
    'yminify': '精簡程式碼',
    'yredirects': '重新導向',
    'ydupjs': '重複腳本',
    'yetags': 'ETag 設定',
    'xcache': '快取 Ajax'
}
```

## 工具使用

### 安裝 YSlow

```html
<!-- 安裝 YSlow 書籤工具 -->
<a href="javascript:(function(){...})()">YSlow</a>
```

### Firebug 整合

```javascript
// YSlow 可以與 Firebug 整合
// 顯示網頁效能分析結果
```

## 改進建議

### 優先順序

```python
# 高優先順序改進
high_priority = [
    '啟用 Gzip 壓縮',
    '新增 Expires 頭',
    '合併 JS/CSS 檔案'
]

# 中優先順序改進
medium_priority = [
    '使用 CDN',
    'DNS 預讀取',
    '優化圖片大小'
]

# 低優先順序改進
low_priority = [
    '刪除重複腳本',
    '避免重新導向',
    '設定 ETag'
]
```

## 結論

YSlow 提供了系統化的效能優化方法。遵循這些法則可以顯著提升網站效能。

---

**延伸閱讀**

- [Yahoo+performance+rules](https://www.google.com/search?q=Yahoo+performance+rules+14)
- [YSlow+firefox](https://www.google.com/search?q=YSlow+firebug)