# 事件處理與委派

## 事件綁定

### 基本事件

```javascript
$('#button').click(function() {
    alert('Clicked!');
});

$('#button').dblclick(function() {
    alert('Double clicked!');
});

$('#input').focus(function() {
    $(this).addClass('focused');
});

$('#input').blur(function() {
    $(this).removeClass('focused');
});
```

### 快捷方法

```javascript
// 滑鼠事件
.click()      .dblclick()
.mouseenter() .mouseleave()
.mouseover()  .mouseout()
.hover()      // mouseenter + mouseleave

// 鍵盤事件
.keypress()   // 按鍵
.keydown()    // 按下
.keyup()      // 放開

// 表單事件
.submit()     .reset()
.change()     .select()

// 文件事件
.ready()      // DOM 就緒
.load()       // 載入完成
.unload()     // 離開頁面
```

### hover 方法

```javascript
$('#menu li').hover(
    function() { // mouseenter
        $(this).addClass('hover');
    },
    function() { // mouseleave
        $(this).removeClass('hover');
    }
);
```

## 事件處理函數

### event 物件

```javascript
$('#element').click(function(event) {
    console.log(event.type);     // 'click'
    console.log(event.target);   // 觸發元素
    console.log(event.currentTarget); // 當前元素
    console.log(event.pageX);     // 滑鼠 X
    console.log(event.pageY);     // 滑鼠 Y
    console.log(event.which);     // 鍵盤/滑鼠按鍵
    console.log(event.preventDefault()); // 阻止默認
    console.log(event.stopPropagation()); // 阻止冒泡
});
```

### 事件委託

```javascript
// 直接綁定（對每個 matched 元素）
$('#list li').click(handler);

// 委託到父元素（在父元素上監聽）
$('#list').delegate('li', 'click', handler);

// 動態元素也需要事件時，用委託
$('#list').on('click', 'li', handler);
```

### 委託的優勢

```javascript
// 假設列表動態新增項目
$('#list').on('click', 'li', function() {
    // 新增的 li 也會有事件
    $(this).toggleClass('active');
});
```

## 自訂事件

### 觸發自訂事件

```javascript
// 觸發事件
$('#element').trigger('myCustomEvent');
$('#element').triggerHandler('myCustomEvent');

// 带資料
$('#element').trigger('myCustomEvent', { key: 'value' });
```

### 監聽自訂事件

```javascript
$('#element').on('myCustomEvent', function(event, data) {
    console.log(data.key); // 'value'
});
```

## 一次性事件

```javascript
// 只執行一次
$('#button').one('click', function() {
    alert('This will show only once!');
});
```

## 移除事件

```javascript
// 移除所有 click 事件
$('#button').off('click');

// 移除特定處理函數
function handler() {
    alert('Clicked!');
}
$('#button').on('click', handler);
$('#button').off('click', handler);

// 移除所有事件
$('#button').off();
```

## 命名空間

```javascript
// 使用命名空間
$('#button').on('click.pluginName', handler);
$('#button').on('mouseenter.pluginName', handler);

// 只移除命名空間下的事件
$('#button').off('click.pluginName');

// 觸發特定命名空間的事件
$('#button').trigger('click.pluginName');
```

## 結論

jQuery 的事件系統功能完整且易用。事件委託是處理動態元素的首選方案。

---

**延伸閱讀**

- [DOM 操作與選擇器](focus2.md)
- [Ajax 與非同步請求](focus4.md)
- [jQuery+events](https://www.google.com/search?q=jQuery+events+tutorial)