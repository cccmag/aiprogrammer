# pip 進階使用

## 依賴鎖定

在 AI 專案中，套件版本的精確控制至關重要。稍微不同的套件版本可能導致訓練結果無法重現。

```bash
# 精準鎖定所有套件版本
pip freeze > requirements.txt

# 安裝時嚴格比對
pip install -r requirements.txt
```

使用 `pip-tools` 可以更精細地管理依賴關係，將頂層依賴與傳遞性依賴分離：

```bash
# 安裝 pip-tools
pip install pip-tools

# 撰寫 requirements.in（只列頂層依賴）
echo "torch>=2.0" > requirements.in
echo "transformers" >> requirements.in
echo "datasets" >> requirements.in

# 編譯出完整依賴樹（包含傳遞性依賴的鎖定版本）
pip-compile requirements.in  # 產出 requirements.txt

# 同步目前環境與 requirements.txt
pip-sync requirements.txt
```

## 離線安裝

在無法連網的環境中（如內網伺服器），可提前下載所有套件：

```bash
# 下載套件及其依賴到本地目錄
pip download -d ./packages -r requirements.txt

# 離線安裝
pip install --no-index --find-links=./packages -r requirements.txt
```

## 私有套件源

企業內部可搭建私有 PyPI 伺服器，存放自訂套件：

```bash
# 安裝時指定額外索引
pip install my-private-pkg --extra-index-url https://pypi.mycompany.com/simple
```

也可以在 `~/.pip/pip.conf` 中設定：

```ini
[global]
extra-index-url = https://pypi.mycompany.com/simple
trusted-host = pypi.mycompany.com
```

## pip 快取管理

```bash
# 查看快取大小與統計
pip cache info

# 清除特定套件快取
pip cache remove torch

# 清除所有快取
pip cache purge
```

## 疑難排解

```bash
# 查看完整的依賴樹
pip install pipdeptree
pipdeptree

# 強制重新安裝（跳過快取）
pip install --force-reinstall --no-cache-dir torch
```

## 參考資源

- https://www.google.com/search?q=pip+tools+compile+dependencies+lock+file+Python
- https://www.google.com/search?q=pip+offline+install+download+dependencies+no+internet
- https://www.google.com/search?q=pip+private+package+index+extra+index+url+setup
