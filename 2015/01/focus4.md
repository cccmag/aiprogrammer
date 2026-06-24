# 響應式網頁設計：Media Query、Mobile First、Bootstrap

## 前言

智慧手機的普及讓響應式設計從「加分項」變成「必要條件」。2015 年，超過 50% 的網頁流量來自行動裝置。

## Media Query 媒體查詢

### 基本語法

```css
/* 當視窗寬度小於 768px 時套用 */
@media (max-width: 768px) {
  .container {
    width: 100%;
    padding: 10px;
  }
}

/* 當視窗寬度在 768px 到 1024px 之間 */
@media (min-width: 768px) and (max-width: 1024px) {
  .container {
    width: 750px;
  }
}

/* 螢幕方向 */
@media (orientation: landscape) {
  .banner {
    width: 100vh;
  }
}

/* 彩色 vs 黑白螢幕 */
@media (monochrome) {
  body {
    background: white;
    color: black;
  }
}
```

### 常見斷點

```
常見響應式斷點（2015 年主流）：
─────────────────────────────────
Mobile:    320px - 480px
Tablet:    481px - 768px
Small:     769px - 1024px
Medium:    1025px - 1200px
Large:     1200px+

Bootstrap 3 斷點：
─────────────────
xs (超小):  < 768px
sm (小):    >= 768px
md (中等):  >= 992px
lg (大):    >= 1200px
```

### Mobile First vs Desktop First

```css
/* Mobile First（推薦）*/
/* 從最小螢幕開始，逐步增強 */

.container {
  width: 100%;              /* 行動裝置：佔滿寬度 */
  padding: 10px;
}

@media (min-width: 768px) {
  .container {
    width: 750px;            /* 平板：固定寬度 */
    padding: 20px;
  }
}

@media (min-width: 1024px) {
  .container {
    width: 970px;            /* 小桌面 */
  }
}

@media (min-width: 1200px) {
  .container {
    width: 1170px;           /* 大桌面 */
  }
}

/* Desktop First（不推薦）*/
/* 從最大螢幕開始，逐步削弱 */

.container {
  width: 1170px;            /* 大桌面 */
  padding: 30px;
}

@media (max-width: 1199px) {
  .container {
    width: 970px;            /* 較小桌面 */
  }
}

@media (max-width: 991px) {
  .container {
    width: 750px;            /* 平板 */
  }
}

@media (max-width: 767px) {
  .container {
    width: 100%;             /* 行動裝置 */
    padding: 10px;
  }
}
```

## Flexible Images 彈性圖片

```css
/* 圖片自適應容器 */
img {
  max-width: 100%;
  height: auto;
}

/* 背景圖片 */
.hero {
  background-image: url('hero-mobile.jpg');
  background-size: cover;
  background-position: center;
}

@media (min-width: 768px) {
  .hero {
    background-image: url('hero-desktop.jpg');
  }
}
```

### Picture 元素與 srcset

```html
<!-- 響應式圖片 -->
<picture>
  <source media="(min-width: 1200px)"
          srcset="image-large.jpg 1200w,
                  image-medium.jpg 800w">
  <source media="(min-width: 768px)"
          srcset="image-tablet.jpg 768w">
  <img src="image-mobile.jpg" alt="描述文字">
</picture>
```

## Bootstrap 框架應用

### Bootstrap 網格系統

```html
<div class="container">
  <!-- 12 欄格系統 -->
  <div class="row">
    <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
      卡片 1
    </div>
    <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
      卡片 2
    </div>
    <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
      卡片 3
    </div>
    <div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">
      卡片 4
    </div>
  </div>
</div>
```

### Bootstrap 元件

```html
<!-- 導航列 -->
<nav class="navbar navbar-default">
  <div class="container-fluid">
    <div class="navbar-header">
      <button type="button" class="navbar-toggle collapsed"
              data-toggle="collapse"
              data-target="#navbar">
        <span class="sr-only">導航</span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
        <span class="icon-bar"></span>
      </button>
      <a class="navbar-brand" href="#">品牌</a>
    </div>
    <div class="collapse navbar-collapse" id="navbar">
      <ul class="nav navbar-nav">
        <li class="active"><a href="#">首頁</a></li>
        <li><a href="#">關於</a></li>
      </ul>
    </div>
  </div>
</nav>

<!-- 按鈕 -->
<button class="btn btn-primary btn-lg">主要按鈕</button>
<button class="btn btn-secondary">次要按鈕</button>

<!-- 表單 -->
<form>
  <div class="form-group">
    <label for="email">Email</label>
    <input type="email" class="form-control"
           id="email" placeholder="Email">
  </div>
  <button type="submit" class="btn btn-default">提交</button>
</form>
```

### Bootstrap 響應式工具類別

```html
<!-- 可見性控制 -->
<div class="visible-xs-block">只在手機顯示</div>
<div class="visible-sm-block">只在平板顯示</div>
<div class="visible-md-block">只在中等螢幕顯示</div>
<div class="visible-lg-block">只在大螢幕顯示</div>

<div class="hidden-xs">在手機隱藏</div>
<div class="hidden-sm">在平板隱藏</div>

<!-- 列印 -->
<div class="visible-print-block">只在列印時顯示</div>
<div class="hidden-print">列印時隱藏</div>
```

## 實戰：建立響應式部落格

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
        content="width=device-width, initial-scale=1">
  <title>我的部落格</title>
  <style>
    /* 基礎樣式 */
    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
    }

    /* Mobile First 佈局 */
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 15px;
    }

    header {
      background: #333;
      color: white;
      padding: 20px 0;
    }

    nav ul {
      list-style: none;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    nav a {
      color: white;
      text-decoration: none;
    }

    .posts {
      display: flex;
      flex-direction: column;
      gap: 20px;
      margin-top: 20px;
    }

    .post {
      background: #f4f4f4;
      padding: 20px;
      border-radius: 5px;
    }

    footer {
      background: #333;
      color: white;
      text-align: center;
      padding: 20px 0;
      margin-top: 40px;
    }

    /* Tablet+ */
    @media (min-width: 768px) {
      nav ul {
        flex-direction: row;
        gap: 20px;
      }

      .posts {
        flex-direction: row;
        flex-wrap: wrap;
      }

      .post {
        flex: 1 1 300px;
      }
    }

    /* Desktop+ */
    @media (min-width: 1024px) {
      .main {
        display: flex;
        gap: 30px;
      }

      .content {
        flex: 2;
      }

      .sidebar {
        flex: 1;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <h1>我的部落格</h1>
      <nav>
        <ul>
          <li><a href="#">首頁</a></li>
          <li><a href="#">文章</a></li>
          <li><a href="#">關於</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="container main">
    <div class="content">
      <div class="posts">
        <article class="post">
          <h2>響應式設計基礎</h2>
          <p>學習如何使用 Media Query 建立響應式網站...</p>
        </article>
        <article class="post">
          <h2>CSS Flexbox 教程</h2>
          <p>Flexbox 讓布局變得前所未有的簡單...</p>
        </article>
      </div>
    </div>
    <aside class="sidebar">
      <div class="post">
        <h3>關於我</h3>
        <p>業餘程式設計師，喜歡分享技術文章。</p>
      </div>
    </aside>
  </main>

  <footer>
    <p>&copy; 2015 我的部落格</p>
  </footer>
</body>
</html>
```

## 結語

響應式設計不是一個技術，而是一種思維方式。從 Mobile First 出發，讓內容在所有設備上都能良好呈現，是 2015 年後網頁開發的基本功。

---

## 延伸閱讀

- [MDN 響應式設計指南](https://www.google.com/search?q=responsive+web+design+media+queries+tutorial)
- [Bootstrap 官方文檔](https://www.google.com/search?q=Bootstrap+3+tutorial+responsive)
- [Mobile First 設計策略](https://www.google.com/search?q=mobile+first+responsive+design+strategy)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」歷史回顧系列之一。*