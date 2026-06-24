# CSS3 動畫與轉場效果：告別 Flash 的動畫革命

## CSS 動畫的歷史背景

### Flash 時代的結束

在 2009 年之前，網頁動畫主要依靠以下技術：

1. **Flash / ActionScript**
   - 強大但需要外掛
   - iOS 不支援
   - SEO 不友好

2. **JavaScript + DOM 操作**
   - 程式碼複雜
   - 效能不佳
   - 各瀏覽器不一致

3. **GIF 動畫**
   - 色彩限制
   - 檔案大
   - 互動性差

```
Flash 動畫的缺點：
┌─────────────────────────────────────┐
│ 1. 需要 Flash Player 外掛          │
│ 2. iPhone/iPad 完全不支援            │
│ 3. 耗電量大，行動裝置不友善          │
│ 4. 無障礙支援差                     │
│ 5. 搜尋引擎難以索引                 │
│ 6. 效能取決於外掛實現               │
└─────────────────────────────────────┘
```

CSS 3 的動畫功能提供了一個優雅的替代方案。

## CSS Transitions（轉場效果）

### 基本語法

```css
.element {
  /* 原始狀態 */
  background-color: blue;
  transition: background-color 0.3s ease;
}

.element:hover {
  /* 最終狀態 */
  background-color: red;
}
```

### transition 屬性詳解

```css
.element {
  /* 完整語法 */
  transition: property duration timing-function delay;

  /* 範例 */
  transition: all 0.3s ease-in-out 0.1s;
}
```

| 屬性 | 說明 |
|------|------|
| property | 要過渡的 CSS 屬性（all, width, background-color 等） |
| duration | 過渡持續時間（s 或 ms） |
| timing-function | 時間函數（ease, linear, ease-in, ease-out, ease-in-out） |
| delay | 延遲時間（s 或 ms） |

### timing-function 圖示

```
ease:        ████████████░░░░░  （先快後慢）
linear:      ████████████████    （等速）
ease-in:     ███░░░░░░░░░░░░    （慢慢開始）
ease-out:    ░░░░░░░░░░████    （慢慢結束）
ease-in-out: ██░░░░░░░░░░██    （慢起慢終）
```

### 多重轉場

```css
.button {
  background-color: #3498db;
  transform: scale(1);
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  transition:
    background-color 0.2s ease,
    transform 0.2s ease,
    box-shadow 0.2s ease;
}

.button:hover {
  background-color: #2980b9;
  transform: scale(1.05);
  box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}
```

## CSS Animations（關鍵影格動畫）

### @keyframes 語法

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

### 動畫屬性

```css
.element {
  animation-name: slideIn;           /* 關鍵影格名稱 */
  animation-duration: 0.5s;          /* 持續時間 */
  animation-timing-function: ease;   /* 時間函數 */
  animation-delay: 0s;                /* 延遲 */
  animation-iteration-count: 1;       /* 播放次數（infinite = 無限） */
  animation-direction: normal;        /* 方向（normal, reverse, alternate） */
  animation-fill-mode: forwards;      /* 播放前後的樣式 */
  animation-play-state: running;       /* 播放/暫停 */
}
```

### 簡寫語法

```css
.element {
  animation: slideIn 0.5s ease-out 0.1s infinite alternate forwards;
}
```

### 百分比關鍵影格

```css
@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-30px);
  }
  100% {
    transform: translateY(0);
  }
}
```

## 實用動畫範例

### 載入指示器

```css
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.loader {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

### 淡入動畫

```css
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.fade-in {
  animation: fadeIn 0.5s ease-out;
}
```

### 彈跳效果

```css
@keyframes bounceIn {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  50% {
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.9);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}
```

### 文字打字效果

```css
@keyframes typing {
  from {
    width: 0;
  }
  to {
    width: 12ch;
  }
}

.typing-text {
  overflow: hidden;
  white-space: nowrap;
  animation: typing 3s steps(12) forwards;
}
```

## 硬體加速

### transform: translateZ(0) 技巧

```css
/* 觸發 GPU 加速，讓動畫更順暢 */
.smooth-animation {
  transform: translateZ(0);
  will-change: transform;
}
```

### 效能優化原則

1. **只動畫 transform 和 opacity**
   - 這兩個屬性不需要重新佈局或重繪
   - 其他屬性動畫效能較差

2. **避免動畫 width 和 height**
   - 會觸發 reflow
   - 使用 transform: scale() 替代

3. **使用 will-change 提示瀏覽器**
   ```css
   .animated-element {
     will-change: transform, opacity;
   }
   ```

### 效能對比

```
動畫效能測試（2009年瀏覽器）：

屬性         效能評級    說明
─────────────────────────────────────
transform    ★★★★★     GPU 加速，最佳選擇
opacity      ★★★★☆     僅重繪效能佳
box-shadow   ★★☆☆☆    效能較差
background   ★★☆☆☆    效能較差
width/height ★☆☆☆☆    觸發 reflow，最差
```

## 瀏覽器支援（2009年）

### 前綴字

```css
.element {
  /* Firefox */
  -moz-transition: all 0.3s ease;
  -moz-animation: slideIn 0.5s ease;

  /* Safari, Chrome */
  -webkit-transition: all 0.3s ease;
  -webkit-animation: slideIn 0.5s ease;

  /* Opera */
  -o-transition: all 0.3s ease;
  -o-animation: slideIn 0.5s ease;

  /* 標準 */
  transition: all 0.3s ease;
  animation: slideIn 0.5s ease;
}
```

### 支援矩陣

| 功能 | Firefox | Safari | Chrome | Opera |
|------|---------|--------|--------|-------|
| transition | 4.0+ | 3.1+ | 1.0+ | 10.5+ |
| @keyframes | 5.0+ | 4.0+ | 1.0+ | 12.0+ |

## CSS 動畫的優勢

```
CSS Animation vs Flash / JavaScript：

┌────────────────┬─────────────┬─────────────┬─────────────┐
│ 特性           │ CSS 動畫    │ Flash       │ JS 動畫     │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ 程式碼複雜度    │ 低          │ 中          │ 高          │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ 效能           │ 好（GPU）   │ 好          │ 一般        │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ 外掛依賴        │ 無          │ 需要        │ 無          │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ 行動裝置支援    │ 好          │ 差          │ 一般        │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ SEO            │ 友好        │ 不友好      │ 友好        │
├────────────────┼─────────────┼─────────────┼─────────────┤
│ 設計工具支援    │ 有限        │ 成熟        │ N/A         │
└────────────────┴─────────────┴─────────────┴─────────────┘
```

## 結語

CSS 3 的動畫功能標誌著網頁動畫的範式轉移。告別 Flash 並不代表放棄豐富的動畫體驗，而是用更開放、更高效的方式來實現。

下一篇文章將介紹 CSS 3 的媒體查詢功能，以及它如何推動了響應式設計的興起。

---

## 延伸閱讀

- [CSS Animations 規格](https://www.google.com/search?q=CSS+animation+W3C+specification)
- [CSS Transitions 規格](https://www.google.com/search?q=CSS+transition+W3C+specification)
- [動畫效能優化](https://www.google.com/search?q=CSS+animation+performance+optimization)
- [Flash 到 CSS 動畫的遷移](https://www.google.com/search?q=migrate+flash+animation+to+CSS)

---

*本篇文章為「AI 程式人雜誌 2009 年 7 月號」焦點系列之一。*