# jQuery 實作範例

## 概述

本文介紹 jQuery 的核心概念和實作範例，幫助讀者快速掌握這個強大的 JavaScript 框架。我們將展示選擇器、事件處理、AJAX 請求和動畫效果等常見用法。

## 環境設定

jQuery 可從官方網站下載，或使用 CDN：

```html
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.1.0/jquery.min.js"></script>
```

## 基本選擇器

jQuery 的核心是其強大的選擇器引擎，支援 CSS 1-3 選擇器：

```python
"""
jQuery 選擇器概念 Python 實作展示
實際的 jQuery 是 JavaScript，但概念適用於多種語言
"""

def demo():
    print("=" * 50)
    print("jQuery 選擇器概念展示")
    print("=" * 50)

    # CSS 選擇器類比
    selectors = {
        "ID 選擇器": "#elementId",
        "類別選擇器": ".className",
        "標籤選擇器": "div",
        "群組選擇器": "div, p, span",
        "後代選擇器": "div p",
        "子選擇器": "div > p",
        "屬性選擇器": "input[type=text]",
    }

    print("\n--- CSS 選擇器語法 ---")
    for name, selector in selectors.items():
        print(f"{name}: {selector}")

    # jQuery 鏈式操作概念
    print("\n--- 鏈式操作範例 ---")
    print("""
# jQuery 鏈式操作程式碼：
$("#myElement")
    .addClass("highlight")    # 新增類別
    .css("color", "red")       # 設定樣式
    .fadeIn()                  # 淡入動畫
    .click(handleClick);       # 綁定點擊事件
    """)

    # AJAX 請求範例
    print("\n--- jQuery AJAX 請求 ---")
    ajax_code = """
$.ajax({
    url: "api/data.json",
    type: "GET",
    dataType: "json",
    success: function(data) {
        console.log("資料載入成功");
        $("#result").html(data.content);
    },
    error: function(xhr, status, error) {
        console.error("請求失敗:", error);
    }
});

// 簡化版本
$.get("api/data.json", function(data) {
    $("#result").html(data);
});
"""
    print(ajax_code)

    # 事件處理範例
    print("\n--- 事件處理範例 ---")
    event_code = """
// 文件載入後執行
$(document).ready(function() {
    // 點擊事件
    $("#btn").click(function() {
        alert("按鈕被點擊！");
    });

    // 滑鼠懸停
    $(".card").hover(
        function() { $(this).addClass("hover"); },
        function() { $(this).removeClass("hover"); }
    );

    // 鍵盤事件
    $(document).keydown(function(e) {
        if (e.ctrlKey && e.keyCode === 83) {
            e.preventDefault();
            saveDocument();
        }
    });
});
"""
    print(event_code)

    # DOM 操作範例
    print("\n--- DOM 操作範例 ---")
    dom_code = """
// 創建新元素
var newDiv = $("<div class='item'>新元素</div>");

// 插入元素
$("#container").append(newDiv);
$("#container").prepend(newDiv);
$("#container").after(newDiv);
$("#container").before(newDiv);

// 修改內容
$("#content").html("<p>新 HTML 內容</p>");
$("#content").text("純文字內容");

// 修改屬性
$("img").attr("src", "new-image.jpg");
$("input").val("輸入值");
$("a").prop("href", "https://example.com");
"""
    print(dom_code)

    # 動畫效果範例
    print("\n--- 動畫效果範例 ---")
    animation_code = """
// 顯示/隱藏
$("#element").show();
$("#element").hide();
$("#element").toggle();

// 淡入/淡出
$("#element").fadeIn();
$("#element").fadeOut();
$("#element").fadeTo("slow", 0.5);

// 滑動
$("#element").slideDown();
$("#element").slideUp();
$("#element").slideToggle();

// 自定義動畫
$("#element").animate({
    opacity: 0.5,
    left: "+=50",
    height: "toggle"
}, 500, function() {
    console.log("動畫完成");
});
"""
    print(animation_code)

    print("\n" + "=" * 50)
    print("jQuery 核心概念展示完畢")
    print("=" * 50)

if __name__ == "__main__":
    demo()