# Nios II 嵌入式處理器

## Nios II 簡介

Nios II 是 Intel（原 Altera）FPGA 中的軟核處理器，使用 RISC 架構。

## 處理器類型

### Nios II/f（快速）

- 5 級流水線
- 哈佛記憶體架構
- 可配置指令和資料快取
- 最高效能

### Nios II/s（標準）

- 6 級流水線
- 靜態分支預測
- 可配置快取
- 中等效能

### Nios II/e（經濟）

- 無流水線
- 所有指令單周期執行
- 無快取
- 最小資源使用

## 系統結構

```
┌────────────────────────────────────┐
│         Nios II Processor          │
├────────────────────────────────────┤
│  Regs │ ALU │ shifter │ Exception  │
└────────────────────────────────────┘
         │              │
    ┌────┴────┐   ┌────┴────┐
    │Instruction│   │  Data   │
    │  Cache   │   │  Cache  │
    └─────────┘   └─────────┘
         │              │
    ┌────┴──────────────┴────┐
    │   On-Chip Memory/Flash │
    └────────────────────────┘
```

## Qsys 系統整合

### 新增 Nios II

```
Qsys → Component Library → Nios II Processor
```

### 設定選項

- 選擇處理器類型（f/s/e）
- 設定例外處理
- 設定緊密耦合記憶體
- 設定 JTAG 調試模組

### 周邊連接

```tcl
# Qsys 產生的 TCL
connect_component_interfaces
connect_signal avalon_master_0 sram_slave
connect_signal uart_0 irq_controller
```

## 軟體開發

### BSP 設定

```c
// system.h 中的指標
#define ALT_DEVICE_FAMILY "Cyclone V"
#define ALT_CPU_FREQ 50000000L
#define ALT_OS_LINUX 0
#define ALT_HAS_DMA 1
```

### 記憶體配置

```ld
MEMORY
{
    FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 16M
    SRAM   (rw) : ORIGIN = 0x00010000, LENGTH = 64K
    SDRAM  (rw) : ORIGIN = 0x01000000, LENGTH = 128M
}
```

## 範例程式

### 基本 GPIO 控制

```c
#include "system.h"
#include "altera_avalon_pio_regs.h"

int main() {
    volatile int *led = LED_BASE;
    int count = 0;

    while (1) {
        *led = count & 0xFF;
        for (volatile int i = 0; i < 100000; i++);
        count++;
    }

    return 0;
}
```

### 中斷處理

```c
#include "sys/alt_irq.h"
#include "altera_avalon_pio_regs.h"

void button_isr(void* context) {
    volatile int* led = (volatile int*)context;
    *led = ~*led;
    IORD_ALTERA_AVALON_PIO_EDGE_CAP(BUTTON_BASE) = 0xFF;
}

int init_button_interrupt() {
    IOWR_ALTERA_AVALON_PIO_IRQ_MASK(BUTTON_BASE, 0xFF);
    IOWR_ALTERA_AVALON_PIO_EDGE_CAP(BUTTON_BASE, 0xFF);

    alt_ic_isr_register(BUTTON_IRQ_INTERRUPT_CONTROLLER_ID,
                        BUTTON_IRQ,
                        button_isr,
                        (void*)LED_BASE,
                        0x0);

    return 0;
}
```

## 效能優化

### 緊密耦合記憶體

```tcl
# 在 Qsys 中新增 ITCM 和 DTCM
add_memory_segment itcm MEMORY
set_memory_assignments itcm -is_flash 0 -is_ram 1 -origin 0x01000000 -length 16K
connect_signal cpu_0 instruction_master itcm_0
connect_signal cpu_0 data_master dtcm_0
```

### 快取配置

```tcl
# 設定指令快取大小
set_instance_parameter_value cpu_0 instruction_cache_size 16K

# 設定資料快取大小
set_instance_parameter_value cpu_0 data_cache_size 16K
```

### 使用 DSP 指令

```c
// 使用 Nios II DSP 指令
register int a asm("r8");
register int b asm("r9");
int result;

// Nios II 有乘法累加指令
asm volatile ("mulxss %0, %1, %2" : "=r"(result) : "r"(a), "r"(b));
```

## 參考資料

- [Nios II 官方文檔](https://www.google.com/search?q=Nios+II+processor+documentation)
- [Nios II EDS 使用指南](https://www.google.com/search?q=Nios+II+Embedded+Design+Suite+tutorial)