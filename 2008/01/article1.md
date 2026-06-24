# Linux 核心與 Android 的關係

## 前言

Android 系統的基礎是 Linux 核心，但要將 Linux 用於手機平台，需要進行大量的修改和最佳化。本文將探討 Linux 核心與 Android 之間的關係。

## Linux 核心簡介

Linux 核心是由 Linus Torvalds 於 1991 年開始開發的作業系統核心，如今已成為世界上最廣泛使用的核心之一。

### 核心的主要功能

- **行程管理**：建立、調度、終結行程
- **記憶體管理**：虛擬記憶體、分頁管理
- **檔案系統**：Ext4、Btrfs 等多種檔案系統
- **網路堆疊**：TCP/IP、Socket 介面
- **裝置驅動**：各種硬體裝置的支援

## Android 與 Linux 的關係

### 使用 Linux 的原因

Google 選擇 Linux 作為 Android 的基礎，有以下幾個原因：

1. **開放原始碼**：Linux 是 GPL 授權，適合開放平台
2. **成熟的驅動程式**：大量硬體廠商提供 Linux 驅動
3. **安全模型**：Unix 風格的權限機制
4. **網路功能**：完整的 TCP/IP 堆疊
5. **可移植性**：支援多種硬體架構

### 需要的修改

Linux 核心雖然功能強大，但並非完全適合手機環境。Android 對 Linux 核心進行了多项修改：

```
┌─────────────────────────────┐
│     Android 框架層          │
├─────────────────────────────┤
│     Android 執行環境         │
├─────────────────────────────┤
│     修改過的 Linux 核心      │
│  (Ashmem, Binder, wakelocks)│
├─────────────────────────────┤
│     硬體抽象層 (HAL)         │
└─────────────────────────────┘
```

## Android 專屬的核心修改

### Binder（IPC 機制）

Binder 是 Android 特有的行程間通訊（IPC）機制，取代了 Linux 傳統的 IPC：

| 特性 | Binder | 傳統 IPC (管道/訊息) |
|------|--------|----------------------|
| 效能 | 高 | 中 |
| 安全性 | 強 | 弱 |
| 支援遠端呼叫 | 原生 | 需自行實作 |

```c
// Binder 核心驅動的簡化概念
struct binder_write_read {
    ssize_t write_size;
    ssize_t write_consumed;
    binder_uintptr_t write_buffer;
    ssize_t read_size;
    ssize_t read_consumed;
    binder_uintptr_t read_buffer;
};
```

### Ashmem（匿名共享記憶體）

Ashmem 提供了記憶體共享機制，讓多個行程可以共享記憶體區域：

- 自動回收未使用的共享記憶體
- 減少記憶體複製，提高效能
- 支援記憶體鎖定

### Power Management（電源管理）

Android 新增了 `wakelocks` 機制來管理電源：

```c
// Wake lock 的使用
 wake_lock(&wake_lock_idle);
 // 進行重要工作
 wake_unlock(&wake_lock_idle);
```

### Low Memory Killer

當記憶體不足時，Low Memory Killer 會終結較不重要的行程以釋放記憶體：

| 優先級 | 行程類型 |
|--------|----------|
| 0 | Foreground Activity |
| 1 | Visible Activity |
| 2 | Service |
| 3 | Background Activity |
| 4 | Empty Activity |

## 核心版本演進

### Android 1.0 - Linux 2.6.25

最初的 Android 版本使用 Linux 2.6.25 核心，包含基本的系統支援。

### 核心版本的演變

```
2008: Linux 2.6.25 (Android 1.0/1.1)
2009: Linux 2.6.27 (Android 1.5 Cupcake)
2010: Linux 2.6.32 (Android 2.2 Froyo)
2011: Linux 2.6.39 (Android 3.x/4.0)
2012: Linux 3.0+ (Android 4.x+)
```

### 版本差異的影響

不同版本的 Linux 核心帶來了不同的功能：

- **記憶體管理改進**：更好的記憶體分配策略
- **電源管理**：更精細的電源控制
- **安全性**：更強的安全機制

## Android 的硬體抽象層 (HAL)

### 為什麼需要 HAL？

Android 不能直接使用標準的 Linux 驅動程式，因為：

1. **商業考量**：保護硬體廠商的智慧財產權
2. **介面標準化**：統一硬體介面
3. **升級彈性**：核心升級不影響硬體支援

### HAL 架構

```
應用程式
    ↓
Framework (Java)
    ↓
Native Libraries (C/C++)
    ↓
HAL (硬體抽象層)
    ↓
Linux Kernel Driver
```

## 驅動程式開發

### Android 驅動程式的特點

在 Android 上開發驅動程式，需要注意：

```c
// Android 驅動程式的結構
#include <linux/module.h>
#include <linux/kernel.h>

static int __init android_driver_init(void) {
    printk(KERN_INFO "Android Driver initialized\n");
    return 0;
}

static void __exit android_driver_exit(void) {
    printk(KERN_INFO "Android Driver removed\n");
}

module_init(android_driver_init);
module_exit(android_driver_exit);
```

## 與主流 Linux 的差異

### 使用者空間差異

Android 的使用者空間（userspace）與傳統 Linux 差異很大：

| 元件 | 傳統 Linux | Android |
|------|-----------|---------|
| C 函式庫 | glibc | Bionic |
| 系統init | SysV init | init.rc |
| Shell | bash | mksh (或 Toolbox) |
| 工具程式 | coreutils | Busybox/Toolbox |

### Bionic libc

Google 開發了 Bionic 作為 Android 的 C 函式庫：

- **小型**：占用空間小，適合嵌入式
- **快速**：針對 ARM 進行最佳化
- **BSD 授權**：避免 GPL 傳染

## 未來展望

Android 對 Linux 核心的貢獻也回饋到了主線：

- Binder 可能在未來進入主線核心
- 電源管理改進已被 Linux 採用
- 記憶體管理最佳化

---

**延伸閱讀**

- [Linux kernel official site](https://www.google.com/search?q=Linux+kernel+official+site)
- [Android+Linux+kernel+modifications](https://www.google.com/search?q=Android+Linux+kernel+modifications)
- [Binder+IPC+Android](https://www.google.com/search?q=Binder+IPC+Android)