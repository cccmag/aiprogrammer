# Thrust 與 GPU 演算法

## Thrust 簡介

Thrust 是 CUDA 的高階演算法庫，提供類似 C++ STL 的介面：

```cpp
#include <thrust/host_vector.h>
#include <thrust/device_vector.h>
#include <thrust/sort.h>

int main() {
    thrust::device_vector<int> data(1000000);

    // 初始化
    thrust::sequence(data.begin(), data.end());

    // 排序
    thrust::sort(data.begin(), data.end());

    return 0;
}
```

## 容器類型

```cpp
// 主機端向量（CPU）
thrust::host_vector<float> h_vec(100);

// 設備端向量（GPU）
thrust::device_vector<float> d_vec(100);
```

## 常用演算法

### 變換

```cpp
// 每個元素乘以 2
thrust::transform(vec.begin(), vec.end(),
                  vec.begin(),
                  thrust::placeholders::_1 * 2);
```

### 歸約

```cpp
// 求和
int sum = thrust::reduce(vec.begin(), vec.end(), 0, thrust::plus<int>());

// 最大值
int max = thrust::reduce(vec.begin(), vec.end(),
                        0, thrust::maximum<int>());
```

### 掃描

```cpp
// 前綴和
thrust::inclusive_scan(vec.begin(), vec.end(), vec.begin());
```

### 排序

```cpp
// 鍵值對排序
thrust::sort_by_key(keys.begin(), keys.end(), values.begin());
```

## 與 STL 的比較

| 功能 | Thrust | STL |
|------|--------|-----|
| 容器 | host_vector / device_vector | vector |
| 執行策略 | CUDA GPU | CPU |
| 效能 | 極高 | 一般 |

---

## 延伸閱讀

- [Thrust 官方文檔](https://www.google.com/search?q=Thrust+CUDA+library+documentation)
- [Thrust+範例教學](https://www.google.com/search?q=Thrust+tutorial+examples)
- [GPU+演算法實現](https://www.google.com/search?q=GPGPU+algorithms+Thrust)

*本篇文章為「AI 程式人雜誌 2021 年 3 月號」精選文章。*