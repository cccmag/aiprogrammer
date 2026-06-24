def demo():
    print("=" * 56)
    print("2018 年 AI 技術年度回顧")
    print("=" * 56)

    events = [
        ("02", "ELMo 發布 — 雙向 LSTM 預訓練語言模型"),
        ("06", "GPT 發布 — 單向 Transformer 生成式預訓練"),
        ("08", "NVIDIA Turing 顯示卡發布"),
        ("10", "BERT 發布 — 雙向 Transformer 預訓練"),
        ("11", "PyTorch 1.0 正式版發布"),
        ("12", "TensorFlow 2.0 預覽版發布"),
    ]

    print("\n[1] 2018 年重要事件時間線")
    print("\n月份    事件")
    for month, event in events:
        print(f"{month}      {event}")

    tech_maturity = [
        ("預訓練語言模型", "高", "快速增長"),
        ("Transformer", "高", "主流"),
        ("深度學習框架", "高", "雙雄並立"),
        ("AI 硬體", "高", "持續進化"),
        ("邊緣 AI", "中", "新興領域"),
    ]

    print("\n[2] 技術成熟度評估")
    print(f"\n{'技術':<18} {'成熟度':<8} {'採用度'}")
    print("-" * 40)
    for tech, maturity, adoption in tech_maturity:
        print(f"{tech:<18} {maturity:<8} {adoption}")

    model_params = [
        ("ELMo", "94M"),
        ("GPT", "110M"),
        ("BERT-base", "110M"),
        ("BERT-large", "340M"),
    ]

    print("\n[3] 預訓練模型規模")
    print(f"\n{'模型':<15} {'參數量'}")
    print("-" * 30)
    for model, params in model_params:
        print(f"{model:<15} {params}")

    print("\n[4] 年度關鍵數據")
    print(f"\n最大預訓練模型: ~340M 參數 (BERT-large)")
    print(f"GPU 效能提升: ~50% (vs Pascal)")
    print(f"主要開源框架: TensorFlow, PyTorch")
    print(f"頂級會議: NeurIPS, ICML, ACL, CVPR")

    highlights = [
        "NLP 預訓練元年",
        "Transformer 主流化",
        "AI 倫理意識覺醒",
        "開源生態繁榮",
    ]

    print("\n[5] 年度關鍵詞")
    for i, h in enumerate(highlights, 1):
        print(f"  {i}. {h}")

    print(f"\n{'=' * 56}")
    print("回顧完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()