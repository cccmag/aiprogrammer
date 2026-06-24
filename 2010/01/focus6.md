# 主題六：HTML5 觸控 API

## Touch Events 規範

### 標準 Touch Events

2010 年 W3C 正在制定 Touch Events 規範：

```javascript
// Touch Events 是觸控開發的基礎 API
// 主要事件：touchstart, touchmove, touchend, touchcancel
```

### 事件比較

| 事件 | 觸發時機 | 可用屬性 |
|------|----------|----------|
| touchstart | 手指接觸螢幕 | touches, targetTouches |
| touchmove | 手指移動 | touches, targetTouches |
| touchend | 手指離開螢幕 | changedTouches |
| touchcancel | 觸控中斷 | changedTouches |

### Touch 物件結構

```javascript
interface Touch {
  readonly attribute long    identifier;  // 觸控唯一識別碼
  readonly attribute EventTarget target;  // 觸控目標元素
  readonly attribute long    clientX;     // 視窗座標 X
  readonly attribute long    clientY;     // 視窗座標 Y
  readonly attribute long    pageX;       // 頁面座標 X
  readonly attribute long    pageY;       // 頁面座標 Y
  readonly attribute long    screenX;     // 螢幕座標 X
  readonly attribute long    screenY;     // 螢幕座標 Y
  readonly attribute long    radiusX;     // 觸控範圍 X
  readonly attribute long    radiusY;     // 觸控範圍 Y
  readonly attribute float   rotationAngle; // 觸控旋轉角度
  readonly attribute float   force;       // 觸控壓力（支援與否視裝置）
};
```

## Touch 事件處理

### 基本使用

```javascript
const canvas = document.getElementById('canvas');

canvas.addEventListener('touchstart', (e) => {
  e.preventDefault(); // 防止滾動

  for (let touch of e.touches) {
    console.log('Touch start:', touch.identifier, touch.clientX, touch.clientY);
  }
}, { passive: false });

canvas.addEventListener('touchmove', (e) => {
  e.preventDefault();

  for (let touch of e.touches) {
    // 更新觸控位置
    updateTouchPosition(touch.identifier, touch.clientX, touch.clientY);
  }
}, { passive: false });

canvas.addEventListener('touchend', (e) => {
  for (let touch of e.changedTouches) {
    console.log('Touch end:', touch.identifier);
    removeTouch(touch.identifier);
  }
});
```

### 多點觸控追蹤

```javascript
const activeTouches = new Map();

canvas.addEventListener('touchstart', (e) => {
  for (let touch of e.touches) {
    activeTouches.set(touch.identifier, {
      x: touch.clientX,
      y: touch.clientY,
      startX: touch.clientX,
      startY: touch.clientY
    });
  }
});

canvas.addEventListener('touchmove', (e) => {
  for (let touch of e.touches) {
    const data = activeTouches.get(touch.identifier);
    if (data) {
      data.x = touch.clientX;
      data.y = touch.clientY;
    }
  }
});

canvas.addEventListener('touchend', (e) => {
  for (let touch of e.changedTouches) {
    activeTouches.delete(touch.identifier);
  }
});
```

## Gesture Events

### 早期 Gesture Events（已廢棄）

注意：Gesture Events 已被廢棄，不建議使用：

```javascript
// 已廢棄的 API - 僅供參考
element.addEventListener('gesturestart', (e) => {
  console.log('Gesture start');
});

element.addEventListener('gesturechange', (e) => {
  console.log('Scale:', e.scale);
  console.log('Rotation:', e.rotation);
});

element.addEventListener('gestureend', (e) => {
  console.log('Gesture end');
});
```

### 手勢偵測的現代方式

使用 Touch Events 類比手勢：

```javascript
// 捏合縮放手勢
let lastDistance = 0;

canvas.addEventListener('touchmove', (e) => {
  if (e.touches.length === 2) {
    const distance = Math.hypot(
      e.touches[0].clientX - e.touches[1].clientX,
      e.touches[0].clientY - e.touches[1].clientY
    );

    if (lastDistance > 0) {
      const scale = distance / lastDistance;
      console.log('Pinch scale:', scale);
    }

    lastDistance = distance;
  }
});

canvas.addEventListener('touchend', (e) => {
  if (e.touches.length < 2) {
    lastDistance = 0;
  }
});
```

## Pointer Events

### Pointer Events 簡介

Pointer Events 是統一觸控、鼠標、筆觸的未來標準：

```javascript
// Pointer Events 提供了統一的輸入介面
// 支援：觸控、鼠標、筆觸
```

### 基本使用

```html
<div id="draw-area"></div>

<style>
#draw-area {
  touch-action: none;
}
</style>
```

```javascript
const drawArea = document.getElementById('draw-area');
const points = [];

// pointerdown = touchstart + mousedown
drawArea.addEventListener('pointerdown', (e) => {
  drawArea.setPointerCapture(e.pointerId);
  points.push({ x: e.clientX, y: e.clientY });
});

// pointermove = touchmove + mousemove
drawArea.addEventListener('pointermove', (e) => {
  if (e.buttons > 0) { // 按住時移動
    points.push({ x: e.clientX, y: e.clientY });
    draw();
  }
});

// pointerup = touchend + mouseup
drawArea.addEventListener('pointerup', (e) => {
  drawArea.releasePointerCapture(e.pointerId);
});

// pointercancel
drawArea.addEventListener('pointercancel', (e) => {
  console.log('Pointer cancelled');
});
```

### Pointer Events 屬性

```javascript
interface PointerEvent extends MouseEvent {
  readonly attribute long    pointerId;    // 指標識別碼
  readonly attribute float   width;        // 接觸範圍寬度
  readonly attribute float   height;       // 接觸範圍高度
  readonly attribute float   pressure;     // 壓力（0-1）
  readonly attribute float   tangentialPressure; // 切向壓力
  readonly attribute long    tiltX;        // 水平傾斜
  readonly attribute long    tiltY;        // 垂直傾斜
  readonly attribute long    twist;        // 旋轉角度
  readonly attribute DOMString pointerType; // 指標類型
  readonly attribute boolean isPrimary;    // 是否為主指標
}
```

## 觸控事件效能優化

### 被動監聽器

```javascript
// 使用 passive 提升效能
element.addEventListener('touchstart', handler, { passive: true });
// 瀏覽器可以立即滾動，不等待 handler 完成
```

### 防止不必要的佈局

```javascript
// 避免在 touchmove 中觸發佈局
let lastLayoutTime = 0;

element.addEventListener('touchmove', (e) => {
  // 只在必要時更新佈局
  const now = Date.now();
  if (now - lastLayoutTime > 16) { // ~60fps
    updateLayout();
    lastLayoutTime = now;
  }
}, { passive: true });
```

### 使用 transform 而非 position

```css
.touch-element {
  will-change: transform;
}
```

```javascript
// 使用 transform 動畫（GPU 加速）
element.addEventListener('touchmove', (e) => {
  const x = e.touches[0].clientX;
  const y = e.touches[0].clientY;

  element.style.transform = `translate(${x}px, ${y}px)`;
  // 而非 element.style.left = x + 'px';
});
```

## 觸控事件與滾動

### 滾動與觸控的衝突

```javascript
// 垂直滾動容器
const scrollContainer = document.getElementById('scroll');

// 橫向滑動操作
scrollContainer.addEventListener('touchstart', (e) => {
  this.startX = e.touches[0].clientX;
  this.startY = e.touches[0].clientY;
  this.isScrolling = null;
});

scrollContainer.addEventListener('touchmove', (e) => {
  const dx = e.touches[0].clientX - this.startX;
  const dy = e.touches[0].clientY - this.startY;

  // 判斷滑動意圖
  if (this.isScrolling === null) {
    this.isScrolling = Math.abs(dy) > Math.abs(dx);
  }

  if (!this.isScrolling) {
    e.preventDefault(); // 阻止垂直滾動
    // 執行橫向操作
  }
}, { passive: false });
```

### touch-action CSS

```css
/* 讓瀏覽器處理觸控 */
.touch-auto {
  touch-action: auto;
}

/* 阻止所有觸控操作 */
.touch-none {
  touch-action: none;
}

/* 僅允許垂直滾動 */
.touch-scroll-y {
  touch-action: pan-y;
}

/* 僅允許水平滾動 */
.touch-scroll-x {
  touch-action: pan-x;
}

/* 僅允許捲動，禁用雙擊縮放 */
.touch-manipulation {
  touch-action: manipulation;
}
```

## 觸控偵測

### 功能偵測

```javascript
// 偵測觸控支援
const supportsTouch = 'ontouchstart' in window ||
                      navigator.maxTouchPoints > 0;

// 偵測多點觸控
const supportsMultiTouch = navigator.maxTouchPoints > 1;

// 偵測 Pointer Events
const supportsPointer = 'onpointerdown' in window;
```

### 彈性設計

```javascript
// 根據輸入方式調整事件處理
if (supportsTouch) {
  // 使用 Touch Events
  canvas.addEventListener('touchstart', handleTouch);
  canvas.addEventListener('touchmove', handleTouch);
  canvas.addEventListener('touchend', handleTouch);
} else {
  // 使用 Mouse Events
  canvas.addEventListener('mousedown', handleMouse);
  canvas.addEventListener('mousemove', handleMouse);
  canvas.addEventListener('mouseup', handleMouse);
}

// 使用 Pointer Events（推薦方式）
if (supportsPointer) {
  canvas.addEventListener('pointerdown', handlePointer);
  canvas.addEventListener('pointermove', handlePointer);
  canvas.addEventListener('pointerup', handlePointer);
}
```

---

## 結論

HTML5 Touch Events API 為觸控開發提供了標準化的介面。雖然早期需要處理多個瀏覽器的相容性問題，但統一的 API 讓開發者能夠建立跨平台的觸控應用。

未來的 Pointer Events 將進一步統一輸入介面，提供更好的開發體驗。

關鍵要點：
1. 使用 preventDefault() 防止預設行為
2. 設定被動監聽器提升效能
3. 使用 transform 優化動畫
4. 妥善處理 touch-action CSS
5. 考慮 Pointer Events 作為未來方案

---

*本期文章到此結束。*