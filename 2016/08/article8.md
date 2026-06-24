# Rocket Chip 生成器

## Rocket Chip 簡介

Rocket Chip 是 UC Berkeley 開發的參數化 RISC-V 處理器產生器，使用 Chisel 語言撰寫。

## 特色

- **參數化**：可配置快取大小、管線深度、分支預測器等
- **可擴展**：支援自訂指令擴展
- **開源**：BSD 授權
- **學術認可**：被許多研究機構使用

## 系統架構

```
Rocket Chip SoC
├── Rocket Cores (可配置數量)
│   ├── L1 I-Cache
│   ├── L1 D-Cache
│   ├── Branch Predictor
│   └── Pipeline Control
├── L2 Cache (可選)
├── DRAM Controller
├── Peripheral Controllers
│   ├── UART
│   ├── GPIO
│   ├── SPI
│   └── PWM
└── Tilelink Interconnect
```

## 設定與建置

### 環境需求

```bash
# 安裝依賴
sudo apt-get install build-essential autoconf g++ flex bison
sudo apt-get install default-jdk sbt nodejs npm

# 安裝 riscv-tools
git clone https://github.com/riscv/riscv-tools.git
cd riscv-tools
./build.sh
```

### 建立 Rocket Chip 專案

```bash
git clone https://github.com/freechipsproject/rocket-chip.git
cd rocket-chip
git submodule update --init --recursive

# 設定 RISCV 環境變數
export RISCV=/path/to/riscv
export PATH=$PATH:$RISCV/bin
```

### 設定參數

在 `src/main/scala/` 中設定：

```scala
class DefaultConfig extends Config(
    new WithNMedCores(1) ++          // 1 個中型核心
    new WithInclusiveCache ++        // 使用包容性快取
    new BaseConfig                    // 基本配置
)

class RocketConfig extends Config(
    new WithNBigCores(1) ++           // 1 個大核心
    new BaseConfig
)
```

### 編譯

```bash
make CONFIG=DefaultConfig
```

## 自訂配置

### 調整核心數量

```scala
class DualCoreConfig extends Config(
    new WithNMedCores(2) ++    // 2 個核心
    new BaseConfig
)
```

### 調整快取大小

```scala
class L2CacheConfig extends Config(
    new WithNMedCores(1) ++
    new WithL2Cache(
        nBanks = 1,
        capacityKB = 512,
        blockBytes = 64
    ) ++
    new BaseConfig
)
```

### 新增自訂指令

```scala
// 在 RISC-V CSR 中新增自訂欄位
class CustomCSR extends CSR {
    val custom_field = UInt(8.W)
}
```

## Rocket 核心微架構

### 5 級管線

```
IF → ID → EX → MEM → WB
```

- **IF**：指令獲取
- **ID**：指令解碼
- **EX**：執行/位址計算
- **MEM**：記憶體訪問
- **WB**：回寫結果

### 分支預測

支援多種類型：
- BTB（分支目標緩冲區）
- BHT（分支歷史表）
- RAS（返回位址堆疊）

## 軟體開發

### 編譯軟體

```bash
# 使用 riscv-gcc 編譯
riscv64-unknown-elf-gcc \
    -march=rv64ima \
    -mabi=lp64 \
    -o program.elf program.c

# 連結到 Rocket Chip
spike pk program.elf
```

### 開機載入程式

```assembly
.section .text
.global _start

_start:
    csrw mstatus, zero
    csrw mie, zero
    la sp, _stack_end
    call main
```

## 模擬

### 使用 Verilator

```bash
make CONFIG=DefaultConfig verilator
```

### 使用 VCS

```bash
make CONFIG=DefaultConfig vcs
```

## 參考資料

- [Rocket Chip GitHub](https://www.google.com/search?q=Rocket+Chip+github)
- [Chisel 語言](https://www.google.com/search?q=Chisel+language+tutorial)
- [RISC-V 軟核](https://www.google.com/search?q=RISC-V+softcore+tutorial)