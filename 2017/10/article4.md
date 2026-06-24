# Kotlin 正式支援 iOS 開發

## 前言

Kotlin 1.2 於 2017 年 11 月發布，帶來了多平台程式設計（Multiplatform Projects）的概念，使得 Kotlin 可以同時開發 Android、iOS 和 Web 應用。

## Kotlin/Native

Kotlin/Native 將 Kotlin 程式碼編譯為原生二進位檔，支援 iOS 和其他平台：

```kotlin
// 共享邏輯
expect fun getPlatformName(): String

// Android 實現
actual fun getPlatformName(): String = "Android"

// iOS 實現
actual fun getPlatformName(): String = "iOS"
```

## 多平台專案結構

```
┌─────────────────────────────────────────────────────────┐
│            Kotlin Multiplatform Project                 │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌─────────────┐    ┌─────────────┐                   │
│   │   Android   │    │     iOS     │                   │
│   │   App       │    │     App     │                   │
│   └──────┬──────┘    └──────┬──────┘                   │
│          │                  │                          │
│          └────────┬─────────┘                          │
│                   │                                    │
│            ┌──────┴──────┐                            │
│            │  Shared     │                            │
│            │   Code      │                            │
│            └─────────────┘                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 優勢

- 單一語言開發多平台應用
- 減少重複程式碼
- 統一的開發體驗

---

**延伸閱讀**

- [Kotlin 1.2 Release](https://www.google.com/search?q=Kotlin+1.2+release)
- [Kotlin/Native](https://www.google.com/search?q=Kotlin+Native+iOS)