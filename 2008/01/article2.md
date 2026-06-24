# Java 在手機平台的發展

## 前言

Java 是 Android 應用程式開發的主要語言。但 Java 在手機平台的發展，並非從 Android 開始。本文回顧 Java 在手機領域的歷史演進。

## Java ME 的起源

### J2ME 時代

在 Android 出現之前，Java ME（原名 J2ME）是手機應用程式開發的主流技術：

```
Java ME 架構：
┌──────────────────────────┐
│      MIDlet (應用程式)     │
├──────────────────────────┤
│     MIDP (設定檔)         │
├──────────────────────────┤
│     CLDC (連線裝置組態)    │
├──────────────────────────┤
│     Java 執行環境         │
└──────────────────────────┘
```

### CLDC 與 MIDP

**CLDC（Connected Limited Device Configuration）**：
- 適用於記憶體有限的裝置
- 最小需求： 160KB RAM、32KB 儲存空間

**MIDP（Mobile Information Device Profile）**：
- 基於 CLDC
- 提供 UI、網路、儲存等 API

### Java ME 的限制

Java ME 有許多限制，阻礙了它的發展：

```java
// Java ME 的限制
// 1. 有限的 UI 支援
// 2. 效能不佳
// 3. 各廠商實作不一致
// 4. 缺乏統一的資料儲存 API
// 5. 第三方函式庫支援不足

// 範例：簡單的 Java ME 程式
public class HelloMIDlet extends MIDlet {
    public void startApp() {
        Display.getDisplay(this).setCurrent(
            new TextBox("Hello", "Java ME!", 20, 0)
        );
    }
}
```

## Java 在 Android 的角色

### Dalvik VM 的 Java 支援

Android 使用 Dalvik VM 執行 Java 程式碼：

| 特性 | 標準 JVM | Dalvik VM |
|------|----------|-----------|
| 位元組碼格式 | .class | .dex |
| 架構 | 基於堆疊 | 基於暫存器 |
| 記憶體模型 | 較大 | 精簡 |
| 執行模式 | 直譯+JIT | 直譯+JIT+AOT |

### 語法相容性

Android 支援大部分 Java 語法：

```java
// Android 支援的 Java 特性
public class AndroidClass {
    // 類別
    static class InnerClass {}

    // 介面
    interface MyInterface {
        void method();
    }

    // 泛型
    List<String> list = new ArrayList<>();

    // 注解
    @Override
    public void method() {}

    // 列舉
    enum Color { RED, GREEN, BLUE }

    // 可變參數
    public void foo(String... args) {}
}
```

## Android 與標準 Java 的差異

### 類別庫差異

Android 使用的類別庫與 Java SE 有顯著差異：

| 套件 | 支援情況 |
|------|----------|
| java.lang.* | 大部分支援 |
| java.util.* | 支援 |
| java.io.* | 部分支援 |
| javax.net.* | 支援 |
| java.swing/* | 不支援（使用 Android UI） |
| java.applet | 不支援 |

### Android 特有的類別

Android 提供了大量的專屬類別庫：

```java
// Android 專屬類別庫
import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;
import android.content.Intent;
import android.view.View;

// 標準 Java 類別庫
import java.util.HashMap;
import java.io.InputStream;
```

## Android 對 Java 的影響

### 推動 Java 現代化

Android 的成功帶動了 Java 的發展：

1. **Lambda 表達式**：Java 8 加入（受 Android 推動）
2. **現代 API 設計**：Stream API、Optional
3. **效能最佳化**：JVM 持續改進

### 社群影響

- 大量 Java 開發者轉向 Android
- Java 圖書和教學數量大幅增加
- Java 再次成為熱門語言

## Java 版本在 Android 的支援

### 各版本特性

```
Java 1.0-1.4：基礎語法支援
Java 5：   泛型、注解、枚舉、Auto-boxing
Java 6：   更多的標準函式庫
Java 7：   Try-with-resources, Diamond operator
Java 8：   Lambda, Stream API (Android N+)
Java 9+：  模組系統 (仍在發展中)
```

### Android 對 Java 8 的支援

Android 對 Java 8 語法的支援是漸進的：

```java
// Java 8 Lambda 表達式
// 傳統寫法
button.setOnClickListener(new View.OnClickListener() {
    @Override
    public void onClick(View v) {
        doSomething();
    }
});

// Lambda 寫法 (Android N+)
button.setOnClickListener(v -> doSomething());

// 方法參照 (Android N+)
button.setOnClickListener(this::doSomething);
```

## 開發工具演進

### Eclipse + ADT

2008 年的主流開發環境：

```
Eclipse + Android Development Tools (ADT)
├── 程式碼編輯
├── UI 設計工具
├── 模擬器
├── 除錯工具
└── APK 打包
```

### 現代工具

現在的 Android 開發更加現代化：

- **Android Studio**：IntelliJ IDEA 基礎
- **Gradle**：現代建置系統
- **Kotlin**：Android 官方支援的語言

## 未來展望

### Kotlin 的崛起

2017 年，Google 宣佈 Kotlin 為 Android 官方語言：

```kotlin
// Kotlin 範例
class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.main)

        button.setOnClickListener {
            doSomething()
        }
    }
}
```

### Java 的持續演進

Java 仍是 Android 開發的重要語言。隨著時間推移，Android 對新版 Java 的支援將持續改善。

---

**延伸閱讀**

- [Java ME official site](https://www.google.com/search?q=Java+ME+official+site)
- [Android+Java+compatibility](https://www.google.com/search?q=Android+Java+compatibility)
- [Dalvik+vs+JVM](https://www.google.com/search?q=Dalvik+vs+JVM)