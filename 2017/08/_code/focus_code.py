#!/usr/bin/env python3
"""電腦視覺示範"""

def demo():
    print("=" * 50)
    print("電腦視覺示範")
    print("=" * 50)

    print("\n1. 圖像基本概念:")
    print("   數位圖像 = 像素矩陣")
    print("   每像素 = RGB 三通道")
    print("   尺寸如 640x480 = 307,200 像素")

    print("\n2. 卷積操作概念:")
    print("   卷積核在圖像上滑動")
    print("   計算加權和產生特徵圖")

    print("\n3. 池化操作:")
    print("   Max Pooling: 取最大值")
    print("   Avg Pooling: 取平均值")
    print("   作用: 降維、保持特徵")

    print("\n4. CNN 架構:")
    print("   Conv → Pool → Conv → Pool → ... → FC → Output")

    print("\n5. 物體偵測:")
    print("   Two-stage: R-CNN (候選 → 分類)")
    print("   One-stage: YOLO (直接預測)")

    print("\n6. IoU (Intersection over Union):")
    print("   IoU = 重疊面積 / 總面積")
    print("   用於評估偵測框準確度")

    print("\n" + "=" * 50)
    print("電腦視覺示範完成")
    print("=" * 50)

if __name__ == "__main__":
    demo()