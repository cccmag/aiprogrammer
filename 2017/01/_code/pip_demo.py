#!/usr/bin/env python3
"""pip 與虛擬環境使用示範"""

def demo():
    print("=" * 60)
    print("pip 與虛擬環境使用示範")
    print("=" * 60)

    print("\n1. 常用 pip 命令：")
    print("   pip install <package>          # 安裝套件")
    print("   pip install <package>==1.0.0   # 安裝特定版本")
    print("   pip install -r requirements.txt # 從檔案安裝")
    print("   pip list                        # 列出已安裝套件")
    print("   pip show <package>              # 顯示套件資訊")
    print("   pip uninstall <package>         # 卸載套件")
    print("   pip freeze > requirements.txt   # 產出依賴檔案")

    print("\n2. 虛擬環境命令：")
    print("   python3 -m venv myenv           # 創建虛擬環境")
    print("   source myenv/bin/activate       # 激活（Linux/macOS）")
    print("   myenv\\Scripts\\activate         # 激活（Windows）")
    print("   deactivate                      # 退出虛擬環境")

    print("\n3. 現代替代方案：pipenv")
    print("   pip install pipenv              # 安裝 pipenv")
    print("   pipenv install <package>       # 安裝套件")
    print("   pipenv shell                    # 激活環境")
    print("   pipenv run python script.py     # 直接執行腳本")

    print("\n4. 示例虛擬環境工作流：")
    print("   $ python3 -m venv myproject_env")
    print("   $ source myproject_env/bin/activate")
    print("   (myproject_env) $ pip install numpy pandas matplotlib")
    print("   (myproject_env) $ pip freeze > requirements.txt")
    print("   (myproject_env) $ python my_script.py")
    print("   (myproject_env) $ deactivate")

if __name__ == "__main__":
    demo()