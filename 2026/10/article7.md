# LLM 在核心安全審計中的應用 — 用 AI 發現驅動程式漏洞

## 1. 引言

Linux 核心的驅動程式是安全漏洞的最大來源之一。根據 2025 年的統計，超過 70% 的核心安全漏洞出現在驅動程式中——這並不意外，因為驅動程式由大量第三方開發者撰寫，對安全最佳實踐的理解參差不齊。大型語言模型（LLM）在程式碼分析方面的能力正在改變這一現狀。

## 2. 核心驅動程式的常見漏洞類型

### 2.1 記憶體安全漏洞

在 C 語言驅動程式中，記憶體安全漏洞是最常見的：

```c
// 典型 C 驅動漏洞：緩衝區溢位
static ssize_t my_read(struct file *fp, char __user *buf,
                       size_t count, loff_t *off) {
    char tmp[64];
    // 如果 count > 64，發生堆疊溢位！
    copy_to_user(buf, tmp, count);
    return count;
}

// 典型 C 驅動漏洞：釋放後使用
static void my_irq_handler(void *data) {
    struct my_dev *dev = data;
    // 如果 dev 已被 kfree，這裡是 UAF！
    writel(0, dev->regs);
}
```

### 2.2 邏輯漏洞

```c
// 整數溢位導致緩衝區過小
static int my_ioctl(struct file *fp, unsigned int cmd, unsigned long arg) {
    unsigned int size = arg;
    // 如果 arg = 0xFFFFFFFF，size + 1 溢位為 0
    void *buf = kmalloc(size + 1, GFP_KERNEL);
    copy_from_user(buf, (void __user *)arg, size); // 堆積溢位！
}
```

## 3. LLM 在程式碼審計中的應用

### 3.1 靜態分析的增強

傳統靜態分析工具（如 Coccinelle、Sparse、Smatch）可以發現部分漏洞，但召回率有限：

| 漏洞類型 | 傳統靜態分析 | LLM 增強分析 |
|---------|------------|------------|
| 緩衝區溢位 | ~60% | ~88% |
| 釋放後使用 | ~45% | ~82% |
| 競爭條件 | ~25% | ~71% |
| 整數溢位 | ~55% | ~85% |
| 邏輯錯誤 | ~10% | ~65% |

### 3.2 LLM 審計的工作流程

```
1. 原始碼輸入
2. LLM 建立控制流程圖（CFG）
3. 分析每個執行路徑的資源管理
4. 交叉比對：lock/unlock、alloc/free、get/put
5. 標記異常模式
6. 生成漏洞報告（含解釋和修復建議）
```

### 3.3 實際案例

以下是一個 LLM 發現的真實漏洞範例：

```rust
// 開發者提交的 Rust 驅動程式碼
impl MyDev {
    fn process_packet(&self, data: &[u8]) -> Result<()> {
        let mut buf = vec![0u8; 1024];

        // LLM 警告：data.len() 可能超過 1024，導致 panic
        buf[..data.len()].copy_from_slice(data);

        Ok(())
    }
}

// LLM 建議的修復
fn process_packet(&self, data: &[u8]) -> Result<()> {
    let len = core::cmp::min(data.len(), 1024);
    let mut buf = vec![0u8; len];
    buf.copy_from_slice(&data[..len]);
    Ok(())
}
```

## 4. 競爭條件檢測

LLM 在分析併發問題時表現出色，因為它能理解鎖定語義：

```rust
// LLM 分析以下程式碼：
fn irq_handler(dev: &MyDev) {
    // LLM 標記：可能需要持有 lock 才能安全存取 shared_data
    let val = dev.shared_data.load(Ordering::Relaxed);

    if val != 0 {
        // LLM 警告：此處在中斷上下文呼叫可能導致死結
        // 如果 spinlock 已被 process_context 持有
        dev.mutex.lock();
        dev.process(val);
        dev.mutex.unlock();
    }
}
```

LLM 會輸出如下分析：

```
安全問題分析報告
────────────────
檔案: src/driver.rs:42
嚴重度: HIGH
類型: 競爭條件

描述: irq_handler 在未確認鎖定狀態的情況下存取
shared_data。Relaxed ordering 無法保證跨 CPU 的可見性。

建議:
1. 使用 AtomicU32 搭配 Ordering::Acquire/Release
2. 或在中斷上下文中使用 spin_lock_irqsave
```

## 5. 自動化漏洞挖掘

2025-2026 年間，出現了多個專門用於核心漏洞挖掘的 LLM 工具：

### 5.1 KernelGPT

KernelGPT 是一個基於 LLM 的核心漏洞自動挖掘系統：

```bash
# 掃描一個驅動程式目錄
kernelgpt scan drivers/net/ethernet/intel/ --model claude-6

# 輸出格式：
[INFO] Scanning 47 files...
[HIGH] drivers/net/ethernet/intel/ixgbe/ixgbe_main.c:1234
  → Use-after-free in ixgbe_clean_rx_irq()
  → Confidence: 92%
  → CVE: CVE-2026-1234

[MEDIUM] drivers/net/ethernet/intel/e1000e/netdev.c:567
  → Double unlock in e1000e_update_stats()
  → Confidence: 78%
```

### 5.2 模糊測試的 AI 增強

LLM 也可以增強傳統的模糊測試（Fuzzing）工具：

```rust
// LLM 根據驅動程式碼生成的智能測試案例
#[test]
fn ioctl_edge_cases() {
    // LLM 生成邊界情況測試
    // 從 ioctl handler 分析得出：
    // - cmd=0, arg=0  → 正常
    // - cmd=0, arg=INVALID → 錯誤處理
    // - cmd=0xFF, arg=0  → 預設分支
    // - cmd=IOCTL_RESET, arg=任意值 → 重置操作
    // - 連續多次 IOCTL_RESET → 重入測試
}
```

## 6. 與傳統工具協作

LLM 不是取代傳統安全工具，而是增強它們：

```
傳統靜態分析 (Smatch, Coccinelle)
    → 產生初始候選清單
    → LLM 過濾誤報、補充上下文
    → 開發者審查

模糊測試 (syzkaller)
    → 觸發 crash
    → LLM 分析 crash dump 並定位根因
    → LLM 生成修補程式

形式化驗證 (Kani, Creusot)
    → 定義安全屬性
    → LLM 自動推導驗證契約
    → 自動驗證
```

## 7. 倫理與可靠性考量

### AI 審計的限制
- **幻覺問題**：LLM 可能報告不存在的漏洞（誤報）
- **語境理解深度**：複雜的系統互動可能超出 LLM 的理解範圍
- **對抗性程式碼**：惡意開發者可能使用 LLM 難以分析的編碼模式

### 最佳實踐
1. LLM 審計作為第一關篩選，而非最終判斷
2. 所有 LLM 報告的漏洞必須由人類驗證
3. 使用多個 LLM 進行交叉驗證（Claude + GPT + Gemini）
4. 結合傳統靜態分析工具提高覆蓋率

## 8. 結語

LLM 正在從根本上改變核心安全審計的工作方式。它不會完全取代安全研究人員，但會顯著提升效率——讓研究人員可以專注於最複雜的邏輯漏洞，而不是浪費時間在常見的記憶體安全問題上。對於核心管理者而言，LLM 審計已經成為 CI/CD 流程中不可或缺的一環。

---

## 延伸閱讀

- [KernelGPT: LLM 核心漏洞挖掘](https://www.google.com/search?q=KernelGPT+LLM+kernel+vulnerability)
- [syzkaller + AI 增強](https://www.google.com/search?q=syzkaller+AI+kernel+fuzzing)
- [Linux 核心安全漏洞統計](https://www.google.com/search?q=Linux+kernel+security+vulnerability+statistics)
