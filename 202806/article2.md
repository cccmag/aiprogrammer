# vLLM PagedAttention 深入

## 傳統 KV Cache 的問題

Transformer 推理時，每個 token 都需要計算與之前所有 token 的注意力。為了避免重複計算，系統會快取 Key 與 Value 矩陣。問題在於：

1. **記憶體碎片**：KV cache 大小隨著請求動態成長，連續分配導致大量碎片
2. **保留過多**：請求完成前，整塊記憶體被鎖定，無法共享或復用
3. **浪費約 60-80%** 的 GPU 記憶體

## PagedAttention 核心思想

vLLM 將作業系統的**分頁（paging）**概念引入 GPU 記憶體管理：

```python
class PagedKVCache:
    """Simulated PagedAttention KV cache"""
    PAGE_SIZE = 16

    def __init__(self, total_pages: int, d_model: int):
        self.blocks = {}  # page_id -> (k_block, v_block)
        self.page_table = {}  # logical page -> physical page
        self.total_pages = total_pages
        self.d_model = d_model

    def alloc_page(self) -> int:
        """Allocate a physical page"""
        for pid in range(self.total_pages):
            if pid not in self.blocks:
                self.blocks[pid] = (
                    [0.0] * (self.PAGE_SIZE * self.d_model),
                    [0.0] * (self.PAGE_SIZE * self.d_model)
                )
                return pid
        raise MemoryError("GPU OOM")

    def write(self, logical_page: int, key: list, value: list):
        if logical_page not in self.page_table:
            self.page_table[logical_page] = self.alloc_page()
        phys = self.page_table[logical_page]
        k_block, v_block = self.blocks[phys]
        for i, (k, v) in enumerate(zip(key, value)):
            k_block[i % self.PAGE_SIZE * self.d_model + i // self.PAGE_SIZE] = k
            v_block[i % self.PAGE_SIZE * self.d_model + i // self.PAGE_SIZE] = v
```

## 共享分頁（Copy-on-Write）

多個請求的 prefix 相同時（例如系統提示詞），PagedAttention 讓它們**共享同一組物理分頁**：

```python
class Scheduler:
    def fork(self, seq_group, parent_page_table):
        child_table = {}
        for lpage, ppage in parent_page_table.items():
            child_table[lpage] = ppage  # share physical page
            self.ref_count[ppage] += 1
        return child_table
```

## 效能數據

vLLM 在實際部署中：
- 吞吐量提升 **2-4 倍** vs HuggingFace Transformers
- 記憶體利用率從 **~30% 提升至 ~95%**
- 支援 **連續批次**（in-flight batching）

## 實務連結

- [vLLM 官方倉庫](https://www.google.com/search?q=vLLM+PagedAttention)
- [PagedAttention 論文](https://www.google.com/search?q=PagedAttention+efficient+memory+management)
- [vLLM 部署指南](https://www.google.com/search?q=vLLM+deployment+guide)

PagedAttention 是讓 LLM 推理服務從「可用」邁向「高效」的關鍵架構突破。其分頁記憶體管理加上 copy-on-write 共享機制，直接解決了 KV cache 的記憶體浪費問題。
