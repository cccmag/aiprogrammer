# 程式實作：模型推論最佳化工具

## 簡介

從零建構推論最佳化工具，涵蓋量化、剪枝、知識蒸餾、KV Cache。完整程式碼在 `_code/inference_opt.py`。

## 核心功能

- **權重量化**：FP32 → INT8，4x 壓縮
- **幅度剪枝**：依權重大小移除不重要參數
- **知識蒸餾**：大模型教小模型
- **KV Cache**：Transformer 推論快取

## 執行方式

```bash
cd _code
python3 inference_opt.py
```
