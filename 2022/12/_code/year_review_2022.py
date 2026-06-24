#!/usr/bin/env python3
"""2022 AI Annual Review - Data Analysis & Timeline Generator"""

def demo():
    print("=" * 60)
    print("  2022 AI 年度回顧 — 數據與時間線")
    print("=" * 60)

    models = [
        ("2022-01", "DeepMind", "AlphaCode", "Codeforces 競賽級程式生成"),
        ("2022-03", "OpenAI", "DALL-E 2", "文字生成影像 (4x 解析度提升)"),
        ("2022-04", "OpenAI", "InstructGPT", "基於人類回饋的指令微調"),
        ("2022-05", "Google", "PaLM (540B)", "Pathways 架構, 540B 參數"),
        ("2022-06", "DeepMind", "Gato", "通用代理, 600+ 任務"),
        ("2022-07", "Google", "LaMDA 2", "對話 AI, 開放測試"),
        ("2022-08", "Stability AI", "Stable Diffusion", "開源文字生成影像, 1.5B"),
        ("2022-09", "Meta", "Make-A-Video", "文字生成影片"),
        ("2022-10", "Google", "Imagen Video", "高品質文字生成影片"),
        ("2022-11", "Google", "PaLM API", "LLM API 開放"),
        ("2022-11", "OpenAI", "ChatGPT (GPT-3.5)", "對話式 AI, 5 天 100 萬用戶"),
        ("2022-12", "DeepSpeed", "ZeRO-3 Offload", "開源大模型訓練優化"),
    ]

    market = {
        "2020": 15.7,
        "2021": 24.9,
        "2022": 42.5,
        "2023E": 71.0,
        "2024E": 118.6,
        "2025E": 190.6,
    }

    funding_deals = [
        ("2022-01", "Scale AI", "$325M", "Series E, $7.3B 估值"),
        ("2022-04", "Hugging Face", "$100M", "Series C, $2B 估值"),
        ("2022-05", "Synthesia", "$50M", "AI 影片生成"),
        ("2022-08", "Jasper AI", "$125M", "AI 內容寫作, $1.7B 估值"),
        ("2022-10", "Stability AI", "$101M", "種子輪, $1B 估值"),
        ("2022-11", "Lightricks", "$130M", "AI 影像編輯"),
    ]

    topics = [
        "大型語言模型競賽: GPT-3.5, PaLM (540B), LLaMA (Meta)",
        "AI 繪圖爆發: DALL-E 2, Stable Diffusion, Midjourney",
        "ChatGPT 誕生: 5 天 100 萬用戶, 史上最快成長",
        "開源生態成熟: Hugging Face, Stable Diffusion, LangChain",
        "AI 監管加速: EU AI Act, 美國 AI Bill of Rights",
        "程式生成突破: AlphaCode, GitHub Copilot GA",
        "通用代理崛起: DeepMind Gato, 多任務學習",
        "影片生成萌芽: Make-A-Video, Imagen Video",
        "訓練基礎設施: TPU v4, A100 供不應求",
        "倫理爭議: 生成式 AI 版權, 深度偽造規範",
    ]

    print(f"\n{'─' * 60}")
    print("  一、2022 AI 重要模型與產品時間線")
    print(f"{'─' * 60}")
    for date, company, name, desc in models:
        print(f"\n  [{date}]")
        print(f"    {company:15s} | {name:30s}")
        print(f"    {'':15s}   {desc}")

    print(f"\n{'─' * 60}")
    print("  二、全球 AI 市場規模 (單位: 十億美元)")
    print(f"{'─' * 60}")
    print(f"\n  {'年度':>8s}  {'市場規模':>12s}  {'YoY 成長':>10s}")
    print(f"  {'-' * 34}")
    prev = None
    for year, val in sorted(market.items()):
        yoy = f"+{((val - prev) / prev * 100):.1f}%" if prev else "  -"
        print(f"  {year:>8s}  {val:>10.1f} B$  {yoy:>10s}")
        prev = val
    print(f"\n  CAGR (2020-2022): {((market['2022'] / market['2020']) ** (1/2) - 1) * 100:.1f}%")

    print(f"\n{'─' * 60}")
    print("  三、2022 AI 投資重點案件")
    print(f"{'─' * 60}")
    print(f"\n  {'日期':>12s}  {'公司':>18s}  {'金額':>12s}   {'備註'}")
    print(f"  {'-' * 60}")
    for date, company, amount, note in funding_deals:
        print(f"  {date:>12s}  {company:>18s}  {amount:>10s}   {note}")

    print(f"\n{'─' * 60}")
    print("  四、2022 年十大 AI 主題")
    print(f"{'─' * 60}")
    for i, topic in enumerate(topics, 1):
        print(f"\n  {i:2d}. {topic}")

    print(f"\n{'─' * 60}")
    print("  五、AI 產業結論")
    print(f"{'─' * 60}")
    conclusions = [
        "2022 是生成式 AI 的轉捩點, ChatGPT 與 Stable Diffusion 重新定義了 AI 產品",
        "大型語言模型的參數競賽達到頂峰, 後續重心將轉向效率與開源",
        "開源生態 (Hugging Face, Stable Diffusion) 挑戰了封閉模型的壟斷地位",
        "AI 監管框架開始成形, 歐盟與美國相繼提出法案",
        "ChatGPT 的誕生預示著 2023 年將是 LLM 全面商業化的開始",
    ]
    for c in conclusions:
        print(f"  \u2022 {c}")

    print(f"\n{'=' * 60}")
    print("  報告產生完成")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    demo()
