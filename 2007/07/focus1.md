# 主題一：jQuery 1.1 發布

## 簡化 DOM 操作的革命

2007 年 7 月，jQuery 1.1 正式發布，這是自 2006 年 jQuery 首次亮相以來最具意義的版本更新。jQuery 1.1 不僅大幅簡化了 DOM 操作，更在效能上有了質的飛躍，被譽為「簡化 JavaScript 開發的革命性工具」。

## jQuery 的誕生背景

在 jQuery 出現之前，開發者面臨著嚴峻的挑戰：

1. **瀏覽器相容性問題** -- IE、Firefox、Safari 等瀏覽器的 DOM API 存在顯著差異
2. **繁瑣的 DOM 操作** -- 創建、遍歷、修改 DOM 元素需要大量程式碼
3. **複雜的事件處理** -- 事件綁定、記憶體管理、事件委託都需要小心處理
4. **AJAX 開發繁瑣** -- 不同瀏覽器的 XMLHttpRequest 實作各不相同

John Resig 在 2005 年開始開發 jQuery，目標是創造一個「寫得更少，做得更多」的 JavaScript 庫。

## jQuery 1.1 的核心改進

### 效能大幅提升

jQuery 1.1 採用了全新的選擇器引擎 Sizzle，在效能上實現了 3 倍以上的提升。選擇器是 jQuery 最常用的功能之一，效能的改善直接影響了整體使用體驗。

### API 簡化

jQuery 1.1 進一步簡化了 API，將常見操作濃縮成鏈式方法呼叫：

```javascript
// 複雜的 DOM 操作，傳統方式需要數十行
var element = document.getElementById("myId");
var children = element.getElementsByTagName("div");
for (var i = 0; i < children.length; i++) {
    if (children[i].className === "highlight") {
        children[i].style.backgroundColor = "yellow";
    }
}

// jQuery 方式，一行搞定
$("#myId div.highlight").css("backgroundColor", "yellow");
```

### 事件處理的革新

jQuery 1.1 提供了統一代的事件處理 API，解決了跨瀏覽器的相容性問題：

```javascript
// 自動處理瀏覽器差異
$("#button").click(function() {
    alert("Clicked!");
});

// 事件委託，適用於動態內容
$("ul").click(function(event) {
    if ($(event.target).is("li")) {
        $(event.target).toggleClass("active");
    }
});

// 一次性事件
$(document).one("ready", function() {
    console.log("文檔載入完成");
});
```

### AJAX 請求的簡化

```javascript
// 傳統 AJAX 請求需要處理 XMLHttpRequest 的瀏覽器差異
var xhr = window.XMLHttpRequest ? new XMLHttpRequest() : new ActiveXObject("Microsoft.XMLHTTP");
xhr.open("GET", "data.json", true);
xhr.onreadystatechange = function() {
    if (xhr.readyState === 4 && xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        // 處理資料
    }
};
xhr.send();

// jQuery AJAX
$.getJSON("data.json", function(data) {
    // 處理資料
});
```

## jQuery 的哲學

jQuery 的成功源於其核心理念：

1. **簡潔性** -- 用最少的程式碼完成最多的工作
2. **鏈式呼叫** -- 方法可以無縫鏈接，形成流暢的程式碼
3. **隱藏複雜性** -- 開發者不需要關心瀏覽器差異
4. **擴充性** -- 提供插件機制，讓社群可以自由擴展

## jQuery 選擇器語法

jQuery 支援完整的 CSS 選擇器，並添加了自己的擴展：

```javascript
// 基本選擇器
$("#id")           // ID 選擇器
$(".class")        // 類別選擇器
$("div")           // 標籤選擇器
$("*")             // 通用選擇器

// 層級選擇器
$("parent > child")    // 子元素
$("ancestor descendant") // 後代元素
$("prev + next")        // 相鄰兄弟
$("prev ~ siblings")    // 所有兄弟

// 屬性選擇器
$("input[type=text]")
$("a[href^=https]")
$("img[src$=.png]")

// jQuery 擴充
$(":animated")      // 正在動畫的元素
$(":visible")       // 可見元素
$(":contains(text)") // 包含文字的元素
```

## jQuery 1.1 的影響

jQuery 1.1 的發布對 Web 開發領域產生了深遠影響：

1. **降低前端開發門檻** -- 非專業 JavaScript 開發者也能輕鬆實現動態效果
2. **推動 AJAX 普及** -- 簡化的 AJAX API 讓更多網站採用非同步技術
3. **促進標準化** -- jQuery 的選擇器語法後來被廣泛借鑒
4. **插件生態形成** -- jQuery 插件庫開始蓬勃發展

## 版本演進

- **2006 年 1 月** -- jQuery 首次公開發布
- **2006 年 8 月** -- jQuery 1.0 正式發布
- **2007 年 7 月** -- jQuery 1.1 發布，效能提升 3 倍
- **此後** -- jQuery 持續更新，成為最受歡迎的 JavaScript 庫

## 結語

jQuery 1.1 的發布標誌著前端開發進入了一個新時代。它以簡潔的 API、優異的效能和強大的擴充性，徹底改變了 JavaScript 開發的方式。直到今日，jQuery 仍然是世界上使用最廣泛的 JavaScript 庫之一，其影響力延續至今。

---

*延伸閱讀：*
- [jQuery 官方網站](https://developers.google.com/search/?q=jquery+official+website)
- [jQuery 選擇器文件](https://developers.google.com/search/?q=jquery+selectors+documentation)