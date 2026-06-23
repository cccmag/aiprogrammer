# AI 輔助 AI 框架開發

## LLM 生成算子、NAS 搜尋、自動化測試、編譯器預測（2024-2026）

### LLM 生成算子實作

2024 年之後，LLM 的能力已經足夠生成**可直接編譯的算子實作**。這對 Rust AI 框架的開發產生了深遠的影響——過去需要數天實現的 GPU kernel，現在可能只需要幾分鐘的 LLM 提示工程。

以 Candle 的 GELU kernel 為例，傳統實作需要同時撰寫 Rust 綁定和 CUDA kernel：

```cuda
// CUDA kernel for GELU (手寫)
__global__ void gelu_kernel(const float* x, float* y, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i < n) {
        float xi = x[i];
        float x3 = xi * xi * xi;
        float inner = 0.79788456f * (xi + 0.044715f * x3);
        y[i] = 0.5f * xi * (1.0f + tanhf(inner));
    }
}
```

現在，開發者可以請 LLM 同時生成 CUDA、Metal、和 WGSL 三個後端的實作：

```
提示: "Write a fused kernel that computes GELU(x) = 
0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))
for CUDA, Metal Shading Language, and WGSL.
Include warp-level optimizations for CUDA."
```

LLM 會產出三種語言的 kernel，並且可以自動加上 fusion 策略——例如將 GELU 與前後的 LayerNorm 或 Linear 合併。

**AI 輔助開發的局限性**：
- 生成的 kernel 需要完善的測試來驗證正確性
- LLM 對特定 GPU 架構（如 Ada Lovelace 的第四代 Tensor Core）的細節了解有限
- 生成的程式碼有時會使用不存在的 API 或已棄用的指令

### AI 輔助模型架構搜尋（NAS）

神經網路架構搜尋（Neural Architecture Search, NAS）過去是計算密集的任務——在數千個候選架構中訓練和評估。但在 Rust 框架中，NAS 可以透過**編譯期生成**和**型別層級約束**來加速：

```rust
// dfdx 風格的型別層級 NAS（概念）
use dfdx::prelude::*;

// 搜尋空間定義為型別枚舉
enum ArchSearchSpace<const HIDDEN: usize> {
    Mlp(Linear<HIDDEN, 256>, ReLU, Linear<256, 10>),
    Cnn(Conv2D<1, 32, 3>, ReLU, Flatten, Linear<..., 10>),
    Transformer(TransformerEncoder<...>, Linear<..., 10>),
}

// AI 驅動的架構生成器
struct NASGenerator {
    llm: Box<dyn LLMBackend>,
}

impl NASGenerator {
    fn suggest_architecture(&self, task: &str) -> String {
        // LLM 根據任務特性（影像分類、語意分割等）
        // 建議適當的架構配置
        let prompt = format!(
            "Suggest a neural network architecture for {}. \
             Use only these layer types: Conv2D, Linear, ReLU, \
             GELU, LayerNorm, MaxPool. \
             Output as valid Rust code using the dfdx API.",
            task
        );
        self.llm.generate(&prompt)
    }
}
```

AI 輔助 NAS 有以下優勢：
- **減少搜尋次數**：LLM 可以基於先驗知識直接推薦好的架構候選
- **硬體感知**：LLM 可以考慮目標裝置的記憶體限制和計算能力
- **型別安全**：生成的 Rust 程式碼在編譯期就驗證了形狀相容性

### 自動化測試生成

Rust 的型別系統可以預防大量 bug，但數值正確性需要測試。LLM 可以自動生成測試案例：

```rust
// AI 生成的測試：驗證 GELU 反向傳播的正確性
#[test]
fn test_gelu_backward() {
    let x = Tensor::randn(&[32, 128]);
    let grad_output = Tensor::randn(&[32, 128]);
    
    // 前向
    let y = gelu(&x);
    
    // 數值梯度（有限差分）
    let eps = 1e-4;
    let mut numerical_grad = Tensor::zeros(x.shape());
    for i in 0..x.data().len() {
        let mut x_plus = x.clone();
        x_plus.data_mut()[i] += eps;
        let y_plus = gelu(&x_plus);
        
        let mut x_minus = x.clone();
        x_minus.data_mut()[i] -= eps;
        let y_minus = gelu(&x_minus);
        
        numerical_grad.data_mut()[i] =
            ((y_plus - y_minus) * &grad_output).sum() / (2.0 * eps);
    }
    
    // 反向傳播梯度
    let analytical_grad = gelu_backward(&x, &y, &grad_output);
    
    // 比較：相對誤差 < 1e-3
    let rel_error = (&numerical_grad - &analytical_grad).abs()
        / (numerical_grad.abs().max(1e-8));
    assert!(rel_error.mean().item() < 1e-3);
}
```

LLM 生成的測試不僅包含正確性驗證，還可以包含：
- **邊界條件**：空張量、形狀為 1 的維度、非常大的數值
- **記憶體洩漏檢測**：使用 Rust 的 `alloc` 計數器檢查 GPU 記憶體是否正確釋放
- **效能迴歸測試**：在 CI 中追蹤 kernel 的執行時間

### AI 預測編譯器最佳化

編譯器最佳化是另一個 AI 可以大幅貢獻的領域。傳統的編譯器（如 LLVM）使用啟發式演算法來決定何時進行內聯、迴圈展開、向量化等。AI 模型可以預測哪種最佳化策略對特定程式碼最有效。

在 Rust AI 框架的脈絡中，這特別適用於**自動調優（auto-tuning）**：

```rust
// AI 驅動的 kernel 選擇器
struct AITuner {
    model: Box<dyn LLMBackend>,
}

impl AITuner {
    fn select_best_kernel(
        &self,
        op: &str,
        shapes: &[usize],
        device: &Device,
    ) -> Kernel {
        // 收集硬體資訊和運算特徵
        let profile = format!(
            "Select the fastest kernel for {} with shapes {:?} \
             on device {:?}. Options: [naive, tiled_16x16, \
             tiled_32x32, warp_specialized]. \
             Consider memory bandwidth and compute capacity.",
            op, shapes, device
        );
        
        // AI 預測最佳策略
        let prediction = self.model.generate(&profile);
        self.parse_kernel_choice(&prediction)
    }
}
```

Candle 的開發團隊已經開始使用 AI 來分析效能 profiling 資料，自動建議可以 fusion 的算子對。

### 未來展望

2024-2026 年，AI 輔助開發從「新奇玩具」變成了「日常工具」。對 Rust AI 框架開發者的影響：

| 面向 | 傳統方式 | AI 輔助方式 |
|------|---------|-----------|
| Kernel 實作 | 手寫 CUDA/Metal | LLM 生成 + 人工驗證 |
| 架構設計 | 論文複現 | AI 建議 + 型別安全約束 |
| 測試編寫 | 手動寫 test case | AI 自動生成邊界案例 |
| 效能調校 | 手動 profiling | AI 預測 + auto-tuning |

最重要的改變不是「AI 取代了工程師」，而是**開發者可以專注於高層次的設計決策**——記憶體模型、後端抽象、型別系統設計——而將繁瑣的 GPU kernel 實現和測試案例編寫交給 AI。

---

**下一步**：回到[首頁](focus.md)

## 延伸閱讀

- [LLM for CUDA kernel generation](https://www.google.com/search?q=LLM+CUDA+kernel+generation+AI)
- [Neural Architecture Search with LLMs](https://www.google.com/search?q=LLM+neural+architecture+search+NAS)
- [AI-assisted test generation for ML frameworks](https://www.google.com/search?q=AI+test+generation+deep+learning+framework)
- [Auto-tuning deep learning kernels](https://www.google.com/search?q=auto-tuning+GPU+kernel+deep+learning)
- [Rust compiler optimization with AI](https://www.google.com/search?q=AI+compiler+optimization+Rust+LLVM)
