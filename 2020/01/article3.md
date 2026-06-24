# pip install 進階用法

## 版本指定語法

```bash
# 精確版本
pip install requests==2.22.0

# 範圍版本
pip install "requests>=2.22.0,<3.0"

# 相容版本（PEP 440）
pip install "requests~=2.22.0"  # >=2.22.0, ==2.*

# 預發布版
pip install --pre requests

# 從 git
pip install git+https://github.com/psf/requests.git
pip install git+https://github.com/psf/requests.git@v2.22.0
```

## 離線安裝

```bash
# 下載套件到本地目錄
pip download -r requirements.txt -d ./packages

# 無網路安裝
pip install --no-index --find-links=./packages -r requirements.txt
```

## 私人 PyPI

```bash
# 使用私人 PyPI
pip install --index-url=https://my-private-pypi.com/simple package

# 多個來源
pip install \
    --index-url=https://my-private-pypi.com/simple \
    --trusted-host=my-private-pypi.com \
    package

# 或使用 pip.conf
# ~/.config/pip/pip.conf (Linux)
# ~/Library/Application Support/pip/pip.conf (macOS)
```

## 環境指定

```bash
# 安裝到使用者目錄（不需要 sudo）
pip install --user package

# 安裝到指定路徑
pip install --target=./lib package
```

## wheels 與原始碼

```bash
# 只使用 wheel（不下載原始碼）
pip install --only-binary=:all: package

# 只使用原始碼（不下載 wheel）
pip install --only-source=:all: package
```

## 驗證與安全

```bash
# 檢查已安裝套件的安全性
pip install safety
safety check

# 列出可升級的套件
pip list --outdated

# 升級到最新版本
pip install --upgrade package_name
```

## pip-tools

```bash
pip install pip-tools

# requirements.in（只列直接相依）
echo "flask>=1.1" > requirements.in
echo "requests>=2.22" >> requirements.in

# 編譯成鎖定檔案
pip-compile requirements.in

# 安裝已鎖定的相依
pip-sync requirements.txt
```

## 參考資源

- https://www.google.com/search?q=pip+install+tutorial+advanced+options+2020
- https://www.google.com/search?q=pip+offline+install+private+package+Python+2020
- https://www.google.com/search?q=pip-tools+pip-compile+dependency+lock+Python+guide