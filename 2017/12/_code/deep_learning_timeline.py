#!/usr/bin/env python3
"""Deep Learning Timeline demonstration for 2017 year-end review"""

def demo():
    print("Deep Learning Timeline: 2012-2017")
    print("=" * 60)

    milestones = [
        ("2012", "AlexNet", "深度學習復興，CNN 突破"),
        ("2013", "OverFeat", "統一的檢測、分類、定位"),
        ("2014", "VGGNet", "更深網路 (16-19層)"),
        ("2014", "GAN", "生成對抗網路誕生"),
        ("2014", "Inception", "GoogLeNet, 稀疏結構"),
        ("2015", "ResNet", "殘差學習, 152層"),
        ("2015", "Batch Norm", "加速訓練"),
        ("2016", "YOLO", "即時物體檢測"),
        ("2016", "DenseNet", "密集連接"),
        ("2017", "Transformer", "純注意力機制"),
        ("2017", "AlphaGo Zero", "從零學習"),
    ]

    print("\n重要里程碑:")
    for year, name, desc in milestones:
        print(f"\n{year}: {name}")
        print(f"  {desc}")

    print("\n" + "=" * 60)
    print("\n2017 年關鍵統計:")
    print("  - ImageNet 錯誤率: ~2.3% (SENet)")
    print("  - 最大 CNN: 1000+ 層 (ResNet)")
    print("  - 最大 GAN 模型: 數十億參數")
    print("\nDemo completed!")

if __name__ == "__main__":
    demo()