# C++26 標準發布：反射與模式匹配

## 前言

2026 年 4 月，C++ 標準委員會正式發布了 C++26——這是 C++ 歷史上最具突破性的版本之一。新標準引入了反射（Reflection）、模式匹配（Pattern Matching）和合約（Contracts）三大核心特性，以及數十項重要改進。本文深入解析 C++26 的關鍵新特性。

## 反射：編譯期的程式碼內省

### 為什麼需要反射？

反射讓程式可以在編譯期檢查和操作自身的結構——包括型別資訊、成員變數、基底類別等。這是 C++ 社群期待了十多年的功能。

### 基本語法

C++26 使用 `^` 運算子來獲取型別或表達式的反射資訊：

```cpp
#include <experimental/meta>
#include <iostream>
#include <type_traits>

struct Person {
    std::string name;
    int age;
    double salary;
};

template<typename T>
void print_members() {
    // 獲取型別的反射資訊
    constexpr auto members = ^T.members();
    
    // 在編譯期遍歷成員
    template for (constexpr auto member : members) {
        std::cout << member.name << ": " 
                  << member.type.name() << "\n";
    }
}

int main() {
    print_members<Person>();
    // 輸出：
    // name: std::string
    // age: int
    // salary: double
}
```

### 反射的應用場景

**1. 自動序列化：**

```cpp
// 一行程式碼生成 JSON 序列化
template<typename T>
std::string to_json(const T& obj) {
    std::string json = "{";
    bool first = true;
    
    template for (constexpr auto member : ^T.members()) {
        if (!first) json += ", ";
        first = false;
        
        json += "\"" + member.name + "\": ";
        json += to_string(obj.*(member.pointer));
    }
    
    return json + "}";
}

struct Config {
    std::string host = "localhost";
    int port = 8080;
    bool debug = false;
};

auto cfg = Config{};
std::cout << to_json(cfg);
// {"host": "localhost", "port": 8080, "debug": false}
```

**2. 自動比較運算子：**

```cpp
// 自動生成 == 運算子
template<typename T>
auto operator==(const T& a, const T& b) -> bool {
    template for (constexpr auto member : ^T.members()) {
        if (a.*(member.pointer) != b.*(member.pointer))
            return false;
    }
    return true;
}
```

## 模式匹配：強大的結構化解構

### 語法設計

C++26 的模式匹配語法參考了 Rust 和 Haskell 的設計，使用 `inspect` 關鍵字：

```cpp
// 基本模式匹配
std::variant<int, double, std::string> value = 42;

inspect(value) {
    as int i        => std::cout << "整數: " << i;
    as double d     => std::cout << "浮點數: " << d;
    as std::string s => std::cout << "字串: " << s;
};
```

### 結構化模式

```cpp
// 解構元組和結構體
std::tuple<int, std::string, double> record = {1, "Alice", 95.5};

inspect(record) {
    as (int id, std::string name, double score) => {
        std::cout << name << " (" << id << "): " << score;
    }
};
```

### 數值範圍模式

```cpp
int score = 85;

inspect(score) {
    as 100            => std::cout << "滿分！";
    as >= 90          => std::cout << "優秀";
    as >= 80          => std::cout << "良好";
    as >= 60          => std::cout << "及格";
    as < 60           => std::cout << "不及格";
};
```

### 哨兵模式（Guard）

```cpp
std::optional<int> maybe_value = 42;

inspect(maybe_value) {
    as std::optional<int> v if v > 0 => 
        std::cout << "正數: " << *v;
    as std::optional<int> v if v < 0 =>
        std::cout << "負數: " << *v;
    as none =>
        std::cout << "空值";
};
```

## 合約（Contracts）

### 語法設計

C++26 引入了 `[[expects]]`、`[[ensures]]` 和 `[[assert]]` 屬性來表達合約：

```cpp
// 前置條件與後置條件
int divide(int dividend, int divisor)
    [[expects: divisor != 0]]           // 前置條件
    [[ensures: result >= 0]]            // 後置條件
{
    return dividend / divisor;
}

// 不變式
void push_back(std::vector<int>& vec, int value)
    [[ensures: vec.size() == old(vec.size()) + 1]]
{
    vec.push_back(value);
}
```

### 編譯期與執行期

合約可以在不同模式下使用：

```cpp
// 編譯期：constexpr 函式中的合約
constexpr int factorial(int n)
    [[expects: n >= 0]]
    [[ensures: result > 0 || n == 0]]
{
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// 執行時：除錯模式下的檢查
// 在 debug 模式下，合約違反會觸發 handler
// 在 release 模式下，合約被完全消除（零開銷）
```

## 其他重要改進

### 更好的 constexpr

C++26 進一步擴展了 constexpr 的能力：

```cpp
// constexpr 中可以使用動態記憶體分配
constexpr std::vector<int> create_data() {
    std::vector<int> v;
    v.push_back(1);
    v.push_back(2);
    v.push_back(3);
    return v;  // C++26 中合法
}

constexpr auto data = create_data();
static_assert(data.size() == 3);
```

### 模式匹配的異常處理

```cpp
// 用模式匹配取代 try-catch
auto result = may_throw();

inspect(result) {
    as int value  => std::cout << "成功: " << value;
    as error e if e == Error::NotFound => 
        std::cout << "找不到資源";
    as error e    =>
        std::cout << "錯誤: " << e.what();
};
```

### 協程改進

```cpp
// 簡化的協程語法
task<int> fetch_data() {
    auto response = co_await http_get("https://api.example.com");
    auto data = co_await response.json();
    co_return data["value"].as<int>();
}
```

## 相容性與遷移

### 與 C++20/23 的相容性

C++26 保持了良好的向後相容性：

- 所有 C++23 程式碼無需修改即可使用 C++26 編譯
- 新模式匹配與現有 `switch` 語句不衝突
- 反射是一個新的標準函式庫，不影響現有程式碼

### 編譯器支援

| 編譯器 | 反射支援 | 模式匹配支援 | 合約支援 |
|--------|---------|-------------|---------|
| GCC 15 | 實驗性 | 實驗性 | 部分支援 |
| Clang 20 | 完整支援 | 完整支援 | 完整支援 |
| MSVC 2026 | 完整支援 | 實驗性 | 完整支援 |
| EDG | 完整支援 | 完整支援 | 完整支援 |

## 結語

C++26 是 C++ 語言現代化過程中的一個重要里程碑。反射、模式匹配和合約三大特性，加上持續改進的 constexpr 和協程，使得 C++ 在保持高效能的同時，大幅提升了表達力和安全性。對於新專案，強烈建議開始使用 C++26 模式；對於既有專案，可以逐步將反射和模式匹配引入新開發的模組中。

---

**延伸閱讀**

- [C++26 標準草案](https://www.google.com/search?q=C%2B%2B26+standard+draft)
- [反射提案 P2996](https://www.google.com/search?q=P2996+C%2B%2B+reflection)
- [模式匹配提案 P2688](https://www.google.com/search?q=P2688+C%2B%2B+pattern+matching)
