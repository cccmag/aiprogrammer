# 目標程式碼生成

## 從 IR 到機器碼

目標程式碼生成（Code Generation）是編譯器的最後階段，將中間表示（IR）轉換為目標機器的實際指令。這個階段涉及指令選擇、暫存器分配和指令排程三大核心問題。

## 指令選擇

指令選擇（Instruction Selection）將 IR 指令映射到目標處理器的真實指令。不同處理器有不同的指令集，選擇的關鍵是覆蓋模式和成本模型。

### 模板匹配

一種常用的指令選擇方法是模式匹配：

```
IR 模式                  x86 指令
─────────               ─────────
t = a + b               ADD t, a, b
t = a * b               MUL t, a, b
t = a + 1               INC t
t = 0                   XOR t, t    (比 MOV t, 0 更高效)
t = a[b]                MOV t, [a + b*scale]
```

### 樹覆蓋

將 IR 表示為樹狀結構，然後用目標機器的指令模式去覆蓋這棵樹。這個問題可以轉化為最短路徑問題，並使用動態規劃求解。

## 暫存器分配

暫存器分配（Register Allocation）決定哪些變數存放在暫存器中，哪些存放在記憶體中。由於暫存器數量有限，這是一個關鍵的效能因素。

### 圖著色演算法

最經典的暫存器分配方法是圖著色（Graph Coloring）：

1. 建立干擾圖（Interference Graph）：節點是虛擬暫存器，邊表示不能共享同一實體暫存器
2. 用 K 種顏色（K 個實體暫存器）對圖著色
3. 如果無法著色，將某些變數溢出（Spill）到記憶體

```
干擾圖範例：
  t1 ── t2
  │      │
  t3 ── t4

如果只有 2 個暫存器：
  R0 = {t1, t4}
  R1 = {t2, t3}
```

### 線性掃描

另一種簡單高效的暫存器分配演算法是線性掃描（Linear Scan），它將變數的生命週期視為區間，然後在活躍變數超過暫存器數量時進行溢出。這種方法比圖著色更快，但可能產生較差的分配結果。

## 指令排程

指令排程（Instruction Scheduling）重新排列指令的順序，以提高處理器管線的利用率。現代處理器有多級管線和多重發射能力，指令順序對效能影響極大。

### 依賴關係

指令排程需要遵守資料依賴關係：

```
RAW (Read After Write): t1 = a + b; t2 = t1 * c  // t2 依賴 t1
WAR (Write After Read): t1 = a + b; a = t2 * c    // 可能需要重新命名
WAW (Write After Write): t1 = a + b; t1 = t2 * c   // 重新命名
```

### 列表排程

列表排程（List Scheduling）是最常用的區域排程演算法：
1. 計算每個指令的優先級
2. 維護一個就緒隊列（依賴已滿足的指令）
3. 每次從隊列中選擇最優指令發射

## 實際範例

對於表達式 `x := 3 + 4 * 2`：

**未最佳化的排程：**
```
LOADI R0 3
LOADI R1 4
LOADI R2 2
MUL   R3 R1 R2
ADD   R4 R0 R3
STORE x R4
```

**經過指令選擇後的 x86 程式碼：**
```asm
mov eax, 4
imul eax, 2
add eax, 3
mov [x], eax
```

## 延伸閱讀

- [指令選擇技術](https://www.google.com/search?q=instruction+selection+compiler+tiling)
- [圖著色暫存器分配](https://www.google.com/search?q=graph+coloring+register+allocation)
- [指令排程](https://www.google.com/search?q=instruction+scheduling+compiler+pipeline)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之七。*
