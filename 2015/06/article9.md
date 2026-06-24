# C 語言的未來：C2x

## C 標準的歷史

- **C89/C90**：第一個 ANSI/ISO 標準
- **C99**：重要的改進版本
- **C11**：支援多執行緒
- **C17/C18**：錯誤修正
- **C2x**：下一個標準

## C2x 的進展

C2x（預計 2023 年發布）正在積極討論中。

### 已經確定的特性

#### 改善的安全性

- 更多邊界檢查函式（可選）
- 更好的指標安全性

#### 擴充的屬性

```c
[[nodiscard]] int func(void);
[[maybe_unused]] int var;
[[deprecated("用 new_func 代替")]] void old_func(void);
```

## 正在討論的特性

### 契約（Contracts）

```c
void sort(int *arr, size_t n)
    [[ Expects: arr != NULL ]]
    [[ Ensures: is_sorted(arr, n) ]]
{
    // 實作
}
```

### 宣告枚舉的 case

```c
enum Color { RED, GREEN, BLUE };

void foo(enum Color c) {
    case RED: ...
    case GREEN: ...
    // 編譯器警告如果枚舉有未處理的成員
}
```

### nameof 運算子

```c
int my_variable;
const char *name = nameof(my_variable);  // "my_variable"
```

## 持續的改進方向

### 記憶體安全

C2x 正在討論增加更多記憶體安全的特性：
- 更好的靜態分析
- 可選的邊界檢查
- 指標驗證

### 多執行緒改進

C11 引入的執行緒支援將繼續改進。

### 泛型改進

_Generic 的增強。

## 與 C++ 的差異

C 語言繼續保持與 C++ 的差異：
- C 不是 C++ 的子集
- 保持簡單性
- 不引入類別和 OOP 特性

## 社群討論

### 採用新特性

開發者對新特性的態度謹慎：
- 保持向後相容
- 可選特性
- 不增加複雜性

### 記憶體安全的討論

這是 C2x 最重要的話題之一。

## 結論

C 語言持續演進，但保持其核心原則：簡單、高效、接近硬體。C2x 將繼續改善安全性，同時保持 C 的本質。作為系統程式設計師，關注標準的發展可以幫助你準備好使用新特性。