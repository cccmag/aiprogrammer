# 主題二：DOM 操作簡化

## 選擇器與遍歷

DOM（Document Object Model）是網頁的程式化表示，掌握 DOM 操作是 JavaScript 開發的核心能力。2007 年，隨著 jQuery 等框架的興起，複雜的 DOM 操作變得前所未有的簡單。

## 傳統 DOM 操作的困境

在框架出現之前，開發者需要面對繁瑣的原生 DOM API：

### 選擇元素

```javascript
// 取得元素 - 不同瀏覽器語法不同
var element = document.getElementById("myId");
var elements = document.getElementsByTagName("div");
var elements = document.getElementsByClassName("myClass"); // IE9+ 才支援

// 使用 XPath（部分瀏覽器支援）
var result = document.evaluate("//div[@class='myClass']", document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);
```

### 修改元素內容

```javascript
// 取得/設定文字內容
var text = element.firstChild.nodeValue;
element.firstChild.nodeValue = "新文字";

// 取得/設定 HTML 內容
var html = element.innerHTML;
element.innerHTML = "<p>新內容</p>";

// 設定屬性
element.setAttribute("src", "image.jpg");
element.src = "image.jpg";
```

這些操作不僅繁瑣，還需要處理各種瀏覽器相容性問題。

## jQuery 選擇器革命

jQuery 提供了統一且強大的選擇器語法：

### 基本選擇器

```javascript
// ID 選擇器 - 最快速
$("#header")

// 類別選擇器
$(".intro")

// 標籤選擇器
$("div")

// 群組選擇器
$("div, p, span")

// 所有元素
$("*")
```

### 層級選擇器

```javascript
// 後代選擇器 - 選擇所有後代
$("form input")

// 子選擇器 - 僅選擇直接子元素
$("form > input")

// 相鄰兄弟選擇器
$("label + input")

// 兄弟選擇器
$("form ~ input")
```

### 屬性選擇器

```javascript
// 匹配屬性
$("a[href]")
$("a[href='http://example.com']")

// 開頭/結尾匹配
$("a[href^='https']")   // href 以 https 開頭
$("a[href$='.pdf']")     // href 以 .pdf 結尾

// 包含匹配
$("a[href*='google']")  // href 包含 google
```

### 偽類選擇器

```javascript
// 位置偽類
$("tr:first")
$("tr:last")
$("tr:even")
$("tr:odd")
$("td:nth-child(2)")

// 表單偽類
$(":text")
$(":password")
$(":radio")
$(":checkbox")
$(":submit")
$(":input")

// 可見性偽類
$(":visible")
$(":hidden")
```

## DOM 遍歷

jQuery 提供了豐富的遍歷方法：

### 向上遍歷

```javascript
// 父元素
$("span").parent()
$("span").parents("div")  // 限定父元素為 div
$("span").closest("div")  // 最近的第一個符合條件的祖先

// 祖先鏈
$("span").parentsUntil("body")  // 到 body 為止的所有祖先
```

### 向下遍歷

```javascript
// 子元素
$("div").children()
$("div").children(".highlight")

// 後代元素
$("div").find("span")

// 首個/末個子元素
$("div").first()
$("div").last()
```

### 兄弟遍歷

```javascript
// 所有兄弟
$("h2").siblings()

// 指定兄弟
$("h2").siblings(".note")

// 之後/之前的兄弟
$("h2").next()
$("h2").nextAll()
$("h2").nextUntil("h3")

$("h2").prev()
$("h2").prevAll()
$("h2").prevUntil("h1")
```

## DOM 修改

jQuery 使得 DOM 修改變得非常直觀：

### 創建元素

```javascript
// 使用 HTML 字串創建
$("<div>", {
    "class": "widget",
    "id": "main-widget",
    "text": "Hello World",
    "css": { "color": "red" },
    "click": function() { alert("Clicked!"); }
})
```

### 插入內容

```javascript
// 在元素內插入
$("#container").append("<p>新段落</p>");
$("#container").prepend("<p>開頭段落</p>");

// 作為子元素插入
$("<li>新項目</li>").appendTo("#list");
$("<li>新項目</li>").prependTo("#list");

// 在元素外插入
$("#container").after("<div>之後</div>");
$("#container").before("<div>之前</div>");
```

### 修改內容和屬性

```javascript
// HTML 和文字
$("#content").html("<strong>粗體</strong>");
$("#content").text("純文字");

// 屬性操作
$("img").attr("src", "new.jpg");
$("img").removeAttr("alt");
$("input").prop("disabled", true);

// 類別操作
$("p").addClass("highlight");
$("p").removeClass("highlight");
$("p").toggleClass("highlight");
$("p").hasClass("highlight");

// CSS 操作
$("p").css("color", "blue");
$("p").css({ "color": "blue", "font-size": "16px" });
```

### 刪除元素

```javascript
// 移除元素
$("#widget").remove();
$("#widget").detach();  // 保留事件和資料

// 清空內容
$("#container").empty();
```

## 效能優化

### 快取 jQuery 物件

```javascript
// 不好的寫法
$("#button").click(function() {
    $("#result").html("Clicked!");
    $("#result").addClass("highlight");
});

// 好的寫法
var $result = $("#result");
$("#button").click(function() {
    $result.html("Clicked!").addClass("highlight");
});
```

### 使用最近選擇器

```javascript
// 避免
$("div").find(".item").each(...);
$("div").children(".item").each(...);

// 使用
$(".item", ".container")  // 相當於 $(".container").find(".item")
```

### 事件委託

```javascript
// 不好的寫法 - 為每個 li 綁定事件
$("ul li").click(handler);

// 好的寫法 - 委託到父元素
$("ul").on("click", "li", handler);
```

## 結語

DOM 操作是 Web 開發的基礎。jQuery 等框架的出現，讓開發者可以專注於業務邏輯，而不是被繁瑣的瀏覽器相容性問題困擾。掌握選擇器和遍歷技巧，是提高 DOM 操作效率的關鍵。

---

*延伸閱讀：*
- [jQuery DOM 操作文件](https://developers.google.com/search/?q=jquery+dom+manipulation)
- [MDN DOM 文件](https://developers.google.com/search/?q=mdn+dom+tutorial)