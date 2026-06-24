# LLM 部署與量化（2022-2026）

## 模型量化方法

量化將模型權重從 FP16（16 位浮點）減少到較低位數，大幅降低記憶體和計算需求。

### 主流量化格式

| 方法 | 位元 | 適用模型 | 品質損失 |
|------|------|---------|---------|
| **GPTQ** | 4-bit/3-bit | GPU 部署 | 輕微 |
| **GGUF** | 2-8 bit | CPU/邊緣 | 可控 |
| **AWQ** | 4-bit | GPU 部署 | 極輕微 |
| **BitsAndBytes** | 4-bit/8-bit | Hugging Face 生態 | 輕微 |

```
模型大小對比 (7B 參數)：
──────────────────────────────
FP16 (原始) : ~14 GB → 需要 24GB GPU
INT8        : ~7 GB  → 需要 12GB GPU
INT4 (GPTQ) : ~4 GB  → 需要 8GB GPU
INT4 (GGUF) : ~4 GB  → 可在 8GB RAM 的 Mac 上執行
```

### GPTQ 原理

GPTQ（2023）基於 Optimal Brain Quantization 框架，逐層最小化量化誤差：

```python
def gptq_quantize(layer_weight, calibration_data):
    # 1. 對權重進行 Hessian 分析
    H = calibration_data.T @ calibration_data
    # 2. 找出對輸出影響最小的權重
    errors = diag(H) * (layer_weight - quantize(layer_weight))**2
    # 3. 用剩餘權重補償量化誤差
    compensated = layer_weight - update_by_hessian(layer_weight, H)
    return quantize(compensated)
```

GPTQ 是目前 GPU 上 4-bit 推理的事實標準。

## 推論引擎比較

| 引擎 | 語言 | 支援硬體 | 特點 |
|------|------|---------|------|
| **llama.cpp** | C/C++ | CPU/GPU | GGUF 格式，不需 GPU |
| **vLLM** | Python/CUDA | GPU | PagedAttention，高吞吐 |
| **TGI** | Rust/Python | GPU | Hugging Face 官方 |
| **TensorRT-LLM** | C++/CUDA | NVIDIA GPU | 最佳 NVIDIA 效能 |
| **MLC-LLM** | TVM | 全平台 | 手機、Web 均可 |

### vLLM PagedAttention

vLLM（2023）的核心貢獻是 PagedAttention——將 KV Cache 分頁管理，類似作業系統的虛擬記憶體：

```
傳統 KV Cache: 每個請求分配固定連續記憶體（大量碎片浪費）
PagedAttention: KV Cache 以 page 為單位動態分配（接近零碎片）
```

效果：**vLLM 可處理的請求數量是傳統方法的 2-4 倍**。

## GPU vs CPU 部署策略

```
選擇部署策略：
──────────────────────────────

GPU 部署（生產環境）:
├── 模型格式：GPTQ / AWQ
├── 引擎：vLLM / TensorRT-LLM
├── 優點：低延遲 (50-200ms/token)
└── 缺點：成本高 (A100 $3-5/hr)

CPU 部署（邊緣/個人）:
├── 模型格式：GGUF (Q4_K_M 推薦)
├── 引擎：llama.cpp / Ollama
├── 優點：成本低 (無需 GPU)
└── 缺點：延遲較高 (5-20 tokens/sec)

混合部署:
├── 前段：GPU (快取常用 prompt)
├── 後段：大型批次 → CPU 排程
└── 適合：成本敏感的非即時任務
```

## KV Cache 與連續批次處理

### KV Cache

Transformer Decoder 的自回歸特性意味著每生成一個 token，需要重新計算之前所有 token 的 K 和 V——KV Cache 將它們快取下來避免重複計算。

```
KV Cache 記憶體需求：
──────────────────────────────
7B 模型, FP16, n_layers=32, d_kv=128, n_heads=32
每個 token: 2 × 32 × 128 × 32 × 2 bytes = ~0.5 MB

4K 上下文: ~2 GB
32K 上下文: ~16 GB
128K 上下文: ~64 GB
```

這也是為什麼長上下文 LLM 的 KV Cache 管理是重要研究領域。

### 連續批次處理（Continuous Batching）

傳統批次處理等待所有序列完成才開始新批次。連續批次處理允許新序列動態插入：

```
傳統批次:
[seq1] [seq1] [seq1] [seq1] [seq1]  [完成]
[seq2] [seq2] [seq2] [seq2]         [完成]
                              [等待新批次開始]

連續批次:
[seq1] [seq1] [seq3] [seq3] [seq4]  [seq1:完成]
[seq2] [seq2] [seq2] [seq5] [seq5]  [seq3:新加入]
                              [seq4:新加入]
```

連續批次可將 GPU 利用率從 50% 提升到 95% 以上。

---

## 延伸閱讀

- [GPTQ 量化論文](https://www.google.com/search?q=GPTQ+Accurate+Post-Training+Quantization+Generative+Pre-trained+Transformers)
- [vLLM PagedAttention](https://www.google.com/search?q=vLLM+PagedAttention+efficient+memory+management+LLM)
- [llama.cpp 專案](https://www.google.com/search?q=llama.cpp+CPU+inference+LLM+GGUF)
- [AWQ 量化方法](https://www.google.com/search?q=AWQ+Activation-aware+Weight+Quantization+LLM)

---

*AI 程式人雜誌 2026 年 7 月號 — 大型語言模型實戰*
