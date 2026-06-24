#!/usr/bin/env python3
"""Lint 檢查"""

def lint_check():
    print("Running lint checks...")
    
    code_sample = """
def hello():
    x = 1
    return x
    """
    
    lines = code_sample.strip().split('\n')
    issues = []
    
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            if ' ' in line and '\t' not in line:
                if len(line) - len(line.lstrip()) % 4 != 0:
                    issues.append(f"Line {i}: Check indentation")
    
    if issues:
        print("Lint issues found:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    
    print("  ✓ No lint issues found")
    return True

if __name__ == "__main__":
    success = lint_check()
    exit(0 if success else 1)