# AI + 系統程式

## AI 輔助 unsafe Rust、自動化 FFI 生成（2024-2026）

### 前言

AI 輔助系統程式設計是一個新興但極具潛力的領域。與 Web 開發不同，系統程式設計中的錯誤可能導致崩潰、安全漏洞甚至物理損壞。這使得 AI 在系統程式設計中的角色更加微妙——AI 必須在「提供生產力」和「保證正確性」之間取得平衡。

### AI 在系統程式設計中的獨特挑戰

```
一般程式設計 (Web)
  AI 錯誤 → HTTP 500 → 開發者修復 ✅

系統程式設計 (Embedded/Kernel)
  AI 錯誤 → 記憶體崩潰 / 安全漏洞 / 硬體損壞 ❌
```

這意味著 AI 在系統程式設計中的應用必須更加謹慎——**AI 生成的程式碼必須經過 Rust 編譯器的嚴格檢查**，而 Rust 正是最適合這個任務的語言。

### AI 輔助 unsafe 程式碼審查

unsafe Rust 是最容易引入 bug 的地方，但也是最適合 AI 協助的領域：

```rust
// AI 審查：這個 unsafe 區塊是否有問題？
unsafe {
    let slice = std::slice::from_raw_parts(ptr, len);
    // AI 分析：
    // 1. ptr 是否有效？ 需要檢查 ptr.is_null()
    // 2. len 是否過大？ 可能超出分配範圍
    // 3. 記憶體是否已初始化？ 需要確認
}

// AI 建議的修正：
if ptr.is_null() {
    return Err("Null pointer");
}
// 假設我們知道 ptr 指向 len 個已初始化的元素
let slice = unsafe { std::slice::from_raw_parts(ptr, len) };
```

### AI 輔助 FFI 綁定生成

AI 可以從 C 頭文件自動生成 Rust FFI 綁定，超越了 bindgen 的能力：

```
輸入（C 頭文件）：
  int process_data(const char* input, int len, Output* out);

AI 生成的 Rust 綁定（自動加上安全封裝）：
  pub fn process_data(input: &str) -> Result<Output, Error> {
      let c_input = CString::new(input).map_err(|_| Error::InvalidInput)?;
      let mut out = Output::default();
      let result = unsafe { sys::process_data(c_input.as_ptr(), input.len() as i32, &mut out) };
      if result == 0 { Ok(out) } else { Err(Error::from_code(result)) }
  }
```

**AI 的超能力**：AI 可以理解 C 程式碼的意圖，而不僅僅是機械地轉換型別：

- 推斷參數的「輸入/輸出」語義
- 識別錯誤處理模式（回傳值 vs errno vs 異常）
- 理解所有權語義（誰分配、誰釋放）
- 自動添加安全邊界檢查

### 實際案例：用 AI 審查嵌入式驅動程式

```rust
// AI 審查的嵌入式驅動程式碼

// GPIO 中斷處理（AI 發現的問題）
#[interrupt]
fn EXTI0_IRQHandler() {
    // AI: 這是在中斷上下文中！
    // AI: Mutex::lock() 可能導致死鎖！
    
    static DATA: Mutex<u32> = Mutex::new(0);
    let data = DATA.lock().unwrap();  // ❌ 可能死鎖！
    *data += 1;
    
    // AI 建議：使用中斷安全的 atomic
    static COUNTER: AtomicU32 = AtomicU32::new(0);
    COUNTER.fetch_add(1, Ordering::Relaxed);  // ✅
}
```

### AI 輔助形式化驗證

Rust 的形式化驗證工具（Kani、Creusot）正在整合 AI：

```rust
// AI 自動生成的驗證條件（Contracts）

// 人類寫的函式
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    let mut left = 0;
    let mut right = arr.len();
    while left < right {
        let mid = left + (right - left) / 2;
        if arr[mid] == target {
            return Some(mid);
        } else if arr[mid] < target {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    None
}

// AI 生成的驗證契約
#[kani::requires(arr.is_sorted())]     // 前提：陣列已排序
#[kani::ensures(
    match result {
        Some(i) => arr[i] == target,    // 找到的必須是目標
        None => !arr.contains(&target), // 沒找到表示不存在
    }
)]
fn binary_search(arr: &[i32], target: i32) -> Option<usize> {
    // ...
}
```

### AI 輔助嵌入式開發工作流程

```
┌─────────────┐
│  需求描述    │  「在 STM32F4 上點亮 LED，使用定時器中斷」
└──────┬──────┘
       │
┌──────┴──────┐
│  AI 生成骨架  │  
│   - 專案結構  │
│   - 依賴配置  │
│   - 初始化碼  │
└──────┬──────┘
       │
┌──────┴──────┐
│  編譯器檢查   │  cargo build → 錯誤修正 → cargo build ✅
└──────┬──────┘
       │
┌──────┴──────┐
│  AI 安全審查  │  
│   - unsafe 區塊  │
│   - 中斷安全  │
│   - 記憶體佈局  │
└──────┬──────┘
       │
┌──────┴──────┐
│  測試驗證    │  
│   - 單元測試  │
│   - 硬體測試  │
└─────────────┘
```

### AI + 系統程式設計的工具生態

| 工具 | 功能 | Rust 支援 |
|------|------|-----------|
| Claude Code | unsafe 審查、FFI 生成 | ✅ 優秀 |
| OpenCode | 嵌入式專案骨架、驅動程式碼 | ✅ 優秀 |
| Kani + AI | 自動生成驗證條件 | 🟡 實驗性 |
| Creusot | 契約式驗證 | 🟡 實驗性 |
| cargo-audit + AI | 安全漏洞掃描 | ✅ 生產級 |

### 限制與風險

**AI 在系統程式設計中的限制**：

1. **硬體知識**：AI 不理解特定 MCU 的硬體行為
2. **即時約束**：AI 無法分析任務的 WCET（最差情況執行時間）
3. **安全關鍵系統**：AI 生成的程式碼不適合 DO-178C / ISO 26262 認證
4. **低階最佳化**：AI 不理解快取一致性、記憶體屏障等概念

**最佳實踐**：
- AI 生成骨架 → 人類完成硬體相關部分
- AI 審查 unsafe → 人類 double-check
- AI 生成測試 → 人類審查邊界條件
- AI 生成文件 → 人類驗證技術正確性

### 未來展望

1. **專用模型**：針對 Rust 系統程式設計微調的 AI 模型
2. **硬體感知**：AI 理解特定 MCU/SoC 的硬體細節
3. **形式化驗證整合**：AI + 形式化驗證的混合方法
4. **安全認證輔助**：AI 協助生成符合安全標準的文件和程式碼

### 小結

AI + 系統程式設計是一個仍在早期但快速發展的領域。與 Web 開發不同，系統程式設計對正確性的要求極高——但這也正是 Rust 的優勢所在：

**Rust 的編譯器作為安全網**，確保 AI 生成的程式碼不會引入記憶體安全漏洞。AI 提供生產力，Rust 提供安全性——這種組合讓系統程式設計變得前所未有的高效和安全。

---

## 延伸閱讀

- [Kani Rust Verifier](https://www.google.com/search?q=Kani+Rust+verifier)
- [Creusot: Rust Verifier](https://www.google.com/search?q=Creusot+Rust+verifier)
- [AI for Embedded Systems](https://www.google.com/search?q=AI+for+embedded+systems+Rust)
