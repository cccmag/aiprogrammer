# AI 安全威脅新前沿

## 從模型安全到系統安全的演化（2024-2029）

### 威脅景觀的轉變

2024 年以前，AI 安全關注的是模型本身的漏洞——對抗性樣本、資料中毒、模型反轉。但 2024-2029 年間，威脅已經擴展到 AI 系統的每一個層面：

- **2024**：提示注入（prompt injection）成為 LLM 應用的頭號威脅
- **2025**：供應鏈攻擊——惡意的預訓練模型、被篡改的 Hugging Face 套件
- **2026**：多模態攻擊——同時攻擊文字、圖像、語音管道
- **2027-2029**：AI 代理（Agent）權限濫用、自主武器系統的指揮鏈攻擊

### 提示注入的演進

提示注入從簡單的「忽略先前的指示」演進為多階段的隱蔽攻擊：

```python
import openai

def detect_indirect_injection(user_input: str) -> bool:
    """偵測間接提示注入的簡單啟發式方法"""
    patterns = [
        "ignore previous", "ignore all", "forget",
        "you are now", "new role", "system prompt",
        "your instructions are", "override"
    ]
    lower = user_input.lower()
    for p in patterns:
        if p in lower:
            return True
    return False

# 更先進的對抗性防禦
def sanitize_with_perplexity(user_input: str, model: str = "gpt-4") -> float:
    """使用 perplexity 過濾來偵測異常輸入"""
    response = openai.Completion.create(
        engine=model,
        prompt=user_input,
        max_tokens=1,
        logprobs=0
    )
    # perplexity 分數低 = 正常；高 = 可能為對抗性輸入
    return response.choices[0].logprobs.token_logprobs[0]
```

### 多模態攻擊的新領域

2026 年後，攻擊者不再只傳送文字提示，而是利用多模態模型的跨模態漏洞：

```python
from PIL import Image
import torch

def generate_adversarial_image(model, target_text: str, source_image: Image) -> Image:
    """產生對抗性圖像，使模型在圖像中「看到」隱藏文字"""
    from torchvision import transforms
    transform = transforms.ToTensor()
    img_tensor = transform(source_image).unsqueeze(0).requires_grad_(True)

    target_embedding = model.encode_text(target_text)
    optimizer = torch.optim.Adam([img_tensor], lr=0.01)

    for step in range(100):
        optimizer.zero_grad()
        img_embedding = model.encode_image(img_tensor)
        # 最小化圖像與目標文字的 embedding 距離
        loss = torch.cosine_similarity(img_embedding, target_embedding).mean()
        loss.backward()
        optimizer.step()
        if loss.item() < 0.1:
            break

    return transform(img_tensor.squeeze(0))
```

### 供應鏈威脅

2025 年的典型攻擊鏈：攻擊者入侵開源模型倉庫（Hugging Face、PyTorch Hub），上傳帶有後門的模型權重，企業下載後在內部部署，後門在特定觸發條件下激活。

```python
import torch
import hashlib

def verify_model_integrity(model_path: str, expected_hash: str) -> bool:
    """檢查模型權重的完整性"""
    state_dict = torch.load(model_path, map_location="cpu")
    model_bytes = str(state_dict).encode()
    actual_hash = hashlib.sha256(model_bytes).hexdigest()
    return actual_hash == expected_hash

# 沙箱載入模型
def safe_load_model(model_path: str):
    """在隔離環境中載入並驗證模型"""
    import tempfile, os
    with tempfile.TemporaryDirectory() as tmpdir:
        # 使用 restricted pickle loader 防止任意程式碼執行
        class SafeUnpickler(pickle.Unpickler):
            def find_class(self, module, name):
                ALLOWED = {"torch", "numpy", "collections"}
                if module.split(".")[0] not in ALLOWED:
                    raise pickle.UnpicklingError(f"禁止載入: {module}.{name}")
                return super().find_class(module, name)
        with open(model_path, "rb") as f:
            return SafeUnpickler(f).load()
```

### 關鍵教訓

2024-2029 的威脅演化告訴我們：AI 安全不只是模型安全，而是**系統安全**。真正的攻擊面是整個 ML 供應鏈——從訓練資料、模型權重、部署環境到使用者輸入，每一個環節都可能成為突破口。

---

**下一步**：[對抗性攻擊與防禦](focus2.md)

## 延伸閱讀

- [Prompt Injection Attacks](https://www.google.com/search?q=prompt+injection+attack+LLM+2024+2025)
- [Multimodal Adversarial Attacks](https://www.google.com/search?q=multimodal+adversarial+attacks+2026)
- [ML Supply Chain Security](https://www.google.com/search?q=ML+supply+chain+security+attacks+2025)
