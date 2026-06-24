# 主題四：JIT 編譯技術

## JIT 編譯概述

即時編譯（Just-In-Time Compilation）是將位元組碼或中間表示即時編譯為機器碼的技術，結合了編譯和解釋的優點。

```
原始碼 → 位元組碼 → JIT 編譯 → 機器碼
              ↑           ↑
           解釋執行     即時編譯
```

## 為何需要 JIT？

### 解釋執行的問題

```python
# 每次執行都需要解釋
for i in range(1000000):
    result = x + y  # 每次都需要 decode + execute
```

### AOT 編譯的問題

跨平臺困難，需要為每個平臺分別編譯。

### JIT 的優勢

- 跨平臺（只需要平臺相關的 JIT）
- 利用執行時資訊優化
- 彈性部署

## V8 的 JIT 編譯架構

Google 的 V8 JavaScript 引擎採用多層 JIT 編譯：

### 1. Ignition 解釋器

快速啟動，解釋執行位元組碼：

```
JS 原始碼 → Parse → 位元組碼 → Ignition 執行
                               ↓
                        收集分析資料
```

### 2. TurboFan 優化編譯器

對熱點程式碼進行高度優化：

```javascript
// 熱點檢測
function add(a, b) {
    return a + b;
}

for (let i = 0; i < 1000000; i++) {
    add(1, 2);  // 這段程式會被 TurboFan 優化
}
```

### 3. Deoptimization

當假設失敗時回退到直譯執行：

```javascript
function add(a, b) {
    // TurboFan 假設 a, b 都是數字
    return a + b;
}

add(1, 2);     // 數字版本
add("a", "b"); // 類型變化，觸發 Deoptimization
```

## JIT 優化技術

### 內聯（Inlining）

將函式呼叫替換為函式本體：

```python
# 內聯前
def inner(x):
    return x + 1

def outer(x):
    return inner(x) + inner(x)

# 內聯後（概念）
def outer_optimized(x):
    return (x + 1) + (x + 1)  # 直接展開
```

### 類型特殊化（Type Specialization）

為不同類型生成專門的機器碼：

```java
// JIT 可能生成兩個版本
int add(int a, int b) { return a + b; }           // int 版本
double add(double a, double b) { return a + b; }  // double 版本
```

### 逃逸分析（Escape Analysis）

判斷物件是否逃離當前範圍：

```java
// 未逃逸，可以在棧上分配
String result = "";
for (int i = 0; i < 10; i++) {
    result += i;  // JIT 可能優化為 StringBuilder
}
```

### 永遠執行假設（Monorphic Inline Cache）

快取呼叫點的類型資訊：

```python
# 第一個類型：Integer
result = obj.method()  # 快取 obj 是 Integer

# 類型變化：觸發 Megamorphic呼叫
obj = String()
result = obj.method()  # 重新查詢
```

## JIT 的工作流程

```
1. 解釋執行 + 收集プロファイル
2. 識別熱點（Hot Spots）
3. 觸發 JIT 編譯
4. 生成優化機器碼
5. 執行優化碼
6. 若假設失敗，Deoptimize
```

## 各語言的 JIT 實現

### Java：HotSpot JVM

Oracle 的 HotSpot 使用分層編譯：

```
Level 0: 解釋執行
Level 1: 簡單 C1 編譯
Level 2: 有限 C1 編譯
Level 3: 完全 C1 編譯
Level 4: C2 編譯（高度優化）
```

### V8：Ignition + TurboFan

2016 年 V8 開始整合 Ignition 解釋器，減少記憶體使用。

### PyPy：RPython JIT

PyPy 的 JIT 編譯器自動從 Python 解釋器生成 JIT：

```
PyPy 解釋器 → RPython JIT Framework → JIT 編譯器
```

## JIT 的效能考量

### 預熱時間

JIT 需要時間來分析和編譯，不能立即達到最佳效能：

```python
import time

def hot_function():
    # 前幾次呼叫很慢（解釋執行）
    pass

for i in range(10000):
    hot_function()  # 之後會 JIT 編譯
```

### 記憶體使用

JIT 編譯的機器碼占用記憶體：

- HotSpot：Code Cache
- V8：程式碼空間

```java
// JVM 調整 Code Cache 大小
java -XX:ReservedCodeCacheSize=256m MyApp
```

## JVM 的 JIT 選項

```bash
# 列出 JIT 編譯事件
java -XX:+PrintCompilation MyApp

# 顯示內聯資訊
java -XX:+PrintInlining MyApp

# 調整 JIT 閾值
java -XX:CompileThreshold=10000 MyApp
```

## 什麼是 AOT 編譯？

預先編譯（ Ahead-of-Time）與 JIT 相對：

```java
// 使用 jaotc 進行 AOT 編譯
jaotc --output libHelloWorld.so HelloWorld.class
java -XX:AOTLibrary=./libHelloWorld.so HelloWorld
```

## 小結

JIT 編譯是現代虛擬機的核心技術。透過結合解釋執行的快速啟動和編譯執行的高效能，JIT 實現了兩全其美。