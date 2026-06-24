# 6. 依賴管理與環境重現

## 依賴管理的挑戰

Python 依賴管理複雜的原因在於：依賴鏈可能非常深，A 依賴 B，B 依賴 C 與 D，C 又依賴 E。任何一層的版本變化都可能導致程式行為改變。確保環境在不同時間、不同機器上能完全重現，是建置可靠系統的關鍵。

## 語意化版本（Semantic Versioning）

Python 套件遵循語意化版本：`major.minor.patch`

- **Major**（破壞性更新）：API 不相容
- **Minor**（功能新增）：向後相容
- **Patch**（修正）：向後相容

```toml
# 語意化版本範例
package = "^1.2.3"    # >=1.2.3, <2.0.0  (相當於 ~1.2)
package = "~1.2.3"    # >=1.2.3, <1.3.0
package = ">=1.2.3"    # >=1.2.3
package = "==1.2.3"   # 完全相等
```

## 環境重現策略

### 1. 使用鎖定檔案

```bash
# pip-tools
pip-compile requirements.in
pip-sync requirements.txt

# Poetry
poetry lock
poetry install

# Pipenv
pipenv lock
pipenv sync
```

### 2. Docker 化

Docker 確保應用程式在任何環境都能一致執行：

```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### 3. Nix 環境

Nix 提供了更徹底的可重現性保証：

```nix
# shell.nix
with import <nixpkgs> {};
mkShell {
  buildInputs = [
    python38
    python38Packages.numpy
    python38Packages.pandas
  ];
}
```

## 依賴解析衝突

當相依版本發生衝突時，需要手動解決：

```toml
# Poetry 中明確指定版本
[tool.poetry.dependencies]
requests = "^2.22"
urllib3 = "1.25.8"
```

## 開發 vs 生產依賴

```bash
# 只在開發環境安裝
poetry add pytest --dev
pipenv install pytest --dev

# 生產環境不安裝 dev 依賴
poetry install --no-dev
pipenv install --prod
```

## 安全性

```bash
# 檢查已知漏洞
pip install safety
safety check

# pip-audit（更完整）
pip install pip-audit
pip-audit
```

## 依賴審查

```bash
# 顯示依賴樹
pip install pipdeptree
pipdeptree

# 檢查過時套件
pip list --outdated
```

## 參考資源

- https://www.google.com/search?q=Python+dependency+management+reproducible+environment+2020
- https://www.google.com/search?q=Python+requirements+lock+reproducibility+best+practices
- https://www.google.com/search?q=Python+security+audit+dependency+vulnerability+pip+2020