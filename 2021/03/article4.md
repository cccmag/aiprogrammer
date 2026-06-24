# Warp 與執行效率

## Warp 基本概念

Warp 是 GPU 執行的基本單位，包含 32 個執行緒：

```
Warp 0: thread 0-31
Warp 1: thread 32-63
...
```

所有同一 Warp 的執行緒執行相同指令，但操作不同資料。

## 分支發散（Branch Divergence）

```cpp
if (threadIdx.x < 16) {
    // 只有一半執行緒執行
    data[threadIdx.x] *= 2;
} else {
    // 另一半執行不同的程式碼
    data[threadIdx.x] *= 3;
}
```

### 效能影響

- 發散分支導致執行緒序列化
- 應該盡量避免同一 Warp 內的分支

## 合併記憶體訪問

### 好（合併）

```cpp
//連續執行緒訪問連續記憶體
float value = data[threadIdx.x];  // Good
```

### 壞（不合併）

```cpp
// 隨機訪問
int idx = hash(threadIdx.x);
float value = data[idx];  // Bad
```

## 指令吞吐量

| 指令類型 | 每時鐘週期每 SM |
|---------|----------------|
| 浮點加法 | 32 |
| 浮點乘法 | 32 |
| 特殊函數 | 4 |

---

## 延伸閱讀

- [Warp+執行模型](https://www.google.com/search?q=SIMT+warp+execution+CUDA)
- [分支發散優化](https://www.google.com/search?q=branch+divergence+optimization+GPU)
- [記憶體合併訪問](https://www.google.com/search?q=coalesced+memory+access+CUDA)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*