# 靜態 vs 動態連結

## 連結基礎

連結是將多個目標檔案合併成單一可執行檔的過程。

## 靜態連結

### 概念

靜態連結在編譯時完成，所有程式碼被複製到最終的可執行檔中。

```bash
# 編譯靜態連結的可執行檔
gcc -static -o program program.c -lm
```

### 優點

- 部署簡單：單一檔案，無需考慮函式庫依賴
- 執行速度稍快：無需在執行時載入
- 離線可執行：不依賴系統函式庫

### 缺點

- 檔案較大：每個可執行檔都包含函式庫副本
- 更新困難：更新函式庫需要重新編譯所有程式
- 記憶體浪費：多個程式載入相同函式庫，占用更多記憶體

## 動態連結

### 概念

動態連結在執行時完成，函式庫作為共享目標被多個程式使用。

```bash
# 編譯動態連結的可執行檔
gcc -o program program.c
```

### 優點

- 檔案較小：共用同一份函式庫
- 更新容易：替換函式庫即可更新
- 記憶體效率：同一份函式庫在記憶體中只有一份

### 缺點

- 部署複雜：需要確保函式庫在系統中
- 執行時開銷：符號解析和載入
- 相容性問題：ABI 相容性

## 函式庫檔案

```
靜態函式庫：libxxx.a
  - 副檔名 .a（archive）
  - 包含目標檔案的集合

動態函式庫：
  - Linux：libxxx.so
  - macOS：libxxx.dylib
  - Windows：xxx.dll
```

## 建立和使用函式庫

### 建立靜態函式庫

```bash
# 1. 編譯為目標檔案
gcc -c foo.c -o foo.o
gcc -c bar.c -o bar.o

# 2. 建立靜態函式庫
ar rcs libmylib.a foo.o bar.o

# 3. 連結
gcc main.c -L. -lmylib -o program
```

### 建立動態函式庫

```bash
# 1. 編譯為位置無關碼（PIC）
gcc -fPIC -c foo.c -o foo.o
gcc -fPIC -c bar.c -o bar.o

# 2. 建立動態函式庫
gcc -shared -o libmylib.so foo.o bar.o

# 3. 連結
gcc main.c -L. -lmylib -o program
```

### RPATH 設定

```bash
# 設定 RPATH
gcc -Wl,-rpath,'$ORIGIN/lib' -o program main.c -L./lib -lmylib
```

## 符號解析

### 延遲綁定

```c
// 使用 dlopen/dlsym 延遲綁定
#include <dlfcn.h>

void *handle = dlopen("./libmylib.so", RTLD_LAZY);
if (handle) {
    int (*func)(int) = dlsym(handle, "my_function");
    if (func) {
        func(42);
    }
    dlclose(handle);
}
```

## 函式庫的符號衝突

### 解決方案

1. **符號版本控制**
2. **靜態連結到單一目標檔案**
3. **隱藏符號**

```bash
# 使用 -fvisibility=hidden
gcc -fvisibility=hidden -shared -o libmylib.so foo.c

# 標記要導出的符號
__attribute__((visibility("default")))
void exported_function() {}
```

## 選擇建議

使用靜態連結：
- 需要簡單部署
- 追求最大執行效率
- 需要離線執行

使用動態連結：
- 需要共享函式庫
- 经常更新函式庫
- 符合標準部署模式

## 結論

理解靜態連結和動態連結的差異，可以幫助你選擇適合的建構策略，並解決部署中的問題。