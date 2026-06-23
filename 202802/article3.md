# 模型量化實戰：GPTQ/AWQ

## 為什麼需要量化

模型量化將 FP16 權重壓縮到 INT4/INT8，減少 4 倍的記憶體用量，讓消費級 GPU 也能運行大型模型。更重要的是，量化後的模型在頻寬受限的裝置上推論速度顯著提升。

## GPTQ 量化

GPTQ（GPT Post-Training Quantization）基於 Optimal Brain Quantization 演算法，逐層最小化量化誤差：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_name = "meta-llama/Llama-3-8B-Instruct"

# 載入原始模型
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto"
)

# GPTQ 量化（需要校準資料集）
from auto_gptq import BaseQuantizeConfig

quantize_config = BaseQuantizeConfig(
    bits=4,                # INT4
    group_size=128,        # 分組大小
    damp_percent=0.01,     # 阻尼係數
    desc_act=False,        # 按通道排序
)

model = AutoGPTQForCausalLM.from_pretrained(
    model_name, quantize_config
)
model.quantize(
    calib_dataset,         # 校準資料
    use_triton=False
)
model.save_quantized("llama3-8b-gptq-int4")
```

## AWQ 量化

AWQ（Activation-aware Weight Quantization）認識到權重的重要性不均勻——約 1% 的權重包含了大部分資訊：

```python
from awq import AutoAWQForCausalLM

model = AutoAWQForCausalLM.from_pretrained(
    model_name, device_map="auto"
)

tokenizer = AutoTokenizer.from_pretrained(model_name)

# AWQ 量化（保留重要權重通道）
quant_config = {
    "zero_point": True,
    "q_group_size": 128,
    "w_bit": 4,
    "version": "GEMM",
}

model.quantize(tokenizer, quant_config=quant_config)
model.save_quantized("llama3-8b-awq-int4")
```

## 量化前後效能對比

```python
import torch

def benchmark_inference(model, input_ids, n=100):
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)

    torch.cuda.synchronize()
    start.record()
    for _ in range(n):
        model.generate(input_ids, max_new_tokens=128)
    end.record()
    torch.cuda.synchronize()

    latency = start.elapsed_time(end) / n
    print(f"平均延遲: {latency:.1f} ms")
    memory = torch.cuda.max_memory_allocated() / 1e9
    print(f"GPU 記憶體: {memory:.2f} GB")
```

## GPTQ vs AWQ 選擇

- **GPTQ**：成熟穩定，生態系支援最廣（exLlama、AutoGPTQ）
- **AWQ**：在 INT4 下通常保留略高的準確度，對邊緣裝置更友善
- **BitsAndBytes**：最簡單的 NF4 量化，適合快速原型開發

## 延伸閱讀

- [GPTQ 論文](https://www.google.com/search?q=GPTQ+quantization+paper)
- [AWQ 量化原理](https://www.google.com/search?q=AWQ+activation+aware+weight+quantization)
- [HuggingFace 量化指南](https://www.google.com/search?q=HuggingFace+model+quantization+guide)
