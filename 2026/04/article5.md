# Zig 語言的崛起：系統程式設計的現代化之路

## 前言

2026 年春季，Zig 語言迎來了爆發式增長。根據 GitHub 的統計，Zig 在 2026 年第一季度的新專案數量增長了 320%，成為增長最快的系統程式語言之一。Zig 的 0.15 版本引入了原生的套件管理器、更完善的交叉編譯支援，以及與 C 語言的無痛互操作。本文探討 Zig 為何能在競爭激烈的系統程式設計領域脫穎而出。

## Zig 的設計哲學

Zig 由 Andrew Kelley 於 2016 年創立，定位是「作為 C 語言的更好替代」。它的設計哲學可以總結為幾個核心原則：

1. **沒有隱藏的控制流**：沒有隱式的記憶體分配、執行緒或後台執行
2. **沒有隱藏的記憶體分配**：所有記憶體分配都是顯式的
3. **C 語言優先的互操作性**：可以直接包含 C 頭文件
4. **編譯期執行**：強大的 comptime 機制
5. **錯誤作為返回值**：沒有異常，錯誤是返回值

## 0.15 版的核心新特性

### 原生套件管理器

Zig 0.15 引入了原生的套件管理器（Package Manager），解決了 Zig 生態系統最關鍵的缺失：

```zig
// build.zig.zon（Zig Object Notation）
// 類似 Cargo.toml 或 package.json
.{
    .name = "my_project",
    .version = "0.1.0",
    .dependencies = .{
        .zap = .{
            .url = "https://github.com/zigzap/zap/archive/v0.15.0.tar.gz",
            .hash = "1220a3e7a2b5c8f9d1e4f6a7b8c9d0e1f2a3b4c5",
        },
        .zig_http_client = .{
            .url = "https://github.com/ziglibs/zig-http-client/archive/v2.1.0.tar.gz",
            .hash = "098f6bcd4621d373cade4e832627b4f6",
        },
    },
}
```

```zig
// build.zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const exe = b.addExecutable(.{
        .name = "my_app",
        .root_source_file = .{ .path = "src/main.zig" },
        .target = b.standardTargetOptions(.{}),
        .optimize = b.standardOptimizeOption(.{}),
    });
    
    // 從依賴中引入模組
    const zap = b.dependency("zap", .{});
    exe.addModule("zap", zap.module("zap"));
    
    b.installArtifact(exe);
}
```

### 交叉編譯的無縫體驗

Zig 的交叉編譯能力是其最大的賣點之一：

```zig
// 一條指令完成交叉編譯
// zig build-exe -target aarch64-linux-gnu src/main.zig
// zig build-exe -target x86_64-windows-gnu src/main.zig
// zig build-exe -target arm-linux-musleabihf src/main.zig

// 內建支援超過 100 種目標平台
// 無需額外安裝工具鏈！

const targets = [_]std.Target.Query{
    .{ .cpu_arch = .x86_64, .os_tag = .linux, .abi = .gnu },
    .{ .cpu_arch = .aarch64, .os_tag = .macos },
    .{ .cpu_arch = .x86_64, .os_tag = .windows, .abi = .gnu },
    .{ .cpu_arch = .arm, .os_tag = .linux, .abi = .musleabi },
    .{ .cpu_arch = .wasm32, .os_tag = .freestanding },
};
```

### 與 C 語言的無痛互操作

Zig 最大的殺手級功能是它與 C 語言的互操作性：

```zig
// 直接包含 C 頭文件！
const c = @cImport({
    @cInclude("sqlite3.h");
    @cInclude("curl/curl.h");
    @cInclude("sdl2/SDL.h");
});

// 使用 C 函式就像調用 Zig 函式一樣
pub fn queryDatabase(path: [:0]const u8) !void {
    var db: ?*c.sqlite3 = undefined;
    
    // 調用 C API
    const rc = c.sqlite3_open(path.ptr, &db);
    if (rc != c.SQLITE_OK) {
        return error.DatabaseOpenFailed;
    }
    defer _ = c.sqlite3_close(db);
    
    // 執行查詢
    var stmt: ?*c.sqlite3_stmt = undefined;
    _ = c.sqlite3_prepare_v2(db, "SELECT 1", -1, &stmt, null);
    defer _ = c.sqlite3_finalize(stmt);
    
    while (c.sqlite3_step(stmt) == c.SQLITE_ROW) {
        const val = c.sqlite3_column_int(stmt, 0);
        std.debug.print("Value: {}\n", .{val});
    }
}
```

## Zig 的獨特語言特性

### comptime：編譯期執行

Zig 的 comptime 機制允許在編譯期執行任意程式碼：

```zig
const std = @import("std");

// 編譯期計算
fn fibonacci(comptime n: usize) usize {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// 在編譯期計算出的值
const FIB_10 = comptime fibonacci(10);
// FIB_10 = 55（編譯期已計算完成）

// 編譯期的型別生成
fn Vector(comptime T: type, comptime len: usize) type {
    return struct {
        data: [len]T,
        
        fn init(value: T) @This() {
            return .{ .data = [_]T{value} ** len };
        }
        
        fn dot(self: @This(), other: @This()) T {
            var sum: T = 0;
            for (self.data, other.data) |a, b| {
                sum += a * b;
            }
            return sum;
        }
    };
}

const Vec3f = Vector(f32, 3);
const Vec4i = Vector(i32, 4);

// 泛型容器
fn ArrayList(comptime T: type) type {
    return struct {
        items: []T,
        len: usize,
        capacity: usize,
        allocator: std.mem.Allocator,
        
        fn init(allocator: std.mem.Allocator) @This() {
            return .{
                .items = &[_]T{},
                .len = 0,
                .capacity = 0,
                .allocator = allocator,
            };
        }
        // ...
    };
}
```

### 錯誤處理

Zig 使用錯誤聯合類型（Error Union Type），沒有異常：

```zig
const std = @import("std");

// 定義錯誤類型
const FileError = error{
    NotFound,
    PermissionDenied,
    IoError,
};

// 返回錯誤聯合類型
fn readConfig(path: []const u8) FileError![]const u8 {
    const file = std.fs.cwd().openFile(path, .{}) catch |err| {
        return switch (err) {
            error.FileNotFound => FileError.NotFound,
            error.AccessDenied => FileError.PermissionDenied,
            else => FileError.IoError,
        };
    };
    defer file.close();
    
    const content = file.readToEndAlloc(
        std.heap.page_allocator,
        1024 * 1024,
    ) catch return FileError.IoError;
    
    return content;
}

// 使用 try 傳播錯誤
fn processConfig() !void {
    const content = try readConfig("config.json");
    defer std.heap.page_allocator.free(content);
    
    // 處理配置...
}

// 使用 catch 處理錯誤
const config = readConfig("config.json") catch |err| blk: {
    std.log.warn("Failed to read config: {s}", .{@errorName(err)});
    break :blk "{}";
};
```

### 記憶體管理

Zig 沒有內建的 GC，所有記憶體管理都是顯式的：

```zig
const std = @import("std");

pub fn main() !void {
    // 使用通用分配器
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    defer _ = gpa.deinit();
    
    const allocator = gpa.allocator();
    
    // 顯式分配
    var list = std.ArrayList(u32).init(allocator);
    defer list.deinit();
    
    try list.append(1);
    try list.append(2);
    try list.append(3);
    
    // 分配字串
    const greeting = try allocator.dupe(u8, "Hello, Zig!");
    defer allocator.free(greeting);
    
    // Arena 分配器（批次釋放）
    var arena = std.heap.ArenaAllocator.init(allocator);
    defer arena.deinit();
    
    const arena_allocator = arena.allocator();
    _ = try arena_allocator.dupe(u8, "Temporary data");
    // 離開作用域時一次釋放所有記憶體
}
```

## 實際應用案例

### Web 伺服器

```zig
const std = @import("std");
const zap = @import("zap");

fn handleHello(endpoint: *zap.Endpoint, request: zap.Request) void {
    _ = endpoint;
    request.sendJson("{\"message\": \"Hello from Zig!\"}") catch return;
}

fn handleApi(endpoint: *zap.Endpoint, request: zap.Request) void {
    _ = endpoint;
    const params = request.queryParams();
    
    const name = params.get("name") orelse "World";
    
    request.sendJson(
        try std.fmt.allocPrint(
            std.heap.page_allocator,
            "{{\"greeting\": \"Hello, {s}!\"}}",
            .{name},
        )
    ) catch return;
}

pub fn main() !void {
    var listener = zap.Endpoint.Listener.init(.{
        .port = 3000,
        .on_request = null,
        .log = true,
        .max_clients = 100000,
    });
    
    try listener.listen();
    
    var hello_endpoint = zap.Endpoint.init(.{
        .path = "/hello",
        .get = handleHello,
    });
    
    var api_endpoint = zap.Endpoint.init(.{
        .path = "/api",
        .get = handleApi,
    });
    
    // 效能：在 MacBook M4 上達到每秒 250,000+ req/s
    std.debug.print("Server running on http://localhost:3000\n", .{});
    
    // 永不停止...
    try std.process.wait();
}
```

### 嵌入式開發

```zig
// 嵌入式 STM32 程式
const microzig = @import("microzig");
const stm32 = microzig.chip.stm32.stm32f411;

pub fn main() void {
    // 配置 GPIO
    const led_pin = stm32.GPIO.Pin{
        .port = .C,
        .pin = 13,
    };
    led_pin.setDirection(.output);
    
    // 主循環
    while (true) {
        led_pin.toggle();
        microzig.busyWait(500_000); // 500ms
    }
}
```

## 生態系統

### 主要專案與函式庫

| 類別 | 專案 | 說明 |
|------|------|------|
| HTTP 伺服器 | Zap | 高效能 HTTP 伺服器 |
| 資料序列化 | zjson | JSON 處理 |
| 圖形 API | zgpu | WebGPU 封裝 |
| 遊戲開發 | Mach | 遊戲引擎/框架 |
| GUI | zigl | 跨平台 GUI |
| 機器學習 | zml | 機器學習框架 |
| 資料庫 | zig-query | SQL 查詢構建器 |

### Zig 在生產環境中的使用

越來越多的公司將 Zig 用於生產環境：

- **Uber**：使用 Zig 開發部分基礎設施元件
- **Cloudflare**：邊緣服務的效能關鍵部分
- **TigerBeetle**：用 Zig 開發的金融級分散式資料庫
- **SourceGraph**：搜尋引擎的底層元件

## 結語

Zig 的崛起並非偶然。在系統程式設計領域，C 語言的年齡超過了 50 歲，C++ 也超過了 40 歲——開發者對現代化系統語言的需求非常強烈。Zig 以「更好的 C」為定位，提供了無與倫比的 C 互操作性、強大的編譯期計算、安全的記憶體管理以及便捷的交叉編譯。對於嵌入式開發、系統程式設計和高效能 Web 服務等場景，Zig 正在成為一個越來越有吸引力的選擇。

---

**延伸閱讀**

- [Zig 語言官方文件](https://www.google.com/search?q=Zig+language+documentation)
- [Zig 學習資源](https://www.google.com/search?q=learn+Zig+programming)
- [Zig Showtime 社群](https://www.google.com/search?q=Zig+showtime+community)
