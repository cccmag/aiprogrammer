# JavaScript Mobile 框架：觸控時代的瀏覽器技術

## 行動優先的 JavaScript 框架

2007 年，隨著 iPhone 和 Android 的興起，JavaScript 框架開始針對行動裝置進行優化。觸控介面、不同螢幕尺寸、有限的效能——這些都是傳統桌面框架未考慮的問題。

## iUI：iPhone 風格的 UI 框架

iUI 是最早專為 iPhone 設計的 JavaScript UI 框架，發布於 2007 年。

### iUI 的核心概念

iUI 將網頁劃分成「對話方塊」（Dialog）和「面板」（Panel），模仿原生 iPhone UI：

```html
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="iui.css">
  <script src="iui.js"></script>
</head>
<body>
  <!-- 工具列 -->
  <div class="toolbar">
    <h1 id="title">我的應用</h1>
    <a class="button" href="#settings">設定</a>
  </div>

  <!-- 面板導航 -->
  <ul id="home" title="首頁" selected="true">
    <li><a href="#profile">個人資料</a></li>
    <li><a href="#messages">訊息</a></li>
    <li><a href="#friends">朋友</a></li>
  </ul>

  <!-- 設定面板 -->
  <ul id="settings" title="設定">
    <li class="group">通知</li>
    <li><a href="#notifications">通知設定</a></li>
    <li class="group">關於</li>
    <li><a href="#about">關於本應用</a></li>
  </ul>

  <!-- 對話方塊 -->
  <div id="confirm" class="dialog">
    <div class="toolbar">
      <h1>確認</h1>
      <a class="button" href="#">完成</a>
    </div>
    <p>確定要刪除嗎？</p>
    <a class="whiteButton" href="#">取消</a>
    <a class="red button" href="#delete">刪除</a>
  </div>
</body>
</html>
```

### iUI 的導航模式

```javascript
// iUI 支援的三種面板切換
// 1. 內嵌切換（同一頁面）
<a href="#settings">開啟設定</a>

// 2. AJAX 載入（從伺服器取得）
<a href="detail.html">載入詳情</a>

// 3. 對話方塊
<a href="#confirm">開啟對話方塊</a>

// 程式化控制
iui.showPageById('settings');
iui.goBack();
```

## QuickConnection Framework

QuickConnection（簡稱 QC）是一個國人開發的開源行動框架，專為中華電信應用而設計。

### QC 的特色

```javascript
// QC 的模組化設計
QC.Module.define('user', function() {
    return {
        login: function(username, password) {
            return QC.Ajax.post('/api/login', {
                username: username,
                password: password
            });
        },

        logout: function() {
            return QC.Ajax.get('/api/logout');
        },

        getProfile: function() {
            return QC.Ajax.get('/api/profile');
        }
    };
});

// 使用模組
QC.Module.use('user').login('john', 'pass123')
    .then(function(response) {
        console.log('登入成功');
    })
    .catch(function(error) {
        console.error('登入失敗');
    });
```

## jQTouch：jQuery 的行動兄弟

2008 年，jQTouch 發布，它是 jQuery 的行動外掛，提供了類似 iUI 的介面模式。

### jQTouch 設定

```javascript
// 初始化 jQTouch
var jQT = $.jQTouch({
    icon: 'icon.png',
    startupScreen: 'splash.png',
    statusBar: 'black-translucent',
    preloadImages: [
        'images/toolbar.png',
        'images/back_button.png'
    ]
});

// 頁面事件
$('#home').on('pageAnimationStart', function(e, data) {
    if (data.direction === 'out') {
        console.log('離開頁面');
    }
});

$('#home').on('pageAnimationEnd', function(e, data) {
    if (data.direction === 'in') {
        console.log('進入頁面');
    }
});
```

### jQTouch 主題

```css
/* jQTouch 預設主題 */
.theme-jqt ul li {
    border-bottom: 1px solid #999;
    background: -webkit-gradient(linear, 0% 0%, 0% 100%,
        from(#fff), to(#ddd));
}

/* 自訂主題 */
.theme-custom ul li {
    background: rgba(0, 100, 200, 0.1);
}
```

## Sencha Touch

2009 年，Sencha（ExtJS 團隊）發布了 Sencha Touch，這是第一個企業級 HTML5 行動框架。

### Sencha Touch 元件

```javascript
// 建立面板
Ext.Panel({
    fullscreen: true,
    layout: 'card',
    items: [
        {
            xtype: 'toolbar',
            dock: 'top',
            title: '我的應用',
            items: [
                {
                    xtype: 'button',
                    text: '設定',
                    handler: function() {
                        panel.setActiveItem(1);
                    }
                }
            ]
        },
        {
            xtype: 'list',
            itemTpl: '{name}',
            store: myStore,
            listeners: {
                itemtap: function(list, index) {
                    detailPanel.setData(list.getRecord(index).data);
                    panel.setActiveItem(1);
                }
            }
        }
    ]
});
```

## 觸控手勢識別

行動 JavaScript 框架的核心功能之一是手勢識別：

### 基礎手勢

```javascript
// 手勢識別器工廠
function createGestureRecognizer(element) {
    var startX, startY, startTime;
    var threshold = {
        tap: 10,
        longTap: 500,
        swipe: 50
    };

    element.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
        startY = e.touches[0].clientY;
        startTime = Date.now();
    }, false);

    element.addEventListener('touchend', function(e) {
        var endX = e.changedTouches[0].clientX;
        var endY = e.changedTouches[0].clientY;
        var duration = Date.now() - startTime;

        var deltaX = endX - startX;
        var deltaY = endY - startY;

        // 判斷手勢
        if (Math.abs(deltaX) < threshold.tap &&
            Math.abs(deltaY) < threshold.tap) {
            if (duration > threshold.longTap) {
                triggerLongTap(e);
            } else {
                triggerTap(e);
            }
        } else if (Math.abs(deltaX) > threshold.swipe) {
            if (deltaX > 0) {
                triggerSwipeRight(e);
            } else {
                triggerSwipeLeft(e);
            }
        } else if (Math.abs(deltaY) > threshold.swipe) {
            if (deltaY > 0) {
                triggerSwipeDown(e);
            } else {
                triggerSwipeUp(e);
            }
        }
    }, false);
}
```

### 雙指縮放

```javascript
var initialDistance = 0;
var currentScale = 1;

element.addEventListener('touchstart', function(e) {
    if (e.touches.length === 2) {
        initialDistance = getDistance(e.touches[0], e.touches[1]);
    }
}, false);

element.addEventListener('touchmove', function(e) {
    if (e.touches.length === 2) {
        var currentDistance = getDistance(e.touches[0], e.touches[1]);
        var scale = currentDistance / initialDistance;

        element.style.transform = 'scale(' + (currentScale * scale) + ')';
    }
    e.preventDefault();
}, false);

function getDistance(touch1, touch2) {
    var dx = touch1.clientX - touch2.clientX;
    var dy = touch1.clientY - touch2.clientY;
    return Math.sqrt(dx * dx + dy * dy);
}
```

## 框架比較

```
行動 JavaScript 框架比較（2007-2009）：
─────────────────────────────────────────────────────────────
框架          發布時間  檔案大小  依賴       特色
─────────────────────────────────────────────────────────────
iUI           2007      ~15KB     無         模仿 iPhone UI
QuickConnection 2007  ~50KB     Prototype  中華電信應用
jQTouch       2008      ~25KB     jQuery     jQuery 外掛
Sencha Touch  2009      ~150KB    ExtJS      企業級元件
─────────────────────────────────────────────────────────────
```

## 效能優化策略

行動 JavaScript 面臨獨特的效能挑戰：

### 事件委託

```javascript
// 桌面：每個元素一個監聽器
$('.menu-item').each(function() {
    this.addEventListener('click', handleClick);
});

// 行動：事件委託到容器
document.querySelector('.menu').addEventListener('click', function(e) {
    var target = e.target;
    if (target.classList.contains('menu-item')) {
        handleClick.call(target, e);
    }
});
```

### 延遲載入圖片

```javascript
// 懒加載圖片
function lazyLoadImages(container) {
    var observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                var img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });

    container.querySelectorAll('img[data-src]').forEach(function(img) {
        observer.observe(img);
    });
}
```

### 硬體加速

```css
/* 啟用硬體加速 */
.animated-element {
    -webkit-transform: translateZ(0);
    -webkit-backface-visibility: hidden;
    -webkit-perspective: 1000;
}

/* 滑動流暢化 */
.scrollable {
    -webkit-overflow-scrolling: touch;
    overflow-y: scroll;
}
```

## 結語

JavaScript 行動框架的發展從一個側面反映了行動 Web 技術的進步。從最早模仿原生介面的 iUI，到企業級的 Sencha Touch，這些框架在不斷解決一個核心問題：

**如何在瀏覽器的限制下，提供接近原生的使用者體驗？**

隨著瀏覽器能力的提升和 HTML 5 標準的成熟，這個問題的答案正在改變——Web 本身越來越接近原生的能力。

---

## 延伸閱讀

- [iUI+iPhone+UI+framework](https://www.google.com/search?q=iUI+iPhone+UI+framework)
- [jQTouch+touch+framework](https://www.google.com/search?q=jQTouch+touch+framework)
- [Sencha+Touch+framework](https://www.google.com/search?q=Sencha+Touch+HTML5+mobile+framework)
- [touch+event+gesture+recognition+javascript](https://www.google.com/search?q=touch+event+gesture+recognition+javascript)

---

*本篇文章為「AI 程式人雜誌 2007 年 4 月號」本期焦點系列之一。*