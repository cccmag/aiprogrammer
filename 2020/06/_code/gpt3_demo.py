import os


def demo():
    print("=" * 60)
    print("GPT-3 API 示範")
    print("=" * 60)

    print("\n[說明]")
    print("要使用 GPT-3 API，請先：")
    print("1. 前往 https://openai.com 註冊帳戶")
    print("2. 取得 API Key")
    print("3. 設定環境變數：export OPENAI_API_KEY='your-key'")
    print()

    api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        print("[警告] 未設定 OPENAI_API_KEY")
        print("將展示無法實際呼叫 API 的替代方案")
    else:
        print(f"[成功] API Key 已設定（顯示前5字元: {api_key[:5]}...）")

    print("\n[1] GPT-3 模型層級")

    models = [
        ("davinci", "175B 參數", "最強大"),
        ("curie", "6.7B 參數", "平衡"),
        ("babbage", "1.3B 參數", "快速"),
        ("ada", "350M 參數", "最快"),
    ]

    for name, params, desc in models:
        print(f"  - {name}: {params} ({desc})")

    print("\n[2] Few-shot 範例")

    examples = [
        ("Translate English to French:", [
            ("Hello", "Bonjour"),
            ("Good morning", "Bonjour"),
            ("Thank you", "Merci"),
        ], "Good night"),
    ]

    for task, examples_list, test_input in examples:
        print(f"  任務：{task}")
        print(f"  測試：{test_input}")
        print(f"  預期輸出：根據 Few-shot 示範推測")

        if api_key:
            try:
                import openai
                prompt = f"{task}\n"
                for ex_in, ex_out in examples_list:
                    prompt += f"English: {ex_in}\nFrench: {ex_out}\n"
                prompt += f"English: {test_input}\nFrench:"

                response = openai.Completion.create(
                    model="curie",
                    prompt=prompt,
                    max_tokens=50,
                    temperature=0.0
                )
                print(f"  實際輸出：{response.choices[0].text.strip()}")
            except Exception as e:
                print(f"  API 錯誤：{e}")
        print()

    print("[3] 程式碼生成範例")

    code_prompt = """Write a Python function to calculate factorial:

def factorial(n):"""

    print(f"  Prompt：{code_prompt}")
    print("  （需要 API key 才能實際執行）")

    print("\n" + "=" * 60)
    print("示範完成")
    print("=" * 60)

    if not api_key:
        print("\n提示：要完整測試，請設定 OPENAI_API_KEY 環境變數")


if __name__ == "__main__":
    demo()