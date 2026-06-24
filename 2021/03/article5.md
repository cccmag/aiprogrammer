# CUDA Streams 并行

## Stream 基本概念

CUDA Stream 讓不同操作並發執行：

```cpp
cudaStream_t stream1, stream2;
cudaStreamCreate(&stream1);
cudaStreamCreate(&stream2);

// 不同 stream 的操作可以並發
kernel1<<<grid, block, 0, stream1>>>(data1);
kernel2<<<grid, block, 0, stream2>>>(data2);
```

## 同步操作

```cpp
// 等待特定 stream 完成
cudaStreamSynchronize(stream1);

// 等待所有 stream 完成
cudaDeviceSynchronize();

// 查询 stream 狀態
cudaError_t status = cudaStreamQuery(stream1);
```

## 事件（Events）

```cpp
cudaEvent_t start, stop;
cudaEventCreate(&start);
cudaEventCreate(&stop);

cudaEventRecord(start, stream1);
kernel<<<grid, block, 0, stream1>>>(data);
cudaEventRecord(stop, stream1);

cudaEventSynchronize(stop);
float milliseconds = 0;
cudaEventElapsedTime(&milliseconds, start, stop);
```

## 重疊執行

```cpp
// 同時進行記憶體拷貝和核函數執行
cudaMemcpyAsync(d_data, h_data, bytes, cudaMemcpyHostToDevice, stream);
kernel<<<grid, block, 0, stream>>>(d_data);
cudaMemcpyAsync(h_result, d_data, bytes, cudaMemcpyDeviceToHost, stream);
```

---

## 延伸閱讀

- [CUDA Streams 教學](https://www.google.com/search?q=CUDA+streams+tutorial)
- [异動執行](https://www.google.com/search?q=overlapping+CPU+GPU+CUDA)
- [CUDA+事件计時](https://www.google.com/search?q=cudaEvent+timing+example)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*