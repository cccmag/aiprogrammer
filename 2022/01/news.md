# 本月新知

## 2022 年 1 月程式與 AI 技術動態

### 程式語言與框架

**Python 3.11 開發啟動**

Python 核心開發團隊於本月正式啟動 Python 3.11 的開發工作。根據 PEP 657，3.11 將引入更精確的錯誤追蹤資訊，讓開發者能快速定位錯誤位置。PEP 659 則提出基於直觀最佳化的特化自適應解釋器，預計將帶來 10-60% 的效能提升。

**Rust 1.58 發布**

Rust 團隊發布 1.58 穩定版，主要亮點是「格式化字串中的捕獲變數」支援。開發者現在可以直接在格式化字串中使用變數名，無需手動傳遞參數：

```rust
let name = "Alice";
println!("Hello {name}"); // 而非 println!("Hello {}", name)
```

**Google 提出 Carbon 語言**

Google 工程師 Chandler Carruth 在 CppNorth 會議上發表了 Carbon 語言的提案。Carbon 定位為 C++ 的繼任者，旨在提供更好的記憶體安全性、泛型系統和現代化工具鏈。Carbon 語言被設計為與 C++ 完全互操作，並計劃支援基於合約的設計。

### AI 與機器學習

**OpenAI 發表 InstructGPT**

OpenAI 於本月發表 InstructGPT 論文《Training Language Models to Follow Instructions》。該模型基於 GPT-3，使用人類回饋強化學習（RLHF）進行微調，大幅提升了遵循指令的能力。InstructGPT 的 1.3B 參數模型在許多任務上超越了 175B 的原始 GPT-3，證明了對齊訓練的重要性。

**DeepMind 推出 AlphaCode**

DeepMind 發表 AlphaCode，這是一個能自動編寫競賽級程式碼的 AI 系統。AlphaCode 在 Codeforces 平台上的評比中達到了前 54% 人類程式設計師的水準。該系統使用了編碼器-解碼器架構，並在大量開源程式碼上進行預訓練。

**Meta 打造 AI Research SuperCluster**

Meta 宣布正在建造 AI Research SuperCluster（RSC），預計將成為世界上最快的 AI 超級電腦之一。RSC 配備 6080 個 NVIDIA A100 GPU，能在 16 位元精度下達到近 5 Exaflops 的運算能力。該集群將用於訓練大型語言模型和電腦視覺模型。

**Hugging Face Transformers 4.16 發布**

Hugging Face 發布 Transformers 4.16 版本，新增對 Flax 框架的支援。Flax 是基於 JAX 的神經網路庫，提供了更靈活的模型定義方式和 Just-In-Time 編譯，顯著提升了訓練和推論速度。

**PyTorch 1.11 發布候選版**

PyTorch 團隊發布 1.11 版的發布候選版本。新版本引入了 TorchData（一個靈活的資料載入庫）和 functorch（受 JAX 啟發的函數式轉換庫）。此外，PyTorch 1.11 優化了 GPU 通訊效能，對分散式訓練提供了更好的支援。

### 開發工具

**GitHub Copilot 擴大預覽**

GitHub Copilot 在 2021 年底開始公開預覽後，於 2022 年 1 月進一步擴大測試範圍。由 OpenAI Codex 驅動的這款 AI 程式設計助手已支援 Visual Studio Code、JetBrains 和 Neovim 等主流編輯器。

**WebAssembly System Interface 進展**

WASI（WebAssembly System Interface）工作組發布了新的 snapshot，引入了對網路 socket 和檔案系統操作的標準化介面。這意味著 WebAssembly 在伺服器端和邊緣運算中能夠更好地與作業系統互動。

### 標準與規範

- **ECMAScript 2022 定案**：新標準納入了 Class Fields、Top-level await、.at() 等特性
- **C++23 標準進展**：C++23 的 std::print 和 std::expected 已獲得通過
- **ISO 正式發布 Ruby 3.1**：引入 pattern matching 和 debugger 支援

### 業界動態

- **微軟以 687 億美元收購動視暴雪**：佈局元宇宙戰略
- **NVIDIA 發布 RTX 3050**：入門級光追顯卡，支援 DLSS
- **Intel 推出 Arc Alchemist 獨立顯卡**：重返 GPU 市場
