# 模型量化與部署：將 LLM 放到生產環境

## 前言

將大型語言模型部署到生產環境涉及大量工程挑戰：如何在有限的 GPU 記憶體中運行數百億參數的模型？如何達到可接受的推論延遲？如何管理成本？這些問題在 2027 年的今天仍然沒有銀彈解法，但一系列成熟的工具與方法已經讓部署流程大幅簡化。本文將深入探討模型量化、部署框架與生產化最佳實務，幫助讀者將 LLM 從研究環境順利遷移到生產系統。

## 模型量化原理

量化是將模型權重從高精度（如 FP16）映射到低精度（如 INT4、INT8）的過程。你可以把量化想像成壓縮圖片：一張 4K 照片壓縮成 1080p 後，肉眼可能看不出差異，但檔案大小減少許多。同樣地，LLM 的權重量化後，模型體積大幅縮減，推論速度加快，而能力損失往往在可接受的範圍內。以 INT4 量化為例，參數大小從 16-bit 降至 4-bit，記憶體需求減少 75%，這意味著原本需要 80GB 記憶體的 70B 模型，量化後僅需 20GB，讓單張消費級 GPU 也能運行。

### 量化誤差

量化必然引入資訊損失。想像你有一個精確到小數點後十位的數字，現在只能保留整數部分——這就是量化造成的精度損失。不過，LLM 的權重分佈通常具有一定的冗餘性，許多參數的微小變化對最終輸出影響不大。透過校準資料集（calibration dataset）來最小化量化誤差，可以讓模型在壓縮後仍保持接近原始水準的表現。關鍵是要選擇與實際使用場景相近的校準資料，例如若是程式碼模型，就應該用程式碼片段進行校準。

```python
import torch

def quantize_tensor(tensor, bits=4):
    """對張量進行對稱量化"""
    qmin = -(2 ** (bits - 1))
    qmax = 2 ** (bits - 1) - 1
    scale = tensor.abs().max() / qmax
    quantized = torch.round(tensor / scale).clamp(qmin, qmax)
    return quantized, scale

# 比較量化前後
original = torch.randn(1000) * 2.0
quantized, scale = quantize_tensor(original, bits=4)
dequantized = quantized * scale
mse = ((original - dequantized) ** 2).mean()
print(f"量化 MSE：{mse:.6f}")
```

## 主要量化方法

### GPTQ（GPU 後訓練量化）

GPTQ 使用 Hessian 矩陣進行權重校正，是目前 GPU 上最流行的量化方法：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM

model_name = "Qwen/Qwen2.5-7B-Instruct"

# 量化模型
model = AutoGPTQForCausalLM.from_pretrained(
    model_name,
    quantize_config=dict(
        bits=4,
        group_size=128,
        desc_act=False,  # 是否按行量化
        damp_percent=0.01,
    ),
    dataset="c4",  # 校準資料集
)

model.save_quantized("./qwen-4bit-gptq")

# 載入量化模型推論
quantized_model = AutoGPTQForCausalLM.from_quantized(
    "./qwen-4bit-gptq",
    device="cuda:0",
    use_triton=True  # Triton 加速
)
```

### GGUF（CPU/混合部署）

GGUF 是 llama.cpp 使用的量化格式，支援純 CPU 或 CPU+GPU 混合推論：

```bash
# 使用 llama.cpp 量化
# 1. 安裝 llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# 2. 將 HuggingFace 模型轉換為 GGUF
python convert_hf_to_gguf.py --outfile model.gguf \
    --outtype q4_k_m --model /path/to/model

# 3. 推論
./main -m model.gguf -p "什麼是深度學習？" -n 256
```

### AWQ（啟動感知量化）

AWQ 根據啟動值的分佈進行量化，保留對輸出影響較大的權重：

```python
from awq import AutoAWQForCausalLM

model = AutoAWQForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-Instruct-v0.3"
)
tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.3")

# 量化
model.quantize(
    tokenizer,
    quant_config={"zero_point": True, "q_group_size": 128, "w_bit": 4}
)
model.save_quantized("mistral-awq-4bit")
```

## 高效推論框架

### vLLM

vLLM 是目前最快的開源推論引擎，核心技術是 PagedAttention：

```python
from vllm import LLM, SamplingParams

# 啟動模型
llm = LLM(
    model="meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=1,   # 多 GPU 分佈
    dtype="float16",
    gpu_memory_utilization=0.9,
    max_model_len=8192,
)

sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=512,
)

# 批次推論
prompts = ["解釋注意力機制", "什麼是梯度下降？"]
outputs = llm.generate(prompts, sampling_params)
for output in outputs:
    print(output.outputs[0].text)
```

### llama.cpp

適合 CPU 或混合部署情境：

```python
from llama_cpp import Llama

llm = Llama(
    model_path="./models/llama-3.1-8b-q4_k_m.gguf",
    n_ctx=4096,
    n_threads=8,
    n_gpu_layers=35,  # GPU 加速層數（-1 為全部）
)

output = llm(
    "Q: 什麼是 Transformer？ A:",
    max_tokens=256,
    temperature=0.7,
    echo=True,
)
print(output["choices"][0]["text"])
```

## 生產環境部署

### API 設計（FastAPI）

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time

app = FastAPI()
# 全域載入模型（啟動時載入一次）
llm = LLM(model="Qwen/Qwen2.5-7B-Instruct")

class ChatRequest(BaseModel):
    messages: list
    temperature: float = 0.7
    max_tokens: int = 512

class ChatResponse(BaseModel):
    response: str
    latency_ms: float

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    start = time.time()
    try:
        prompt = tokenizer.apply_chat_template(
            request.messages, tokenize=False
        )
        outputs = llm.generate(
            [prompt],
            SamplingParams(
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
        )
        latency = (time.time() - start) * 1000
        return ChatResponse(
            response=outputs[0].outputs[0].text,
            latency_ms=latency
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 啟動：uvicorn main:app --host 0.0.0.0 --port 8000
```

### 監控與日誌

```python
import logging
from prometheus_client import Counter, Histogram

# Prometheus 指標
REQUEST_COUNT = Counter("llm_requests_total", "總請求數")
LATENCY = Histogram("llm_latency_seconds", "推論延遲")
TOKEN_COUNT = Histogram("llm_tokens_generated", "生成的 Token 數")

def monitored_generate(prompt, sampling_params):
    REQUEST_COUNT.inc()
    with LATENCY.time():
        outputs = llm.generate([prompt], sampling_params)
    TOKEN_COUNT.observe(len(outputs[0].outputs[0].token_ids))
    return outputs
```

## 多 GPU 擴展

```bash
# vLLM 多 GPU 推論（tensor parallelism）
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --dtype bfloat16 \
    --port 8000
```

## 成本最佳化

| 策略 | 效果 | 取捨 |
|------|------|------|
| INT4 量化 | 記憶體減少 75% | 品質略微下降 |
| KV Cache 量化 | 長上下文記憶體減半 | 實作複雜度 |
| 連續批次 | 吞吐量提升 10-20x | 延遲略有增加 |
| Speculative Decoding | 推論速度提升 2-3x | 需要 draft model |

## 參考資源

- [vLLM 官方文件](https://www.google.com/search?q=vllm+pagedattention+documentation)
- [llama.cpp 專案](https://www.google.com/search?q=llama.cpp+github+gguf)
- [GPTQ 論文](https://www.google.com/search?q=GPTQ+accurate+post+training+quantization)
- [AWQ 量化方法](https://www.google.com/search?q=AWQ+activation+aware+weight+quantization)
