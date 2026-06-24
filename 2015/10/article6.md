# 重構壞味道程式碼

## 前言

壞味道是程式碼中潛在的問題指標。識別並修復壞味道是維持程式碼品質的關鍵。

## 常見壞味道

### 1. 重複程式碼（Duplicated Code）

**徵兆**：同樣的程式碼出現多次

**修復**：提取為公共函數或類別

```python
# 重構前
if user.type == "premium":
    send_email(user.email, "Premium offer")
    update_report("premium_email_sent")

if user.type == "premium":
    send_sms(user.phone, "Premium offer")
    update_report("premium_sms_sent")

# 重構後
def notify_premium_user(user, channel):
    if channel == "email":
        send_email(user.email, "Premium offer")
    elif channel == "sms":
        send_sms(user.phone, "Premium offer")
    update_report(f"premium_{channel}_sent")
```

### 2. 過長函數（Long Method）

**徵兆**：函數超過一頁螢幕

**修復**：分解為多個小函數

### 3. 過大類別（Large Class）

**徵兆**：類別承擔過多職責

**修復**：拆分為多個專門類別

### 4. 霰彈式修改（Shotgun Surgery）

**徵兆**：修改一個功能需要改多個檔案

**修復**：移動相關功能到同一個地方

### 5. 依賴過多（Feature Envy）

**徵兆**：類別方法過度使用另一個類別的資料

**修復**：移動方法到資料所屬的類別

## 重構步驟

1. **識別壞味道**：了解常見的壞味道類型
2. **撰寫測試**：確保有測試覆蓋
3. **小步伐進行**：每次只做一個改變
4. **測試驗證**：每次改變後執行測試
5. **提交程式碼**：每次成功的重構都是獨立的 commit

## 小結

定期識別和修復壞味道是保持程式碼健康的關鍵實踐。

---

## 延伸閱讀

- [Code Smell Catalog](https://www.google.com/search?q=code+smell+catalog)
- [Refactoring Techniques](https://www.google.com/search?q=refactoring+techniques+martin+fowler)