# AI 硬體市場變化

## 算力短缺的一年

2022 年，AI 硬體市場經歷了史無前例的供需失衡。生成式 AI 的爆發讓 GPU 需求暴增，NVIDIA A100 的價格在二級市場翻了數倍，交期延長到數月。這一章回顧 2022 年 AI 硬體的關鍵變化。

## NVIDIA 的霸主地位

### A100 的統治

NVIDIA A100（Ampere 架構）在 2022 年仍然是 AI 訓練的黃金標準：

- **80GB HBM2e 記憶體**：足夠容納大多數 LLM 的單卡訓練
- **TF32 精度**：顯著提升訓練吞吐量
- **NVLink**：多卡互連的高頻寬方案
- **MIG（多實例 GPU）**：單卡切分給多個用戶

### 供不應求的市場

```python
# 2022 年 GPU 價格變化估算
gpu_prices = {
    "A100_80GB_MSRP": 15000,    # 建議零售價
    "A100_80GB_spot": 25000,    # 二級市場價格
    "A100_80GB_lease": "3-5x",  # 雲端租用漲幅
}
```

## H100 的登場

NVIDIA 在 2022 年 3 月發布了 H100（Hopper 架構），但量產延遲到年底：

| 規格 | A100 | H100 |
|------|------|------|
| 架構 | Ampere | Hopper |
| 製程 | 7nm | 4nm |
| 電晶體 | 540 億 | 800 億 |
| FP8 | 無 | 有 |
| Transformer Engine | 無 | 有 |
| 記憶體 | 80GB HBM2e | 80GB HBM3 |
| 頻寬 | 2.0 TB/s | 3.35 TB/s |

## 挑戰者出現

### AMD MI250 / MI300

AMD Instinct MI250 在 2022 年的 HPC 市場取得了一些進展。MI300X 的發布在 2023 年成為 NVIDIA 的潛在挑戰者：

- **CDNA 3 架構**：專為 AI/ML 優化
- **192GB HBM3**：超越 A100 的記憶體容量
- **Infinity Fabric**：晶片間互連

### Google TPU v4

TPU v4 是 PaLM 540B 訓練的幕後英雄。Google 在 2022 年公開了更多 TPU v4 的技術細節：

- **4096 顆 TPU v4 組成 pod**
- **10 倍於 TPU v3 的效能提升**
- **光學交換網路**：動態拓撲配置
- **液體冷卻**：提升能源效率

### 自研晶片趨勢

更多公司開始自研 AI 晶片：

- **AWS Trainium / Inferentia**：亞馬遜的訓練與推論晶片
- **微軟 Athene**：與 OpenAI 合作設計的 AI 晶片
- **Meta**：自研推論晶片

## 雲端 GPU 市場

2022 年雲端 GPU 市場的變化：

- **價格暴漲**：A100 實例價格漲幅達 3-5 倍
- **配額限制**：雲端供應商開始限制 GPU 配額
- **替代方案**：Spot 實例、預留實例的需求增加
- **新進者**：CoreWeave、Lambda Labs 等 GPU 雲端新創崛起

## 推論硬體的演進

訓練獲得了最多關注，但推論硬體也在快速發展：

- **TensorRT**：NVIDIA 的推論優化工具鏈
- **ONNX Runtime**：跨平台推論框架
- **vLLM**：LLM 推論的記憶體管理創新
- **量化技術**：FP16 → INT8 → INT4 逐步普及

## 延伸閱讀

- [NVIDIA H100 技術概覽](https://www.google.com/search?q=NVIDIA+H100+Hopper+architecture+2022)
- [Google TPU v4 論文](https://www.google.com/search?q=TPU+v4+Google+paper+2022)
- [AMD MI300 分析](https://www.google.com/search?q=AMD+MI300+Instinct+AI+accelerator)
- [CoreWeave GPU 雲端](https://www.google.com/search?q=CoreWeave+GPU+cloud+2022)
- [LLM Inference Optimization](https://www.google.com/search?q=LLM+inference+optimization+vLLM+2023)
