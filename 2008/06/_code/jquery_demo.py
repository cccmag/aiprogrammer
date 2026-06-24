#!/usr/bin/env python3
"""jQuery 示範 - DOM 操作、Ajax、動畫模擬"""

def demo():
    print("=" * 50)
    print("jQuery 示範")
    print("=" * 50)

    print("\n1. 選擇器（模擬）：")
    selectors = [
        "$('#id')         → 選擇 ID 為 id 的元素",
        "$('.class')      → 選擇類別為 class 的元素",
        "$('div')         → 選擇所有 div 元素",
        "$('div.content') → 選擇有 content 類別的 div",
        "$('ul > li')     → 選擇 ul 的直接 li 子元素",
        "$('li:first')    → 選擇第一個 li"
    ]
    for s in selectors:
        print(f"   {s}")

    print("\n2. DOM 操作（模擬）：")
    operations = [
        "$('#id').addClass('active')   → 添加類別",
        "$('#id').removeClass('active') → 移除類別",
        "$('#id').toggleClass('active') → 切換類別",
        "$('#id').text('Hello')        → 設定文字",
        "$('#id').html('<p>...</p>')   → 設定 HTML",
        "$('#id').attr('href', 'url')  → 設定屬性",
        "$('#id').css('color', 'red')  → 設定樣式"
    ]
    for op in operations:
        print(f"   {op}")

    print("\n3. 事件處理（模擬）：")
    events = [
        "$('#btn').click(handler)       → 點擊事件",
        "$('#btn').dblclick(handler)    → 雙擊事件",
        "$('#input').focus(handler)     → 取得焦點",
        "$('#input').blur(handler)      → 失去焦點",
        "$('#list').delegate('li', 'click', handler)  → 事件委託"
    ]
    for e in events:
        print(f"   {e}")

    print("\n4. Ajax 請求（模擬）：")
    ajax_calls = [
        "$.get('/api', data, callback)     → GET 請求",
        "$.post('/api', data, callback)     → POST 請求",
        "$.ajax({url, type, success})      → 完整 Ajax",
        "$.getJSON('/api', callback)        → JSON 請求",
        "$('#content').load('/partial')     → 載入 HTML"
    ]
    for a in ajax_calls:
        print(f"   {a}")

    print("\n5. 動畫效果（模擬）：")
    animations = [
        "$('#box').fadeIn()              → 淡入",
        "$('#box').fadeOut()             → 淡出",
        "$('#box').slideUp()             → 上滑",
        "$('#box').slideDown()           → 下滑",
        "$('#box').animate({left: 100})  → 自訂動畫",
        "$('#box').toggle()              → 切換顯示"
    ]
    for an in animations:
        print(f"   {an}")

    print("\n" + "=" * 50)
    print("jQuery 核心思想：Write Less, Do More")
    print("Chain API: $('.item').addClass('x').fadeIn().click(handler)")
    print("=" * 50)

if __name__ == "__main__":
    demo()