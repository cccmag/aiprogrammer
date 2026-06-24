# Dalvik 虛擬機器

## 什麼是 Dalvik？

Dalvik 是專為 Android 設計的虛擬機器（Virtual Machine）。它的名稱來自於北歐民間故事中的一個村莊名稱「Dalvik」，這個村莊位於冰島。

與傳統的 Java 虛擬機器（JVM）不同，Dalvik 是基於暫存器的虛擬機器，專門為記憶體和運算資源受限的嵌入式設備進行了最佳化。

## Dalvik vs JVM

### 架構差異

傳統 JVM 是基於堆疊的虛擬機器（Stack-based VM），而 Dalvik 是基於暫存器的虛擬機器（Register-based VM）。

```
基於堆疊的 VM (JVM)：       基於暫存器的 VM (Dalvik)：

堆疊：                    暫存器：
┌─────┐                  ┌─────┐
│  a  │                  │ R0  │
├─────┤                  ├─────┤
│  b  │                  │ R1  │
├─────┤                  ├─────┤
│  c  │                  │ R2  │
└─────┘                  └─────┘
  需多次 push/pop         直接存取暫存器
```

### 效能比較

基於暫存器的 VM 通常在執行速度上更有優勢：

| 特性 | JVM | Dalvik |
|------|-----|--------|
| 指令獲取次數 | 較多 | 較少 |
| 記憶體使用 | 較高 | 較低 |
| 暫存器操作 | 無 | 有 |
| 位元組碼大小 | 較小 | 較大 |
| 行動裝置適用性 | 較差 | 較佳 |

## DEX 位元組碼格式

### 什麼是 DEX？

DEX（Dalvik Executable）是 Dalvik 虛擬機器的位元組碼格式。Android 編譯工具將 Java 原始碼編譯為 `.class` 檔案，再轉換為單一的 `.dex` 檔案。

```
編譯流程：

Java 原始碼 (.java)
      ↓ javac
Java 位元組碼 (.class)
      ↓ dx 工具
Dalvik 位元組碼 (.dex)
```

### DEX 的優勢

**單一檔案包含所有類別**：

傳統 Java 程式每個類別一個 `.class` 檔案，而 Android 將所有類別打包成單一的 `.dex` 檔案。這減少了檔案數量和總大小。

**共用字串常數**：

在 DEX 格式中，重複的字串常值只會儲存一次，大幅節省儲存空間。

**位元組碼驗證**：

Dalvik 的位元組碼驗證過程經過特別設計，在記憶體受限的環境中更有效率。

## Dalvik 的記憶體管理

### 專為手機設計

手機設備的記憶體資源有限，Dalvik 對記憶體管理進行了諸多最佳化：

1. **較小的物件標頭**：Dalvik 物件的記憶體標頭比 JVM 更精簡
2. **不同的 GC 策略**：適合小型設備的垃圾收集機制
3. **獨立的堆積空間**：為每位元組碼解譯器設置最佳化的堆積

### 記憶體限制

早期 Android 設備對每個應用程式的記憶體使用有嚴格限制：

```java
// 應用程式記憶體限制（早期設備）
最大堆積大小：約 16-32 MB
```

這使得開發者必須特別注意記憶體使用效率。

## JIT 編譯

### 即時編譯

Dalvik 支援 JIT（Just-In-Time）編譯，在執行時將熱門的 DEX 位元組碼動態編譯為本地機器碼：

```
第一次執行：
 DEX 位元組碼 → 直譯執行

後續執行：
 DEX 位元組碼 → JIT 編譯 → 本地機器碼執行
```

### AOT 編譯（Android 7.0+）

較新版本的 Android 引入 AOT（Ahead-Of-Time）編譯，在安裝時就將 DEX 編譯為本地碼，提升執行效率。

## 與標準 Java 的差異

### 類別庫差異

Dalvik 使用的類別庫與標準 Java SE 有所不同：

| 類別庫 | 說明 |
|--------|------|
| 核心類別 | java.lang.*, java.util.* |
| 圖形類別 | Android 專用 UI 框架 |
| I/O 類別 | java.io.*, 部分 java.nio.* |
| 網路類別 | java.net.*, Apache HttpClient |

### 不支援的 Java 特性

部分 Java 特性在 Dalvik 中不受支援或有限制：

- **反射 API 有限制**：某些高階用法無法使用
- **無完整 Java Native Interface**：僅支援 JNI
- **類載入器模型不同**：與標準 JVM 有差異

## 程式範例

以下程式展示如何在 Dalvik 上執行簡單的 Java 程式碼：

```java
package com.example;

public class HelloDalvik {
    public static void main(String[] args) {
        int sum = 0;
        for (int i = 1; i <= 100; i++) {
            sum += i;
        }
        System.out.println("Sum: " + sum);
    }
}
```

編譯後會產生 `.dex` 檔案，由 Dalvik VM 執行。

## 未來發展

隨著 Android 的演進，Dalvik 也持續改進：

- **ART（Android Runtime）**：Android 5.0 引入的新執行環境
- **AOT 編譯**：預先編譯提升效能
- **G11n 支援**：更好的國際化支援

---

**延伸閱讀**

- [Dalvik VM documentation](https://www.google.com/search?q=Dalvik+VM+documentation)
- [Android+Execution+environment](https://www.google.com/search?q=Android+execution+environment)
- [DEX+file+format](https://www.google.com/search?q=DEX+file+format+Dalvik)