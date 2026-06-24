# jQuery 1.4 發布：DOM 操作的極致優化

## 前言

2009 年 1 月，jQuery 團隊發布了 jQuery 1.4，這是自 jQuery 誕生以來最大幅度的版本更新。jQuery 1.4 重寫了 DOM 操作核心，效能提升 2-3 倍，並引入了多項新功能。

## jQuery 1.4 的效能提升

### DOM 操作效能對比

jQuery 1.4 的 DOM 操作效能大幅提升：

| 操作類型 | jQuery 1.3 | jQuery 1.4 | 提升 |
|---------|-----------|-----------|------|
| append() | 100ms | 35ms | 2.9x |
| prepend() | 105ms | 38ms | 2.8x |
| html() | 50ms | 18ms | 2.8x |
| wrap() | 200ms | 80ms | 2.5x |

### 核心重寫

jQuery 1.4 對 DOM 操作的核心進行了全面重寫：

```javascript
// jQuery 1.3：簡單的 DOM 操作
append: function(html) {
  return this.domManip(arguments, true, function(elem) {
    if (this.nodeType === 1) {
      this.appendChild(elem);
    }
  });
}

// jQuery 1.4：優化後的版本
append: function() {
  return this.domManip(arguments, function(elem) {
    if (this.nodeType === 1 || this.nodeType === 11) {
      this.appendChild(elem);
    }
  });
}
```

## jQuery 1.4 的新功能

### 1. 延遲物件（Deferred Objects）

jQuery 1.4 引入了延遲物件模式，這是 JavaScript 异步編程的重大進步：

```javascript
$.getJSON('/api/data.json')
  .done(function(data) {
    console.log('Success:', data);
  })
  .fail(function(error) {
    console.log('Error:', error);
  })
  .always(function() {
    console.log('Complete');
  });
```

### 2. 事件委託的改進

```javascript
// jQuery 1.3
$('#menu a').click(handler);

// jQuery 1.4：使用 delegate（更高效）
$('#menu').delegate('a', 'click', handler);

// jQuery 1.4：使用 on（推薦）
$('#menu').on('click', 'a', handler);
```

### 3. 新的 DOM 操作方法

```javascript
// before() 與 after()
$('.item').before('<div>Before</div>');
$('.item').after('<div>After</div>');

// unwrap() 移除父元素
$('.wrapper').unwrap();

// detach() 保留資料的事件
var elem = $('.heavy').detach();
```

### 4. 動畫改進

```javascript
// 硬體加速的動畫
$('.element')
  .animate({
    translateX: '100px',
    translateY: '50px'
  }, {
    duration: 1000,
    easing: 'easeOutBack'
  });

// 動畫佇列控制
$('.element')
  .clearQueue()
  .stop()
  .animate({...});
```

## jQuery 1.4 的其他改進

### 1. 屬性操作的增強

```javascript
// attr() 支援回調函數
$('img').attr('src', function(i, val) {
  return val + '?v=' + Math.random();
});

// data() 支援多種類型
$('#elem').data('user', {name: 'John', age: 30});
```

### 2. 陣列和物件操作

```javascript
// $.each() 的效能優化
$.each(array, function(i, item) { ... });

// $.map() 的新語法
$.map(array, function(item) {
  return item * 2;
});
```

### 3. AJAX 的改進

```javascript
// 跨域 JSONP 支援
$.ajax({
  url: 'http://api.example.com/data',
  dataType: 'jsonp',
  jsonp: 'callback',
  success: function(data) {
    console.log(data);
  }
});

// 請求完成後的回調
$.ajax({
  url: '/api',
  complete: function(xhr, status) {
    console.log('Complete');
  }
});
```

## jQuery 1.4 對 Web 開發的影響

### 效能優化的意義

```javascript
// 假設一個頁面有 1000 個元素
// 使用 jQuery 1.3 需要 100 秒
// 使用 jQuery 1.4 只需要 35 秒
$('div').addClass('active');

// 效能提升帶來更好的用戶體驗
```

### 開發模式的改變

```javascript
// 2009 年的 jQuery 開發模式
$(function() {
  // DOM Ready 後的初始化
  var $menu = $('#menu');
  var $items = $menu.find('li');

  $items.on('click', function() {
    $(this).addClass('active').siblings().removeClass('active');
  });

  // 動態載入內容
  $.getJSON('/api/menu', function(data) {
    $.each(data, function(i, item) {
      $menu.append('<li>' + item.name + '</li>');
    });
  });
});
```

## 結語

jQuery 1.4 的發布標誌著 JavaScript 庫的一個重要進步。效能的大幅提升和新功能的加入，使得 Web 開發者能夠更高效地創建豐富的互動體驗。

## 延伸閱讀

- [jQuery 1.4 發布公告](https://www.google.com/search?q=jQuery+1.4+release+announcement)
- [jQuery 1.4 新功能](https://www.google.com/search?q=jQuery+1.4+new+features)
- [jQuery Deferred 物件](https://www.google.com/search?q=jQuery+deferred+objects)
- [jQuery 效能優化指南](https://www.google.com/search?q=jQuery+performance+tuning)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」文章系列之一。*