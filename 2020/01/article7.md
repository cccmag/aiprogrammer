# requirements.txt 管理策略

## 基本格式

```txt
# requirements.txt
requests>=2.22.0
flask>=1.1.0
numpy>=1.17.0
```

## 嚴格版本鎖定

```txt
# requirements.txt（精確版本）
requests==2.22.0
flask==1.1.1
```

## 分離 dev 與 production

```txt
# requirements.txt（生產環境）
flask>=1.1.0
gunicorn>=19.9.0

# requirements-dev.txt（開發環境）
-r requirements.txt
pytest>=5.2.0
black>=19.0.0
flake8>=3.7.0
```

## 使用 pip-tools 鎖定

```bash
pip install pip-tools

# requirements.in
flask>=1.1
requests>=2.22

# 編譯成 locked 版本
pip-compile requirements.in

# 這會生成 requirements.txt，鎖定所有相依版本
```

## 多環境設定

```txt
# requirements.txt
-r requirements-base.txt
-r requirements-dev.txt
```

## 自動產生

```bash
# 從環境匯出
pip freeze > requirements.txt

# 使用 pipreqs（只包含實際使用的套件）
pip install pipreqs
pipreqs . --force
```

## 版本規範

```txt
# 精確版本
package==1.2.3

# 範圍
package>=1.2.0,<2.0

# 相容版本
package~=1.2.0

# 不指定版本（最新）
package
```

## 最佳實踐

1. 永遠 commit requirements.txt 到版本控制
2. 使用 `--no-deps` 安裝不需要相依的套件
3. 定期執行 `pip-compile --upgrade` 更新依賴

## 參考資源

- https://www.google.com/search?q=requirements.txt+best+practices+Python+2020
- https://www.google.com/search?q=pip-tools+pip-compile+lock+dependencies+Python
- https://www.google.com/search?q=Python+requirements+management+dev+prod+separation