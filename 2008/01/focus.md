# 本期焦點

## Android 開發環境 — 開放手機平台新時代

### 引言

2007 年 11 月，Google 宣布了 Android 計畫，一個基於 Linux 核心的開放手機平台。2008 年 1 月，Android SDK 預覽版正式開放開發者下載。本期雜誌將帶您深入了解 Android 平台的開發環境，為未來的行動應用開發做好準備。

Android 的誕生標誌著手機產業的重大轉變。不同於傳統的封閉式手機平台，Android 提供了完整的開放原始碼解決方案，讓任何人都能夠開發、測試、和發布應用程式。

---

## 大綱

* [Android SDK 程式實作](focus_code.md)
   - Activity 生命週期
   - Intent 與元件通訊
   - UI 元件範例

1. [Android 的誕生與行動開發新時代](focus1.md)
   - 開放手機聯盟的成立
   - Android 與傳統手機平台的差異
   - 行動開發的新典範

2. [Dalvik 虛擬機器](focus2.md)
   - Dalvik vs JVM
   - 暫存器-based 的設計
   - DEX 位元組碼格式

3. [Android SDK 與開發環境架設](focus3.md)
   - SDK 元件
   - Eclipse 整合開發環境
   - ADT 擴充套件

4. [Activity 與生命週期](focus4.md)
   - Activity 狀態
   - 生命週期回調
   - 堆疊管理

5. [Intent 與元件通訊](focus5.md)
   - Explicit Intent
   - Implicit Intent
   - Intent Filter

6. [UI 設計與 Views](focus6.md)
   - View 層級結構
   - 常見 UI 元件
   - 佈局管理器

7. [Android 開發實戰](focus7.md)
   - 第一個 Hello World
   - 實際開發流程
   - 測試與部署

---

## 濃縮回顧

### Android 架構

```
┌─────────────────┐
│   Applications  │
├─────────────────┤
│   Application   │
│   Framework     │
├─────────────────┤
│   Libraries     │
├─────────────────┤
│   Android       │
│   Runtime       │
├─────────────────┤
│   Linux Kernel  │
└─────────────────┘
```

### Dalvik VM 特點

- 基於暫存器（Register-based）的虛擬機器
- 最佳化於記憶體受限的設備
- DEX 位元組碼格式，適合嵌入式系統

### 四大元件

| 元件 | 用途 |
|------|------|
| Activity | 使用者介面螢幕 |
| Service | 背景執行服務 |
| BroadcastReceiver | 接收系統廣播 |
| ContentProvider | 資料共享機制 |

### Intent 的角色

Intent 是 Android 中的訊息物件，用於啟動 Activity、Service，或傳遞訊息。

```java
// 啟動新的 Activity
Intent intent = new Intent(this, SecondActivity.class);
startActivity(intent);
```

### Activity 生命週期

```
onCreate() → onStart() → onResume()
                          ↓
                 [Activity 運行中]
                          ↓
onPause() → onStop() → onDestroy()
```

---

## 結論與展望

Android 的出現為行動開發者帶來了前所未有的機會。開放的平台上任何人都能發揮創意。隨著 SDK 的持續完善和硬體的進步，Android 應用的未來充滿可能。

在後續的主題中，我們將深入探討 Android 開發的各個面向，從基礎概念到實際應用。

---

## 延伸閱讀

- [Android 的誕生](focus1.md)
- [Dalvik 虛擬機器](focus2.md)
- [SDK 開發環境](focus3.md)
- [Activity 生命週期](focus4.md)
- [Intent 通訊](focus5.md)
- [UI 設計](focus6.md)
- [開發實戰](focus7.md)

---

*本期焦點到此結束。下期我們將探討 Google Chrome 瀏覽器，敬請期待。*