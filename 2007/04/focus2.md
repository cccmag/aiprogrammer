# WML 與 XHTML Mobile：標記語言的演進

## WML 的設計哲學

1999 年的 WML（Wireless Markup Language）是一種專為「痛苦」設計的語言——設計假設是：網路緩慢、螢幕狭小、輸入困難、電力有限。

### WML 的核心概念

**卡片式導航**

WML 將內容組織成「牌組」（Deck）和「卡片」（Card）。一個牌組可以包含多張卡片，使用者可以在卡片之間導航。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN"
"http://www.wapforum.org/DTD/wml_1.1.xml">

<wml>
  <!-- 第一張卡片：登入表單 -->
  <card id="login" title="會員登入">
    <p>
      帳號：<input name="username" maxlength="20"/><br/>
      密碼：<input type="password" name="password" maxlength="16"/><br/>
      <anchor>登入
        <go href="login.wmls#checkLogin()" method="get">
          <postfield name="u" value="$(username)"/>
          <postfield name="p" value="$(password)"/>
        </go>
      </anchor>
    </p>
  </card>

  <!-- 第二張卡片：登入成功 -->
  <card id="success" title="登入成功">
    <p>
      歡迎回來，$(username)！
      <do type="accept" label="進入系統">
        <go href="main.wml"/>
      </do>
    </p>
  </card>
</wml>
```

### 任務（Task）與導航

WML 定義了幾種任務類型：

```xml
<!-- go 任務：導航到 URL -->
<go href="http://example.com/news.wml"/>

<!-- prev 任務：返回上一頁 -->
<prev/>

<!-- refresh 任務：重新整理當前頁面 -->
<refresh/>

<!-- noop 任務：什麼都不做 -->
<noop/>
```

### 事件處理

```xml
<card id="main">
  <onevent type="onenterbackward">
    <!-- 當使用者按「返回」鍵時 -->
    <go href="home.wml"/>
  </onevent>

  <onevent type="onenterforward">
    <!-- 當使用者進入此卡片時 -->
    <refresh/>
  </onevent>

  <do type="accept" label="下一步">
    <go href="next.wml"/>
  </do>

  <p>內容...</p>
</card>
```

## WMLScript

WML 搭配 WMLScript 使用，這是一種類似 JavaScript 的客戶端腳本語言：

```wmls
// WMLScript 範例：validators.wmls
extern function validateEmail(email) {
    var regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+.[a-zA-Z]{2,}$";
    return(email.match(regex) != null);
};

extern function isAdult(age) {
    return age >= 18;
};
```

```xml
<!-- 呼叫 WMLScript -->
<do type="accept" label="驗證">
  <go href="validators.wmls#validateEmail('$(email)')"/>
</do>
```

## XHTML MP 的興起

隨著裝置能力提升，WML 逐漸無法滿足需求。2002 年，WAP Forum 推出了 XHTML Mobile Profile（XHTML MP），這是 XHTML Basic 的擴展。

### XHTML MP vs WML

```xml
<!-- WML 版本 -->
<?xml version="1.0"?>
<!DOCTYPE wml PUBLIC "-//WAPFORUM//DTD WML 1.1//EN"
"http://www.wapforum.org/DTD/wml_1.1.xml">
<wml>
  <card id="main">
    <p>Hello World</p>
  </card>
</wml>

<!-- XHTML MP 版本 -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//WAPFORUM//DTD XHTML Mobile 1.0//EN"
"http://www.wapforum.org/DTD/xhtml-mobile10.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <title>Hello World</title>
  </head>
  <body>
    <p>Hello World</p>
  </body>
</html>
```

### XHTML MP 的額外元素

XHTML MP 增加了 WML 的特有元素，如軟體按鍵（accessibility）和導航：

```xml
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>表單範例</title>
</head>
<body>
  <form action="submit.wmlx" method="post">
    <p>
      <label for="name">姓名：</label><br/>
      <input id="name" name="name" type="text" size="20"/>
    </p>
    <p>
      <label for="email">Email：</label><br/>
      <input id="email" name="email" type="text" size="30"/>
    </p>
    <p>
      <do type="accept" label="送出">
        <go href="submit.wmlx" method="post">
          <postfield name="name" value="$(name)"/>
          <postfield name="email" value="$(email)"/>
        </go>
      </do>
      <do type="prev" label="取消">
        <prev/>
      </do>
    </p>
  </form>
</body>
</html>
```

## 從 WML 到 HTML 的遷移策略

隨著智慧型手機的普及，越來越多網站需要從 WML 遷移到 HTML。以下是實務策略：

### 內容協商（Content Negotiation）

伺服器可以根據客戶端的 Accept 頭資訊回應不同格式：

```python
def serve_content(request):
    accept = request.headers.get('Accept', '')

    if 'application/xhtml+xml' in accept:
        return render_xhtmlmp(request)
    elif 'text/vnd.wap.wml' in accept:
        return render_wml(request)
    else:
        return render_html(request)
```

### 漸進增強（Progressive Enhancement）

```html
<!-- 基本內容：所有裝置可見 -->
<p>商品價格：$999</p>

<!-- 增強樣式：僅桌面瀏覽器 -->
<style>
@media screen and (min-width: 1024px) {
    .product-detail { columns: 2; }
}
</style>

<!-- 增強互動：僅支援 JavaScript 的瀏覽器 -->
<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('.buy-button').onclick = addToCart;
});
</script>
```

## CSS Mobile 設定檔

為了適應行動裝置，CSS 提供了 Mobile 設定檔：

```css
/* Mobile CSS */
@import url('base.css');

/* 隱藏桌面專用元素 */
.desktop-only { display: none; }

/* 觸控友好的點擊區域 */
button, a, input[type="submit"] {
    min-height: 44px; /* iOS 建議最小點擊區域 */
    font-size: 16px;  /* 避免 iOS 自動縮放 */
}

/* 防止水平滾動 */
body {
    max-width: 100%;
    overflow-x: hidden;
}
```

## 比較：三大標記語言

| 特性 | WML | XHTML MP | XHTML Mobile |
|------|-----|----------|-------------|
| 基於 | XML | XHTML | XHTML |
| 卡片模型 | 有 | 無 | 無 |
| 任務導航 | 有 | 標準連結 | 標準連結 |
| CSS 支援 | 有限 | 外部 CSS | 外部 CSS |
| JavaScript | WMLScript | 無（通常） | 可選 |
| 圖片格式 | WBMP | WBMP, PNG, JPEG | 標準 Web 圖片 |
| 2007 年使用率 | ~5% | ~15% | ~80% |

## 結語

WML 是一個時代的產物——它教會我們如何在資源受限的環境下設計資訊架構。即使 WML 已經退出主流市場，它的設計原則仍然適用：

1. **小螢幕優先**：先為小螢幕設計，再逐步增強
2. **離線考量**：考慮網路不穩定的情境
3. **輸入簡化**：減少使用者輸入需求
4. **內容優先**：把最重要的資訊放在最前面

XHTML Mobile 的出現標誌著行動 Web 正式進入「豐富」時代，但這個轉變也帶來了新的挑戰——如何在更大的螢幕上保持一致的體驗。

---

## 延伸閱讀

- [WML 1.1 規範](https://www.google.com/search?q=WML+1.1+specification+WAPForum)
- [XHTML+Mobile+Profile+規範](https://www.google.com/search?q=XHTML+Mobile+Profile+specification)
- [Mobile+Web+development+best+practices](https://www.google.com/search?q=Mobile+Web+development+best+practices+W3C)
- [WML+to+XHTML+migration](https://www.google.com/search?q=WML+to+XHTML+migration+strategy)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*