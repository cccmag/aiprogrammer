# Anthropic Claude 5 發布：可解釋 AI 的新標竿

## 概述

2026 年 6 月 9 日，Anthropic 正式發布 Claude Fable 5 與 Claude Mythos 5，這是第五代 Claude 模型系列。Fable 5 是對外公開的最強版本，Mythos 5 則透過 Project Glasswing 提供給經過嚴格審核的研究機構——後者移除了安全分類器，專注於前沿安全研究。

```
Claude 5 系列規格
─────────────────

Claude Fable 5（公開版本）
├── 上下文窗口：100 萬 tokens
├── 最大輸出：128K tokens
├── 定價：$10 / $50 每百萬 tokens（輸入 / 輸出）
├── 自適應思考：始終啟用
└── 推理模式：effort 參數控制思考深度

Claude Mythos 5（Glasswing 限定）
├── 與 Fable 5 相同能力
├── 無安全分類器限制
└── 僅限合作的生物/化學/網路安全研究
```

## Transparent Attention：可解釋性的突破

Claude 5 最大的技術亮點是 Natural Language Autoencoders（NLA），一種讓模型用自然語言解釋自身內部激活的方法：

```
NLA 工作原理
─────────────────

輸入："請完成這個對聯：風聲雨聲讀書聲，聲聲入耳"

Claude 內部激活：[0.23, -0.87, 0.45, ..., 0.12]  (4096 維)
                    ↓
NLA 編碼器將激活轉換為文字解釋：
"模型正在構思與'聲'相關的押韻詞，搜索家事國事天下事..."
                    ↓
NLA 解碼器從文字重建原始激活
重建誤差 → 評估解釋品質
```

傳統的可解釋性工具（如稀疏自編碼器、歸因圖）雖然有用，但需要訓練有素的研究人員仔細解讀。NLA 的突破在於：

- **自動化解釋**：模型自行描述其推理過程
- **雙向驗證**：從解釋重建原始激活，確保解釋忠實度
- **實際效益**：在安全審計中，使用 NLA 的審計員檢測到違規行為的比例從 <3% 提升到顯著水準

## 幻覺減少 70%

Claude 5 在幻覺控制上實現了質的飛躍。Anthropic 採用了一種稱為「信念殺死」（belief killing）的訓練技術：

```
幻覺率比較（MMLU + 開放生成評估）
─────────────────

Claude Opus 4.8     ████████████████░░░░  18%
Claude Fable 5      ██████░░░░░░░░░░░░░░   5.4%
GPT-6               ███████░░░░░░░░░░░░░   6.8%
Gemini 3 Ultra      █████████░░░░░░░░░░░   9.2%

降低幅度：Fable 5 相較 Opus 4.8 減少約 70%
```

關鍵技術包括：

1. **自適應思考**：模型自動決定何時需要更多推理步驟，而非固定深度
2. **程式執行驗證**：在數學和邏輯問題上，模型主動編寫並執行程式碼來驗證答案
3. **長期任務預算**：透過 `task-budgets-2026-03-13` 標頭，支援跨數天的非同步自主工作

## 對抗攻擊成功率降低 85%

安全性是 Claude 5 的核心設計目標。Fable 5 內建三層安全架構：

```
Claude Fable 5 安全架構
─────────────────

第一層：輸入分類器
├── 偵測越獄嘗試（jailbreak）
├── 偵測提示注入（prompt injection）
└── 延遲：<50ms

第二層：模型內建安全
├── 對抗訓練（adversarial training）
├── 價值觀對齊（constitutional AI）
└── 信念穩定性訓練

第三層：輸出分類器
├── 偵測有害內容生成
├── 偵測幻覺高危區域
└── 可選擇的安全模式
```

在 Anthropic 內部的紅隊測試中，Claude 5 的攻擊成功率僅為 2.7%，而 Opus 4.8 為 18%，GPT-6 為 12.3%。

## 基準測試表現

Claude Fable 5 在幾乎所有主要基準測試上達到或超越 GPT-6：

| 基準測試 | Fable 5 | GPT-6 | Gemini 3 Ultra |
|---------|---------|-------|---------------|
| MMLU | 93.4% | 93.1% | 92.0% |
| HumanEval | 96.8% | 96.2% | 94.5% |
| SWE-bench Verified | 72.3% | 70.1% | 65.8% |
| MATH | 95.1% | 94.8% | 93.2% |
| Hebbia Finance | 89.2% | 86.5% | 84.0% |
| GPQA (博士級) | 78.5% | 76.9% | 74.1% |

其中 SWE-bench Verified 的分數尤為值得關注——這是真實 GitHub issue 修復的測試，Fable 5 是首個突破 70% 的模型。

## 程式開發實戰表現

```python
# Claude Fable 5 在長上下文程式開發中的表現

# 情境：將一個 5000 行的 React 專案從 Class Component 遷移到 Hooks
# 以下為 Claude Fable 5 自主生成的遷移計畫與部分實作

"""
遷移計畫：
1. 分析所有 Class Component 的生命週期方法
2. 映射到對應的 Hooks API
   - componentDidMount → useEffect([], [])
   - componentDidUpdate → useEffect()
   - shouldComponentUpdate → React.memo
   - componentWillUnmount → useEffect cleanup
3. 將 this.state / this.setState → useState
4. 提取共用邏輯到自訂 Hooks
"""

# 自動生成的 Hook 範例
function useUserData(userId) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const controller = new AbortController()

    async function fetchUser() {
      try {
        setLoading(true)
        const response = await fetch(`/api/users/${userId}`, {
          signal: controller.signal
        })
        if (!response.ok) throw new Error('Failed to fetch')
        const data = await response.json()
        setUser(data)
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message)
        }
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
    return () => controller.abort()
  }, [userId])

  return { user, loading, error }
}
```

Anthropic 報告稱，Claude Fable 5 能夠自主完成「一年前需要一百次提示才能完成的應用程式」，並且「在客戶真正遇到困難時，是我們自己也會使用的模型」。

## 結語

Claude Fable 5 代表著 AI 可解釋性和安全性的重要里程碑。NLA 技術讓模型的「黑盒子」首次對人類打開了一扇窗——這不僅提升信任度，也讓安全研究人員有了前所未有的工具。在能力方面，Fable 5 在多項基準測試上超越 GPT-6，證明了「安全不等於妥協能力」。隨著 100 萬 token 上下文和 128K 輸出的支援，軟體開發、科學研究與知識工作都將迎來新一波效率提升。

## 延伸閱讀

- [Anthropic Claude Fable 5 官方公告](https://www.anthropic.com/news/claude-fable-5-mythos-5)
- [Natural Language Autoencoders 研究論文](https://www.anthropic.com/research/natural-language-autoencoders)
- [Claude 5 API 文件](https://platform.claude.com/docs/en/about-claude/models/introducing-claude-fable-5-and-claude-mythos-5)
- [可解釋 AI 技術](https://www.google.com/search?q=interpretable+AI+transparent+attention+2026)
- [Claude 5 vs GPT-6 基準測試比較](https://www.google.com/search?q=Claude+Fable+5+benchmarks+comparison+GPT-6)

---

*本文為 AI 程式人雜誌 2026 年 6 月號 AI 技術專題之一。*
