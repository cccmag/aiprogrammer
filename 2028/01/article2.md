# CodeGen 模型深入

## 1. 引言

程式碼生成模型（CodeGen）是 AI 輔助軟體工程的核心技術。從 2021 年的 Codex 到 2026 年的開源模型，CodeGen 的架構、訓練資料與推理策略都有了質的飛躍。

## 2. 模型架構演進

### 2.1 編碼器-解碼器架構

早期模型（如 CodeBERT、PLBART）採用編碼器-解碼器結構，適合程式碼理解任務（如 bug 偵測、程式碼搜尋），但不擅長生成。

### 2.2 純解碼器架構

Codex、StarCoder、Code Llama 等模型採用純解碼器的 Transformer 架構，與 GPT 系列相同。核心改進包括：

- **Fill-in-the-Middle（FIM）**：讓模型不僅可以從左到右生成，還可以填空（給定前後文，生成中間內容），非常適合編輯器補完場景
- **長上下文訓練**：從最初的 2K tokens 到現在的 128K tokens，讓模型可以理解整個專案結構

```python
# FIM 訓練範例示意
# 給定 prefix（前文）和 suffix（後文）
# 模型學習生成 middle（中間內容）
prefix = "def fibonacci(n: int) -> int:\n    "
suffix = "\n        return b"
# 目標：生成 "if n <= 1: return n\n    a, b = 0, 1\n    for _ in range(2, n+1):\n        a, b = b, a + b"
```

## 3. 訓練資料策略

現代 CodeGen 模型的訓練資料已從單純的 GitHub 公開儲存庫擴展為多元資料來源：

| 資料類型 | 來源 | 比例 |
|---------|------|------|
| 原始碼 | GitHub | 60% |
| 程式碼文件 | Markdown、Docstring | 15% |
| 程式碼討論 | Stack Overflow、論壇 | 10% |
| 合成資料 | 模型自我生成的程式碼+測試 | 10% |
| 自然語言-程式碼配對 | 教學文章、筆記 | 5% |

## 4. 推理最佳化

### 4.1 Speculative Decoding

加速生成的關鍵技術。用小模型快速生成候選序列，大模型一次性驗證，可以實現 2-3 倍的推理加速。

### 4.2 樹狀搜尋（Tree-of-Thought for Code）

傳統 greedy decoding 容易陷入區域最優。樹狀搜尋讓模型同時探索多個生成路徑，選擇通過編譯和測試的路徑作為最終輸出。

## 5. 開源模型比較

| 模型 | 參數 | 上下文長度 | 支援語言 |
|------|------|-----------|---------|
| Code Llama | 7B-34B | 100K | Python、C++、Java |
| StarCoder 2 | 3B-15B | 16K | 600+ 語言 |
| DeepSeek Coder | 1.3B-33B | 128K | 87 種語言 |
| Qwen2.5-Coder | 0.5B-32B | 128K | 92 種語言 |

## 6. 結語

CodeGen 模型的發展正在加速。開源模型與閉源模型的差距持續縮小，客製化微調（fine-tuning）讓企業可以用內部程式碼庫打造專屬的 CodeGen 模型。接下來的突破將來自於更長的上下文、更好的工具使用能力、以及多模態（圖表到程式碼）的生成。

---

## 延伸閱讀

- [Code Llama 論文](https://www.google.com/search?q=Code+Llama+meta+AI+paper)
- [StarCoder 2 介紹](https://www.google.com/search?q=StarCoder+2+BigCode)
- [DeepSeek Coder 技術報告](https://www.google.com/search?q=DeepSeek+Coder+technical+report)
- [Fill-in-the-Middle 論文](https://www.google.com/search?q=Fill-in-the-Middle+code+generation+paper)
