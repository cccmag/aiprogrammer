import subprocess
import sys


def run_command(cmd, timeout=10):
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=isinstance(cmd, str)
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except FileNotFoundError:
        return False, "", "Command not found"
    except Exception as e:
        return False, "", str(e)


def parse_docker_ps(output):
    lines = output.strip().split("\n")
    if len(lines) < 2:
        return []

    headers = lines[0].split()
    containers = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= len(headers):
            containers.append({
                "id": parts[0],
                "image": parts[1],
                "status": " ".join(parts[2:]) if len(parts) > 2 else ""
            })
    return containers


def parse_docker_images(output):
    lines = output.strip().split("\n")
    if len(lines) < 2:
        return []

    images = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 4:
            images.append({
                "repository": parts[0],
                "tag": parts[1],
                "id": parts[2],
                "size": parts[3] if len(parts) > 3 else ""
            })
    return images


def parse_docker_stats(output):
    lines = output.strip().split("\n")
    if len(lines) < 2:
        return []

    stats = []
    for line in lines[1:]:
        if line.strip():
            parts = line.split()
            if len(parts) >= 4:
                stats.append({
                    "container_id": parts[0],
                    "cpu": parts[1] if len(parts) > 1 else "N/A",
                    "mem_usage": parts[2] if len(parts) > 2 else "N/A",
                    "mem_limit": parts[3] if len(parts) > 3 else "N/A"
                })
    return stats


def demo():
    print("=" * 56)
    print("Docker 容器管理工具")
    print("=" * 56)

    success, _, _ = run_command(["docker", "info"])
    if not success:
        print("\n錯誤：Docker 未安裝或 Daemon 未運行")
        return

    print("\n[容器列表]")
    success, stdout, _ = run_command(["docker", "ps", "--format", "{{.ID}} {{.Image}} {{.Status}}"])
    if success and stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    print(f"  {parts[0][:12]}  {parts[1]}  {' '.join(parts[2:])}")
    else:
        print("  無執行中的容器")

    print("\n[映象列表]")
    success, stdout, _ = run_command(["docker", "images", "--format", "{{.Repository}} {{.Tag}} {{.ID}} {{.Size}}"])
    if success and stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 4:
                    print(f"  {parts[0]}:{parts[1]}  {parts[2]}  {parts[3]}")
    else:
        print("  無映象")

    print("\n[資源使用]")
    success, stdout, _ = run_command(
        ["docker", "stats", "--no-stream", "--format", "{{.Container}} {{.CPUPerc}} {{.MemUsage}}"]
    )
    if success and stdout.strip():
        for line in stdout.strip().split("\n"):
            if line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    print(f"  {parts[0][:12]}  CPU: {parts[1]}  MEM: {parts[2]}")
    else:
        print("  無容器運行")

    print("\n[系統資訊]")
    success, stdout, _ = run_command(["docker", "version", "--format", "{{.Server.Version}}"])
    if success and stdout.strip():
        print(f"  Docker 版本: {stdout.strip()}")
    else:
        print("  無法取得版本資訊")

    print(f"\n{'=' * 56}")
    print("檢測完成")
    print("=" * 56)


if __name__ == "__main__":
    demo()