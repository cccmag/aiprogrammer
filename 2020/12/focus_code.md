# 2020 年 AI 里程碑時間線

## 前言

讓我們回顧 2020 年最重要的 AI 和技術事件。

---

## 原始碼

完整的時間線回顧程式：[_code/ai_timeline.py](_code/ai_timeline.py)

```python
#!/usr/bin/env python3
"""2020 年 AI 里程碑時間線"""

def demo():
    print("=" * 60)
    print("2020 年 AI 里程碑時間線")
    print("=" * 60)

    milestones = [
        ("2020年1月", "Python 2 正式終結支援"),
        ("2020年1月", "TensorFlow 2.1 發布"),
        ("2020年3月", "T5 (Google) 發布 - 110億參數"),
        ("2020年5月", "GPT-3 發布 - 1750億參數"),
        ("2020年6月", "GPT-3 API 開始測試"),
        ("2020年7月", "EleutherAI 發布 GPT-Neo"),
        ("2020年9月", "DeepMind 公布 AlphaFold2 預告"),
        ("2020年10月", "Python 3.9 正式發布"),
        ("2020年11月", "AlphaFold2 CASP14 獲勝"),
        ("2020年11月", "GPT-3 API 開始向合作夥伴開放"),
        ("2020年12月", "GitHub 活躍用戶突破 5000萬"),
    ]

    print("\n2020 年 AI 發展歷程：")
    print("-" * 40)
    for date, event in milestones:
        print(f"{date}: {event}")

    print("\n" + "=" * 60)
    print("2020 年是 AI 突破的一年！")
    print("=" * 60)

if __name__ == "__main__":
    demo()
```

---

## 按月份重要事件

```
2020 年重要事件：
────────────────────────────────

1月：
- Python 2.7 停止支援
- TensorFlow 2.1 發布

3月：
- Google T5 模型發布

5月：
- OpenAI 發布 GPT-3

6月：
- GPT-3 論文發布
- AI 抗疫開始受到關注

9月：
- DeepMind 預告 AlphaFold2

10月：
- Python 3.9 正式發布
- GPT-3 應用開始流行

11月：
- AlphaFold2 CASP14 獲勝 ◄── 年度最大 AI 突破
- GPT-3 API 開放

12月：
- GitHub 用戶突破 5000 萬
- 年終盤點
```

---

*本期程式實作到此結束。*