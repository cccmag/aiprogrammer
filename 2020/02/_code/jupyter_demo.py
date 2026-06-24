import sys
import os


def demo():
    print("=" * 56)
    print("Jupyter 互動式計算基礎展示")
    print("=" * 56)

    print("\n[1] 格式化輸出")
    data = list(range(1, 101))
    max_val = max(data)
    min_val = min(data)
    avg_val = sum(data) / len(data)
    print(f"    資料處理結果：")
    print(f"    - 最大值：{max_val}")
    print(f"    - 最小值：{min_val}")
    print(f"    - 平均值：{avg_val}")

    print(f"\n[2] 視覺化資訊")
    print(f"    在 Jupyter 環境中可以使用 matplotlib 進行互動式繪圖")
    print(f"    範例程式碼：")
    print(f"    ```python")
    print(f"    %matplotlib inline")
    print(f"    import matplotlib.pyplot as plt")
    print(f"    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])")
    print(f"    plt.show()")
    print(f"    ```")

    print(f"\n[3] 互動式模擬（純文字版）")
    print(f"    在 Jupyter 中使用 ipywidgets 建立互動式 UI：")
    print(f"    ```python")
    print(f"    from ipywidgets import interact")
    print(f"    @interact(x=(0, 100))")
    print(f"    def show(x):")
    print(f"        return x ** 2")
    print(f"    ```")

    print(f"\n{'=' * 56}")
    print("展示完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()