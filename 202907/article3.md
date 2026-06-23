# 供應鏈安全實踐

## 前言

AI 系統的建構高度依賴第三方套件與預訓練模型，從 PyPI 套件到 Hugging Face 模型庫，每一環都可能成為攻擊鏈的一環。2025 年發生的多起供應鏈攻擊事件（如惡意 PyPI 套件植入後門），凸顯了 AI 供應鏈安全的迫切性。

## 依賴管理

建立完整且可驗證的依賴清單（SBOM, Software Bill of Materials）是供應鏈安全的起點：

```python
import hashlib
import json

def generate_sbom(packages):
    sbom = {"packages": []}
    for name, version, content in packages:
        sha = hashlib.sha256(content).hexdigest()
        sbom["packages"].append({
            "name": name, "version": version, "sha256": sha
        })
    return json.dumps(sbom, indent=2)
```

## 模型來源驗證

使用數位簽章與完整性校驗確保模型檔案未被篡改：

```python
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

def verify_model_signature(model_path, signature_path, public_key_path):
    with open(public_key_path, "rb") as f:
        pub = serialization.load_pem_public_key(f.read())
    with open(model_path, "rb") as f:
        model_data = f.read()
    with open(signature_path, "rb") as f:
        signature = f.read()
    pub.verify(signature, model_data, ec.ECDSA(hashes.SHA256()))
```

## 自動化安全掃描

將依賴掃描整合進 CI/CD pipeline，使用 `pip-audit`、`safety` 等工具自動檢查已知漏洞，並在偵測到高風險套件時阻止部署。參考 [https://www.google.com/search?q=AI+supply+chain+security+2026](https://www.google.com/search?q=AI+supply+chain+security+2026) 獲取最新工具資訊。
