# Google 發布 Material Design 設計語言

## 前言

Google 在 2014 年 I/O 大會上發布了 Material Design 設計語言，2015 年這套設計語言開始全面推廣。

## 核心原則

```
Material Design 三大原則：
──────────────────────────

1. 層次感（Material as a Metaphor）
   - 基於紙張與墨水的視覺隱喻
   - 現實物理世界的模擬

2. 大膽鮮明（Dimensionality）
   - 大膽的顏色運用
   - 刻意為之的陰影層次

3. 動畫有意義（Motion with Meaning）
   - 有目的的轉場動畫
   - 使用者操作的回饋
```

## 設計語言要素

```css
/* 色彩系統 */
:root {
  --primary: #2196F3;     /* 藍色主色 */
  --primary-dark: #1976D2;
  --accent: #FF5722;      /* 強調色 */
  --background: #FAFAFA;
  --surface: #FFFFFF;
}

/* 陰影系統 */
.elevation-1 { box-shadow: 0 1px 3px rgba(0,0,0,.12); }
.elevation-2 { box-shadow: 0 3px 6px rgba(0,0,0,.16); }
.elevation-3 { box-shadow: 0 10px 20px rgba(0,0,0,.19); }

/* 動畫 */
transition: all 0.2s ease-in-out;
```

## 影響

Material Design 成為 2015 年最具影響力的 UI 設計語言，影響了無數 Web 和移動應用的設計。

---

## 延伸閱讀

- [Material Design 官方網站](https://www.google.com/search?q=Material+Design+Google+design+language)

---

*本篇文章為「AI 程式人雜誌 2015 年 1 月號」文章之一。*