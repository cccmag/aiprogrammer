import re
import math
import sys


def check_password_strength(password):
    result = {
        "length": len(password),
        "has_lowercase": bool(re.search(r"[a-z]", password)),
        "has_uppercase": bool(re.search(r"[A-Z]", password)),
        "has_digit": bool(re.search(r"\d", password)),
        "has_special": bool(re.search(r"[!@#$%^&*()_+\-=\[\]{}|;':\",./<>?\\`~]", password)),
        "errors": []
    }

    if len(password) < 8:
        result["errors"].append("密碼長度至少需要 8 個字元")
    if len(password) < 12:
        result["errors"].append("建議使用 12 個字元以上")

    if not result["has_lowercase"]:
        result["errors"].append("需要包含小寫字母")
    if not result["has_uppercase"]:
        result["errors"].append("需要包含大寫字母")
    if not result["has_digit"]:
        result["errors"].append("需要包含數字")
    if not result["has_special"]:
        result["errors"].append("需要包含特殊符號")

    common_passwords = [
        "password", "12345678", "qwerty", "abc123", "letmein",
        "admin", "welcome", "monkey", "dragon", "master"
    ]
    if password.lower() in common_passwords:
        result["errors"].append("密碼太過常見，請使用更複雜的密碼")

    return result


def estimate_crack_time(password):
    charsets = 0
    if re.search(r"[a-z]", password):
        charsets += 26
    if re.search(r"[A-Z]", password):
        charsets += 26
    if re.search(r"\d", password):
        charsets += 10
    if re.search(r"[!@#$%^&*()_+\-=\[\]{}|;':\",./<>?\\`~]", password):
        charsets += 32

    if charsets == 0:
        return "無法估算"

    combinations = charsets ** len(password)
    guesses_per_second = 1_000_000_000
    seconds = combinations / guesses_per_second / 2

    if seconds < 1:
        return "瞬間"
    elif seconds < 60:
        return f"{int(seconds)} 秒"
    elif seconds < 3600:
        return f"{int(seconds / 60)} 分鐘"
    elif seconds < 86400:
        return f"{int(seconds / 3600)} 小時"
    elif seconds < 31536000:
        return f"{int(seconds / 86400)} 天"
    elif seconds < 31536000 * 100:
        return f"{int(seconds / 31536000)} 年"
    elif seconds < 31536000 * 1000:
        return f"{int(seconds / 31536000)} 年"
    elif seconds < 31536000 * 1000000:
        return f"{int(seconds / 31536000)} 年"
    else:
        return "數千年"


def get_strength_rating(result):
    score = 0
    if result["length"] >= 8:
        score += 1
    if result["length"] >= 12:
        score += 1
    if result["length"] >= 16:
        score += 1
    if result["has_lowercase"]:
        score += 1
    if result["has_uppercase"]:
        score += 1
    if result["has_digit"]:
        score += 1
    if result["has_special"]:
        score += 1

    if score <= 2:
        return "極弱", 0
    elif score <= 4:
        return "弱", 1
    elif score <= 5:
        return "中等", 2
    elif score <= 6:
        return "強", 3
    else:
        return "極強", 4


def demo():
    print("=" * 56)
    print("密碼強度檢測工具")
    print("=" * 56)

    if len(sys.argv) > 1:
        password = sys.argv[1]
    else:
        print("\n請輸入密碼進行檢測（或使用命令列：python3 pw_check.py <密碼>）")
        password = input("\n密碼: ")

    result = check_password_strength(password)
    crack_time = estimate_crack_time(password)
    rating, score = get_strength_rating(result)

    print(f"\n{'=' * 56}")
    print(f"密碼: {'*' * len(password)}")
    print(f"{'=' * 56}")

    print("\n[檢查結果]")
    print(f"  長度: {result['length']} 個字元")
    print(f"  小寫字母: {'是' if result['has_lowercase'] else '否'}")
    print(f"  大寫字母: {'是' if result['has_uppercase'] else '否'}")
    print(f"  數字: {'是' if result['has_digit'] else '否'}")
    print(f"  特殊符號: {'是' if result['has_special'] else '否'}")

    print(f"\n  暴力破解時間估算: {crack_time}")
    print(f"  強度評級: {rating}")

    if result["errors"]:
        print(f"\n[問題]")
        for error in result["errors"]:
            print(f"  - {error}")

    print(f"\n{'=' * 56}")

    return score


if __name__ == "__main__":
    demo()