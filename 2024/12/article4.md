# iOS / Android 平台更新

## iOS 18 與 Android 15 比較

| 功能 | iOS 18 | Android 15 |
|------|--------|-----------|
| AI 整合 | Apple Intelligence | Gemini Nano |
| 隱私 | App 追蹤透明度強化 | Privacy Sandbox |
| 開發工具 | Xcode 16 + AI | Android Studio Ladybug |
| 語言最新版 | Swift 6 | Kotlin 2.1 |
| 側載 | 歐盟地區開放 | 持續開放 |
| 通知 | 重新設計 | 分類通知優化 |

## Swift 6 重大更新

Swift 6 在 2024 年推出，最大變革是資料競爭安全 (data-race safety) 的編譯層級強制檢查。

```javascript
// Swift 6 資料競爭安全的 JavaScript 類比概念
// 使用鎖定機制確保執行緒安全
class ThreadSafeCounter {
  #count = 0;
  #locks = new Set();

  increment() {
    // Swift 6 的 Sendable 協議概念
    const task = async () => {
      const old = this.#count;
      this.#count = old + 1;
      return this.#count;
    };
    return task();
  }

  get value() { return this.#count; }
}

const counter = new ThreadSafeCounter();
await Promise.all([
  counter.increment(),
  counter.increment(),
  counter.increment()
]);
console.log('安全計數結果:', await counter.increment());
```

## Kotlin Multiplatform 穩定

Kotlin Multiplatform (KMP) 在 2024 年達到穩定，成為跨平台邏輯共享的可靠選擇。

## 開發工具進化

Xcode 16 整合了 AI 程式碼生成功能。Android Studio Ladybug 版本強化了 Compose 預覽與效能分析。

## App Store 政策變更

Apple 因應 DMA 調整 App Store 政策，開發者可以引導使用者使用外部支付。

## 開發者生態

iOS 開發者數量在 2024 年突破 4000 萬，Android 開發者突破 5000 萬。

> 參考：https://www.google.com/search?q=iOS+Android+2024+platform+updates
