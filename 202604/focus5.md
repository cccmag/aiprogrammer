# 即時編譯與虛擬機器：JVM、JIT 與 .NET CLR（1990s-2000s）

## 即時編譯的誕生

### 直譯 vs 編譯

傳統的靜態編譯在程式執行之前就將原始碼全部轉換為機器碼。而即時編譯（Just-In-Time Compilation, JIT）則在程式執行過程中，將需要的部分（通常是熱點程式碼）動態編譯為機器碼。

```
┌─────────────────────────────────────────────────────┐
│            靜態編譯 vs 即時編譯                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  靜態編譯（如 C/C++）：                             │
│                                                     │
│  原始碼 ──► 編譯器 ──► 可執行檔 ──► 執行            │
│                         （機器碼）                   │
│                                                     │
│  優點：執行速度快                                    │
│  缺點：需要針對每個平台編譯                          │
│                                                     │
│  即時編譯（如 Java/JVM）：                          │
│                                                     │
│  原始碼 ──► javac ──► bytecode ──► JVM ──► 執行    │
│                         (class)     │               │
│                                     │               │
│                              ┌──────┘               │
│                              ▼                      │
│                        即時編譯器                    │
│                        (熱點程式碼 → 機器碼)        │
│                                                     │
│  優點：跨平台、動態最佳化                            │
│  缺點：啟動時需要暖機                                │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## Smalltalk 與即時編譯的先驅

### 第一個 JIT 系統

Smalltalk-80 是最早採用即時編譯技術的系統之一。1970 年代末，Xerox PARC 的 Smalltalk 團隊面臨一個問題：Smalltalk 的直譯器太慢了。

Dan Ingalls 在 1980 年代開發了 Smalltalk 的即時編譯器，他的設計理念成為後來 JIT 系統的基礎：

1. **位元組碼（Bytecode）**：將原始碼編譯為平台無關的中間碼
2. **虛擬機器（VM）**：執行位元組碼的執行環境
3. **即時編譯**：將頻繁執行的位元組碼編譯為機器碼

## Java 與 JVM 的革命

### Java 的誕生

1995 年，Sun Microsystems 發布了 Java 語言。Java 的核心賣點是「Write Once, Run Anywhere」——這得益於 Java 虛擬機器（JVM）的設計。

```
Java 原始碼 (.java)
      │
      ▼ javac（前端編譯器）
Java Bytecode (.class)
      │
      ▼
┌─────────────────────┐
│ Java Virtual Machine │
│                      │
│  ┌────────────────┐  │
│  │  Class Loader  │  │
│  └────────┬───────┘  │
│           │          │
│           ▼          │
│  ┌────────────────┐  │
│  │  Bytecode      │  │
│  │  Verifier      │  │
│  └────────┬───────┘  │
│           │          │
│           ▼          │
│  ┌────────────────┐  │
│  │  Interpreter   │  │
│  └────────┬───────┘  │
│           │          │
│           ▼          │
│  ┌────────────────┐  │
│  │  JIT Compiler  │  │
│  │ - C1 (Client)  │  │
│  │ - C2 (Server)  │  │
│  └────────────────┘  │
│           │          │
│           ▼          │
│      機器碼           │
└─────────────────────┘
```

### JVM 的即時編譯架構

JVM 的 HotSpot 編譯器（1999 年發布）引入了兩個關鍵概念：

**1. 熱點偵測（Hot Spot Detection）：**

JVM 監控程式執行，找出哪些方法或程式碼路徑被頻繁執行——這些就是「熱點」。

```
// 熱點偵測示意
// 計數器追蹤每個方法的調用次數
class Method {
    int invocation_count = 0;
    
    void execute() {
        invocation_count++;
        if (invocation_count > COMPILE_THRESHOLD) {
            // 這個方法變成熱點了！
            // 調用 JIT 編譯器
            compile_to_native_code(this);
        }
        // 執行方法...
    }
}
```

**2. 分層編譯（Tiered Compilation）：**

HotSpot 提供多個編譯層級，在啟動速度和執行效能之間取得平衡：

| 層級 | 編譯器 | 最佳化程度 | 適用場景 |
|------|--------|-----------|---------|
| 0 | 直譯器 | 無 | 啟動初期 |
| 1 | C1（簡單 JIT） | 低 | 非熱點程式碼 |
| 2 | C1 + 計數 | 低 | 有限編譯 |
| 3 | C1 + 完整分析 | 中 | 收集資訊 |
| 4 | C2（優化 JIT） | 高 | 熱點程式碼 |

### JIT 的動態最佳化

JIT 編譯器可以進行靜態編譯器無法做到的最佳化：

**1. 內置多型分派（Inline Caching）：**

```java
// Java 中的虛函式調用
interface Shape {
    double area();
}

class Circle implements Shape {
    double radius;
    public double area() { return Math.PI * radius * radius; }
}

class Rect implements Shape {
    double w, h;
    public double area() { return w * h; }
}

// JIT 看到大部分調用都是 Circle.area()
// 它會生成：
// if (shape.getClass() == Circle.class)
//     return shape.radius * shape.radius * PI;  // 直接內聯
// else
//     call virtual shape.area();  // 回退到一般調用
```

**2. 逃逸分析（Escape Analysis）：**

```java
// 原始碼
Point sum(Point a, Point b) {
    Point result = new Point(a.x + b.x, a.y + b.y);
    return result;
}

// 如果 JIT 確定 result 不逃逸出當前作用域
// 它可以分配在堆疊上，甚至分配到暫存器中！
// 完全避免堆積分配和 GC 開銷
```

**3. 去最佳化（Deoptimization）：**

```
JIT 編譯器可以根據監控資訊進行大膽假設：
- 「這個方法參數總是 String 類型」
- 「這個條件判斷總是 true」
- 「這個介面調用總是 Circle.area()」

如果假設被打破（例如突然傳入不同類型）：
- JIT 可以「去最佳化」——回退到直譯模式
- 重新編譯以適應新的執行模式
```

### Java JIT 的影響

Java 的 JIT 技術證明了：

1. **動態編譯可以比靜態編譯更快**：JIT 可以利用執行時資訊
2. **跨平台的可行性**：位元組碼 + VM 實現了真正的可攜性
3. **開發體驗與執行效能的平衡**：不需要等待長時間的編譯

## .NET CLR 與共通語言基礎架構

### 微軟的回應

2002 年，微軟發布了 .NET Framework，其核心是 Common Language Runtime（CLR）。CLR 是 JVM 的競爭對手，也是即時編譯技術的另一個重要里程碑。

```
.NET 編譯流程：

C#      VB.NET    F#
  │        │        │
  ▼        ▼        ▼
┌─────────────────────────┐
│ 語言特定編譯器          │
│ (csc, vbc, fsc)        │
└───────────┬─────────────┘
            ▼
      Common Intermediate Language (CIL / IL)
            │
            ▼
┌─────────────────────────┐
│ Common Language Runtime │
│                         │
│  ┌───────────────────┐  │
│  │  JIT Compiler     │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │  NGEN (AOT)       │  │
│  └───────────────────┘  │
│  ┌───────────────────┐  │
│  │  GC               │  │
│  └───────────────────┘  │
└───────────┬─────────────┘
            ▼
         機器碼
```

### CLR 的獨特設計

CLR 引入了幾個重要的編譯器概念：

**1. 泛型的即時編譯：**

```csharp
// C# 泛型
List<T>  // 使用者在程式碼中寫的

// JIT 為不同的 T 生成不同的機器碼
List<int>   → JIT 生成 int 專用版本
List<string> → JIT 生成 string 專用版本

// 但對於參考類型，JIT 會共享程式碼（代碼共享最佳化）
List<string> 和 List<object> 使用同一份機器碼！
```

**2. NGEN（Native Image Generator）：**

CLR 支援提前編譯（AOT），在安裝時就將 IL 編譯為機器碼，減少啟動時間。

**3. RyuJIT：**

2015 年，微軟用 RyuJIT 取代了舊的 JIT 實現。RyuJIT 用 C++ 重寫，支援 SIMD、更好的暫存器分配，以及更快的編譯速度。

## JavaScript 引擎的 JIT 大戰

### 從直譯到 JIT

1995 年，Brendan Eich 在 Netscape 開發了 JavaScript——最初只是一個簡單的直譯器。隨著 Web 應用越來越複雜，JavaScript 的執行速度成為瓶頸。

### V8 引擎的革命

2008 年，Google 發布了 Chrome 瀏覽器，其 V8 JavaScript 引擎引入了革命性的設計：

```
// V8 引擎的編譯管線

JavaScript 原始碼
      │
      ▼
┌─────────────────────┐
│  Parser             │  => AST
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Ignition           │  => Bytecode（2016 引入）
│  (Interpreter)      │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Sparkplug          │  => 非最佳化機器碼（快速生成）
│  (Baseline JIT)     │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│  Turbofan           │  => 高度最佳化機器碼
│  (Optimizing JIT)   │
└─────────────────────┘
```

### V8 的關鍵創新

**1. 隱藏類別（Hidden Classes）：**

```javascript
// JavaScript 中的物件
function Point(x, y) {
    this.x = x;
    this.y = y;
}

var p1 = new Point(1, 2);
var p2 = new Point(3, 4);

// V8 建立隱藏類別：
// Point(1,2) 和 Point(3,4) 共用同一個隱藏類別
// 屬性存取可以轉換為固定偏移量的記憶體讀取！
```

**2. 內聯快取（Inline Caching）：**

```javascript
// 反覆調用同一個函式
function add(a, b) { return a + b; }

// V8 記錄 a 和 b 的類型
// 如果一直是 number，直接生成加法指令
// 如果突變成 string，去最佳化並重新學習
```

### JavaScript JIT 的競爭

2008-2015 年間，瀏覽器廠商展開了激烈的 JavaScript JIT 效能大戰：

| 瀏覽器 | JavaScript 引擎 | JIT 技術 | 發布年份 |
|--------|---------------|---------|---------|
| Chrome | V8 | Ignition + Turbofan | 2008 |
| Firefox | SpiderMonkey | Baseline + IonMonkey | 2008 |
| Safari | JavaScriptCore | LLInt + DFG + FTL | 2008 |
| Edge | Chakra | SimpleJIT + FullJIT | 2015 |

這場競爭使得 JavaScript 的執行效能提升了數百倍，讓 AJAX、單頁應用（SPA）和 Node.js 伺服器端 JavaScript 成為可能。

## JIT 的關鍵優勢

與靜態編譯相比，JIT 具有以下獨特優勢：

### 1. 執行時資訊

```
靜態編譯：只能在編譯時看到靜態資訊
JIT 編譯：可以看到實際的資料型別、分支走向

// JIT 知道：
// - 這個分支 99% 是 true
// - 這個變數總是 int 類型
// - 這個調用總是同一個實作
```

### 2. 適應性最佳化

```
JIT 可以根據執行階段的行為動態調整：
- 啟動階段：使用直譯器或簡單 JIT
- 穩定階段：對熱點程式碼進行深度最佳化
- 行為改變：去最佳化並重新編譯
```

### 3. 按需編譯

```
不需要編譯所有程式碼，只編譯實際執行的部分！
- 不會執行的錯誤處理程式碼：不編譯
- 不常用的功能：維持直譯模式
- 熱點程式碼：深度最佳化
```

## 結語

即時編譯技術的發展，代表了編譯器從「靜態產物」到「動態系統」的轉變。JVM 的 HotSpot 在伺服器端證明了自己的能力；V8 的 JIT 則讓瀏覽器從文件閱讀器進化為應用程式平台。

下一篇文章將探討 2000 年代至今的 LLVM 與現代編譯器基礎設施——一個真正改變了編譯器生態的開源專案。

---

## 延伸閱讀

- [Java HotSpot 效能調優](https://www.google.com/search?q=Java+HotSpot+JIT+compiler)
- [V8 JavaScript 引擎](https://www.google.com/search?q=V8+JavaScript+engine+architecture)
- [.NET RyuJIT 概述](https://www.google.com/search?q=RyuJIT+.NET+JIT+compiler)

---

*本篇文章為「AI 程式人雜誌 2026 年 4 月號」歷史回顧系列之五。*
