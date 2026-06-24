# CSS 動畫與過渡

## CSS 過渡（Transition）

CSS 過渡讓屬性值變化時產生平滑的動畫效果，而非瞬間切換。

### 基本語法

```css
.element {
  background: blue;
  transition: background 0.3s ease;
}
.element:hover {
  background: red;
}
```

當滑鼠懸停時，背景色在 0.3 秒內平滑過渡。

### transition 屬性

```css
transition: property duration timing-function delay;

/* 範例 */
transition: all 0.3s ease;
transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
transition: opacity 0.2s, transform 0.3s ease-out;
```

| 屬性 | 說明 |
|------|------|
| transition-property | 要過渡的 CSS 屬性 |
| transition-duration | 持續時間 |
| transition-timing-function | 速度曲線 |
| transition-delay | 延遲時間 |

### 可過渡的屬性

並非所有屬性都可過渡。常見可過渡屬性：

- **transform**：translate、rotate、scale
- **opacity**：透明度（高效能）
- **color、background-color**：顏色
- **width、height、margin、padding**：尺寸（注意效能）

### 最佳化建議

使用 transform 和 opacity 進行動畫，它們可由 GPU 加速：

```css
/* 好：GPU 加速 */
.element {
  transform: translateX(100px);
  opacity: 0.5;
}

/* 不好：觸發重排 */
.element {
  left: 100px;
}
```

---

## CSS 動畫（Animation）

CSS 動畫使用 @keyframes 定義多階段動畫，可以循環播放。

### 基本語法

```css
@keyframes slideIn {
  from {
    transform: translateX(-100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.element {
  animation: slideIn 0.5s ease-out;
}
```

### 多階段動畫

使用百分比定義多個階段：

```css
@keyframes bounce {
  0%   { transform: translateY(0); }
  50%  { transform: translateY(-30px); }
  70%  { transform: translateY(-10px); }
  100% { transform: translateY(0); }
}

.ball {
  animation: bounce 1s ease infinite;
}
```

### animation 屬性

```css
animation: name duration timing-function delay iteration-count direction fill-mode play-state;

/* 範例 */
animation: fadeIn 0.5s ease 0.2s 1 normal forwards;
```

| 屬性 | 說明 |
|------|------|
| animation-name | @keyframes 名稱 |
| animation-duration | 持續時間 |
| animation-timing-function | 速度曲線 |
| animation-delay | 延遲時間 |
| animation-iteration-count | 播放次數（infinite） |
| animation-direction | 方向（normal、reverse、alternate） |
| animation-fill-mode | 結束狀態（forwards、backwards） |
| animation-play-state | 播放狀態（paused、running） |

---

## CSS 動畫範例

### 載入動畫

```css
@keyframes spin {
  to { transform: rotate(360deg); }
}
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #ddd;
  border-top-color: #007bff;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
```

### 淡入效果

```css
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.card {
  animation: fadeIn 0.5s ease forwards;
}
.card:nth-child(2) { animation-delay: 0.1s; }
.card:nth-child(3) { animation-delay: 0.2s; }
```

### 脈衝效果

```css
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}
.btn {
  animation: pulse 2s ease infinite;
}
```

---

## 動畫效能最佳化

### 觸發重排 vs 合成

瀏覽器渲染管線：

```
JavaScript → Style → Layout → Paint → Composite
```

| 操作 | 觸發階段 | 效能 |
|------|---------|------|
| transform | Composite | 最佳 |
| opacity | Composite | 最佳 |
| color | Paint | 一般 |
| width/height | Layout + Paint | 最差 |

### 使用 will-change

提前告知瀏覽器哪些屬性會變化：

```css
.element {
  will-change: transform, opacity;
}
```

不要對太多元素使用 will-change，否則會消耗記憶體。

---

## 實戰：按鈕懸浮效果

```css
.btn {
  padding: 12px 24px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s, background 0.2s;
}
.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,123,255,0.4);
  background: #0056b3;
}
.btn:active {
  transform: translateY(0);
}
```

---

## 延伸閱讀

- [MDN: CSS Transitions](https://www.google.com/search?q=MDN+CSS+transitions)
- [MDN: CSS Animations](https://www.google.com/search?q=MDN+CSS+animations)
- [CSS 動畫效能指南](https://www.google.com/search?q=CSS+animation+performance+guide)
- [cubic-bezier 生成器](https://www.google.com/search?q=cubic+bezier+CSS+generator)

---

*本篇文章為「AI 程式人雜誌 2024 年 3 月號」前端開發系列之一。*
