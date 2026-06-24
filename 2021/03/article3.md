# GPU 記憶體管理

## 統一虛擬記憶體（UVM）

### 主機與設備共享虛擬位址

```cpp
// 分配統一路徑
void *ptr;
cudaMallocManaged(&ptr, bytes);

// 主機和設備代碼都可以直接使用
kernel<<<grid, block>>>(ptr);
```

## 分頁鎖定記憶體（Page-Locked）

### 主機記憶體優化

```cpp
float *h_data_pinned;
cudaMallocHost(&h_data_pinned, bytes);
// 或
cudaHostAlloc(&h_data_pinned, bytes, cudaHostAllocDefault);

// 拷貝
cudaMemcpy(d_data, h_data_pinned, bytes, cudaMemcpyHostToDevice);
```

### 優點

- 更高的傳輸頻寬
- 可與重疊的核函數執行
- 支援 DMA（直接記憶體存取）

## 可定址記憶體

### 零拷貝記憶體

```cpp
float *h_data;
cudaHostAlloc(&h_data, bytes, cudaHostAllocWriteCombined |
                          cudaHostAllocMapped);

// 獲取設備指標
float *d_ptr;
cudaHostGetDevicePointer(&d_ptr, h_data, 0);

// 設備直接訪問主機記憶體
kernel<<<grid, block>>>(d_ptr);
```

---

## 延伸閱讀

- [統一記憶體介紹](https://www.google.com/search?q=CUDA+unified+memory)
- [分頁鎖定記憶體](https://www.google.com/search?q=page-locked+host+memory+CUDA)
- [零拷貝技術](https://www.google.com/search?q=zero-copy+CUDA+memory)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*