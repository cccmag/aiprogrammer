# 行動優先設計：Mobile-First 策略與實作

## 前言

隨著智慧型手機的普及，越來越多的用戶通過行動設備訪問網站。Google 在 2015 年宣布將「行動友好度」作為排名信號，進一步推動了行動優先設計的普及。

但「行動優先」不僅僅是為了 SEO，更是一種以使用者為中心的設計理念——從一開始就考慮最小螢幕的使用體驗，然後逐步增強。

## Mobile-First 的核心理念

### 從桌面優先到行動優先

傳統的「桌面優先」方法：

```
桌面設計 → 測試 → 縮小到平板 → 測試 → 縮小到手机
                                              ↓
                                    出現問題：佈局混亂
                                    解決方案：隱藏或縮小
```

「桌面優先」的問題：
1. 為大螢幕設計的元素在小螢幕上難以使用
2. 行動版本往往是桌面版本的「精簡版」
3. 核心功能被不當地刪除或隱藏

「行動優先」方法：

```
手機設計 → 測試 → 擴展到平板 → 測試 → 擴展到桌面
                                              ↓
                                    更好的核心體驗
                                    漸進增強
```

### Mobile-First 的優勢

1. **聚焦核心功能**：在小螢幕上，沒有空間容納多餘的元素
2. **效能優先**：行動網路通常較慢，必須優化效能
3. **觸控友好**：從一開始就考慮觸控交互
4. **漸進增強**：大螢幕是獎賞，而非必要

## 響應式設計策略

### 斷點設計

```css
/* 預設（手機）— 最基本的樣式 */
.container {
  width: 100%;
  padding: 0 10px;
}

/* 平板（768px 以上） */
@media (min-width: 768px) {
  .container {
    max-width: 720px;
    padding: 0 20px;
  }
}

/* 桌面（1024px 以上） */
@media (min-width: 1024px) {
  .container {
    max-width: 960px;
    padding: 0 30px;
  }
}

/* 大桌面（1200px 以上） */
@media (min-width: 1200px) {
  .container {
    max-width: 1140px;
  }
}
```

### 內容優先級

在手機上，內容應該按優先級排列：

```html
<!-- 手機上應該只顯示最重要的內容 -->
<article>
  <h1>文章標題</h1>           <!-- 總是顯示 -->
  <p class="lead">摘要</p>      <!-- 總是顯示 -->
  <div class="article-body">   <!-- 可折疊或分頁 -->
    完整內容...
  </div>
  <div class="related">        <!-- 可能隱藏或移到最後 -->
    相關文章...
  </div>
</article>
```

## 觸控優化

### 點擊目標大小

Apple 人機界面指南建議最小點擊區域為 44×44 點：

```css
/* 設定最小點擊區域 */
button,
a,
input[type="checkbox"],
input[type="radio"] {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* 對於小按鈕，使用較大的內邊距 */
.btn-xs {
  padding: 16px 24px;  /* 增大點擊區域 */
}
```

### 手指友好的間距

```css
/* 元素之間的間距 */
.list-item {
  padding: 16px 0;
  border-bottom: 1px solid #ddd;
}

/* 防止誤觸鄰近元素 */
.nav-menu li {
  margin-bottom: 8px;  /* 增加間距 */
}
```

### 移除 Hover 依賴

```css
/* 桌面優先的設計（不好） */
@media (hover: hover) {
  .dropdown:hover .dropdown-menu {
    display: block;
  }
}

/* 行動優先的設計 */
.dropdown-menu {
  display: none;  /* 預設隱藏 */
}

.dropdown.open .dropdown-menu {
  display: block;  /* 通過點擊觸發 */
}
```

## 效能優化

### 圖片優化

```css
/* 響應式圖片 */
img {
  max-width: 100%;
  height: auto;
}

/* 根據設備像素比提供不同圖片 */
@media (-webkit-min-device-pixel-ratio: 2) {
  .logo {
    background-image: url(logo@2x.png);
    background-size: 100px 50px;
  }
}
```

### 延遲載入

```javascript
// 延遲載入非關鍵資源
function loadImages() {
  var images = document.querySelectorAll('[data-src]');

  for (var i = 0; i < images.length; i++) {
    var img = images[i];
    img.src = img.dataset.src;
    img.removeAttribute('data-src');
  }
}

// 使用 Intersection Observer（2010 年末期支援）
if ('IntersectionObserver' in window) {
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        loadImages();
        observer.disconnect();
      }
    });
  });

  observer.observe(document.body);
}
```

### CSS 性能

```css
/* 避免過度使用 box-shadow */
.card {
  box-shadow: 0 1px 3px rgba(0,0,0,0.12);  /* 輕量陰影 */
}

/* 使用 transform 替代 layout 屬性 */
.animation {
  transform: translateX(100px);  /* GPU 加速 */
}

/* 減少繪製區域 */
.badge {
  will-change: transform;
}
```

## Bootstrap 的行動優先實作

### Bootstrap 3 的 Mobile First

```html
<!-- Bootstrap 3 的栅格語法 -->
<div class="container">
  <div class="row">
    <!-- 預設（xs）: 總是全寬 -->
    <!-- sm: 576px+ -->
    <!-- md: 768px+ -->
    <!-- lg: 992px+ -->
    <!-- xl: 1200px+ -->

    <div class="col-12 col-sm-6 col-md-4 col-lg-3">
      響應式卡片
    </div>
  </div>
</div>
```

### Bootstrap 4/5 的改進

```css
/* Bootstrap 5 的現代響應式斷點 */
:root {
  --bs-breakpoint-sm: 576px;
  --bs-breakpoint-md: 768px;
  --bs-breakpoint-lg: 992px;
  --bs-breakpoint-xl: 1200px;
  --bs-breakpoint-xxl: 1400px;
}

/* 行動優先的 flex 工具 */
.d-flex {
  display: flex;
}

@media (min-width: 768px) {
  .d-md-flex {
    display: flex;
  }
}
```

## 導航設計模式

### 底部導航欄（手機優先）

```html
<!-- 手機：底部固定導航 -->
<nav class="bottom-nav">
  <a href="#" class="nav-item active">
    <span class="icon">首頁</span>
  </a>
  <a href="#" class="nav-item">
    <span class="icon">搜尋</span>
  </a>
  <a href="#" class="nav-item">
    <span class="icon">個人</span>
  </a>
</nav>

<!-- 平板+：頂部橫向導航 -->
@media (min-width: 768px) {
  .bottom-nav {
    position: static;
    display: flex;
  }
}
```

### 汉堡選單

```html
<!-- 手機：隱藏導航 -->
<nav class="navbar">
  <button class="navbar-toggle" data-toggle="collapse"
          data-target="#menu">
    ☰
  </button>
  <div id="menu" class="collapse navbar-collapse">
    <ul class="nav navbar-nav">
      <li><a href="#">首頁</a></li>
      <li><a href="#">關於</a></li>
    </ul>
  </div>
</nav>
```

## 表單設計

### 觸控友好的表單

```html
<!-- 使用正確的 input type -->
<input type="email" placeholder="email">
<input type="tel" placeholder="電話">
<input type="date" placeholder="日期">

<!-- 標籤始終可見 -->
<label for="email">電子郵件 *</label>
<input type="email" id="email" class="form-control">

<!-- 足夠的間距 -->
<form class="mobile-form">
  <div class="form-group">
    <label for="name">姓名</label>
    <input type="text" id="name" class="form-control">
  </div>
</form>
```

```css
.mobile-form .form-group {
  margin-bottom: 20px;  /* 增加間距 */
}

.mobile-form input {
  font-size: 16px;  /* 防止 iOS 縮放 */
  padding: 12px;    /* 增加觸控區域 */
}
```

## 測試與調試

### 設備測試

1. **真實設備**：在多種真實設備上測試
2. **瀏覽器開發者工具**：Chrome/Firefox 的設備模擬
3. **線上工具**：BrowserStack、CrossBrowserTesting

### 常見問題

```css
/* iOS 文字大小調整 */
html {
  -webkit-text-size-adjust: 100%;
}

/* iOS 輸入框內邊距 */
input, textarea {
  -webkit-appearance: none;
  border-radius: 0;
}

/* 防止 iOS 圓角 */
input[type="text"],
input[type="email"],
input[type="search"] {
  -webkit-appearance: none;
}
```

## 結語

行動優先不僅是一種技術策略，更是一種設計哲學。它要求我們：

1. **從核心出發**：先確定最重要的功能和內容
2. **觸控為本**：從一開始就考慮觸控交互
3. **效能導向**：在網路受限的環境下保持高效
4. **漸進增強**：為大螢幕用戶提供更好的體驗

實施行動優先設計需要思維方式的轉變——從「Desktop」到「Mobile」不是簡單的縮放，而是重新思考什麼是真正重要的。

---

## 延伸閱讀

- [Mobile-First Responsive Web Design](https://www.google.com/search?q=mobile+first+responsive+design)
- [Google Mobile-Friendly Test](https://www.google.com/search?q=Google+mobile+friendly+test)
- [Touch Target Size Guidelines](https://www.google.com/search?q=touch+target+size+guidelines)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*