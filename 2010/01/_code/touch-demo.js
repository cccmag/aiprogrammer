# 觸控介面開發實務

## 概述

本期實作將展示觸控介面開發的核心技術，包括基本觸控事件處理、手勢識別、以及常見的觸控 UI 元件實作。

## 基本觸控事件

```javascript
// touch-demo.js - 基本觸控事件展示
function demo() {
  console.log('=== 基本觸控事件展示 ===');

  const element = document.getElementById('touch-area');

  // 觸控開始
  element.addEventListener('touchstart', (e) => {
    e.preventDefault();
    console.log('Touch Start');
    console.log('Touches:', e.touches.length);

    for (let touch of e.touches) {
      console.log('  ID:', touch.identifier);
      console.log('  X:', touch.clientX);
      console.log('  Y:', touch.clientY);
    }
  }, { passive: false });

  // 觸控移動
  element.addEventListener('touchmove', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    console.log('Touch Move:', touch.clientX, touch.clientY);
  }, { passive: false });

  // 觸控結束
  element.addEventListener('touchend', (e) => {
    console.log('Touch End');
    console.log('Changed Touches:', e.changedTouches.length);
  });

  // 觸控取消
  element.addEventListener('touchcancel', (e) => {
    console.log('Touch Cancelled');
  });

  console.log('觸控監聽器已設定');
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { demo };
}