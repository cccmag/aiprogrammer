# DOM 操作與選擇器

## jQuery 選擇器

### 基本選擇器

```javascript
// ID 選擇器
$('#header')

// 類別選擇器
$('.item')

// 標籤選擇器
$('div')

// 所有元素
$('*')
```

### 複合選擇器

```javascript
// 多個選擇器
$('div, .item, #header')

// 交集
$('div.container')

// 後代
$('div .item')

// 直接子元素
$('ul > li')

// 同胞元素
$('#prev ~ .sibling')
```

### 屬性選擇器

```javascript
$('[href]')                      // 有 href 屬性
$('[href="#"]')                  // href 等於 #
$('[href!="#"]')                 // href 不等於 #
$('[href^="https"]')             // href 開頭為 https
$('[href$=".pdf"]')              // href 結尾為 .pdf
$('[href*="google"]')            // href 包含 google
```

### 位置選擇器

```javascript
$('li:first')    // 第一個
$('li:last')     // 最後一個
$('li:even')     // 偶數（0-indexed）
$('li:odd')      // 奇數
$('li:eq(2)')    // 指定索引
$('li:gt(2)')    // 大於索引
$('li:lt(2)')    // 小於索引
```

### 表單選擇器

```javascript
$(':text')      // 文字輸入
$(':password')  // 密碼輸入
$(':radio')     // 單選
$(':checkbox')   // 複選
$(':submit')    // 提交
$(':reset')      // 重設
$(':button')     // 按鈕
$(':file')       // 檔案選擇
```

## DOM 操作

### 屬性操作

```javascript
// 讀取屬性
$('a').attr('href')

// 設定屬性
$('a').attr('href', 'http://example.com')

// 移除屬性
$('a').removeAttr('href')

// 讀取 HTML
$('#content').html()

// 設定 HTML
$('#content').html('<p>New content</p>')

// 讀取文字
$('#content').text()

// 設定文字
$('#content').text('Hello')
```

### 類別操作

```javascript
// 新增類別
$('#element').addClass('active')

// 移除類別
$('#element').removeClass('active')

// 切換類別
$('#element').toggleClass('active')

// 是否有類別
$('#element').hasClass('active')
```

### CSS 操作

```javascript
// 讀取 CSS
$('#element').css('color')

// 設定 CSS
$('#element').css('color', 'red')
$('#element').css({
    color: 'red',
    fontSize: '14px'
})
```

### 尺寸操作

```javascript
// 內容尺寸
$('#element').width()    // 寬度
$('#element').height()   // 高度

// 內邊距尺寸
$('#element').innerWidth()
$('#element').innerHeight()

// 外邊距尺寸（含邊框）
$('#element').outerWidth()
$('#element').outerHeight()

// 相對於文件的位置
$('#element').offset()
$('#element').position()
```

## 建立元素

```javascript
// 基本建立
$('<div>')
$('<div>Hello</div>')

// 带屬性和內容
$('<div>', {
    id: 'container',
    class: 'box',
    text: 'Hello World'
})

// 完整範例
var $div = $('<div>', {
    id: 'myDiv',
    class: 'container',
    css: { backgroundColor: 'blue' }
}).text('Hello');

$('body').append($div);
```

## 結論

jQuery 的選擇器強大而直覺，配合鏈式 API，可以優雅地完成複雜的 DOM 操作。

---

**延伸閱讀**

- [jQuery 的設計哲學](focus1.md)
- [事件處理與委派](focus3.md)
- [jQuery+selectors](https://www.google.com/search?q=jQuery+selectors+tutorial)