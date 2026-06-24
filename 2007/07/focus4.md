# 主題四：Prototype 框架

## Ruby 風格的 JavaScript

Prototype 是另一款在 2007 年極受歡迎的 JavaScript 框架，由 Sam Stephenson 開發。它以優雅的語法、對原生物件的擴展和 Ruby 風格的 API 設計，在 Rails 社群中獲得了廣泛的採用。

## Prototype 的設計理念

Prototype 的核心理念是「增強 JavaScript 內建物件」：

```javascript
// 擴展 String 物件
"hello".include("ell")    // true
"hello".strip()           // "hello"
"  hello  ".trim()        // "hello"

// 擴展 Array 物件
$A(document.getElementsByTagName("div"))  // 轉換為 Prototype 陣列
[1, 2, 3].first()         // 1
[1, 2, 3].last()          // 3
[1, 2, 3].without(2)      // [1, 3]

// 擴展 Function 物件
var greet = function(name) {
    return "Hello, " + name;
}.curry("World");         // 函式柯里化

greet();  // "Hello, World"
```

## 核心功能

### 美元函式 ($)

```javascript
// $() 是 document.getElementById() 的簡寫
$("header")              // 取得 ID 為 header 的元素
$("header", "footer")    // 取得多個元素

// $F() 取得表單元素的值
$F("username")           // 取得 ID 為 username 的輸入框值

// $H() 轉換為雜湊物件
$H({ name: "John", age: 30 }).toQueryString()
// "name=John&age=30"
```

### 美元雙重函式 ($$)

```javascript
// $$() 使用 CSS 選擇器
$$("div")                // 所有 div 元素
$$("#container p")       // container 內的所有 p
$$(".item.active")       // 有 active 類別的 item

// 支援更複雜的選擇器
$$("ul li:nth-child(even)")
```

### Ajax 請求

```javascript
// 基本 AJAX 請求
new Ajax.Request("/api/data", {
    method: "get",
    onSuccess: function(transport) {
        var data = transport.responseText.evalJSON();
        // 處理資料
    },
    onFailure: function(transport) {
        alert("請求失敗: " + transport.status);
    }
});

// POST 請求
new Ajax.Request("/api/submit", {
    method: "post",
    parameters: { name: "John", email: "john@example.com" },
    onSuccess: function(transport) {
        // 處理成功
    }
});

// 更新元素
new Ajax.Updater("result", "/api/content", {
    method: "get"
});
```

### 觀察者模式 (Event.observe)

```javascript
// 添加事件監聽
Event.observe("button", "click", function(event) {
    alert("Button clicked!");
});

// 自動化 DOM 載入後執行
document.observe("dom:loaded", function() {
    // DOM 載入完成後的處理
});

// 移除事件監聽
Event.stopObserving("button", "click", handler);
```

## Class 物件系統

Prototype 提供了一套優雅的類別系統：

```javascript
var Person = Class.create({
    initialize: function(name, age) {
        this.name = name;
        this.age = age;
    },

    introduce: function() {
        return "Hi, I'm " + this.name + ", " + this.age + " years old.";
    }
});

// 繼承
var Student = Class.create(Person, {
    initialize: function($super, name, age, school) {
        $super(name, age);
        this.school = school;
    },

    introduce: function($super) {
        return $super() + " I study at " + this.school + ".";
    }
});

var john = new Student("John", 20, "MIT");
john.introduce();  // "Hi, I'm John, 20 years old. I study at MIT."
```

## 與 Ruby on Rails 的整合

Prototype 是 Rails 預設的 JavaScript 框架，兩者緊密整合：

```javascript
// Rails 的 link_to_remote
<%= link_to_remote "載入內容", {
    :url => { :controller => "posts", :action => "show", :id => @post },
    :update => "content",
    :loading => "Element.show('loading')",
    :complete => "Element.hide('loading')"
} %>

// Rails 的 form_remote_for
<%= form_remote_for @post, :html => { :id => "post-form" } do |f| %>
    <%= f.text_field :title %>
    <%= f.text_area :body %>
    <%= f.submit "提交" %>
<% end %>
```

## Enumerable 枚舉功能

```javascript
// 強大的枚舉方法
[1, 2, 3, 4, 5].each(function(num) {
    console.log(num);
});

// 映射
[1, 2, 3, 4, 5].map(function(n) { return n * 2; });
// [2, 4, 6, 8, 10]

// 過濾
[1, 2, 3, 4, 5].select(function(n) { return n % 2 == 0; });
// [2, 4]

// 檢查
[1, 2, 3].all(function(n) { return n > 0; });  // true
[1, 2, 3].any(function(n) { return n > 2; }); // true

// 查找
[1, 2, 3, 4, 5].find(function(n) { return n > 3; }); // 4

// 計數
[1, 2, 3, 4, 5].inject(0, function(sum, n) { return sum + n; }); // 15
```

## Object 擴展

```javascript
// Object.extend 相當於 Object.assign
var defaults = { width: 100, height: 50 };
var options = { width: 200 };
Object.extend(options, defaults);
// { width: 200, height: 50 }

// Object.toQueryString
Object.toQueryString({ color: "red", size: "large" });
// "color=red&size=large"

// Object.keys 和 Object.values
Object.keys({ a: 1, b: 2 });   // ["a", "b"]
Object.values({ a: 1, b: 2 }); // [1, 2]
```

## 與 jQuery 的比較

| 特性 | Prototype | jQuery |
|------|-----------|--------|
| API 風格 | Ruby 風格擴展內建物件 | 封裝成 jQuery 物件 |
| 選擇器 | $$() CSS 選擇器 | $() 工廠函式 |
| AJAX | Class-based | 回調函式 |
| 鏈式呼叫 | 有限支援 | 完整支援 |
| 擴展方式 | 修改原生物件 | 包裝成新物件 |

## 影響與貢獻

Prototype 對 JavaScript 框架發展做出了重要貢獻：

1. **推廣函數式程式設計** -- Enumerable 方法影響了後續很多庫
2. **類別系統的實現** -- 為 JavaScript 類別系統的早期探索
3. **Rails 整合** -- 展示了框架整合的可能性
4. **Prototype 語法** -- $ 和 $$ 選擇器被其他框架借鑒

## 結語

Prototype 以其 Ruby 風格的優雅語法和對原生物件的增強，為 JavaScript 開發帶來了新的思路。雖然在這個年代 jQuery 更為流行，但 Prototype 的設計理念仍值得學習和借鑒。

---

*延伸閱讀：*
- [Prototype 官方網站](https://developers.google.com/search/?q=prototype+javascript+framework)
- [Prototype API 文件](https://developers.google.com/search/?q=prototype+api+documentation)