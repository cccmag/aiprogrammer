# JavaScript 插件架構：jQuery 插件與模組化

## 前言

Bootstrap 不僅是一個 CSS 框架，還是一套完整的 JavaScript UI 组件庫。這些组件使用 jQuery 插件的模式實作，提供了一致的 API 和事件處理機制。

本章節將深入探討 Bootstrap 的 JavaScript 插件架構，從 jQuery 插件模式到現代的模組化設計。

## jQuery 插件模式

### 基本插件結構

jQuery 插件是擴展 jQuery 原型物件的方法：

```javascript
// 基本插件模式
$.fn.myPlugin = function() {
  // 'this' 是 jQuery 物件
  return this.each(function() {
    // 對每個匹配元素執行操作
    $(this).text('Hello Plugin');
  });
};

// 使用
$('.target').myPlugin();
```

### 鏈式呼叫

jQuery 的一大特色是鏈式呼叫，插件應該支持這一特性：

```javascript
$.fn.myPlugin = function() {
  return this.css('color', 'red')
             .attr('data-plugin', 'true')
             .addClass('plugin-active');
};
```

### 插件工廠模式

對於需要管理狀態的複雜插件，使用工廠模式：

```javascript
$.fn.modal = function(options) {
  return this.each(function() {
    var $this = $(this);
    var data = $this.data('modal');

    if (!data) {
      // 初始化
      $this.data('modal', {
        target: $this,
        options: $.extend({}, $.fn.modal.defaults, options)
      });
    }
  });
};

$.fn.modal.defaults = {
  backdrop: true,
  keyboard: true,
  show: true
};
```

## Bootstrap 插件架構

### 數據屬性 API

Bootstrap 的核心設計理念是通過 HTML5 data 属性配置插件：

```html
<!-- 通過 data 属性觸發 -->
<button class="btn btn-primary" data-toggle="modal"
        data-target="#myModal">
  開啟模態框
</button>

<!-- 配置選項 -->
<div class="dropdown">
  <button class="btn dropdown-toggle" data-toggle="dropdown"
          data-delay="500" data-hover="dropdown">
    下拉選單
  </button>
</div>
```

### JavaScript API

```javascript
// 程式化調用
$('#myModal').modal({
  backdrop: true,
  keyboard: true
});

// 方法調用
$('#myModal').modal('show');  // 顯示
$('#myModal').modal('hide');  // 隱藏
$('#myModal').modal('toggle'); // 切換

// 銷毀
$('#myModal').modal('dispose');
```

### 事件系統

```javascript
// 監聽事件
$('#myModal').on('show.bs.modal', function(e) {
  // 模態框即將顯示
  console.log('Modal is about to show');
});

$('#myModal').on('shown.bs.modal', function(e) {
  // 模態框已顯示
  console.log('Modal is now visible');
});

$('#myModal').on('hide.bs.modal', function(e) {
  // 模態框即將隱藏
  console.log('Modal is about to hide');
});

$('#myModal').on('hidden.bs.modal', function(e) {
  // 模態框已隱藏
  console.log('Modal is now hidden');
});
```

## 核心插件實作

### Modal（模態框）

```javascript
var Modal = function(element, options) {
  this.options = options;
  this.$body = $(document.body);
  this.$element = $(element);
  this.$backdrop = null;
  this.isShown = false;
};

Modal.prototype.show = function() {
  var that = this;

  if (this.isShown) return;

  this.$body.addClass('modal-open');
  this.$element.addClass('in');
  this.$element.css('display', 'block');

  // 顯示背景
  this.backdrop(function() {
    that.$element.trigger($.Event('shown.bs.modal'));
  });
};

Modal.prototype.hide = function() {
  var that = this;

  if (!this.isShown) return;

  this.$element.removeClass('in');
  this.$element.css('display', 'none');
  this.$body.removeClass('modal-open');

  this.$element.trigger($.Event('hidden.bs.modal'));
};
```

### Dropdown（下拉選單）

```javascript
var Dropdown = function(element) {
  this.$element = $(element);
  this.init();
};

Dropdown.prototype.init = function() {
  this.$element.on('click.bs.dropdown', function(e) {
    $(this).data('bs.dropdown').toggle();
  });
};

Dropdown.prototype.toggle = function() {
  var $parent = this.$element.parent();

  if (this.$element.hasClass('disabled')) return;

  var $ul = this.$element.next('.dropdown-menu');

  if ($ul.is('.open')) {
    $ul.removeClass('open');
    this.$element.removeClass('open');
  } else {
    $ul.addClass('open');
    this.$element.addClass('open');
  }
};
```

### Tab（標籤頁）

```javascript
var Tab = function(element) {
  this.$element = $(element);
};

Tab.prototype.show = function() {
  var $active = this.$element.parent('li').siblings('.active');
  var $next = this.$element.tab('show');

  $active.removeClass('active');
  $next.addClass('active');
};

Tab.prototype.tab = function(tab) {
  var $this = this.$element;

  if (tab === 'show') {
    var href = $this.attr('href');
    var $target = $(href);
    $target.tab('show');
  }

  return $this;
};

// 自動初始化
$(document).on('click.bs.tab.data-api', '[data-toggle="tab"]', function(e) {
  e.preventDefault();
  $(this).tab('show');
});
```

### Transition（過渡動畫）

```javascript
var Transition = function() {
  var el = document.createElement('bootstrap');

  var transEndEventNames = {
    'WebkitTransition': 'webkitTransitionEnd',
    'MozTransition': 'transitionend',
    'OTransition': 'oTransitionEnd',
    'transition': 'transitionend'
  };

  for (var name in transEndEventNames) {
    if (el.style[name] !== undefined) {
      this.transEndEventName = transEndEventNames[name];
      break;
    }
  }
};

Transition.prototype.emulateTransitionEnd = function(duration) {
  var called = false;
  var $el = $(this);

  $el.one(this.transEndEventName, function() {
    called = true;
  });

  setTimeout(function() {
    if (!called) {
      $el.trigger($.support.transition.end);
    }
  }, duration);
};
```

## 插件的組織方式

### IIFE 模式

使用 IIFE（立即調用函數表達式）避免全域污染：

```javascript
;(function($) {
  'use strict';

  var Modal = function(element, options) {
    // ...
  };

  // 插件注册
  $.fn.modal = function(option) {
    return this.each(function() {
      var $this = $(this);
      var data = $this.data('bs.modal');
      var options = typeof option === 'object' && option;

      if (!data) {
        $this.data('bs.modal', new Modal(this, options));
      }
    });
  };

})(jQuery);
```

### 名稱空間

使用統一的命名空間避免衝突：

```javascript
// 所有 Bootstrap 插件使用 'bs.' 前綴
$element.data('bs.modal');
$element.data('bs.dropdown');
$element.data('bs.tab');

// 事件也使用統一前綴
$element.on('show.bs.modal');
$element.on('shown.bs.dropdown');
$element.on('click.bs.button');
```

## 插件的相依性管理

### 可選相依性

某些插件可以獨立使用，某些需要其他插件：

```javascript
var Modal = function(element, options) {
  this.options = options;
  // Modal 可以獨立使用
};

var Tab = function(element) {
  this.$element = $(element);
  // Tab 依賴 Transition
};

Tab.prototype.show = function() {
  // 如果沒有 Transition，降級處理
  if (!$.support.transition) {
    this.$element.tab('show');
    return;
  }

  // 使用 Transition
  this.$element.addClass('transitioning');
};
```

### 聲明相依性

```javascript
// 在插件頂部註明相依性
/**
 * Dropdown Require:
 * - jQuery
 * - Bootstrap Transition (optional)
 */
```

## 結語

Bootstrap 的 JavaScript 插件架構體現了幾個重要的設計原則：

1. **聲明式配置**：通過 HTML 属性即可配置插件行為
2. **一致的 API**：所有插件使用相同的方法命名
3. **事件驅動**：使用 jQuery 事件系統進行通信
4. **狀態管理**：通過 jQuery data() 儲存實例狀態

這些設計模式讓 Bootstrap 的插件既容易使用又容易擴展，影響了後續眾多 UI 框架的 JavaScript 架構設計。

下一篇文章我們將探討前端工具鏈的演化，看看 Less、Sass 和構建系統如何改變了樣式表的開發方式。

---

## 延伸閱讀

- [jQuery Plugin Development](https://www.google.com/search?q=jQuery+plugin+development+pattern)
- [Bootstrap JavaScript API](https://www.google.com/search?q=Bootstrap+javascript+API)
- [jQuery Data Method](https://www.google.com/search?q=jQuery+data+method+usage)

---

*本篇文章為「AI 程式人雜誌 2010 年 7 月號」歷史回顧系列之一。*