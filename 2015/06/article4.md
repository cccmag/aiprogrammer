# Makefile 與建構系統

## Make 基礎

Make 是一個自動化建構工具，透過 Makefile 來描述建構規則。

## 基本 Makefile

```makefile
# Makefile
CC = gcc
CFLAGS = -Wall -Wextra -g
TARGET = program
OBJS = main.o utils.o

$(TARGET): $(OBJS)
    $(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

main.o: main.c utils.h
    $(CC) $(CFLAGS) -c main.c

utils.o: utils.c utils.h
    $(CC) $(CFLAGS) -c utils.c

clean:
    rm -f $(OBJS) $(TARGET)

.PHONY: clean
```

## 模式規則

```makefile
# 使用模式規則
%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@
```

## 自動變數

| 變數 | 意義 |
|------|------|
| `$@` | 目標檔案 |
| `$<` | 第一個前提 |
| `$^` | 所有前提 |
| `$?` | 所有新於目標的前提 |

```makefile
program: main.o utils.o
    $(CC) -o $@ $^
```

## 副規則

```makefile
# 推導副檔名規則
.SUFFIXES: .c .h

.c.o:
    $(CC) $(CFLAGS) -c $<
```

## 函式

```makefile
# 取代副檔名
SRCS = foo.c bar.c
OBJS = $(SRCS:.c=.o)

# 搜尋路徑
VPATH = src:include

# wildcard
SRC = $(wildcard *.c)
```

## 條件式

```makefile
# 條件式
DEBUG = -g
RELEASE = -O2

ifeq ($(MODE),debug)
    CFLAGS = $(DEBUG)
else
    CFLAGS = $(RELEASE)
endif
```

## Make 技巧

### 包含守衛

```makefile
# 防止重複包含
CONFIG_MK := 1
```

### 巢狀 Makefile

```makefile
# 在子目錄執行 make
subdir:
    $(MAKE) -C subdir
```

## CMake 簡介

CMake 是一個更高級的建構系統，产生平台相關的 Makefile。

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.0)
project(MyProject)

set(CMAKE_C_STANDARD 99)

add_executable(program main.c utils.c)
```

```bash
mkdir build
cd build
cmake ..
make
```

## Autotools 簡介

GNU Autotools 是 GNU 軟體標準的建構系統。

### 產生的檔案

- configure.ac 或 configure.in
- Makefile.am
- configure（shell 腳本）
- Makefile.in（模板）

### 基本流程

```bash
autoreconf -i
./configure
make
make install
```

## 結論

學會使用 Make 可以大幅提升開發效率。建議從簡單的 Makefile 開始，逐步學習更高級的功能。