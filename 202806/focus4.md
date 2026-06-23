# 推論引擎架構（2021-2028）

## 從 Python 到生產環境

2021 年以前，大多數模型的推論在訓練框架（PyTorch、TensorFlow）內部完成。但生產環境需要更高的吞吐量和更低的延遲，於是專門的推論引擎應運而生。

## 主流推論引擎比較

| 引擎 | 發起方 | 硬體 | 特點 |
|------|--------|------|------|
| TensorRT | NVIDIA | GPU | 算子融合、FP8/INT8 |
| ONNX Runtime | Microsoft | CPU/GPU | 跨平台 |
| vLLM | UC Berkeley | GPU | PagedAttention |
| llama.cpp | ggerganov | CPU/GPU | 本地部署 |
| TGI | Hugging Face | GPU | 生產 Ready |

## 推論引擎的核心最佳化技術

### 算子融合（Operator Fusion）

將多個相鄰操作合併為一個 kernel，減少記憶體往返：

```
原始圖: A ──► B ──► C ──► D
融合後: A ──► ABCD (單一 kernel)
```

### 動態批次處理

```python
class ContinuousBatching:
    def __init__(self, max_batch=64):
        self.requests = []
        self.max_batch = max_batch
        self.running = set()
    
    def can_add(self, seq_len):
        if len(self.running) >= self.max_batch:
            return False
        return True
    
    def schedule(self):
        """將可執行的請求加入批次"""
        while len(self.running) < self.max_batch and self.requests:
            req = self.requests.pop(0)
            self.running.add(req)
```

### 記憶體管理

LLM 推論最頭痛的問題是 KV Cache 的記憶體爆炸。vLLM 的 PagedAttention 對此做出了突破：

```
傳統記憶體配置：
┌──────┬──────┬──────┬──────┐
│ Seq1 │ Seq2 │ Seq3 │ Seq4 │
└──────┴──────┴──────┴──────┘
每個序列需要連續大塊記憶體

PagedAttention：
┌──┬──┬──┬──┐
│S1│S2│S1│S3│
├──┼──┼──┼──┤
│S1│S4│S2│S2│
└──┴──┴──┴──┘
分頁管理，無內部碎片
```

## 編譯與圖優化

```python
# ONNX Runtime 的圖優化層次
graph = onnx.load("model.onnx")

# 層次 1: 常量折疊（Constant Folding）
graph = fold_constants(graph)

# 層次 2: 冗餘節點消除
graph = eliminate_dead_end(graph)

# 層次 3: 算子融合
graph = fuse_ops(graph, patterns=[
    ("Conv+BatchNorm", fused_conv_bn),
    ("MatMul+Add+Bias", fused_linear),
    ("LayerNorm+Residual", fused_layernorm_residual),
])
```

## 2024-2028 趨勢

推論引擎正趨向統一標準。OpenAI 的 Triton 語言和 MLIR 編譯器基礎設施讓不同硬體的後端可以共用前端最佳化。未來推論引擎的競爭將不再是「能不能跑」，而是「能不能在正確的硬體上以最低成本跑」。

## 延伸閱讀

- [TensorRT: GPU Inference Optimization](https://www.google.com/search?q=TensorRT+NVIDIA+inference+optimization)
- [vLLM: PagedAttention for LLM Inference](https://www.google.com/search?q=vLLM+PagedAttention+LLM+inference)
- [llama.cpp: LLM Inference in C/C++](https://www.google.com/search?q=llama.cpp+LLM+inference+C+CPU)

---

*本篇文章為「AI 程式人雜誌 2026 年 6 月號」焦點系列之四。*
