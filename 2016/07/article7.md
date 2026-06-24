# DirectX 12 圖學管線

## DirectX 12 概述

DirectX 12 是微軟新一代圖形 API，提供了更低層級的硬體控制和更高的效能。

## 與 DirectX 11 的主要區別

| 特性 | DX11 | DX12 |
|-----|------|------|
| API 層級 | 高階 | 低階 |
| 多執行緒 | 有限 | 完全支援 |
| 記憶體管理 | 自動 | 手動控制 |
| CPU 負擔 | 較高 | 極低 |

## 命令列印

```cpp
class CommandQueue {
    ID3D12CommandQueue* queue;
    ID3D12CommandAllocator* allocator;
    ID3D12GraphicsCommandList* commandList;

public:
    void init(ID3D12Device* device) {
        D3D12_COMMAND_QUEUE_DESC desc = {};
        desc.Type = D3D12_COMMAND_LIST_TYPE_DIRECT;
        device->CreateCommandQueue(&desc, IID_PPV_ARGS(&queue));

        device->CreateCommandAllocator(
            D3D12_COMMAND_LIST_TYPE_DIRECT,
            IID_PPV_ARGS(&allocator)
        );

        device->CreateCommandList(
            0, D3D12_COMMAND_LIST_TYPE_DIRECT,
            allocator, nullptr,
            IID_PPV_ARGS(&commandList)
        );
    }

    void begin() {
        allocator->Reset();
        commandList->Reset(allocator, nullptr);
    }

    void end() {
        commandList->Close();
        queue->ExecuteCommandLists(1, (ID3D12CommandList**)commandList);
    }
};
```

## 描述符堆

```cpp
class DescriptorHeap {
    ID3D12DescriptorHeap* heap;
    UINT handleSize;
    UINT capacity;
    UINT currentIndex;

public:
    void init(ID3D12Device* device, UINT count) {
        D3D12_DESCRIPTOR_HEAP_DESC desc = {};
        desc.NumDescriptors = count;
        desc.Type = D3D12_DESCRIPTOR_HEAP_TYPE_CBV_SRV_UAV;
        desc.Flags = D3D12_DESCRIPTOR_HEAP_FLAG_SHADER_VISIBLE;

        device->CreateDescriptorHeap(&desc, IID_PPV_ARGS(&heap));
        handleSize = device->GetDescriptorHandleIncrementSize(desc.Type);
        capacity = count;
    }
};
```

## 同步機制

```cpp
class Fence {
    ID3D12Fence* fence;
    HANDLE event;
    UINT64 value;

public:
    void init(ID3D12Device* device) {
        device->CreateFence(0, D3D12_FENCE_FLAG_NONE, IID_PPV_ARGS(&fence));
        event = CreateEvent(nullptr, FALSE, FALSE, nullptr);
    }

    void wait() {
        fence->SetEventOnCompletion(value, event);
        WaitForSingleObject(event, INFINITE);
        value++;
    }
};
```

## 參考資料

- [DirectX 12 教程](https://www.google.com/search?q=DirectX+12+tutorial+beginner)
- [DX12 程式設計指南](https://www.google.com/search?q=DirectX+12+programming+guide)