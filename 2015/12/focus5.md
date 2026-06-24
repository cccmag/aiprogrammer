# 程式語言趨勢

## 前言

2015 年是程式語言領域重要的一年。Rust 1.0 正式發布，Swift 宣布開源，Go 在雲端運算領域站穩腳跟，JavaScript 生態持續繁榮。讓我們回顧這一年的程式語言發展。

## 程式語言排行榜

### TIOBE 指數（2015 年 12 月）

| 排名 | 語言 | 佔比 | 變化 |
|------|------|------|------|
| 1 | Java | 17.9% | -1.2% |
| 2 | C | 10.5% | -1.3% |
| 3 | C++ | 6.7% | +0.5% |
| 4 | Python | 5.1% | +0.7% |
| 5 | C# | 4.9% | -0.3% |
| 6 | JavaScript | 3.3% | +0.2% |
| 7 | PHP | 2.7% | -0.1% |
| 8 | Ruby | 2.3% | -0.2% |
| 9 | Perl | 2.1% | -0.2% |
| 10 | Swift | 1.4% | NEW |

### GitHub 語言統計

| 排名 | 語言 | 比例 |
|------|------|------|
| 1 | JavaScript | 28% |
| 2 | Python | 14% |
| 3 | Java | 11% |
| 4 | Ruby | 10% |
| 5 | PHP | 9% |
| 6 | C++ | 5% |
| 7 | C | 5% |
| 8 | Go | 2% |
| 9 | Swift | 1.5% |
| 10 | Rust | 0.5% |

## Rust 1.0 發布

### 里程碑

Rust 1.0 在 2015 年 5 月正式發布：

- **記憶體安全**：編譯時保證
- **零成本抽象**：高效能
- **實用性**：系統程式設計
- **社群**：活躍的貢獻者

### 核心概念

```rust
// 所有權系統
fn main() {
    let s1 = String::from("hello");
    let s2 = s1;  // s1 被移動到 s2
    // println!("{}", s1);  // 編譯錯誤！
    println!("{}", s2);
}

// 借用
fn calculate_length(s: &String) -> usize {
    s.len()
}  // s 在這裡離開作用域，但並不 drop

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1);
    println!("{}", len);
}

// 生命週期
struct ImportantExcerpt<'a> {
    part: &'a str,
}
```

### 應用場景

- **網路服務**：Servo 瀏覽器引擎
- **命令列工具**：ripgrep
- **區塊鏈**：Parity 以太坊客戶端
- **嵌入式**：Rust 嵌入式工作組

## Swift 開源

### 宣布與影響

Apple 在 12 月宣布 Swift 開源：

- **平台支援**：macOS、Linux
- **授權**：Apache 2.0
- **願景**：成為最安全的語言

### 語言特點

```swift
// 安全性
let array = ["hello", "world"]
// array.append(123)  // 編譯錯誤

// 現代語法
protocol Drawable {
    func draw()
}

struct Circle: Drawable {
    var x: Double
    var y: Double
    var radius: Double

    func draw() {
        print("Drawing circle at (\(x), \(y))")
    }
}

// 函數式
let numbers = [1, 2, 3, 4, 5]
let doubled = numbers.map { $0 * 2 }
let evens = numbers.filter { $0 % 2 == 0 }
let sum = numbers.reduce(0) { $0 + $1 }
```

### 伺服器端 Swift

Swift 開源後，伺服器框架開始出現：
- **Vapor**：類似 Laravel
- **Perfect**：全功能框架
- **Kitura**：IBM 主導

## Go 在雲端的應用

### 生態發展

Go 在 2015 年繼續鞏固雲端運算的地位：

- **Kubernetes**：容器編排標準
- **Docker**：容器引擎核心
- **Terraform**：基礎設施即程式碼
- **Prometheus**：監控系統

### 語言特點

```go
// 併發
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Println("worker", id, "processing job", j)
        results <- j * 2
    }
}

func main() {
    jobs := make(chan int, 100)
    results := make(chan int, 100)

    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    for j := 1; j <= 5; j++ {
        jobs <- j
    }
    close(jobs)
}
```

## JavaScript 生態

### ES6 標準化

ES6（ECMAScript 2015）在 2015 年正式發布：
- Classes、Modules、Arrow Functions
- Promises、Generators、Symbols
- Template Literals、Destructuring

### 執行環境

| 環境 | 引擎 | 特點 |
|------|------|------|
| Node.js 4.0 | V8 4.0 | LTS 版本 |
| Chrome 47 | V8 4.7 | ES6 支援良好 |
| Firefox 43 | SpiderMonkey | ES6 支援良好 |
| Edge 13 | Chakra | 持續改進 |

### 編譯目標

```javascript
// Babel 轉譯
// ES6 → ES5
const foo = (x) => x.map(y => y * 2);

// 轉換後
"use strict";
var foo = function foo(x) {
  return x.map(function (y) {
    return y * 2;
  });
};
```

## Python 的崛起

### 2015 年發展

Python 在 2015 年持續增長：

- **資料科學**：pandas、scikit-learn 成熟
- **網頁開發**：Django 1.9、Flask 0.10
- **雲端**：AWS Lambda 支援
- **AI/ML**：TensorFlow Python API

### 特點

```python
# 現代 Python
from dataclasses import dataclass
from typing import List

@dataclass
class User:
    name: str
    email: str
    roles: List[str] = []

    def has_role(self, role: str) -> bool:
        return role in self.roles

# 列表推導
squares = [x**2 for x in range(10)]

# 生成器
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# 非同步（Python 3.5+）
async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://example.com') as response:
            return await response.json()
```

## 其他語言

### Java

- **Java 8** 全面普及
- **Lambda 表達式**
- **Stream API**
- **Java 9** 開發中

### C++

- **C++14** 標準發布
- **C++17** 制定中
- **編譯器支援改善**

### Ruby

- **Rails 5** 開發中
- **Ruby 2.3** 發布
- **效能持續改進**

## 未來展望

### 2016 年預期

1. **Rust 持續成長**：社群和生態擴大
2. **Swift 3.0**：API 改進和標準化
3. **Go 2.0 討論**：泛型等特性
4. **WebAssembly**：新的程式目標
5. **更多靜態類型 JavaScript**：TypeScript 成長

## 小結

2015 年程式語言領域精彩紛呈：

- **Rust 1.0**：系統程式語言成熟
- **Swift 開源**：開啟新篇章
- **Go 站穩腳跟**：雲端基礎設施
- **JavaScript 現代化**：ES6 新時代
- **Python 普及**：資料科學和 AI

選擇語言要根據場景，沒有最好的語言，只有最適合的語言。

---

## 延伸閱讀

- [Rust Official Site](https://www.google.com/search?q=Rust+programming+language)
- [Swift Open Source](https://www.google.com/search?q=Swift+open+source)
- [Go Language](https://www.google.com/search?q=Go+language+official)
- [TIOBE Index](https://www.google.com/search?q=TIOBE+programming+community+index)