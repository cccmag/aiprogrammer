# 觸控介面程式實作

## 程式碼展示

本期程式碼位於 `_code/` 目錄：

- `touch-demo.js` - 基本觸控事件展示
- `gesture-demo.js` - 手勢識別範例
- `canvas-draw.js` - 觸控繪圖範例

## 觸控事件處理

```javascript
// 基本觸控監聽
element.addEventListener('touchstart', (e) => {
  e.preventDefault();
  console.log('Touches:', e.touches.length);
}, { passive: false });
```

## 手勢識別

```javascript
// 滑動偵測
let startX = 0;
element.addEventListener('touchstart', (e) => {
  startX = e.touches[0].clientX;
});
element.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].clientX - startX;
  console.log('Swipe:', dx > 0 ? 'right' : 'left');
});
```

## 觸控繪圖

```javascript
// Canvas 觸控繪圖
canvas.addEventListener('touchstart', (e) => {
  e.preventDefault();
  const touch = e.touches[0];
  ctx.beginPath();
  ctx.moveTo(touch.clientX, touch.clientY);
});
canvas.addEventListener('touchmove', (e) => {
  const touch = e.touches[0];
  ctx.lineTo(touch.clientX, touch.clientY);
  ctx.stroke();
});
```

---

*本期程式實作到此結束。*