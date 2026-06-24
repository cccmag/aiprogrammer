#!/usr/bin/env python3
"""
CI/CD Pipeline 實戰示範

展示一個簡化的 CI/CD Pipeline，包含：
- Lint 檢查
- 單元測試
- 容器建置
"""
import subprocess
import time

def run_command(name, cmd):
    print(f"[{name}] {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[{name}] Failed: {result.stderr}")
        return False
    print(f"[{name}] ✓")
    return True

def main():
    print("=" * 50)
    print("CI/CD Pipeline Demo")
    print("=" * 50)
    
    start = time.time()
    
    stages = [
        ("Lint", "python3 lint_check.py"),
        ("Test", "python3 run_tests.py"),
        ("Build", "python3 build_image.py"),
    ]
    
    for name, cmd in stages:
        print(f"\n[{name}] Starting...")
        if not run_command(name, cmd):
            print(f"\nPipeline failed at stage: {name}")
            return 1
    
    elapsed = time.time() - start
    print(f"\n{'=' * 50}")
    print(f"CI/CD Pipeline Completed in {elapsed:.1f}s")
    print("=" * 50)
    return 0

if __name__ == "__main__":
    exit(main())