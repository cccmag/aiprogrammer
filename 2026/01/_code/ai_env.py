import sys
import os
import subprocess
import platform


def demo():
    print("=" * 56)
    print("AI 開發環境檢測工具")
    print("=" * 56)

    # 1. Python 版本檢查
    print(f"\n[1] Python 版本")
    print(f"    Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"    實作: {platform.python_implementation()}")
    print(f"    架構: {platform.machine()}")

    # 2. 虛擬環境資訊
    print(f"\n[2] 虛擬環境")
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f"    狀態: 啟用中")
        print(f"    路徑: {sys.prefix}")
    else:
        print(f"    狀態: 未啟用（全域 Python）")
        print(f"    路徑: {sys.prefix}")

    # 3. CUDA 檢查（透過 nvidia-smi）
    print(f"\n[3] GPU / CUDA")
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,driver_version",
             "--format=csv,noheader"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            for line in result.stdout.strip().split("\n"):
                if line:
                    print(f"    GPU: {line}")
            nvcc = subprocess.run(
                ["nvcc", "--version"],
                capture_output=True, text=True, timeout=5
            )
            if nvcc.returncode == 0:
                for line in nvcc.stdout.strip().split("\n"):
                    if "release" in line:
                        print(f"    CUDA: {line.strip()}")
            else:
                print(f"    CUDA: nvcc 未安裝")
        else:
            print(f"    GPU: 未檢測到 NVIDIA GPU 或驅動未安裝")
    except FileNotFoundError:
        print(f"    GPU: nvidia-smi 未找到（可能沒有 NVIDIA GPU）")
    except subprocess.TimeoutExpired:
        print(f"    GPU: 檢測超時")

    # 4. Docker 資訊
    print(f"\n[4] Docker")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"    Docker: {result.stdout.strip()}")
            ps = subprocess.run(
                ["docker", "ps", "--format", "{{.Names}}"],
                capture_output=True, text=True, timeout=5
            )
            running = [n for n in ps.stdout.strip().split("\n") if n]
            print(f"    運行中容器: {len(running)}")
        else:
            print(f"    Docker: 未運行或未安裝")
    except subprocess.TimeoutExpired:
        print(f"    Docker: 檢測超時")
    except FileNotFoundError:
        print(f"    Docker: 未安裝")

    print(f"\n{'=' * 56}")
    print("檢測完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()
