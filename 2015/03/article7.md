# SQL 注入攻擊防護

## 前言

SQL 注入是最常見的 Web 安全漏洞之一，本篇介紹防護方法。

## 攻擊原理

```sql
-- 恶意輸入
' OR '1'='1

-- 產生的查詢
SELECT * FROM users WHERE name = '' OR '1'='1';
-- 結果：繞過認證
```

## 防護方法

### 參數化查詢

```javascript
// Node.js + PostgreSQL
const query = 'SELECT * FROM users WHERE id = $1';
const result = await pool.query(query, [userId]);

// Node.js + MySQL
const query = 'SELECT * FROM users WHERE id = ?';
const result = await pool.query(query, [userId]);
```

### 儲存程序

```sql
-- 儲存程序自動處理參數
CREATE OR REPLACE FUNCTION get_user(p_id INTEGER)
RETURNS TABLE(id INTEGER, name TEXT) AS $$
BEGIN
    RETURN QUERY SELECT id, name FROM users WHERE id = p_id;
END;
$$ LANGUAGE plpgsql;
```

### ORM

```javascript
// Sequelize
const user = await User.findById(userId);

// Mongoose
const user = await User.findById(userId);
```

## 最佳實踐

```
安全清單：
──────────
□ 總是使用參數化查詢
□ 最小權限原則
□ 輸入驗證
□ 錯誤訊息不暴露細節
□ 定期安全審計
```

---

## 延伸閱讀

- [SQL Injection Prevention](https://www.google.com/search?q=SQL+injection+prevention+OWASP)

---

*本篇文章為「AI 程式人雜誌 2015 年 3 月號」文章之一。*