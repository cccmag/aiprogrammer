# Prototype.js 1.6：Ruby 風格的 DOM 操作

## 前言

Prototype.js 是最早流行的 JavaScript 框架之一。1.6 版本帶來了多項改進，使其成為 Ruby on Rails 專案的標準選擇。

## Prototype 的核心特色

### 美元符號函數

```javascript
// 取代 document.getElementById
$('elementId');

// 取代 document.getElementsByClassName
$$('.className');

// DOM 元素擴展
$('myForm').serialize(); // 表單序列化
$('myInput').focus();    // 聚焦
```

### 鏈式 API

```javascript
// 鏈式呼叫
$('items').select('.active')
          .invoke('show')
          .first()
          .addClassName('highlighted');
```

### Ajax 支援

```javascript
new Ajax.Request('/api/data', {
    method: 'get',
    parameters: { format: 'json' },
    onSuccess: function(transport) {
        var data = transport.responseJSON;
        updateUI(data);
    },
    onFailure: function(transport) {
        showError('請求失敗');
    }
});
```

## Rails 整合

Prototype.js 與 Ruby on Rails 的整合是其成功的關鍵：

```ruby
# Rails 的 link_to_remote
link_to_remote "更新", :update => "result",
    :url => { :action => "update_status" },
    :complete => "alert('完成')"
```

## 結語

Prototype.js 的簡潔 API 影響了後續的 JavaScript 框架設計。雖然後來被 jQuery 超越，但 Prototype 的設計理念——擴展原生物件——至今仍有影響。

---

## 延伸閱讀

- [Prototype+JavaScript+framework](https://www.google.com/search?q=Prototype+JavaScript+framework)
- [Prototype+1.6+features](https://www.google.com/search?q=Prototype+1.6+features)

---