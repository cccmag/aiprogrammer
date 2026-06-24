# 程式語言演化：Ruby、Python、JavaScript

## Ruby 與 Rails

### Ruby on Rails 的成功

```python
# Ruby on Rails 的影響
# 2007 年 Rails 生态
rails_highlights = {
    'Basecamp': '37signals 的旗艦產品',
    'Twitter': '早期使用 Rails，展示了擴展能力',
    'GitHub': '2008 年上線，基於 Rails',
    'YouTube': '早期使用 Rails',
    'Shopify': '電子商務平台'
}

# Rails 的設計哲學
rails_principles = [
    'Convention over Configuration',
    'Don\'t Repeat Yourself (DRY)',
    'RESTful 設計',
    '敏捷開發友好'
]
```

### Ruby 1.8.6

```ruby
# Ruby 1.8.6 特性
# - 完整的物件導向
# - 動態型別
# - 區塊和迭代器
# - 元程式能力
```

## Python

### Python 2.5 的改進

```python
# Python 2.5（2006 年 9 月）在 2007 年的影響
python_25_features = [
    'with 語句（上下文管理）',
    'try/except/finally 合併',
    '條件表達式 (x if cond else y)',
    '明確相對導入',
    'Windows 的 ctypes',
]

# Django 的繁榮
django_2007 = {
    'Django 0.96': '2007 年 10 月發布',
    'Django 之光': '成為主流 Web 框架',
    '社群成長': '文件和教學資源豐富'
}
```

### Python 的應用領域

```python
# Python 的應用
python_applications = {
    'Web 開發': 'Django, Flask, Pyramid',
    '科學計算': 'NumPy, SciPy',
    '系統管理': 'Fabric, Ansible 前身',
    '遊戲開發': 'Pygame',
    '嵌入式': 'Python for S60',
}
```

## JavaScript

### JavaScript 框架大爆發

```javascript
// 2007 年的 JavaScript 框架
var frameworks_2007 = {
    'jQuery': '1.1.2 版本，DOM 操作簡化',
    'Prototype': '1.6 版本，Ruby 風格',
    'Dojo': '1.0 正式版，企業級',
    'Ext JS': '2.0 版本，UI 元件豐富',
    'MooTools': '1.11 版本，模組化設計',
    'YUI': '2.3 版本，Yahoo 出品'
};

// jQuery 的簡潔性
$('#button').click(function() {
    $('#result').load('/api/data');
});

// Prototype 的物件導向
var MyClass = Class.create({
    initialize: function(name) {
        this.name = name;
    },
    greet: function() {
        return 'Hello, ' + this.name;
    }
});
```

### AJAX 的普及

```javascript
// AJAX 的標準模式
function fetchData(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            callback(JSON.parse(xhr.responseText));
        }
    };
    xhr.send();
}

// 使用 jQuery
$.getJSON('/api/data', function(data) {
    console.log(data);
});
```

## 結語

2007 年是程式語言的轉捩點：
- Ruby 證明了敏捷開發的效率
- Python 鞏固了 Web 開發的地位
- JavaScript 從「玩具語言」變成「主流語言」

---

## 延伸閱讀

- [programming+languages+2007+review](https://www.google.com/search?q=programming+languages+2007+review)

---