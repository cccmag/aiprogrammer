# Salesforce 與 CRM 雲端化

## Salesforce 概述

Salesforce 由 Marc Benioff 於 1999 年創立，是 SaaS CRM 的先驅。

### 發展歷程

- **1999 年**：公司成立
- **2004 年**：NYSE 上市
- **2005 年**：AppExchange 平台發布
- **2008 年**：Force.com 平台成熟

## Force.com 平台

### 平台架構

```
┌──────────────────────────────────────────┐
│           Force.com 平台                  │
├──────────────────────────────────────────┤
│                                          │
│  ┌────────────────────────────────────┐ │
│  │         應用程式層                   │ │
│  │  (Apex, Visualforce, API)          │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │         平台服務層                   │ │
│  │  (資料庫、工作流、安全)              │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │         基礎設施層                   │ │
│  │  (Heroku, AWS, 全球化)              │ │
│  └────────────────────────────────────┘ │
│                                          │
└──────────────────────────────────────────┘
```

## Apex 程式設計

### Apex 語法

```java
// 簡單的 Apex 類別
public class AccountHelper {
    public static void updateDescription(Id accountId) {
        Account acc = [SELECT Id, Name FROM Account WHERE Id = :accountId];
        acc.Description = 'Updated by Apex';
        update acc;
    }
}
```

### Apex 觸發器

```java
trigger AccountTrigger on Account (before insert, before update) {
    for (Account acc : Trigger.new) {
        if (acc.Name != null) {
            acc.Name = acc.Name.toUpperCase();
        }
    }
}
```

### SOQL 查詢

```java
// 查詢帳戶
List<Account> accounts = [SELECT Id, Name FROM Account WHERE Industry = 'Technology'];

// 關聯查詢
List<Contact> contacts = [SELECT Id, Name, Account.Name FROM Contact];
```

## Visualforce

### 頁面結構

```html
<apex:page controller="MyController">
    <apex:sectionHeader title="My Page" subtitle="Subtitle"/>
    <apex:form>
        <apex:inputField value="{!account.Name}"/>
        <apex:commandButton value="Save" action="{!save}"/>
    </apex:form>
</apex:page>
```

### Controller

```java
public class MyController {
    public Account account { get; set; }

    public PageReference save() {
        update account;
        return null;
    }
}
```

## AppExchange

### 元件市場

```bash
# 查詢 AppExchange 元件
# https://appexchange.salesforce.com/
```

## 雲端 CRM 的優勢

| 特性 | 傳統 CRM | Salesforce |
|------|----------|------------|
| 部署時間 | 月/季度 | 天/周 |
| 前期成本 | 高 | 低 |
| IT 需求 | 需要專職人員 | 最小 |
| 可訪問性 | 辦公室 | 任何地方 |
| 自動更新 | 需要升級項目 | 自動 |

## 結論

Salesforce 開創了雲端 CRM 的時代。Force.com 平台使得開發者能夠在雲端建立自訂應用。

---

**延伸閱讀**

- [SaaS 的興起與發展](focus1.md)
- [雲端平台架構](focus4.md)
- [Salesforce+Force.com](https://www.google.com/search?q=Salesforce+Force.com+platform)