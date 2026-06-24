#!/usr/bin/env python3
"""效能優化示範 - 快取、壓縮、CDN 概念"""

def demo():
    print("=" * 50)
    print("網站效能優化示範")
    print("=" * 50)

    print("\n1. HTTP 請求減少策略（模擬）：")
    strategies = [
        "合併 CSS/JS 檔案 → 1 個請求取代多個",
        "CSS Sprite → 多張圖片合併為一",
        "延遲載入 → 非必要資源後續載入",
        " Inline CSS/JS → 減少外部請求"
    ]
    for s in strategies:
        print(f"   ✓ {s}")

    print("\n2. 快取策略（模擬）：")
    cache_strategies = [
        "Cache-Control: max-age=31536000（靜態資源）",
        "ETag: 資源版本識別",
        "Last-Modified: 最後修改時間",
        "LocalStorage: 用戶端持久化"
    ]
    for c in cache_strategies:
        print(f"   ✓ {c}")

    print("\n3. CDN 效益（模擬）：")
    cdn_comparison = [
        ("台北→源站（美國）", "250ms"),
        ("台北→CDN 節點（香港）", "30ms"),
        ("效能提升", "約 8 倍")
    ]
    print("   ┌───────────────────────┬────────┐")
    print("   │  存取方式              │ 延遲   │")
    print("   ├───────────────────────┼────────┤")
    for scenario, latency in cdn_comparison:
        print(f"   │ {scenario:21} │ {latency:6} │")
    print("   └───────────────────────┴────────┘")

    print("\n4. 壓縮效益（模擬）：")
    compression = [
        ("原始 HTML", "50 KB"),
        ("Gzip 壓縮後", "15 KB"),
        ("壓縮率", "約 70%")
    ]
    print("   ┌───────────────────────┬────────┐")
    print("   │  類型                  │ 大小   │")
    print("   ├───────────────────────┼────────┤")
    for item, size in compression:
        print(f"   │ {item:21} │ {size:6} │")
    print("   └───────────────────────┴────────┘")

    print("\n5. YSlow 評分（模擬）：")
    scores = [
        ("A (90-100)", "優異"),
        ("B (80-89)", "良好"),
        ("C (70-79)", "一般"),
        ("D (60-69)", "較差"),
        ("E (<60)", "需改進")
    ]
    for grade, desc in scores:
        print(f"   {grade}: {desc}")

    print("\n" + "=" * 50)
    print("效能優化關鍵原則：")
    print("  • 減少 HTTP 請求數量")
    print("  • 使用 CDN 加速靜態資源")
    print("  • 善用瀏覽器快取")
    print("  • 壓縮傳輸內容")
    print("  • 持續監控效能")
    print("=" * 50)

if __name__ == "__main__":
    demo()