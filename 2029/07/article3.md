# 供應鏈安全實踐

## 概述

AI 供應鏈安全涵蓋從資料收集、模型訓練到部署的每個環節。惡意套件、中毒資料、不安全的第三方模型都可能成為攻擊突破口。

## 依賴套件安全檢查

使用 SBOM（Software Bill of Materials）管理依賴：

```python
import json
import subprocess
from packaging.version import Version

def generate_sbom(project_dir):
    result = subprocess.run(
        ["pip-licenses", "--format=json"],
        capture_output=True, text=True
    )
    packages = json.loads(result.stdout)
    sbom = {
        "packages": [
            {"name": p["Name"],
             "version": p["Version"],
             "license": p["License"]}
            for p in packages
        ]
    }
    with open(f"{project_dir}/sbom.json", "w") as f:
        json.dump(sbom, f, indent=2)
    return sbom
```

## 模型來源驗證

使用密碼學簽章驗證模型完整性：

```python
import hashlib
import hmac

def verify_model_signing(model_path, expected_hash, secret):
    with open(model_path, "rb") as f:
        content = f.read()
    actual_hash = hmac.new(
        secret.encode(), content, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(actual_hash, expected_hash)
```

## 資料中毒防禦

在訓練管線中嵌入異常檢測：

```python
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_poisoned_samples(features, labels, contamination=0.01):
    clf = IsolationForest(contamination=contamination,
                          random_state=42)
    outliers = clf.fit_predict(features)
    clean_idx = np.where(outliers == 1)[0]
    print(f"移除 {np.sum(outliers == -1)} 個可疑樣本")
    return features[clean_idx], labels[clean_idx]
```

## 容器映像安全掃描

```python
def scan_container_image(image_name):
    result = subprocess.run(
        ["trivy", "image", "--format", "json", image_name],
        capture_output=True, text=True
    )
    vulns = json.loads(result.stdout)
    critical = [v for v in vulns.get("Results", [])
                if v.get("Severity") == "CRITICAL"]
    return critical
```

## CI/CD 安全整合

```python
def pipeline_security_check():
    checks = [
        ("SBOM", generate_sbom(".")),
        ("Dependency Audit",
         subprocess.run(["pip", "audit"], capture_output=True)),
        ("Model Signature",
         verify_model_signing("model.bin", "", os.getenv("SECRET"))),
    ]
    for name, passed in checks:
        if not passed:
            raise RuntimeError(f"{name} 檢查失敗")
    print("供應鏈安全檢查通過")
```

參考資料：https://www.google.com/search?q=AI+supply+chain+security+best+practices+2026
