# 2009 年重要技術事件時間線

## 簡介

本期程式實作將整理 2009 年的重要技術事件，按月份呈現，幫助讀者回顧這一年的技術發展。

## 程式碼

```python
#!/usr/bin/env python3
"""
2009 Technology Year in Review

這個程式整理了 2009 年的重要技術事件，幫助讀者回顧這一年的發展。
"""

from dataclasses import dataclass
from typing import List
from datetime import datetime


@dataclass
class TechEvent:
    month: int
    title: str
    description: str
    category: str


EVENTS = [
    TechEvent(1, "Ruby 1.9.1 發布", "YARV 虛擬機帶來 2-5x 效能提升", "Language"),
    TechEvent(3, "GitHub 突破 50 萬用戶", "社交程式設計持續成長", "Tools"),
    TechEvent(4, "Google App Engine 支援 Java", "擴大 PaaS 平台能力", "Cloud"),
    TechEvent(6, "Firefox 3.5 發布", "CSS 3 / HTML 5 支援增加", "Browser"),
    TechEvent(6, "Safari 4.0 發布", "強化的 JavaScript 效能", "Browser"),
    TechEvent(7, "Chrome OS 宣布", "Google 雲端作業系統計畫", "Cloud"),
    TechEvent(7, "jQuery 1.4 發布", "DOM 操作效能提升 3 倍", "Frontend"),
    TechEvent(8, "MongoDB 1.0 發布", "文件資料庫進入實用階段", "Database"),
    TechEvent(8, "CouchDB 0.10 發布", "離線優先的文件資料庫", "Database"),
    TechEvent(8, "Node.js 0.1 發布", "JavaScript 全端時代來臨", "Language"),
    TechEvent(9, "Ruby on Rails 3.0 Beta", "Merb 合併，重大更新", "Framework"),
    TechEvent(9, "OAuth 1.0a 確認標準", "開放授權標準化", "Platform"),
    TechEvent(10, "Python 3.1 發布", "持續改進", "Language"),
    TechEvent(10, "GitHub 突破 100 萬用戶", "分散式版本控制成主流", "Tools"),
    TechEvent(11, "Go 語言發布", "Google 發布新的程式語言", "Language"),
    TechEvent(11, "Stripe 成立", "支付 API 的簡化方案", "Platform"),
    TechEvent(12, "Google Wave 發布", "協作平台新想像", "Platform"),
    TechEvent(12, "2009 年回顧", "技術變革的關鍵一年", "Summary"),
]


def display_events_by_month():
    """按月份顯示事件"""
    print("\n" + "#" * 60)
    print("# 2009 年重要技術事件時間線")
    print("#" * 60 + "\n")

    current_month = 0
    month_names = [
        "", "一月", "二月", "三月", "四月", "五月", "六月",
        "七月", "八月", "九月", "十月", "十一月", "十二月"
    ]

    for event in sorted(EVENTS, key=lambda x: (x.month, x.title)):
        if event.month != current_month:
            current_month = event.month
            print(f"\n{'=' * 50}")
            print(f"  {month_names[current_month]}")
            print(f"{'=' * 50}")

        print(f"  • {event.title}")
        print(f"    {event.description}")
        print(f"    [分類: {event.category}]")


def display_events_by_category():
    """按分類顯示事件"""
    print("\n" + "#" * 60)
    print("# 2009 年技術分類回顧")
    print("#" * 60 + "\n")

    categories = {}
    for event in EVENTS:
        if event.category not in categories:
            categories[event.category] = []
        categories[event.category].append(event)

    for category in sorted(categories.keys()):
        print(f"\n{'-' * 40}")
        print(f"  {category}")
        print(f"{'-' * 40}")
        for event in categories[category]:
            print(f"  • {event.title} ({event.month}月)")


def display_year_summary():
    """顯示年度總結"""
    print("\n" + "#" * 60)
    print("# 2009 年年度總結")
    print("#" * 60 + "\n")

    categories = {}
    for event in EVENTS:
        if event.category not in categories:
            categories[event.category] = 0
        categories[event.category] += 1

    print("事件分類統計：")
    print("-" * 30)
    for category, count in sorted(categories.items(), key=lambda x: -x[1]):
        bar = "█" * count
        print(f"  {category:15} {count:2} {bar}")


def main():
    print("\n" + "#" * 60)
    print("#" + " " * 20 + "2009 Technology Year in Review")
    print("#" * 60)

    display_events_by_month()
    display_events_by_category()
    display_year_summary()

    print("\n" + "#" * 60)
    print("# 2009 年是技術變革的關鍵一年")
    print("# 雲端運算、NoSQL、前端革命")
    print("# 為後續十年的技術發展奠定了基礎")
    print("#" * 60 + "\n")


if __name__ == "__main__":
    main()
```

## 測試方式

```bash
python3 _code/year_review.py
```

## 實作重點

1. **TechEvent 類別**：儲存事件的基本資訊
2. **按月份顯示**：時間順序回顧
3. **按分類顯示**：類別統計
4. **年度統計**：視覺化的事件數量

---

*本期程式實作到此結束。感謝閱讀 2009 年的最後一期。*