# 主題五：虛擬機的藝術

## 什麼是虛擬機？

虛擬機是在作業系統上模擬硬體的軟體，分為兩類：

- **系統虛擬機**：模擬整個硬體平臺（如 VirtualBox、VMware）
- **程序虛擬機**：運行單一程式（如 JVM、.NET CLR、Python VM）

## JVM 架構

Java 虛擬機是最も成熟的程序虛擬機之一：

```
原始碼（.java）
    ↓ [javac]
位元組碼（.class）
    ↓
JVM 類別載入器
    ↓
位元組碼驗證
    ↓
解釋器 / JIT 編譯器
    ↓
本地碼執行
```

### 記憶體區域

```
執行時資料區：
+-----------+  高位址
|   棧     |  執行緒棧
|    ↓     |
|          |
|    ↑     |
|   堆     |  物件記憶體
+-----------+
| 方法區   |  類別元資料
+-----------+
| PC 暫存器|  當前位址
+-----------+
| 本地方法棧|
+-----------+  低位址
```

### 類別載入器

```java
// 類別載入流程
class ClassLoader {
    // 載入 → 驗證 → 準備 → 解析 → 初始化
    Class<?> loadClass(String name) {
        // 1. 檢查是否已載入
        // 2. 委托父類載入器
        // 3. 找到 .class 檔案
        // 4. 驗證位元組碼
        // 5. 分配記憶體
        // 6. 解析符號引用
        // 7. 執行靜態初始化
    }
}
```

## 位元組碼指令

JVM 使用棧式架構的位元組碼：

```java
// Java 原始碼
public class Example {
    public int add(int a, int b) {
        return a + b;
    }
}
```

編譯後的位元組碼：

```
public int add(int, int);
  iconst_0        // 將 0 放入棧（這個是 a）
  iload_1         // 載入引數 a
  iload_2         // 載入引數 b
  iadd            // 彈出兩個 int，相加，壓入結果
  ireturn         // 返回 int
```

### 常見位元組碼指令

| 指令 | 說明 |
|-----|-----|
| iconst_* | 將常數載入棧 |
| iload_* | 將局部變數載入棧 |
| istore_* | 將棧頂存入局部變數 |
| iadd/isub/imul | 整數算術運算 |
| if_icmp* | 整數比較跳轉 |
| getfield/putfield | 欄位存取 |
| invokevirtual | 方法呼叫 |
| new | 建立新物件 |

## 棧幀（Stack Frame）

每個方法呼叫都會創建一個棧幀：

```
棧幀結構：
+-----------+
| 區域變數表 |  args, local vars
+-----------+
| 運算數棧   |  operand stack
+-----------+
| 幀資料    |  常量池引用, etc
+-----------+
```

## 即時編譯與優化

JVM 使用分层編譯：

```java
// JIT 編譯層級
// C1（client）：快速編譯，簡單優化
// C2（server）：慢速編譯，高度優化
```

### 內聯

```java
// 內聯前
int square(int x) { return x * x; }
int calc(int a) { return square(a) + square(a); }

// 內聯後（概念）
int calc(int a) {
    int t = a * a;  // 內聯 square
    return t + t;   // 內聯 square
}
```

### 常數折疊

```java
// 折疊前
int x = 2 * 3 + 4 * 5;

// 折疊後
int x = 6 + 20;
```

## .NET CLR

微軟的 Common Language Runtime 是另一個成熟的虛擬機：

```
原始碼（C#, VB.NET, F#）
    ↓ [編譯器]
CIL（Common Intermediate Language）
    ↓
CLR JIT 編譯
    ↓
機器碼
```

### CLR 的獨特功能

- **即時代碼驗證**：確保記憶體安全
- **異常處理**：結構化異常處理
- **代碼訪問安全**：安全許可權

## Python 虛擬機

Python 使用基於棧的位元組碼：

```python
# Python 位元組碼示例
import dis

def add(a, b):
    return a + b

dis.dis(add)
```

輸出：
```
LOAD_FAST 0        # 載入 a
LOAD_FAST 1        # 載入 b
BINARY_ADD          # 加法
RETURN_VALUE        # 返回
```

## Lua 虛擬機

Lua 使用基於暫存器的虛擬機（與棧式相比更高效）：

```lua
-- Lua 5.3 使用暫存器 VM
-- 位元組碼更加緊湊，執行效率更高
```

## WebAssembly

Wasm 是一個便攜式位元組碼格式：

```
C/C++/Rust
    ↓ [編譯器]
WebAssembly (.wasm)
    ↓
瀏覽器虛擬機
    ↓
機器碼
```

### Wasm 的優勢

- **便攜**：所有主流瀏覽器支援
- **高效**：接近原生效能
- **安全**：記憶體沙箱
- **可驗證**：類型安全

## 虛擬機的安全話題

### 位元組碼驗證

JVM 會驗證所有載入的位元組碼：

```
1. 類別格式驗證
2. 位元組碼驗證（資料流分析）
3. 符號引用驗證
```

### 記憶體安全

虛擬機負責確保：
- 陣列邊界檢查
- 空指標檢查
- 類型安全存取

## 效能調優

### JVM 效能調優

```bash
# 記憶體設定
java -Xms512m -Xmx2g -Xmn256m MyApp

# GC 選擇
java -XX:+UseG1GC MyApp  # G1 GC
java -XX:+UseZGC MyApp    # ZGC（低延遲）
```

### Python 效能

```python
# PyPy：JIT 加速 Python
# 安裝 PyPy：brew install pypy

# 或使用 Numba 進行 JIT
from numba import jit

@jit(nopython=True)
def fast_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total
```

## 小結

虛擬機是現代軟體工程的傑作。從 JVM 到 .NET CLR，從 Python VM 到 WebAssembly，虛擬機技術讓我們能夠寫一次程式，到處運行。