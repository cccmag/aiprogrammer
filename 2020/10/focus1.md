# pip 與 PyPI 的生態系：Python 套件管理與依賴地獄

## PyPI：Python 的大本營

### PyPI 的歷史

PyPI（Python Package Index）是 Python 語言的官方套件儲存庫，由 Python Packaging Authority (PyPA) 維護。PyPI 於 2003 年上線，至今已成為 Python 生態系的核心基礎設施。

```
PyPI 規模（2020 年）：
────────────────────────────────
套件數量：  27 萬+
總版本數：  30 萬+
月下載量：  10 億+
志願者：    數十位 PyPA 成員
```

任何人都可以將自己的 Python 套件上傳到 PyPI，讓全球的 Python 開發者使用。這種開放的模式極大地促進了 Python 生態系的繁榮發展。

### 如何使用 pip

pip 是 PyPI 的官方用戶端，以下是一些基本操作：

```bash
# 安裝套件
pip install requests

# 安裝特定版本
pip install "requests>=2.25.0,<3.0"

# 從 requirements.txt 安裝
pip install -r requirements.txt

# 列出已安裝的套件
pip list

# 顯示套件資訊
pip show requests

# 升級套件
pip install --upgrade requests

# 卸載套件
pip uninstall requests
```

## 依賴地獄

### 什麼是依賴地獄？

當專案依賴多個套件，而這些套件又依賴不同版本的共同庫時，就會產生所謂的「依賴地獄」：

```
專案需求：
    mypackage 需要 A>=2.0
    A 需要 B>=1.0
    C 需要 B>=2.0

問題：
    B>=1.0 和 B>=2.0 不相容！
    最終導致安裝失敗或執行時錯誤
```

### pip 的依賴解析

pip 20.2 之前，pip 使用貪心演算法解析依賴，經常導致衝突。20.2 版本開始，pip 採用了新的解析器，更加嚴格和可預測：

```bash
# pip 20.2+ 的依賴解析
# 會嚴格檢查所有依賴關係
pip install "django>=3.0"

# 如果出現衝突，會明確報告
# ERROR: Cannot install X because these package versions have conflicting dependencies.
```

### 解決依賴衝突的策略

**策略一：使用虛擬環境**

```bash
# 每個專案使用獨立的虛擬環境
python -m venv project1-env
source project1-env/bin/activate
pip install -r requirements.txt
```

**策略二：鎖定依賴版本**

```bash
# 使用 pip-tools 產生鎖定檔案
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

**策略三：使用較寬鬆的版本約束**

```text
# requirements.txt
# 不要寫得太嚴格
requests>=2.20
flask>=1.0
numpy>=1.15
```

## 私有套件庫

### 為什麼需要私有套件庫？

- 儲存公司內部專用的程式碼
- 保護敏感的商業邏輯
- 控制依賴的版本和安全性

### 建立私有 PyPI

可以使用 pip 的 `--index-url` 參數指定私有倉庫：

```bash
# 使用私有套件庫
pip install mypackage --index-url https://my-private-pypi.com/simple/
```

常用的私有 PyPI 解決方案：
- **pypiserver**：輕量級的私有 PyPI 伺服器
- **Artifactory**：JFrog 的通用套件管理
- **AWS CodeArtifact**：AWS 的托管套件服務

### PyPI 安全性

2020 年，Python 社群加強了對 PyPI 安全性的關注：

- **雙因素認證**：PyPA 推動套件維護者啟用 2FA
- **惡意套件檢測**：自動化系統監測可疑的套件上傳
- **簽名驗證**：鼓勵套件作者對發行版進行 GPG 簽名

```bash
# 驗證套件簽名
pip download --verify-signatures requests
```

## 延伸閱讀

- [PyPI 官方網站](https://www.google.com/search?q=Python+Package+Index+PyPI+official)
- [pip 文件](https://www.google.com/search?q=pip+Python+package+manager+documentation)
- [Python Packaging User Guide](https://www.google.com/search?q=Python+packaging+user+guide+PyPA)
- [pip-tools 使用指南](https://www.google.com/search?q=pip-tools+Python+dependency+locking)
- [建立私有 PyPI](https://www.google.com/search?q=private+PyPI+server+setup+python)

---

*本篇文章為「AI 程式人雜誌 2020 年 10 月號」歷史回顧系列之一。*