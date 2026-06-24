# 主題五：觸控手勢識別

## 手勢基礎

### 為何需要手勢識別

手勢識別讓使用者能夠用自然的方式與應用互動：

```
手勢的價值：
──────────────────────
直覺性：     人類自然溝通方式
效率性：     單一動作完成複雜操作
節省空間：   不需工具列按鈕
情感連結：   增加互動樂趣
```

## 基本手勢

### 點擊（Tap）

```javascript
// 點擊偵測
let touchStartTime = 0;
let touchStartPos = { x: 0, y: 0 };

element.addEventListener('touchstart', (e) => {
  touchStartTime = Date.now();
  touchStartPos.x = e.touches[0].clientX;
  touchStartPos.y = e.touches[0].clientY;
});

element.addEventListener('touchend', (e) => {
  const duration = Date.now() - touchStartTime;
  const touch = e.changedTouches[0];
  const dx = touch.clientX - touchStartPos.x;
  const dy = touch.clientY - touchStartPos.y;
  const distance = Math.sqrt(dx*dx + dy*dy);

  // 判定為點擊：時間短且位移小
  if (duration < 300 && distance < 10) {
    console.log('點擊！');
  }
});
```

### 長按（Long Press）

```javascript
let longPressTimer = null;

element.addEventListener('touchstart', (e) => {
  longPressTimer = setTimeout(() => {
    console.log('長按！');
    // 顯示上下文選單
    showContextMenu(e.touches[0]);
  }, 500);
});

element.addEventListener('touchmove', (e) => {
  // 移動超過一定距離，取消長按
  clearTimeout(longPressTimer);
});

element.addEventListener('touchend', () => {
  clearTimeout(longPressTimer);
});
```

### 滑動（Swipe）

```javascript
// 滑動方向偵測
const SWIPE_THRESHOLD = 50;

let startX = 0;
let startY = 0;
let startTime = 0;

element.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
  startY = e.touches[0].clientY;
  startTime = Date.now();
});

element.addEventListener('touchend', (e) => {
  const endX = e.changedTouches[0].clientX;
  const endY = e.changedTouches[0].clientY;
  const dx = endX - startX;
  const dy = endY - startY;
  const duration = Date.now() - startTime;

  // 檢查是否為有效滑動
  if (duration < 300) {
    if (Math.abs(dx) > Math.abs(dy)) {
      // 水平滑動
      if (dx > SWIPE_THRESHOLD) {
        console.log('向右滑動');
      } else if (dx < -SWIPE_THRESHOLD) {
        console.log('向左滑動');
      }
    } else {
      // 垂直滑動
      if (dy > SWIPE_THRESHOLD) {
        console.log('向下滑動');
      } else if (dy < -SWIPE_THRESHOLD) {
        console.log('向上滑動');
      }
    }
  }
});
```

## 多點觸控手勢

### 雙指縮放（Pinch）

```javascript
let initialDistance = 0;
let currentScale = 1;

function getDistance(touch1, touch2) {
  const dx = touch1.clientX - touch2.clientX;
  const dy = touch1.clientY - touch2.clientY;
  return Math.sqrt(dx * dx + dy * dy);
}

element.addEventListener('touchstart', (e) => {
  if (e.touches.length === 2) {
    initialDistance = getDistance(e.touches[0], e.touches[1]);
  }
});

element.addEventListener('touchmove', (e) => {
  if (e.touches.length === 2) {
    e.preventDefault();
    const currentDistance = getDistance(e.touches[0], e.touches[1]);
    const scale = currentDistance / initialDistance;
    currentScale = scale;

    element.style.transform = `scale(${scale})`;
  }
});
```

### 雙指旋轉（Rotation）

```javascript
let initialAngle = 0;
let currentRotation = 0;

function getAngle(touch1, touch2) {
  return Math.atan2(
    touch2.clientY - touch1.clientY,
    touch2.clientX - touch1.clientX
  ) * 180 / Math.PI;
}

element.addEventListener('touchstart', (e) => {
  if (e.touches.length === 2) {
    initialAngle = getAngle(e.touches[0], e.touches[1]);
  }
});

element.addEventListener('touchmove', (e) => {
  if (e.touches.length === 2) {
    const currentAngle = getAngle(e.touches[0], e.touches[1]);
    const angleDiff = currentAngle - initialAngle;
    currentRotation += angleDiff;

    element.style.transform =
      `rotate(${currentRotation}deg) scale(${currentScale})`;

    initialAngle = currentAngle;
  }
});
```

### 雙擊（Double Tap）

```javascript
let lastTapTime = 0;
let lastTapPos = { x: 0, y: 0 };

element.addEventListener('touchend', (e) => {
  const currentTime = Date.now();
  const touch = e.changedTouches[0];
  const dx = touch.clientX - lastTapPos.x;
  const dy = touch.clientY - lastTapPos.y;
  const distance = Math.sqrt(dx*dx + dy*dy);

  // 檢查是否為雙擊（時間內且位置接近）
  if (currentTime - lastTapTime < 300 && distance < 30) {
    console.log('雙擊！');
    // 執行雙擊動作（如放大）
    handleDoubleTap();
  }

  lastTapTime = currentTime;
  lastTapPos.x = touch.clientX;
  lastTapPos.y = touch.clientY;
});
```

## 手勢庫

### Hammer.js（2010 年早期版本）

```javascript
// Hammer.js 手勢識別
const hammer = new Hammer(element);

// 設定偵測選項
hammer.set({ direction: Hammer.DIRECTION_ALL });

// 單一手勢
hammer.on('tap', (e) => {
  console.log('點擊');
});

hammer.on('doubletap', (e) => {
  console.log('雙擊');
});

hammer.on('longpress', (e) => {
  console.log('長按');
});

// 滑動
hammer.on('swipeleft swiperight', (e) => {
  console.log('滑動方向:', e.type);
});

// 多點觸控
hammer.on('pinch', (e) => {
  element.style.transform = `scale(${e.scale})`;
});

hammer.on('rotate', (e) => {
  element.style.transform = `rotate(${e.rotation}deg)`;
});
```

### 基本手勢類型總結

```
手勢類型：
──────────────────────
點擊（tap）：         選擇、確定
雙擊（double tap）：  放大/縮小
長按（long press）：  顯示選單、預覽
滑動（swipe）：       翻頁、刪除
拖曳（drag）：        移動物件
縮放（pinch）：       縮放圖片、地圖
旋轉（rotate）：      旋轉物件
```

## 進階手勢

### 邊緣滑動

```javascript
// 偵測邊緣滑動
const EDGE_THRESHOLD = 30;

element.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];

  // 檢查是否從邊緣開始
  if (touch.clientX < EDGE_THRESHOLD) {
    console.log('從左邊緣滑動');
  }
  if (touch.clientX > window.innerWidth - EDGE_THRESHOLD) {
    console.log('從右邊緣滑動');
  }
});
```

### 拖曳鎖定

```javascript
// 限制為水平或垂直拖曳
let startX = 0;
let startY = 0;
let isHorizontal = null;

element.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
  startY = e.touches[0].clientY;
  isHorizontal = null;
});

element.addEventListener('touchmove', (e) => {
  if (isHorizontal === null) {
    const dx = e.touches[0].clientX - startX;
    const dy = e.touches[0].clientY - startY;

    // 根據初始移動方向鎖定
    if (Math.abs(dx) > 10 || Math.abs(dy) > 10) {
      isHorizontal = Math.abs(dx) > Math.abs(dy);
    }
  }

  if (isHorizontal) {
    // 僅水平移動
    element.style.transform =
      `translateX(${e.touches[0].clientX - startX}px)`;
  } else {
    // 僅垂直移動
    element.style.transform =
      `translateY(${e.touches[0].clientY - startY}px)`;
  }
});
```

## 手勢識別實作

### 手勢狀態機

```javascript
class GestureRecognizer {
  constructor(element) {
    this.element = element;
    this.state = 'idle';
    this.startPos = { x: 0, y: 0 };
    this.lastPos = { x: 0, y: 0 };

    this.bindEvents();
  }

  bindEvents() {
    this.element.addEventListener('touchstart', this.onStart.bind(this));
    this.element.addEventListener('touchmove', this.onMove.bind(this));
    this.element.addEventListener('touchend', this.onEnd.bind(this));
  }

  onStart(e) {
    const touch = e.touches[0];
    this.state = 'started';
    this.startPos = { x: touch.clientX, y: touch.clientY };
    this.lastPos = { x: touch.clientX, y: touch.clientY };
  }

  onMove(e) {
    if (this.state !== 'started') return;

    const touch = e.touches[0];
    const dx = touch.clientX - this.startPos.x;
    const dy = touch.clientY - this.startPos.y;

    this.emit('move', {
      start: this.startPos,
      current: { x: touch.clientX, y: touch.clientY },
      delta: { x: dx, y: dy }
    });
  }

  onEnd(e) {
    const touch = e.changedTouches[0];
    const dx = touch.clientX - this.startPos.x;
    const dy = touch.clientY - this.startPos.y;

    this.emit('end', {
      start: this.startPos,
      end: { x: touch.clientX, y: touch.clientY },
      velocity: {
        x: dx / (Date.now() - this.startTime),
        y: dy / (Date.now() - this.startTime)
      }
    });

    this.state = 'idle';
  }

  emit(event, data) {
    // 發出自訂事件
    this.element.dispatchEvent(new CustomEvent(event, { detail: data }));
  }
}
```

## 手勢與無障礙

### 替換方案

```javascript
// 提供非觸控操作的替代方案
const supportsTouch = 'ontouchstart' in window;

if (!supportsTouch) {
  // 提供滑鼠操作
  element.addEventListener('click', handleClick);
  element.addEventListener('dblclick', handleDoubleClick);

  // 模擬長按（200ms 後釋放）
  let holdTimer;
  element.addEventListener('mousedown', () => {
    holdTimer = setTimeout(() => {
      handleLongPress();
    }, 500);
  });
  element.addEventListener('mouseup', () => {
    clearTimeout(holdTimer);
  });
}
```

---

## 結論

手勢識別是觸控介面的核心。從簡單的點擊到複雜的多點觸控，手勢讓使用者能夠用直覺的方式與裝置互動。

開發手勢系統時要注意：
1. 足夠的門檻值避免誤判
2. 及時的視覺回饋
3. 支援非觸控環境
4. 避免與系統手勢衝突
5. 提供替代操作方式

---

*本期文章到此結束。*