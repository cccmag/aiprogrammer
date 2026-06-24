# 本期焦點

## Android 開發入門 — Kotlin 與 Jetpack

### 引言

Android 作為全球最大的行動作業系統，每天有超過 30 億台活躍裝置運行著它。從 2008 年第一支 HTC Dream 問世以來，Android 經歷了十多年的演進，如今已經成為一個成熟、完整的開發生態系。

2024 年，隨著 Android 14 的普及和 Android 15 的預覽發布，以及 Kotlin 語言的持續進化，學習 Android 開發正處於最佳時機。本期雜誌將帶領讀者從零開始，全面掌握使用 Kotlin 和 Jetpack 生態系進行 Android 應用程式開發的核心知識。

我們將涵蓋從開發環境建置、語言基礎、宣告式 UI 開發，到資料持久化、網路通訊以及最終發布的完整流程。

---

## 大綱

* [程式實作：Android 概念 Node.js 模擬](focus_code.md)
   - Lifecycle 狀態機模擬
   - ViewModel 狀態管理
   - Navigation 路由模擬
   - Room 資料庫 CRUD 模擬

1. [Android 平台架構](focus1.md)
   - 系統架構四層次
   - Linux 核心與 HAL
   - Android Runtime (ART)
   - 應用框架層
   - 系統應用層

2. [Kotlin 語言基礎](focus2.md)
   - 變數與型別系統
   - 函數與 Lambda
   - 資料類別與密封類別
   - 協程簡介

3. [Jetpack Compose 宣告式 UI](focus3.md)
   - 宣告式 vs 命令式 UI
   - Composable 函數
   - 佈局與修飾符
   - 主題與 Material 3

4. [Activity 與 Fragment 導航](focus4.md)
   - Activity 生命週期
   - Fragment 生命週期
   - Navigation Component
   - 深連結處理

5. [ViewModel 與資料流](focus5.md)
   - MVVM 架構模式
   - ViewModel 原理
   - StateFlow 與 LiveData
   - 狀態提升

6. [Room 資料庫與網路](focus6.md)
   - Room 資料庫設定
   - DAO 與 Entity
   - Retrofit 網路請求
   - Repository 模式

7. [Google Play 上架](focus7.md)
   - 開發者帳號申請
   - App Bundle 與簽署
   - 商店列表最佳化
   - 發布與更新策略

---

## Android 開發生態全景

```
┌─────────────────────────────────────────────┐
│             Android 開發生態系                  │
├─────────────────────────────────────────────┤
│                                             │
│  ┌─────────────────────────────────────┐   │
│  │    應用層 (Your App)                │   │
│  │  Jetpack Compose · ViewModel · Room │   │
│  └──────────┬──────────────────────────┘   │
│             │                               │
│  ┌──────────▼──────────────────────────┐   │
│  │    應用框架層 (Framework)            │   │
│  │  Activity Manager · Window Manager  │   │
│  │  Content Providers · View System    │   │
│  └──────────┬──────────────────────────┘   │
│             │                               │
│  ┌──────────▼──────────────────────────┐   │
│  │    系統執行層 (ART/HAL)             │   │
│  │  Android Runtime · Hardware Abstrac │   │
│  └──────────┬──────────────────────────┘   │
│             │                               │
│  ┌──────────▼──────────────────────────┐   │
│  │    Linux 核心層                     │   │
│  │  行程管理 · 記憶體管理 · 驅動程式    │   │
│  └─────────────────────────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 為什麼選擇 Kotlin + Jetpack？

| 特性 | 說明 |
|------|------|
| 現代語法 | Kotlin 結合 Java 的穩定與現代語言的簡潔 |
| 空安全 | 編譯時期避免 NullPointerException |
| 協程支援 | 簡化非同步與並行程式設計 |
| Jetpack 生態 | Google 官方維護的元件庫 |
| 跨平台潛力 | Kotlin Multiplatform 擴展應用邊界 |

---

## 延伸閱讀

- [Android 平台架構](focus1.md)
- [Kotlin 語言基礎](focus2.md)
- [Jetpack Compose 宣告式 UI](focus3.md)
- [Activity 與 Fragment 導航](focus4.md)
- [ViewModel 與資料流](focus5.md)
- [Room 資料庫與網路](focus6.md)
- [Google Play 上架](focus7.md)

---

*本期焦點到此結束。下期我們將聚焦另一個影響深遠的主題，敬請期待。*
