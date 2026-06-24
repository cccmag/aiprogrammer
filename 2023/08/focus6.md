# 程式碼最佳化

## 為什麼需要最佳化？

編譯器的一個重要任務是產生高效的目標程式碼。程式碼最佳化（Code Optimization）在不改變程式語意的前提下，改善程式的執行速度、記憶體使用或能耗。

最佳化可以發生在不同的層次：

1. **區域最佳化**：在基本區塊內進行的最佳化
2. **全域最佳化**：跨基本區塊進行的最佳化
3. **程序間最佳化**：跨函式的全域最佳化

## 基本區塊與流程圖

基本區塊（Basic Block）是沒有分支的連續指令序列。控制流圖（Control Flow Graph, CFG）以基本區塊為節點，以控制流邊為邊：

```
        [entry]
           |
        [block1]
        /       \
   [block2]   [block3]
        \       /
        [block4]
           |
        [exit]
```

## 常見的最佳化技術

### 1. 常數折疊（Constant Folding）

在編譯期計算可以確定的表達式：

```
x := 3 + 4 * 2
→ x := 11

# LoadImmediate 指令也屬於此類
```

### 2. 常數傳播（Constant Propagation）

將常數變數的值傳播到使用點：

```
x := 5
y := x + 3
→ x := 5
   y := 8
```

### 3. 死碼消除（Dead Code Elimination）

移除永遠不會被使用的變數或程式碼：

```
x := 3
y := 5
z := x + y
# z 從未被使用，可以消除
```

### 4. 公共子表達式消除（CSE）

避免重複計算相同的表達式：

```
a := x + y
b := x + y    # 重複計算
→
t  := x + y
a  := t
b  := t
```

### 5. 複製傳播（Copy Propagation）

減少不必要的複製：

```
t := x
y := t + 1
→ y := x + 1
```

### 6. 迴圈不變式外提（LICM）

將迴圈內不變的計算移到循環外：

```
for i := 1 to 100:
    x := a * b + c   # a*b+c 每次迭代都不變
    y := y + x
→
t  := a * b + c
for i := 1 to 100:
    y := y + t
```

### 7. 強度折減（Strength Reduction）

用便宜的運算取代昂貴的運算：

```
for i := 1 to 100:
    x := i * 3
→
x := 0
for i := 1 to 100:
    x := x + 3
```

## 最佳化的權衡

最佳化並非總是免費的。編譯器需要在以下因素間取得平衡：

1. **編譯時間**：更多最佳化意味著更長的編譯時間
2. **程式碼大小**：某些最佳化（如循環展開）增加程式碼體積
3. **除錯難度**：最佳化後的程式碼與原始碼的對應關係複雜

## 優化級別

大多數編譯器提供不同級別的最佳化：

- **O0**：無最佳化，適合除錯
- **O1**：基本最佳化，平衡編譯時間與效能
- **O2**：積極最佳化，大多數專案的預設選項
- **O3**：極致最佳化，可能增加程式碼體積
- **Os**：針對程式碼大小的最佳化

## 延伸閱讀

- [編譯器最佳化技術](https://www.google.com/search?q=compiler+optimization+techniques)
- [LLVM Pass 架構](https://www.google.com/search?q=LLVM+optimization+pass+architecture)
- [GCC 最佳化選項](https://www.google.com/search?q=GCC+optimization+options+O1+O2+O3)

---

*本篇文章為「AI 程式人雜誌 2023 年 8 月號」編譯器理論系列之六。*
