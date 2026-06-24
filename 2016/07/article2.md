# 記憶體對齊與資料結構

## 為什麼要對齊？

CPU 讀取記憶體時有最佳的對齊方式，未對齊的記憶體訪問會導致效能下降甚至錯誤。

## 對齊規則

| 資料型別 | 對齊要求 |
|---------|---------|
| char | 1 byte |
| short | 2 bytes |
| int | 4 bytes |
| float | 4 bytes |
| double | 8 bytes |
| void* | 4/8 bytes |

## 結構體對齊

```cpp
struct Unaligned {
    char a;    // 1 byte + 3 padding
    double b;  // 8 bytes
    char c;    // 1 byte + 7 padding
};
// sizeof(Unaligned) = 24

struct Aligned {
    double b;  // 8 bytes (放在前面)
    char a;    // 1 byte + 1 padding
    char c;    // 1 byte + 2 padding
};
// sizeof(Aligned) = 16
```

## 手動對齊控制

```cpp
#pragma pack(push, 1)
struct Packed {
    char a;
    double b;
    char c;
};
#pragma pack(pop)
// sizeof(Packed) = 10

struct AlignedStruct {
    alignas(16) float vec[4];
};
```

## 動態記憶體對齊

```cpp
float* alignedAlloc(size_t size, size_t alignment) {
    void* ptr;
    posix_memalign(&ptr, alignment, size * sizeof(float));
    return static_cast<float*>(ptr);
}
```

## 快取行對齊

```cpp
struct CacheLineAligned {
    alignas(64) float data[16];
};
```

## 參考資料

- [記憶體對齊詳解](https://www.google.com/search?q=memory+alignment+C++explained)