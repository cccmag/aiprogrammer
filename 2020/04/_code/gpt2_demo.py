import torch

def demo():
    print("=" * 60)
    print("GPT-2 文字生成示範")
    print("=" * 60)

    try:
        from transformers import GPT2LMHeadModel, GPT2Tokenizer
    except ImportError:
        print("\n錯誤：請先安裝 transformers")
        print("執行：pip install torch transformers")
        return

    print("\n[1] 載入模型...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    print("    GPT-2 模型載入成功")

    print("\n[2] 模型資訊")
    n_params = sum(p.numel() for p in model.parameters())
    print(f"    參數數量: {n_params:,}")

    prompts = [
        "Artificial intelligence is transforming",
        "In the future, computers will",
        "The invention of the wheel was",
    ]

    print("\n[3] 文字生成範例")
    print("-" * 60)

    for i, prompt in enumerate(prompts, 1):
        print(f"\n範例 {i}: \"{prompt}...\"")

        inputs = tokenizer(prompt, return_tensors="pt")

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=30,
                temperature=0.8,
                do_sample=True,
                top_k=50,
                pad_token_id=tokenizer.eos_token_id
            )

        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"生成結果: {generated}")

    print("\n" + "=" * 60)
    print("示範完成")
    print("=" * 60)


if __name__ == "__main__":
    demo()