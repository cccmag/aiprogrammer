# AIML 與 Alice 機器人

## 從 ELIZA 到 ALICE

1995 年，Richard Wallace 博士發布了 ALICE（Artificial Linguistic Internet Computer Entity），這是 ELIZA 之後最具影響力的基於規則的聊天機器人。ALICE 在 2000、2001 和 2004 年三次獲得 Loebner 獎，成為當時最先進的開放域對話系統。

## AIML 語言

AIML（人工智慧標記語言）是 ALICE 的對話引擎核心，是一種基於 XML 的模式匹配語言。AIML 的設計目標是建立一個標準化、可擴展的對話規則描述格式。

### 基本語法

```xml
<?xml version="1.0" encoding="UTF-8"?>
<aiml>
    <category>
        <pattern>HELLO</pattern>
        <template>Hi there! How can I help you?</template>
    </category>
    
    <category>
        <pattern>I AM *</pattern>
        <template>How long have you been <star/>?</template>
    </category>
</aiml>
```

### 高級功能

AIML 支援許多進階功能：

**遞迴引用**：規則可以引用其他規則，形成複雜的對話流程：

```xml
<category>
    <pattern>YES</pattern>
    <template><srai>CONFIRM_YES</srai></template>
</category>
```

**上下文管理**：使用 `<that/>` 標籤引用系統上一輪的輸出，使用 `<topic/>` 標籤管理對話主題：

```xml
<category>
    <pattern>WHAT IS IT</pattern>
    <that>I AM A ROBOT</that>
    <template>I am an artificial intelligence.</template>
</category>
```

## ALICE 的知識庫

ALICE 的 AIML 知識庫包含超過 40,000 條規則，涵蓋了從日常問候到科學知識的廣泛主題。這些規則是由社群志願者經過多年累積編寫而成。

## AIML 的影響與不足

AIML 建立了對話規則語言的事實標準，啟發了許多後續的對話框架。然而，AIML 有其固有不足：

- 規則撰寫耗費大量人力
- 難以覆蓋所有對話場景
- 缺乏深度語言理解能力
- 對話一致性依賴於規則的設計品質

## 延伸閱讀

- [AIML 官方規範](https://www.google.com/search?q=AIML+specification+ALICE)
- [ALICE 機器人源碼](https://www.google.com/search?q=ALICE+chatbot+open+source)
- [Loebner 獎](https://www.google.com/search?q=Loebner+Prize+Turing+Test)
