# AI + Rust

## 用 OpenCode、Copilot、Claude Code 輔助 Rust 開發（2024-2026）

### AI 如何改變 Rust 開發

Rust 以其陡峭的學習曲線聞名——所有權、借用、生命週期、Send/Sync……即使是經驗豐富的程式設計師也需要數月才能熟練。但 2024-2026 年間，AI 輔助開發工具徹底改變了這個局面：

- **初學者**：AI 可以解釋 Rust 概念、生成範例程式碼、幫助除錯
- **中級開發者**：AI 可以撰寫常見的 Rust 模式、處理 unsafe 程式碼
- **專家**：AI 可以進行程式碼審查、效能最佳化建議、大規模重構

### AI Rust 開發工具生態

| 工具 | 公司 | 主要功能 | Rust 支援程度 |
|------|------|---------|-------------|
| **OpenCode** | 開源社群 | 自主代理、多步驟任務 | 最佳（Rust 專用代理模式） |
| **Copilot** | GitHub/Microsoft | 程式碼補全、除錯 | 優秀（深度 crate 理解） |
| **Claude Code** | Anthropic | 自主開發、Git 整合 | 優秀（安全程式碼生成） |
| **Antigravity** | Antigravity | 意圖驅動開發 | 良好 |

### OpenCode：開源 AI 編碼代理

OpenCode 是一個基於 MCP（Model Context Protocol）的開源 AI 開發工具。其獨特的「代理模式」特別適合 Rust 開發：

```yaml
# .opencode/agents/rust-agent.md
---
name: rust-agent
description: Rust development specialist
instructions: |
  You are a Rust expert. When generating Rust code:
  1. Always consider ownership and borrowing
  2. Prefer safe Rust over unsafe Rust
  3. Use idiomatic Rust patterns (Result, Option, ? operator)
  4. Include comprehensive tests
  5. Follow Rust API guidelines
---

```

**OpenCode 在 Rust 開發中的實際應用**：

1. **初始化專案**：`opencode "Create a new Rust CLI project with clap for argument parsing"`
2. **編寫功能**：`opencode "Add a function that reads a CSV file, parses it, and returns statistics"`
3. **除錯**：`opencode "Fix the borrow checker error in src/main.rs"`
4. **重構**：`opencode "Refactor this module to use async/await instead of threads"`

### 實際範例：OpenCode 協助 Rust 開發

假設我們想用 Rust 寫一個簡單的 JSON 解析器，使用 OpenCode：

**使用者提示**：
> Write a simple JSON parser in Rust. It should parse basic JSON strings into a `JsonValue` enum. Support null, booleans, numbers, strings, arrays, and objects.

**OpenCode 生成的初始程式碼**：

```rust
use std::collections::HashMap;

#[derive(Debug, PartialEq)]
pub enum JsonValue {
    Null,
    Bool(bool),
    Number(f64),
    String(String),
    Array(Vec<JsonValue>),
    Object(HashMap<String, JsonValue>),
}

pub struct Parser {
    input: Vec<char>,
    pos: usize,
}

impl Parser {
    pub fn new(input: &str) -> Self {
        Parser {
            input: input.chars().collect(),
            pos: 0,
        }
    }
    
    fn peek(&self) -> Option<char> {
        self.input.get(self.pos).copied()
    }
    
    fn consume(&mut self) -> Option<char> {
        let ch = self.input.get(self.pos).copied();
        self.pos += 1;
        ch
    }
    
    pub fn parse(&mut self) -> Result<JsonValue, String> {
        self.skip_whitespace();
        let value = self.parse_value()?;
        self.skip_whitespace();
        Ok(value)
    }
    
    fn parse_value(&mut self) -> Result<JsonValue, String> {
        match self.peek() {
            Some('n') => self.parse_null(),
            Some('t') | Some('f') => self.parse_bool(),
            Some('"') => self.parse_string().map(JsonValue::String),
            Some('[') => self.parse_array(),
            Some('{') => self.parse_object(),
            Some(c) if c.is_digit(10) || c == '-' => {
                self.parse_number().map(JsonValue::Number)
            }
            Some(c) => Err(format!("Unexpected character: '{}'", c)),
            None => Err("Unexpected end of input".to_string()),
        }
    }
    
    fn skip_whitespace(&mut self) {
        while self.peek().map_or(false, |c| c.is_whitespace()) {
            self.consume();
        }
    }
    
    fn parse_null(&mut self) -> Result<JsonValue, String> {
        if self.consume() == Some('n')
            && self.consume() == Some('u')
            && self.consume() == Some('l')
            && self.consume() == Some('l')
        {
            Ok(JsonValue::Null)
        } else {
            Err("Expected 'null'".to_string())
        }
    }
    
    fn parse_bool(&mut self) -> Result<JsonValue, String> {
        if self.consume() == Some('t')
            && self.consume() == Some('r')
            && self.consume() == Some('u')
            && self.consume() == Some('e')
        {
            Ok(JsonValue::Bool(true))
        } else if self.peek() == Some('f')
            && self.consume() == Some('f')
            && self.consume() == Some('a')
            && self.consume() == Some('l')
            && self.consume() == Some('s')
            && self.consume() == Some('e')
        {
            Ok(JsonValue::Bool(false))
        } else {
            Err("Expected 'true' or 'false'".to_string())
        }
    }
    
    fn parse_number(&mut self) -> Result<f64, String> {
        let start = self.pos;
        while self.peek().map_or(false, |c| c.is_digit(10) || c == '.' || c == '-' || c == 'e' || c == 'E' || c == '+') {
            self.consume();
        }
        let num_str: String = self.input[start..self.pos].iter().collect();
        num_str.parse::<f64>()
            .map_err(|_| format!("Invalid number: '{}'", num_str))
    }
    
    fn parse_string(&mut self) -> Result<String, String> {
        self.consume(); // consume opening '"'
        let mut result = String::new();
        loop {
            match self.consume() {
                Some('"') => return Ok(result),
                Some('\\') => {
                    match self.consume() {
                        Some('"') => result.push('"'),
                        Some('\\') => result.push('\\'),
                        Some('n') => result.push('\n'),
                        Some('t') => result.push('\t'),
                        Some('r') => result.push('\r'),
                        Some(c) => result.push(c),
                        None => return Err("Unexpected end of input in string escape".to_string()),
                    }
                },
                Some(c) => result.push(c),
                None => return Err("Unterminated string".to_string()),
            }
        }
    }
    
    fn parse_array(&mut self) -> Result<JsonValue, String> {
        self.consume(); // consume '['
        let mut items = Vec::new();
        loop {
            self.skip_whitespace();
            if self.peek() == Some(']') {
                self.consume();
                return Ok(JsonValue::Array(items));
            }
            if !items.is_empty() {
                match self.consume() {
                    Some(',') => {},
                    Some(']') => return Ok(JsonValue::Array(items)),
                    Some(c) => return Err(format!("Expected ',' or ']', got '{}'", c)),
                    None => return Err("Unexpected end of input in array".to_string()),
                }
            }
            self.skip_whitespace();
            items.push(self.parse_value()?);
        }
    }
    
    fn parse_object(&mut self) -> Result<JsonValue, String> {
        self.consume(); // consume '{'
        let mut map = HashMap::new();
        loop {
            self.skip_whitespace();
            if self.peek() == Some('}') {
                self.consume();
                return Ok(JsonValue::Object(map));
            }
            if !map.is_empty() {
                match self.consume() {
                    Some(',') => {},
                    Some('}') => return Ok(JsonValue::Object(map)),
                    Some(c) => return Err(format!("Expected ',' or '}}', got '{}'", c)),
                    None => return Err("Unexpected end of input in object".to_string()),
                }
            }
            self.skip_whitespace();
            let key = self.parse_string()?;
            self.skip_whitespace();
            if self.consume() != Some(':') {
                return Err("Expected ':' in object".to_string());
            }
            self.skip_whitespace();
            let value = self.parse_value()?;
            map.insert(key, value);
        }
    }
}
```

**下一步：讓 OpenCode 生成測試**：

```
opencode "Generate comprehensive tests for the JSON parser. Test edge cases like 
empty string, nested objects, all JSON data types, and invalid inputs."
```

OpenCode 會自動生成測試程式碼並執行 `cargo test`。

### Claude Code：自主除錯與重構

Claude Code 2.0 的獨特能力是**自主除錯**——當 Rust 編譯器報錯時，Claude Code 可以：

1. 讀取編譯錯誤訊息
2. 分析錯誤的原因（借用檢查器錯誤、型別不匹配等）
3. 提出修復方案
4. 自動修改程式碼
5. 重新編譯驗證

```bash
# Claude Code 的 Rust 除錯流程
claude "Fix the compilation errors in my Rust project"

# Claude Code 的行動：
# 1. 執行 cargo check
# 2. 分析錯誤：borrowed data escapes outside of closure
# 3. 修改程式碼：添加 'static lifetime bound
# 4. 重新執行 cargo check 驗證
```

**範例**：Claude Code 修復借用檢查器錯誤

原始錯誤：
```
error[E0373]: closure may outlive the current function, but it borrows `data`, which is owned by the current function
```

Claude Code 會自動產生效正：
```rust
// Before (編譯錯誤)
let data = vec![1, 2, 3];
thread::spawn(|| {
    println!("{:?}", data);
});

// After (Claude Code 修正)
let data = vec![1, 2, 3];
thread::spawn(move || {
    println!("{:?}", data);
});
```

### Copilot X：Rust 程式碼補全與審查

GitHub Copilot X 整合了 GPT-6，其 Rust 程式碼補全能力包括：

```rust
// Copilot 可以根據上下文自動補全

// 輸入: "read file asynchronously"
// Copilot 補全:
async fn read_file_async(path: &str) -> Result<String, std::io::Error> {
    let mut file = tokio::fs::File::open(path).await?;
    let mut contents = String::new();
    file.read_to_string(&mut contents).await?;
    Ok(contents)
}

// 輸入: "serialize struct to JSON"
// Copilot 補全:
#[derive(Serialize, Deserialize, Debug)]
struct User {
    id: u64,
    name: String,
    email: String,
}

impl User {
    fn to_json(&self) -> Result<String, serde_json::Error> {
        serde_json::to_string(self)
    }
}
```

### Antigravity：意圖驅動的 Rust 開發

Antigravity 採用了「意圖驅動開發」（Intent-Driven Development）模式——開發者用自然語言描述系統的行為，AI 自動生成完整的實作：

```
// Antigravity 的輸入（自然語言規格）
"""
Build a Rust web service that:
- Listens on port 8080
- Has a POST /users endpoint for creating users
- Has a GET /users/{id} endpoint for getting user by ID
- Uses SQLite for storage
- Returns JSON responses
"""

// Antigravity 生成的專案結構
// src/main.rs, src/models.rs, src/handlers.rs, src/db.rs
// Cargo.toml with all dependencies
// Integration tests
// OpenAPI spec
```

### 安全程式碼生成

AI 工具在生成 Rust 程式碼時的一大優勢是安全性。與 C/C++ 不同，Rust 的編譯器會檢查 AI 生成的程式碼是否安全：

```rust
// AI 生成的程式碼如果違反所有權規則，編譯器會報錯
// 這意味著 AI 在 Rust 中比較不可能產生記憶體錯誤

// 錯誤的 AI 生成（會被 rustc 捕獲）
fn get_first(items: &[i32]) -> &i32 {
    &items[0]
}
fn modify_items(items: &mut Vec<i32>) {
    let first = get_first(items); // 編譯器報錯！
    items.push(4);                 // 不可變引用存在時不能可變借用
    println!("{}", first);
}
```

### Rust 在 AI 基礎設施中的角色

AI 不僅改變了 Rust 的開發方式，Rust 也正在成為 AI 基礎設施的核心語言：

- **Candle**：Hugging Face 的純 Rust ML 推理引擎
- **Burn**：Rust 原生深度學習框架
- **Ort**：Rust 的 ONNX Runtime 綁定
- **safetensors**：Rust 實作的安全張量格式
- **mistral.rs**：Rust 中的 LLM 推論引擎

Rust 對於 AI 基礎設施的吸引力：
1. **低延遲**：適合即時推理
2. **無 GC**：避免不可預測的暫停
3. **輕量**：靜態連結，部署簡單
4. **安全**：適合處理用戶資料

### 小結

AI 與 Rust 的關係是雙向的：

- **AI 讓 Rust 不再難學**：AI 工具可以幫助開發者理解所有權、生成程式碼、修復錯誤
- **Rust 讓 AI 基礎設施更可靠**：Rust 的效能和安全性使其成為 AI 基礎設施的理想語言

這不僅僅是技術的進步，更是一場開發模式變革——**從「手動編寫程式碼」到「AI 輔助開發與人類指導」**。Rust + AI 的組合成為這個新時代的最佳實踐。

---

## 延伸閱讀

- [OpenCode - AI Coding Agent](https://opencode.ai)
- [Claude Code - AI for Software Development](https://www.google.com/search?q=Claude+Code+AI+software+development)
- [GitHub Copilot X](https://www.google.com/search?q=GitHub+Copilot+X+Rust)
- [Candle - Rust ML Framework](https://www.google.com/search?q=Candle+Rust+ML+framework)
