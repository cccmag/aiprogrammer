#!/usr/bin/env python3
"""SaaS 示範 - 雲端服務概念展示"""

def demo():
    print("=" * 50)
    print("SaaS 與雲端服務示範")
    print("=" * 50)

    print("\n1. SaaS 特性（模擬）：")
    saas_features = [
        "多租戶架構：多客戶共用同一實例",
        "可訪問性：透過瀏覽器隨時存取",
        "隨需可用：無需安裝軟體",
        "可擴展性：根據需求動態調整資源",
        "訂閱制：按月/年付費而非一次性購買"
    ]
    for f in saas_features:
        print(f"   ✓ {f}")

    print("\n2. 雲端服務模型（模擬）：")
    cloud_models = [
        ("SaaS", "軟體即服務", "Salesforce, Google Apps"),
        ("PaaS", "平台即服務", "Force.com, Heroku"),
        ("IaaS", "基礎設施即服務", "AWS EC2, Google Compute")
    ]
    print("   ┌────────────┬─────────────────┬──────────────────┐")
    print("   │  模型      │  說明           │  範例            │")
    print("   ├────────────┼─────────────────┼──────────────────┤")
    for m, d, e in cloud_models:
        print(f"   │ {m:10} │ {d:15} │ {e:16} │")
    print("   └────────────┴─────────────────┴──────────────────┘")

    print("\n3. SaaS vs 傳統軟體（模擬）：")
    comparison = [
        ("前期成本", "高 ($100K+)", "低或無"),
        ("維護成本", "高 (需要 IT)", "低 (供應商負責)"),
        ("部署時間", "3-6 個月", "天/周"),
        ("可訪問性", "辦公室/本地", "任何有網路的地方"),
        ("升級", "手動/昂貴", "自動/包含在訂閱")
    ]
    print("   ┌────────────┬─────────────────┬──────────────────┐")
    print("   │  特性      │  傳統軟體       │  SaaS            │")
    print("   ├────────────┼─────────────────┼──────────────────┤")
    for c in comparison:
        print(f"   │ {c[0]:10} │ {c[1]:15} │ {c[2]:16} │")
    print("   └────────────┴─────────────────┴──────────────────┘")

    print("\n4. 熱門 SaaS 服務（2008 年模擬）：")
    saas_services = [
        "Salesforce - CRM",
        "Google Apps - 辦公套件",
        "Amazon S3 - 雲端儲存",
        "Microsoft Azure - 雲端平台"
    ]
    for s in saas_services:
        print(f"   • {s}")

    print("\n" + "=" * 50)
    print("SaaS 的核心價值：")
    print("  • 降低前期成本，採用訂閱制")
    print("  • 消除軟體維護負擔")
    print("  • 隨時隨地的可訪問性")
    print("  • 自動更新，總是使用最新版本")
    print("=" * 50)

if __name__ == "__main__":
    demo()