# 開源 PaaS 的比較

## 前言

2015 年有多個開源 PaaS 平台可供選擇，讓開發者能夠輕鬆部署 Node.js 應用。

## 平台比較

### Heroku

```
優點：易用、支援多種語言、生態系成熟
缺點：昂貴、對應用大小有限制
```

### OpenShift

```
優點：Red Hat 支援、彈性自托管
缺點：設定較複雜
```

### Dokku

```
優點：極簡單、超過 Heroku 相容
缺點：需自行管理伺服器
```

## Dokku 部署

```bash
# 安裝
wget https://raw.githubusercontent.com/dokku/dokku/v0.3.18/bootstrap.sh
sudo DOKKU_TAG=v0.3.18 bash bootstrap.sh

# 建立應用
dokku apps:create myapp

# 部署
git remote add dokku dokku@myserver:myapp
git push dokku master
```

---

## 延伸閱讀

- [開源 PaaS 比較](https://www.google.com/search?q=open+source+PaaS+heroku+alternative+2015)

---

*本篇文章為「AI 程式人雜誌 2015 年 2 月號」文章之一。*