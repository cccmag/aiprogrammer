# 程式碼執行與沙箱技術（2024-2028）

## 讓 AI 寫程式、跑程式、改程式

### 為什麼需要程式碼執行？

LLM 生成文字有個根本弱點：**文字不可驗證**。但程式碼不同——程式要嘛執行正確，要嘛報錯。讓 LLM 生成並執行程式碼，等於賦予它「實驗驗證」的能力。

```python
# 文字回答 vs 程式碼回答
question = "345,678 乘以 987,654 等於多少？"

# 文字模式：模型可能算錯
text_answer = model.generate(f"{question}")  # 不穩定

# 程式碼模式：讓模型寫程式來算，執行後得到精確結果
code = model.generate(f"請寫 Python 程式碼來計算：{question}")
result = execute_sandboxed(code)  # 精確
```

### 程式碼執行架構

2024 年，主流 LLM 平台都內建了程式碼執行功能：

```python
# ChatGPT Code Interpreter（後來改名 Advanced Data Analytics）
# 的簡化版架構
class CodeSandbox:
    def __init__(self):
        self.files = {}      # 檔案系統
        self.libraries = {   # 預裝庫
            "numpy", "pandas", "matplotlib", 
            "scipy", "scikit-learn"
        }

    def execute(self, code):
        restricted_code = self.sanitize(code)
        try:
            result = self.run_in_subprocess(restricted_code)
            return result
        except Exception as e:
            return f"執行錯誤：{e}"
```

### 沙箱技術的演進

沙箱是程式碼執行的核心安全機制：

| 技術 | 隔離程度 | 啟動速度 | 適用場景 |
|------|---------|---------|---------|
| 子程序 | 低 | 快 | 簡單計算 |
| Docker | 中 | 中 | 隔離環境 |
| gVisor | 高 | 中 | 多租戶 |
| Firecracker | 極高 | 快 | 生產環境 |
| WASM | 高 | 極快 | 瀏覽器端 |

```python
# Docker 沙箱執行
import docker

def execute_in_docker(code):
    client = docker.from_env()
    container = client.containers.run(
        image="python:3.12-slim",
        command=["python", "-c", code],
        mem_limit="256m",
        cpu_period=100000,
        cpu_quota=50000,  # 0.5 CPU
        network_disabled=True,  # 禁止網路
        read_only=True,
        remove=True,
        timeout=30
    )
    return container.decode("utf-8")
```

### 2024-2025：Jupyter 整合

Jupyter Notebook 成為 LLM 程式碼執行的天然載體：

```python
# Jupyter Kernel Gateway 整合
import jupyter_client

class JupyterExecutor:
    def __init__(self):
        self.km = jupyter_client.KernelManager(kernel_name="python3")
        self.km.start_kernel()
        self.kc = self.km.client()

    def execute_cell(self, code):
        msg_id = self.kc.execute(code)
        reply = self.kc.get_shell_msg(msg_id)
        return self.extract_result(reply)
```

### 2026：多語言程式碼執行

平台開始支援多語言執行環境：

```python
# 多語言執行器
class MultiLangExecutor:
    def __init__(self):
        self.runtimes = {
            "python": PythonRuntime(),
            "javascript": NodeRuntime(),
            "rust": RustRuntime(wasm=True),
            "sql": SQLRuntime(),
        }

    def execute(self, code, language):
        runtime = self.runtimes.get(language)
        if not runtime:
            return f"不支援的語言：{language}"
        return runtime.run(code)
```

### 2027-2028：自主除錯與迭代

AI 不再只是執行一次程式碼——它會根據結果自主修正：

```python
class SelfDebuggingAgent:
    def solve_with_code(self, problem):
        code = self.generate_initial_code(problem)
        for attempt in range(max_attempts):
            result = self.execute(code)
            if result.success:
                return code, result.output
            
            error = result.error
            fix = self.analyze_error(code, error)
            code = self.apply_fix(code, fix)
        return None, "無法解決"
```

### 程式碼執行的應用

- **資料分析**：上傳 CSV，AI 用 pandas 分析
- **資料視覺化**：生成 matplotlib/seaborn 圖表
- **數學計算**：使用 numpy/scipy 精確計算
- **機器學習**：訓練小型模型並評估
- **API 整合**：撰寫 requests 程式碼呼叫 API

### 安全考量

程式碼執行平台必須防範：

1. **無限循環**：設定 CPU 時間限制
2. **記憶體爆炸**：限制記憶體用量
3. **檔案系統存取**：使用唯讀或隔離檔案系統
4. **網路存取**：預設封鎖網路，按需開放
5. **系統呼叫**：過濾危險的 syscall

### 小結

程式碼執行是「可驗證生成」的關鍵技術。它讓 AI 能夠透過執行和除錯來驗證自己的輸出，大幅提升了生成結果的可靠性。

---

**下一步**：[多模型協作與路由](focus5.md)

## 延伸閱讀

- [OpenAI Code Interpreter 技術分析](https://www.google.com/search?q=OpenAI+Code+Interpreter+technical+details)
- [LLM 程式碼生成的沙箱安全](https://www.google.com/search?q=LLM+code+execution+sandbox+security)
- [Jupyter Kernel Gateway 架構](https://www.google.com/search?q=Jupyter+kernel+gateway+architecture)
