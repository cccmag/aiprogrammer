# 主題二：觸控介面設計原則

## 觸控人機互動基礎

### 觸控 vs 傳統輸入

觸控介面與傳統鍵鼠有根本性的差異：

```
輸入方式比較：
──────────────────────────────
鍵盤/滑鼠：      觸控：
──────────────   ──────────────
精確定位        手指觸碰
支援右鍵        無法區分按鍵
支援拖曳        支援拖曳
精細控制        粗略控制
懸停預覽        無懸停狀態
```

### 觸控的特性

1. **直接操作**：手指直接觸碰螢幕上的物件
2. **直覺性**：所見即所得的操作方式
3. **回饋性**：需要視覺或觸覺回饋
4. **連續性**：支援滑動、拖曳等連續動作

## 觸控目標設計

### 最小觸控區域

根據 Apple Human Interface Guidelines：

```
觸控目標大小標準：
─────────────────
最小目標：   44 x 44 點（iOS）
推薦目標：   48 x 48 點以上
兒童/老人：  56 x 56 點以上

間距：      至少 8 點之間距
```

### 觸控目標設計原則

1. **足夠大**：確保手指能準確點擊
2. **間隔足夠**：避免誤觸相鄰目標
3. **位置合理**：重要動作放在拇指易觸及區域
4. **視覺回饋**：點擊後有明確的視覺回應

```javascript
// 觸控目標 CSS 範例
.touch-target {
  min-width: 44px;
  min-height: 44px;
  padding: 8px;
  margin: 4px;
}
```

## 手指操作區域

### 單手操作的黃金區域

```
平板單手操作區域（右手拇指）：
───────────────────────────
         上方（難以觸及）
         ┌─────────┐
         │  困難區 │
         ├─────────┤
         │         │
左側（困難）  │  輕鬆區  │ 右側（輕鬆）
         │         │
         ├─────────┤
         │  困難區 │
         └─────────┘
         下方（難以觸及）
```

### 雙手操作考量

平板使用情境多為雙手握持：

- **遊戲**：雙手拇指操作
- **打字**：外接鍵盤或螢幕鍵盤
- **閱讀**：雙手持平板，無操作

## 手勢設計

### 基本手勢

```
手勢類型：
──────────────────
點擊（Tap）：       選擇/確認
長按（Long Press）： 顯示內容選單
滑動（Swipe）：      翻頁/刪除
拖曳（Drag）：       移動物件
捏合（Pinch）：      縮放
旋轉（Rotate）：     旋轉物件
```

### 系統 vs 應用手勢

**系統手勢**（由作業系統處理）：
- 點擊Home鍵：回主畫面
- 雙擊Home鍵：顯示多工列
- 四指滑動：切換應用（iOS 7+）

**應用手勢**（由應用自訂）：
- 左右滑動：刪除列表項目
- 下拉：重新整理
- 搖晃：復原/重做

### 手勢衝突

避免自訂手勢與系統手勢衝突：

```
常見衝突：
───────────────────────
邊緣滑動：    iOS 系統手勢（回主畫面）
雙擊：        作業系統功能
三指滑動：    文字選取
```

## UI 元件設計

### 按鈕設計

```html
<!-- 觸控友善的按鈕 -->
<button class="touch-button">
  <span>確認</span>
</button>

<style>
.touch-button {
  min-width: 88px;      /* 雙倍最小觸控區 */
  min-height: 44px;
  padding: 12px 24px;
  font-size: 17px;      /* 足夠大的文字 */
  border-radius: 8px;
  background: #007AFF;
  color: white;
}
</style>
```

### 列表設計

```html
<ul class="touch-list">
  <li class="touch-list-item">
    <span class="item-text">列表項目</span>
    <span class="chevron">›</span>
  </li>
</ul>

<style>
.touch-list-item {
  min-height: 44px;
  padding: 12px 16px;
  border-bottom: 1px solid #E5E5E5;
}
</style>
```

### 開關設計

```html
<label class="toggle">
  <input type="checkbox">
  <span class="toggle-track">
    <span class="toggle-thumb"></span>
  </span>
</label>

<style>
.toggle-track {
  width: 51px;
  height: 31px;
  border-radius: 16px;
}
.toggle-thumb {
  width: 27px;
  height: 27px;
  border-radius: 50%;
}
</style>
```

## 視覺回饋

### 觸控回饋類型

```
回饋類型：
──────────────────
視覺回饋：  色彩變化、陰影變化、動畫
觸覺回饋：  震動（Android）
聽覺回饋：  按鍵聲（可關閉）
```

### 點擊狀態

```css
.touch-button:active {
  background: #0056B3;
  transform: scale(0.97);
  transition: all 0.1s;
}

.touch-button:disabled {
  background: #CCCCCC;
  color: #888888;
}
```

### 手勢進行中的視覺指示

```javascript
// 滑動刪除視覺回饋
function onSwipeStart(e) {
  element.classList.add('swiping');
  element.style.transform = 'translateX(0)';
}

function onSwipeMove(e) {
  const deltaX = e.touches[0].clientX - startX;
  element.style.transform = `translateX(${deltaX}px)`;

  // 顯示刪除區域
  if (deltaX < -50) {
    deleteZone.classList.add('visible');
  }
}
```

## 錯誤處理

### 防止誤觸

1. **確認機制**：危險操作需要二次確認
2. **取消區域**：支援滑動取消
3. **時間延遲**：避免快速連點

```javascript
// 防誤觸：長按確認刪除
let longPressTimer;

element.addEventListener('touchstart', () => {
  longPressTimer = setTimeout(() => {
    showDeleteConfirmation();
  }, 500);
});

element.addEventListener('touchend', () => {
  clearTimeout(longPressTimer);
});

element.addEventListener('touchmove', () => {
  clearTimeout(longPressTimer); // 滑動取消長按
});
```

### 錯誤恢復

提供容易的錯誤恢復方式：

- **Undo 功能**：常見操作支援復原
- **草稿儲存**：自動儲存未完成內容
- **確認對話框**：危險操作前詢問

## 多點觸控考量

### 支援多點觸控

```javascript
element.addEventListener('touchstart', (e) => {
  // 支援多點觸控
  for (let touch of e.touches) {
    console.log('Touch:', touch.identifier, touch.clientX, touch.clientY);
  }
});
```

### 夾捏縮放

```javascript
let initialDistance = 0;
let initialScale = 1;

element.addEventListener('touchstart', (e) => {
  if (e.touches.length === 2) {
    initialDistance = getDistance(e.touches[0], e.touches[1]);
    initialScale = currentScale;
  }
});

element.addEventListener('touchmove', (e) => {
  if (e.touches.length === 2) {
    const currentDistance = getDistance(e.touches[0], e.touches[1]);
    currentScale = initialScale * (currentDistance / initialDistance);
    element.style.transform = `scale(${currentScale})`;
  }
});

function getDistance(touch1, touch2) {
  const dx = touch1.clientX - touch2.clientX;
  const dy = touch1.clientY - touch2.clientY;
  return Math.sqrt(dx * dx + dy * dy);
}
```

---

## 結論

觸控介面設計需要不同的思維方式。開發者需要拋開滑鼠時代的假設，重新思考使用者如何與裝置互動。

關鍵原則：
1. 足夠大的觸控目標
2. 合理的元素位置
3. 清晰的手勢區分
4. 及時的視覺回饋
5. 完善的錯誤處理

---

*本期文章到此結束。*