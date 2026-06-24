# 人機協作案例研究

## 前言

理論再好，不如實戰。本文透過三個具體案例，展示人機協作介面設計在現實中的應用與效果。

## 案例一：AI 輔助程式碼審查

### 問題

開發團隊每天產生大量 Pull Request，人工審查耗時且容易遺漏問題。

### 解決方案

```python
from typing import List, Dict

class AICodeReviewer:
    def __init__(self):
        self.issues_found = []

    def review_code(self, code: str, filename: str) -> List[Dict]:
        issues = []
        lines = code.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("TODO"):
                issues.append({
                    "line": i + 1, "severity": "info",
                    "msg": "遺留 TODO，請確認是否已完成"
                })
            if "print(" in stripped and "def " not in stripped:
                issues.append({
                    "line": i + 1, "severity": "warning",
                    "msg": "偵錯用 print，建議移除或改用 logging"
                })
            if stripped.endswith("except:"):
                issues.append({
                    "line": i + 1, "severity": "error",
                    "msg": "裸 except 會捕獲所有例外，應指定例外類型"
                })
        self.issues_found.extend(issues)
        return issues

    def generate_report(self) -> str:
        error_count = sum(1 for i in self.issues_found if i["severity"] == "error")
        warning_count = sum(1 for i in self.issues_found if i["severity"] == "warning")
        return f"審查完成：{error_count} 個錯誤，{warning_count} 個警告"

reviewer = AICodeReviewer()
code = """
def process(data):
    # TODO: 處理邊界情況
    print("processing")
    try:
        result = data / 0
    except:
        pass
    return result
"""
issues = reviewer.review_code(code, "process.py")
for issue in issues:
    print(f"第 {issue['line']} 行 [{issue['severity']}]：{issue['msg']}")
print(reviewer.generate_report())
```

### 結果

開發者可以專注於架構與邏輯問題，AI 處理重複性的風格與常見錯誤檢查，審查速度提升 60%。

## 案例二：智慧排程系統

### 問題

行政人員每天要協調多人的會議時間，來回確認耗費大量精力。

### 解決方案

```python
from itertools import combinations

class SmartScheduler:
    def __init__(self, participants: List[str]):
        self.participants = participants
        self.constraints = {}

    def add_constraint(self, person: str, available: List[str]):
        self.constraints[person] = available

    def find_slots(self, duration_minutes: int) -> List[str]:
        common = None
        for person in self.participants:
            avail = set(self.constraints.get(person, []))
            common = avail if common is None else (common & avail)
        return sorted(common) if common else []

    def suggest_alternative(self, preferred: str) -> List[str]:
        alternatives = []
        for person in self.participants:
            avail = self.constraints.get(person, [])
            if preferred not in avail:
                alt = avail[0] if avail else "無可用時間"
                alternatives.append(f"{person}：{alt}")
        return alternatives

    def negotiate(self, human_choice: str, ai_suggestion: str) -> str:
        return f"人類選擇 {human_choice}，AI 建議 {ai_suggestion}，最終決策由人類裁定"

scheduler = SmartScheduler(["Alice", "Bob", "Charlie"])
scheduler.add_constraint("Alice", ["09:00", "10:00", "14:00"])
scheduler.add_constraint("Bob", ["10:00", "11:00", "14:00"])
scheduler.add_constraint("Charlie", ["14:00", "15:00", "16:00"])
print(f"共同可用時間：{scheduler.find_slots(60)}")
print(f"替代方案：{scheduler.suggest_alternative('10:00')}")
```

### 結果

排程從平均 12 封郵件往返減少到 2-3 次互動，AI 處理約束滿足問題，人類做最終決策。

## 案例三：文件協作摘要

### 問題

專案經理需要快速掌握大量文件的要點。

### 解決方案

```python
class CollaborativeSummarizer:
    def __init__(self):
        self.sections = {}
        self.feedback = {}

    def add_section(self, title: str, content: str):
        self.sections[title] = content

    def ai_summarize(self, title: str, max_sentences: int = 3) -> str:
        content = self.sections.get(title, "")
        if not content:
            return ""
        sentences = [s.strip() for s in content.replace("。", ".").split(".") if s.strip()]
        return "。".join(sentences[:max_sentences]) + "。"

    def human_edit(self, title: str, edited_summary: str):
        self.feedback[title] = edited_summary
        return f"已記錄 {title} 的人工修正"

    def merge_summaries(self) -> str:
        parts = []
        for title in self.sections:
            if title in self.feedback:
                parts.append(self.feedback[title])
            else:
                parts.append(self.ai_summarize(title))
        return "\n\n".join(parts)

    def learning_improvement(self) -> str:
        pattern = {
            "增加數字": len([f for f in self.feedback.values() if any(c.isdigit() for c in f)]),
            "補充結論": len([f for f in self.feedback.values() if "結論" in f]),
        }
        return str(pattern)

cs = CollaborativeSummarizer()
cs.add_section("設計", "系統採用模組化架構。前端使用 React。後端使用 Python。資料庫使用 PostgreSQL。部署於 AWS。")
cs.ai_summarize("設計")
cs.human_edit("設計", "系統採用模組化架構（前端 React、後端 Python、資料庫 PostgreSQL），部署於 AWS。")
print(cs.merge_summaries())
print(f"學習模式：{cs.learning_improvement()}")
```

### 結果

AI 生成初稿，人類專注於修正與補充，最終產出品質比純人工或純 AI 都高。

## 結語

三個案例的共同教訓：**AI 處理結構化、重複性的工作，人類處理判斷、創造與決策**。成功的協作介面不是讓 AI 取代人類，而是讓雙方各司其職、互補長短。

---

**延伸閱讀**

- [人機協作案例集](https://www.google.com/search?q=human+AI+collaboration+case+studies+2026)
- [程式碼審查自動化](https://www.google.com/search?q=AI+code+review+automation+tools)
- [智慧排程系統設計](https://www.google.com/search?q=AI+powered+meeting+scheduler+design)
