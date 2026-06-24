import sys
import os
import platform


def demo():
    print("=" * 56)
    print("Python 環境檢測工具")
    print("=" * 56)

    print(f"\n[1] Python 版本")
    print(f"    Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"    實作: {platform.python_implementation()}")
    print(f"    平台: {platform.platform()}")

    print(f"\n[2] 虛擬環境")
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print(f"    狀態: 啟用中")
        print(f"    路徑: {sys.prefix}")
    else:
        print(f"    狀態: 未啟用（全域 Python）")
        print(f"    路徑: {sys.prefix}")

    print(f"\n[3] 熱門套件")
    packages = [
        ("numpy", "NumPy"),
        ("pandas", "Pandas"),
        ("matplotlib", "Matplotlib"),
        ("requests", "Requests"),
    ]
    for module_name, display_name in packages:
        try:
            mod = __import__(module_name)
            version = getattr(mod, "__version__", "unknown")
            print(f"    {display_name}: {version}")
        except ImportError:
            print(f"    {display_name}: 未安裝")

    print(f"\n[4] pip 管理")
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            print(f"    {result.stdout.strip()}")
        else:
            print(f"    pip: 無法取得版本")
    except Exception:
        print(f"    pip: 無法檢測")

    print(f"\n{'=' * 56}")
    print("檢測完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()