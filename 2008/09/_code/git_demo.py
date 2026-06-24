#!/usr/bin/env python3
"""Git 示範 - 分散式版本控制概念"""

def demo():
    print("=" * 50)
    print("Git 與分散式版本控制示範")
    print("=" * 50)

    print("\n1. Git 四大區域（模擬）：")
    areas = [
        ("Working Directory", "工作目錄 - 你正在編輯檔案的地方"),
        ("Staging Area", "暫存區 - git add 後的區域"),
        ("Local Repository", "本地倉庫 - .git 目錄"),
        ("Remote Repository", "遠端倉庫 - GitHub 等")
    ]
    print("   ┌────────────────────┬────────────────────────────────┐")
    print("   │  區域              │  說明                          │")
    print("   ├────────────────────┼────────────────────────────────┤")
    for area, desc in areas:
        print(f"   │ {area:16} │ {desc:30} │")
    print("   └────────────────────┴────────────────────────────────┘")

    print("\n2. 工作流程（模擬）：")
    workflow = [
        "編輯檔案 → Working Directory",
        "git add   → Staging Area",
        "git commit → Local Repository",
        "git push  → Remote Repository"
    ]
    for step in workflow:
        print(f"   → {step}")

    print("\n3. 分支操作（模擬）：")
    print("   main ────●────●────●──→ (當前位置)")
    print("            └── merge ←── feature-x ────●──")
    print("                       └─ commit")

    print("\n4. GitHub Fork 流程（模擬）：")
    fork_steps = [
        "1. Fork 倉庫 → 你有了自己的副本",
        "2. Clone 到本地 → 開始開發",
        "3. 建立功能分支 → 安全開發",
        "4. 提交並推送 → git push",
        "5. 發起 Pull Request → 請求審查",
        "6. 審查通過 → 合併到原專案"
    ]
    for step in fork_steps:
        print(f"   {step}")

    print("\n5. 常見 Git 命令（模擬）：")
    commands = [
        ("git init", "初始化新倉庫"),
        ("git clone <url>", "克隆遠端倉庫"),
        ("git add .", "新增所有檔案到暫存區"),
        ("git commit -m 'msg'", "提交更改"),
        ("git push", "推送到遠端"),
        ("git pull", "拉取並合併"),
        ("git branch", "列出分支"),
        ("git checkout -b", "建立並切換分支"),
        ("git merge", "合併分支"),
        ("git log", "查看提交歷史")
    ]
    print("   ┌────────────────────┬────────────────────────────────┐")
    print("   │  命令               │  說明                          │")
    print("   ├────────────────────┼────────────────────────────────┤")
    for cmd, desc in commands:
        print(f"   │ {cmd:18} │ {desc:30} │")
    print("   └────────────────────┴────────────────────────────────┘")

    print("\n" + "=" * 50)
    print("Git 的核心價值：")
    print("  • 分散式 - 每個開發者都有完整倉庫")
    print("  • 快速分支 - 本地分支無成本")
    print("  • 離線工作 - 無需網路即可提交")
    print("  • 社交協作 - GitHub 開創 Fork 模式")
    print("=" * 50)

if __name__ == "__main__":
    demo()