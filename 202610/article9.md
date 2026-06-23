# Linux 核心記憶體管理與 Rust — 核心記憶體配置器、Slab、頁面管理

## 1. 引言

記憶體管理是驅動程式開發的核心主題。驅動程式需要配置核心記憶體、管理 DMA 緩衝區、處理 MMIO——所有這些都涉及核心記憶體管理子系統的深刻理解。Rust 為核心記憶體管理帶來了什麼改變？本文深入探討。

## 2. 核心記憶體配置器的 Rust 抽象

### 2.1 kmalloc/vmalloc 的 Rust 包裝

Linux 核心提供多種記憶體配置方式，Rust 將它們統一在 `Allocator` trait 下：

| C API | 特性 | Rust 對應 |
|-------|------|----------|
| kmalloc | 低開銷，實體連續 | `Box<T>`（GFP_KERNEL） |
| kzalloc | kmalloc + 歸零 | `Box<T>` with `GFP_ZERO` |
| kmalloc_node | 指定 NUMA 節點 | `Box<T>` with node id |
| vmalloc | 虛擬連續，實體不連續 | `VmallocBox<T>` |
| kcalloc | 陣列分配 | `KVirtBox<[T]>` |
| devm_kmalloc | 裝置生命週期綁定 | `DevmBox<T>` |
| alloc_pages | 直接分配頁面 | `PageAlloc` |

```rust
use kernel::alloc::{flags, Box, KVirtBox, VmallocBox};

// Box<T> — 類似 kmalloc
let data = Box::new::<MyStruct>(MyStruct::new(), flags::GFP_KERNEL)?;

// KVirtBox<[u8]> — 類似 kcalloc
let buf = KVirtBox::<[u8]>::new_slice(1024, flags::GFP_KERNEL | flags::__GFP_ZERO)?;

// VmallocBox — 類似 vmalloc，適用於大型緩衝區
let large_buf = VmallocBox::<[u8]>::new_slice(1024 * 1024, flags::GFP_KERNEL)?;
```

### 2.2 GFP 標誌的型別安全

C 語言中 GFP 標誌是整數常量，容易傳錯。Rust 使用位元旗標型別：

```rust
// C 語言：
// void *ptr = kmalloc(size, GFP_KERNEL | __GFP_RETRY_MAYFAIL);

// Rust 版本——型別安全：
let buf = Box::<[u8]>::new_slice(
    1024,
    flags::GFP_KERNEL | flags::__GFP_RETRY_MAYFAIL,
)?;
```

## 3. Slab 分配器

Slab 分配器是核心中用於管理固定大小物件的機制。驅動程式經常使用它來分配「物件快取」：

```rust
use kernel::slab::KmemCache;

struct MyRequest {
    data: [u8; 256],
    dma_addr: u64,
    flags: u32,
}

// 建立 Slab 快取
static REQ_CACHE: KmemCache<MyRequest> =
    KmemCache::new("my_request", |cache| {
        cache.align(64)  // 快取線對齊
             .ctor(MyRequest::init)  // 建構子
             .flags(SLAB_PANIC)
    });

impl MyDriver {
    fn alloc_request(&self) -> Result<Box<MyRequest>> {
        // 從 Slab 快取分配（比 kmalloc 更快）
        let req = REQ_CACHE.alloc(flags::GFP_ATOMIC)?;
        Ok(req)
    }

    fn free_request(req: Box<MyRequest>) {
        // 歸還到 Slab 快取
        drop(req);  // Drop 時自動回到 cache
    }
}
```

## 4. 頁面級記憶體管理

### 4.1 高階頁面分配

驅動程式有時需要直接操作實體頁面：

```rust
use kernel::mm::{PageAlloc, PageFlags, CompoundPage};

impl MyDev {
    fn allocate_dma_pages(&self, order: u32) -> Result<PageAlloc> {
        // 分配 2^order 個連續的實體頁面
        let pages = PageAlloc::alloc(
            order,
            PageFlags::DMA32 | PageFlags::ZERO,
        )?;

        pr_info!("allocated {} pages at {:#x}\n",
            1 << order, pages.phys_addr());

        Ok(pages)
    }

    fn get_virtual_address(pages: &PageAlloc) -> Result<*mut u8> {
        // 將實體頁面映射到核心虛擬空間
        let ptr = unsafe {
            kernel::mm::kmap(pages.page())
        };
        Ok(ptr as *mut u8)
    }
}
```

### 4.2 IOMMU/IOVA 管理

對於使用 IOMMU 的裝置，驅動程式需要管理 I/O 虛擬位址（IOVA）：

```rust
use kernel::iommu::{IommuDomain, IommuMapping};

impl MyDev {
    fn setup_iommu(&self) -> Result<IommuDomain> {
        // 建立 IOMMU domain
        let domain = IommuDomain::new(self.pci_dev.bus())?;

        // 分配 IOVA 區域
        let iova = domain.alloc_iova(0x1000, 0x10000)?;

        // 將 DMA 緩衝區映射到 IOVA
        let mapping = domain.map(
            &dma_buf,
            iova,
            IommuMapping::READ | IommuMapping::WRITE,
        )?;

        // 將 IOVA 寫入裝置暫存器
        self.regs.writel(DMA_ADDR, iova as u32);

        Ok(domain)
    }
}
```

## 5. 記憶體壓力與回收

核心記憶體是稀缺資源。驅動程式需要正確處理記憶體不足的情況：

```rust
impl MyDev {
    fn allocate_with_backoff(&self) -> Result<Box<[u8]>> {
        // 嘗試分配，允許核心回收記憶體
        let result = Box::<[u8]>::new_slice(1024 * 1024,
            flags::GFP_KERNEL | flags::__GFP_RETRY_MAYFAIL);

        match result {
            Ok(buf) => Ok(buf),
            Err(_) => {
                // 記憶體不足——釋放不必要的快取
                self.shrink_caches();

                // 再次嘗試，這次允許 I/O（可能引起磁碟 I/O）
                Box::<[u8]>::new_slice(1024 * 1024,
                    flags::GFP_KERNEL | flags::__GFP_NOFAIL)
            }
        }
    }

    fn shrink_caches(&self) -> usize {
        let mut freed = 0;
        // 清空不需要的快取資料
        if let Some(cache) = self.read_cache.lock().take() {
            freed += cache.len();
        }
        freed
    }
}
```

## 6. Rust 對核心記憶體管理的安全保證

| 記憶體操作 | C 語言的典型 bug | Rust 的保護 |
|-----------|----------------|------------|
| kmalloc/kfree | 忘記 kfree → 記憶體洩漏 | `Box<T>` Drop 時自動 kfree |
| use-after-free | kfree 後繼續使用 | 借用檢查器阻止使用已釋放記憶體 |
| double free | 重複 kfree → crash | 所有權系統確保每個資源只釋放一次 |
| 緩衝區溢位 | 陣列索引越界 | 運行時邊界檢查（可移除） |
| GFP 標誌錯誤 | 傳錯 GFP 標誌 | 型別系統確保位元組合正確 |
| Slab 物件型別混淆 | 將物件歸還給錯誤的 cache | 泛型 `KmemCache<T>` 型別參數 |
| 實體/虛擬位址混淆 | 在需要實體位址時使用虛擬位址 | `PhysAddr` vs `VirtAddr` 型別區分 |

## 7. 結語

核心記憶體管理是 Rust 在核心中最大的 win 之一。C 語言驅動程式中半數以上的 bug 與記憶體管理不當有關——Rust 的所有權系統、Drop 自動化、型別區分記憶體區域（DMA/VRAM/MMIO），在編譯期就消除了這些整類問題。對於驅動程式開發者來說，這意味著可以將更多精力放在實現硬體特定功能上，而不是追蹤記憶體洩漏或緩衝區溢位。

---

## 延伸閱讀

- [Linux 核心記憶體管理文件](https://www.google.com/search?q=Linux+kernel+memory+management)
- [Linux Slab Allocator](https://www.google.com/search?q=Linux+slab+allocator)
- [Linux IOMMU API](https://www.google.com/search?q=Linux+IOMMU+API)
- [Rust 核心配置器設計](https://www.google.com/search?q=Rust+kernel+allocator+KMemCache)
