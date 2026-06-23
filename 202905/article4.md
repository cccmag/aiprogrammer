# 程式碼生成評估 (SWE-bench)

## 1. SWE-bench 的背景

SWE-bench 由普林斯頓大學開發，評估 LLM 解決真實 GitHub issue 的能力。模型需閱讀 issue 描述、理解程式碼庫、產生修補程式，並通過單元測試驗證。

## 2. 任務結構

每個 SWE-bench 實例包含：GitHub 仓库快照、issue 描述、基準提交（base commit）與測試套件。模型需產生 `git diff` 格式的修補程式。

```python
# 評估流程示意
def evaluate_patch(model, instance):
    repo = instance["repo"]
    issue = instance["issue"]
    base_commit = instance["base_commit"]
    test_patch = instance["test_patch"]
    patch = model.generate_patch(repo, issue, base_commit)
    apply_result = apply_patch(repo, base_commit, patch)
    return test_patch(patch) if apply_result else "FAILED"
```

## 3. 評估指標

主要指標為解決率（Resolve Rate）：修補程式通過全部測試的比例。SWE-bench Verified 子集由專業開發者驗證，提供更可靠的評估基準。

## 4. 挑戰與限制

SWE-bench 難度高，即使頂尖模型解決率仍低於 50%。常見失敗模式包括：誤解 issue、修改範圍過大或過小、引入語法錯誤等。

## 5. 延伸基準

SWE-bench Multilingual 擴展至 JavaScript、TypeScript、Rust 等語言。SWE-bench Lite 則精簡為 300 個實例，降低評估成本。

## 6. 結語

SWE-bench 重新定義了程式碼生成評估——從簡單的函數生成邁向真實軟體工程場景。它揭示了當前模型在程式碼理解、錯誤定位與修補生成方面的真實能力邊界。

- https://www.google.com/search?q=SWE-bench+code+generation+benchmark
- https://www.google.com/search?q=SWE-bench+verified+resolve+rate
