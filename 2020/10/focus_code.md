# pip 與虛擬環境實戰

## 前言

pip 和虛擬環境是 Python 部署的基礎設施。本篇文章將帶來實戰性的操作指南，幫助讀者掌握 Python 套件管理的核心技能。

---

## 原始碼

完整的實作範例請參考：[_code/pip_demo.py](_code/pip_demo.py)

```python
#!/usr/bin/env python3
"""pip 與虛擬環境實戰範例"""

import subprocess
import sys
import os
from pathlib import Path

def demo():
    print("=" * 60)
    print("pip 與虛擬環境實戰")
    print("=" * 60)

    print("\n1. pip 基本操作")
    print("-" * 40)
    print("pip --version:", subprocess.check_output([sys.executable, "-m", "pip", "--version"]).decode().strip())
    print("pip list (前 5 個):", end=" ")
    result = subprocess.check_output([sys.executable, "-m", "pip", "list", "--format=freeze"]).decode()
    packages = result.strip().split('\n')[:5]
    print('\n  '.join(packages))

    print("\n2. 建立虛擬環境")
    print("-" * 40)
    venv_path = Path("./demo_venv")
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
        print(f"虛擬環境已建立: {venv_path}")
    else:
        print(f"虛擬環境已存在: {venv_path}")

    print("\n3. 隔離環境中的套件")
    print("-" * 40)
    print("在虛擬環境中安裝 requests:")
    pip_executable = venv_path / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
    subprocess.run([str(pip_executable), "install", "requests"], capture_output=True)
    print("requests 安裝成功！")

    print("\n4. requirements.txt 檔案")
    print("-" * 40)
    requirements_file = Path("requirements_demo.txt")
    requirements_file.write_text("requests>=2.25.0\nflask>=1.1.0\n")
    print(f"已建立 {requirements_file}:")
    print(requirements_file.read_text())

    print("\n5. 清理")
    print("-" * 40)
    import shutil
    if venv_path.exists():
        shutil.rmtree(venv_path)
        print(f"已清理虛擬環境: {venv_path}")
    if requirements_file.exists():
        requirements_file.unlink()
        print(f"已清理: {requirements_file}")

    print("\n" + "=" * 60)
    print("實戰完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()
```

---

## 常用指令速查表

### pip 基本指令

```bash
# 安裝套件
pip install requests                    # 安裝最新版本
pip install requests==2.25.0           # 安裝指定版本
pip install "requests>=2.20"           # 安裝滿足條件的版本
pip install -r requirements.txt         # 從檔案安裝

# 檢視和管理
pip list                                # 列出已安裝的套件
pip show requests                       # 顯示套件資訊
pip freeze > requirements.txt           # 導出當前環境的套件清單

# 卸載和升級
pip uninstall requests                  # 卸載套件
pip install --upgrade requests          # 升級套件
pip install --upgrade pip               # 升級 pip 本身
```

### 虛擬環境指令

```bash
# 建立環境
python -m venv myenv                    # 建立名為 myenv 的環境

# 啟動環境
source myenv/bin/activate               # Linux/macOS
myenv\Scripts\activate                  # Windows

# 停用環境
deactivate

# 其他工具
pip install virtualenv                  # 安裝 virtualenv
mkvirtualenv myenv                     # 使用 virtualenvwrapper
pipenv install                          # 使用 Pipenv
poetry install                          # 使用 Poetry
```

### requirements.txt 格式

```
# 固定版本
requests==2.25.0
flask==1.1.2

# 版本範圍
numpy>=1.19.0,<2.0
pandas~=1.1.0

# 特殊標記
-e git+https://github.com/user/repo.git#egg=package
./local_package
```

---

## 實戰技巧

### 1. 使用虛擬環境隔離專案

```bash
# 建立專案時，先建立虛擬環境
mkdir myproject && cd myproject
python -m venv venv

# 啟動並安裝依賴
source venv/bin/activate
pip install -r requirements.txt

# 開始開發
python main.py

# 開發完成後停用
deactivate
```

### 2. 導出乾淨的依賴清單

```bash
# 只導出直接安裝的套件（不包含傳遞依賴）
pip list --not-required --format=freeze > requirements.txt

# 或使用 pip-tools
pip install pip-tools
pip-compile requirements.in
```

### 3. 使用 pip-chill 簡化輸出

```bash
pip install pip-chill
pip-chill > requirements.txt
```

### 4. 本地快取加速安裝

```bash
# 使用本地震著快取
pip install --cache-dir ./pip-cache -r requirements.txt

# 清除快取
pip cache purge
```

---

## 延伸閱讀

- [pip 官方文件](https://www.google.com/search?q=pip+Python+package+manager+documentation)
- [Python venv 模組](https://www.google.com/search?q=Python+venv+module+tutorial)
- [pip-tools 使用指南](https://www.google.com/search?q=pip-tools+Python+dependency)
- [Pipenv vs Poetry vs venv](https://www.google.com/search?q=Pipenv+vs+Poetry+vs+venv+2020)

---

*本期程式實作到此結束。*