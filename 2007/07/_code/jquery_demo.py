#!/usr/bin/env python3
"""
jQuery 與 JavaScript 框架概念展示
展示選擇器、DOM 操作、AJAX 等核心概念
"""

def demo():
    print("=" * 50)
    print("jQuery 與 JavaScript 框架概念展示")
    print("=" * 50)

    print("\n--- 選擇器概念 ---")
    selectors = {
        "ID 選擇器": "#elementId",
        "類別選擇器": ".className",
        "標籤選擇器": "div",
        "群組選擇器": "div, p, span",
        "後代選擇器": "div p",
        "子選擇器": "div > p",
        "屬性選擇器": "input[type=text]",
    }
    for name, selector in selectors.items():
        print(f"  {name}: {selector}")

    print("\n--- 鏈式操作概念 ---")
    print("""
# jQuery 鏈式操作：
$("#element")
    .addClass("highlight")
    .fadeIn()
    .click(handler)
""")

    print("\n--- AJAX 請求概念 ---")
    print("""
# jQuery AJAX 請求：
$.ajax({
    url: "api/data.json",
    type: "GET",
    success: function(data) {
        $("#result").html(data);
    }
})

# 簡化版本：
$.get("api/data.json", function(data) {
    $("#result").html(data);
})
""")

    print("\n--- 動畫效果概念 ---")
    print("""
# jQuery 動畫：
$("#element").fadeIn()
$("#element").fadeOut()
$("#element").slideDown()
$("#element").animate({ opacity: 0.5 })
""")

    print("\n" + "=" * 50)
    print("jQuery 概念展示完成")

if __name__ == "__main__":
    demo()