# jQuery 的設計哲學

## 「Write Less, Do More」

jQuery 的口號是「Write Less, Do More」，強調用最少的程式碼完成最多的功能。

## Chain API

### 設計原理

jQuery 的大部分方法都會返回 jQuery 物件，支援鍊式調用：

```javascript
$('#element')
    .addClass('active')
    .fadeIn()
    .click(handler)
    .trigger('customEvent');
```

### end() 方法

```javascript
$('div')
    .find('.header')    // 返回找到的元素
    .addClass('title')   // 操作這些元素
    .end()               // 返回 div
    .find('.body')       // 繼續操作
    .hide();
```

## 工廠函數

### $ 函數

```javascript
// 選擇元素
$('#id')
$('.class')
$('div')

// 建立元素
$('<div>')
$('<div>', { class: 'container', text: 'Hello' })

// 包裝 DOM 元素
$(document.getElementById('id'))
```

## 外掛系統

### 如何開發外掛

```javascript
// 方法擴展
$.fn.myPlugin = function(options) {
    return this.each(function() {
        // 對每個元素操作
        $(this).addClass(options.className);
    });
};

// 使用
$('.item').myPlugin({ className: 'active' });
```

### 範例外掛

```javascript
// 公告輪播外掛
$.fn.carousel = function() {
    return this.each(function() {
        var $this = $(this);
        var index = 0;
        var items = $this.find('.item');

        setInterval(function() {
            items.eq(index).hide();
            index = (index + 1) % items.length;
            items.eq(index).show();
        }, 3000);
    });
};
```

## 實用函數

### \$.each

```javascript
$.each([1, 2, 3], function(index, value) {
    console.log(index + ': ' + value);
});

$.each({ name: 'John', age: 30 }, function(key, value) {
    console.log(key + ': ' + value);
});
```

### \$.extend

```javascript
var defaults = { timeout: 5000, autoHide: true };
var options = { timeout: 3000 };

var settings = $.extend({}, defaults, options);
// { timeout: 3000, autoHide: true }
```

## 結論

jQuery 的設計哲學是簡潔、直覺和可擴展。這些原則使其成為前端開發的利器。

---

**延伸閱讀**

- [DOM 操作與選擇器](focus2.md)
- [jQuery+official+site](https://www.google.com/search?q=jQuery+official+site)