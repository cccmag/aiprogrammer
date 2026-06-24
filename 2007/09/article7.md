# 專家系統：CLIPS 實作

## 概述

專家系統是早期 AI 的重要應用，透過規則推導來類比人類專家的決策過程。CLIPS（C Language Integrated Production System）是一個廣泛使用的專家系統工具，2007 年仍持續被應用於各種領域。

## 專家系統的基本結構

```python
"""
專家系統概念展示
展示基於規則的專家系統原理
"""

def demo():
    print("=" * 50)
    print("專家系統概念展示")
    print("=" * 50)

    print("\n--- 專家系統組成 ---")
    components = {
        "知識庫": "存放領域知識的規則集合",
        "事實庫": "當前問題的已知事實",
        "推論引擎": "根據規則進行推導的機制",
        "解釋介面": "解釋推理過程的模組",
        "使用者介面": "與使用者互動的界面",
    }
    for comp, desc in components.items():
        print(f"  {comp}: {desc}")

    print("\n--- 規則範例 ---")
    rules = """
; 汽車診斷專家系統規則

; 規則：如果引擎無法啟動且電池沒電，則建議充電
(defrule 充電建議
    (engine-problem no-start)
    (battery dead)
    =>
    (assert (suggestion charge-battery))
    (printout t "建議：請為電池充電" crlf)
)

; 規則：如果引擎無法啟動且火星塞有問題，則建議更換
(defrule 火星塞建議
    (engine-problem no-start)
    (spark-plug faulty)
    =>
    (assert (suggestion replace-spark-plug))
    (printout t "建議：請更換火星塞" crlf)
)

; 規則：複合條件
(defrule 複合診斷
    (engine-problem no-start)
    (battery dead)
    (fuel-tank empty)
    =>
    (assert (suggestion "充電並加油"))
    (printout t "建議：請充電並加油" crlf)
)
"""
    print(rules)

    print("\n--- 事實表達 ---")
    facts = """
; 宣告事實
(assert (engine-problem no-start))
(assert (battery dead))
(assert (spark-plug faulty))
(assert (fuel-tank empty))

; 查詢事實
(facts)
(list-defrules)
"""
    print(facts)

    print("\n--- 前向推導 vs 後向推導 ---")
    print("""
前向推導（Forward Chaining）：
  - 從已知事實出發
  - 不斷匹配規則的前提條件
  - 滿足時執行規則結論
  - 直到沒有新事實產生

後向推導（Backward Chaining）：
  - 從目標假設出發
  - 尋找支持假設的證據
  - 遞迴驗證子目標
  - 適用於假設驅動的推理
""")

    print("\n--- 專家系統優勢 ---")
    advantages = [
        "可解釋性：推理過程清晰可追蹤",
        "知識模組化：規則易於維護和擴展",
        "專家知識擷取：保存領域專家經驗",
        "一致性：相同輸入產生相同輸出",
    ]
    for adv in advantages:
        print(f"  - {adv}")

    print("\n" + "=" * 50)
    print("專家系統概念展示完成")

if __name__ == "__main__":
    demo()