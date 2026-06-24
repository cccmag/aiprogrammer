# SaaS 架構設計模式

## 多租戶模式

```python
# 多租戶資料隔離
def get_tenant_data(tenant_id):
    return f"SELECT * FROM data WHERE tenant_id = {tenant_id}"
```

## 微服務

```python
# 微服務架構
services = ['user-service', 'order-service', 'payment-service']
```

## 結論

SaaS 架構需要考慮可擴展性和成本效益。

---

**延伸閱讀**

- [雲端平台架構](focus4.md)