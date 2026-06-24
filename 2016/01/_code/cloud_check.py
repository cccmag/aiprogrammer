import subprocess
import os
import sys


def check_command(cmd, version_flag="--version"):
    try:
        result = subprocess.run(
            [cmd, version_flag],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.strip().split("\n")[0]
            return True, version_line
        return False, None
    except FileNotFoundError:
        return False, None
    except Exception:
        return False, None


def check_env_var(var_name):
    value = os.environ.get(var_name)
    if value:
        if len(value) > 0:
            return True, "已設定"
        return False, "環境變數存在但值為空"
    return False, "未設定"


def check_file_exists(path):
    if os.path.exists(path):
        return True, path
    return False, "檔案不存在"


def demo():
    print("=" * 56)
    print("雲端環境檢測工具")
    print("=" * 56)

    print("\n[1] AWS CLI")
    installed, version = check_command("aws")
    if installed:
        print(f"    狀態: 已安裝")
        print(f"    版本: {version}")
    else:
        print(f"    狀態: 未安裝")
    key_id_ok, _ = check_env_var("AWS_ACCESS_KEY_ID")
    secret_ok, _ = check_env_var("AWS_SECRET_ACCESS_KEY")
    if key_id_ok and secret_ok:
        print(f"    憑證: 已設定")
    else:
        print(f"    憑證: 未設定")

    print("\n[2] Google Cloud SDK")
    installed, version = check_command("gcloud")
    if installed:
        print(f"    狀態: 已安裝")
        print(f"    版本: {version}")
    else:
        print(f"    狀態: 未安裝")
    cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if cred_path:
        exists, path = check_file_exists(cred_path)
        if exists:
            print(f"    服務帳號: 已設定 ({path})")
        else:
            print(f"    服務帳號: 檔案不存在 ({path})")
    else:
        print(f"    服務帳號: 未設定")

    print("\n[3] Azure CLI")
    installed, version = check_command("az")
    if installed:
        print(f"    狀態: 已安裝")
        print(f"    版本: {version}")
    else:
        installed_old, _ = check_command("azure")
        if installed_old:
            print(f"    狀態: 已安裝（舊版 CLI）")
        else:
            print(f"    狀態: 未安裝")

    print("\n[4] Terraform")
    installed, version = check_command("terraform")
    if installed:
        print(f"    狀態: 已安裝")
        print(f"    版本: {version}")
    else:
        print(f"    狀態: 未安裝")

    print("\n[5] Docker")
    installed, version = check_command("docker")
    if installed:
        print(f"    狀態: 已安裝")
        print(f"    版本: {version}")
        try:
            ps_result = subprocess.run(
                ["docker", "ps"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if ps_result.returncode == 0:
                containers = [c for c in ps_result.stdout.strip().split("\n") if c]
                print(f"    運行中容器: {len(containers) - 1}")
        except Exception:
            pass
    else:
        print(f"    狀態: 未安裝")

    print(f"\n{'=' * 56}")
    print("檢測完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()