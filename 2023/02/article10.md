# I/O 與設備驅動

## I/O 系統的層次結構

```
應用程式
  │ read() / write() 系統呼叫
VFS (Virtual File System)
  │ 檔案系統驅動
區塊層 (Block Layer)
  │ I/O 排程器
設備驅動程式 (Device Driver)
  │ 中斷處理 / DMA
硬體設備
```

## I/O 控制方式

### 程式控制 I/O（Polling）

CPU 忙等待設備狀態暫存器，直到設備就緒。

```
優點：簡單，不需要中斷處理
缺點：浪費 CPU 週期
```

### 中斷驅動 I/O

CPU 發起 I/O 操作後繼續執行其他工作。設備完成操作後發送中斷信號通知 CPU。

```
優點：CPU 不用忙等待，效率高
缺點：每次 I/O 都需要中斷處理，小資料傳輸時中斷開銷佔比大
```

### DMA（直接記憶體存取）

DMA 控制器直接將資料從設備傳輸到記憶體，無需 CPU 介入。

```
流程：
1. CPU 設定 DMA 控制器（來源、目的地、長度）
2. DMA 控制器執行資料傳輸
3. 傳輸完成後 DMA 控制器發送中斷給 CPU

優點：CPU 完全解放，適合大量資料傳輸
缺點：需要 DMA 控制器硬體支援；記憶體匯流排競爭
```

## 設備驅動程式

設備驅動程式是核心中直接與硬體設備通訊的軟體層。每個設備類型需要對應的驅動程式。

### 驅動程式的功能

1. **設備初始化**：偵測硬體、設定暫存器、分配資源
2. **I/O 請求處理**：接收上層的讀寫請求，轉換為設備命令
3. **中斷處理**：回應設備中斷，完成 I/O 操作
4. **錯誤處理**：處理設備錯誤和異常
5. **電源管理**：設備休眠和喚醒

### Linux 設備類型

| 設備類型 | 存取方式 | 範例 | 設備檔 |
|---------|---------|------|--------|
| 字元設備 | 位元組串流 | 鍵盤、序列埠 | /dev/ttyS0 |
| 區塊設備 | 區塊 I/O | 硬碟、SSD | /dev/sda |
| 網路設備 | 封包 | 網路卡 | eth0 |

## Linux 字元設備範例

```c
// 簡化的字元設備驅動程式框架
#include <linux/module.h>
#include <linux/fs.h>

static int my_open(struct inode *inode, struct file *file) {
    printk("Device opened\n");
    return 0;
}

static ssize_t my_read(struct file *file, char __user *buf,
                        size_t count, loff_t *ppos) {
    // 複製資料到使用者空間
    if (copy_to_user(buf, kernel_buffer, count))
        return -EFAULT;
    return count;
}

static struct file_operations fops = {
    .owner = THIS_MODULE,
    .open = my_open,
    .read = my_read,
};

int init_module(void) {
    register_chrdev(240, "mydev", &fops);
    return 0;
}
```

## I/O 排程器

區塊層的 I/O 排程器負責優化磁碟 I/O 請求的順序：

### 電梯排程（Elevator / SCAN）

磁頭在磁碟上來回移動，沿途處理請求。類似電梯的運作方式。

```
優點：減少尋道時間，輸送量高
缺點：邊緣請求可能等待較久
```

### 截止時間排程（Deadline）

每個請求設有截止時間。正常使用電梯排程，但遇接近截止時間的請求則優先處理。

```
優點：避免請求飢餓，提供延遲保證
```

### CFQ（完全公平佇列）

每個行程擁有獨立的 I/O 佇列，以時間片方式輪轉分配 I/O 頻寬。

```
優點：公平分配 I/O 頻寬
缺點：高負載下輸送量較低
```

### NVMe 與現代 I/O

NVMe（Non-Volatile Memory Express）是專為 SSD 設計的 I/O 協定：

- 多達 64K 個 I/O 佇列（傳統 SCSI 只有 1 個）
- 每個佇列深度 64K
- 不需要傳統的 I/O 排程器——NVMe SSD 的隨機存取時間極短
- 使用 `blk-mq`（多佇列區塊層）直接將請求分配到不同佇列

## 中斷處理流程

```
1. 設備完成 I/O 操作
2. 設備發送中斷信號到中斷控制器
3. 中斷控制器通知 CPU
4. CPU 保存當前執行上下文
5. CPU 執行中斷處理程式（上半部，top half）
   - 保存設備狀態
   - 排程下半部（bottom half）處理
6. 恢復上下文，繼續原本的執行
7. 下半部執行（softirq / tasklet / workqueue）
   - 完成 I/O 操作
   - 喚醒等待的行程
```

上半部（Top Half）在中斷上下文中執行——不可阻塞，必須快速完成。

下半部（Bottom Half）在軟中斷或行程上下文中執行——可以阻塞，可以睡眠。

## 延伸閱讀

- [Linux 設備驅動程式](https://www.google.com/search?q=Linux+device+driver+architecture+char+block)
- [NVMe 協定介紹](https://www.google.com/search?q=NVMe+protocol+IO+queues)
- [DMA 傳輸機制](https://www.google.com/search?q=DMA+direct+memory+access+modes)
- [Linux I/O 排程器](https://www.google.com/search?q=Linux+IO+scheduler+CFQ+deadline+noop)
