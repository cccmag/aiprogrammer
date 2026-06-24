#!/usr/bin/env python3
"""pip 與虛擬環境實戰範例"""

import subprocess
import sys
import os
from pathlib import Path

def demo():
    print("=" * 60)
    print("pip 與虛擬環境實戰")
    print("=" * 60)

    print("\n1. pip 基本操作")
    print("-" * 40)
    print("pip --version:", subprocess.check_output([sys.executable, "-m", "pip", "--version"]).decode().strip())
    print("pip list (前 5 個):", end=" ")
    result = subprocess.check_output([sys.executable, "-m", "pip", "list", "--format=freeze"]).decode()
    packages = result.strip().split('\n')[:5]
    print('\n  '.join(packages))

    print("\n2. 建立虛擬環境")
    print("-" * 40)
    venv_path = Path("./demo_venv")
    if not venv_path.exists():
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
        print(f"虛擬環境已建立: {venv_path}")
    else:
        print(f"虛擬環境已存在: {venv_path}")

    print("\n3. 隔離環境中的套件")
    print("-" * 40)
    print("在虛擬環境中安裝 requests:")
    pip_executable = venv_path / ("Scripts" if sys.platform == "win32" else "bin") / "pip"
    subprocess.run([str(pip_executable), "install", "requests"], capture_output=True)
    print("requests 安裝成功！")

    print("\n4. requirements.txt 檔案")
    print("-" * 40)
    requirements_file = Path("requirements_demo.txt")
    requirements_file.write_text("requests>=2.25.0\nflask>=1.1.0\n")
    print(f"已建立 {requirements_file}:")
    print(requirements_file.read_text())

    print("\n5. 清理")
    print("-" * 40)
    import shutil
    if venv_path.exists():
        shutil.rmtree(venv_path)
        print(f"已清理虛擬環境: {venv_path}")
    if requirements_file.exists():
        requirements_file.unlink()
        print(f"已清理: {requirements_file}")

    print("\n" + "=" * 60)
    print("實戰完成！")
    print("=" * 60)

if __name__ == "__main__":
    demo()