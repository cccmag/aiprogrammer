# AI 輔助雜誌編輯實戰手冊

## 前言

本文記錄使用 AI（OpenCode + Big Pickle）編輯《AI 程式人雜誌》的完整流程與技巧。這些經驗來自於 2026 年 3 月號的實際編輯過程，主題是「Lambda Calculus 與函數式編程」。

---

## 一、專案結構設計

### 1.1 目錄規劃

```
202603/                    # 當期雜誌目錄
├── _code/                 # 程式範例目錄
│   └── lambdaCalculus.py # Lambda Calculus 實作
├── focus.md               # 本期主題概覽
├── focus1-7.md           # 主題深入文章
├── focus_code.md         # 主題程式碼文件
├── news.md               # 本月新知
├── article1-10.md       # 精選文章
├── articles.md          # 文章索引
├── end.md              # 結語
└── README.md           # 雜誌總索引
```

### 1.2 命名慣例

- **焦點主題**：使用 `focus*.md` 命名
- **程式實作**：放在 `_code/` 目錄中
- **程式文件**：`focus_code.md` 作為對應的說明文件
- **文章集錦**：`article*.md` 為單篇文章，`articles.md` 為索引

---

## 二、AI 協作流程

### 2.1 任務分解策略

不要一次要求 AI 完成整本雜誌，而是分層次逐步完成：

1. **先建立骨架**：先完成目錄結構、主要連結
2. **再填入內容**：針對每個檔案逐步填充內容
3. **最後除錯修正**：檢查連結、程式碼正確性

### 2.2 上下文傳遞

在對話開始時，明確告知 AI：

- 當前工作目錄
- 專案目的（編輯雜誌）
- 已完成的檔案列表
- 當前任務目標

### 2.3 進度追蹤

使用摘要開頭（system prompt），讓 AI 知道：

- 已完成的工作
- 當前任務
- 遇到的問題
- 下一個步驟

---

## 三、程式碼處理技巧

### 3.1 嵌套括號問題

**問題**：在 Python Lambda Calculus 實作中，深層嵌套的 Church 數字定義（如 `f(f(f(f(f(f(f(f(f(x))))))))`）在寫入檔案時會被截斷。

**解決方案**：使用 Python 本身來生成和寫入檔案

```bash
python3 << 'EOF'
# 用 Python 程式碼生成並寫入檔案
lines = []
for n in range(11):
    expr = "f(" * n + "x" + ")" * n
    lines.append(f"{names[n]} = lambda f: lambda x: {expr}")
with open('lambdaCalculus.py', 'w') as f:
    f.write('\n'.join(lines))
EOF
```

### 3.2 多檔案連結維護

**策略**：當重新命名檔案時

1. 使用 `mv` 批次重新命名
2. 用 `grep` 找出所有引用舊檔名的地方
3. 使用 `edit` 工具的 `replaceAll` 參數一次性替換

```bash
# 批次重新命名
mv history1.md focus1.md
mv history2.md focus2.md
# ...

# 找出所有引用
grep -rn "history1.md" *.md

# 批次替換
edit oldString="history1.md" newString="focus1.md" replaceAll=true
```

### 3.3 程式碼測試

在 Python 檔案中實作 `test()` 函式：

```python
def test():
    print("Testing Church numbers:")
    for n, name in [...]:
        print(f"{name} = {church_to_int(n)}")

if __name__ == "__main__": test()
```

這樣可以快速驗證程式碼的正確性。

---

## 四、文件一致性維護

### 4.1 連結檢查清單

每次修改檔案結構後，檢查：

- [ ] README.md 的目錄連結
- [ ] focus.md 的大綱連結
- [ ] articles.md 的文章連結
- [ ] 所有交叉引用是否正確

### 4.2 批次取代技巧

使用 `replaceAll=true` 參數時要小心，確保舊字串具有唯一性：

```python
# 危險：會取代所有出現
edit oldString="主題聚焦" newString="本期焦點" replaceAll=true

# 安全：針對具體位置
edit oldString="# 主題聚焦" newString="# 本期焦點"
```

### 4.3 內文同步

修改標題時，要一併更新：

- 檔案開頭的標題 (`# Title`)
- 結語段落中的標題提及
- 所有導航連結中的標題文字

---

## 五、Y Combinator 實作經驗

### 5.1 Python Eager Evaluation 限制

Python 使用嚴格求值（eager evaluation），標準 Y combinator 會導致無限遞迴。

**解決方案**：使用 call-by-name 風格的 Y combinator

```python
# 標準 Y（會無限遞迴）
Y = lambda f: (lambda x: f(x(x)))(lambda x: f(x(x)))

# 解決方案：使用普通 Python 函式包裝遞迴
def church_factorial(n):
    if church_to_bool(IS_ZERO(n)):
        return ONE
    return MULT(n)(church_factorial(PRED(n)))
```

### 5.2 混合實作策略

展示純 Lambda Calculus 版本的同時，也提供可執行的 Python 實作：

- Church 編碼：純 Lambda 定義
- 複雜運算：使用 Python 輔助函式
- Y combinator：說明原理，實際用 Python 函式

---

## 六、常用指令參考

### 6.1 檔案操作

```bash
# 批次重新命名
for f in history*.md; do mv "$f" "${f/history/focus}"; done

# 找出所有引用
grep -rn "pattern" /path/to/dir

# 驗證檔案內容
head -n 20 file.md
tail -n 10 file.md
```

### 6.2 程式測試

```bash
# 測試 Python 程式
python3 _code/lambdaCalculus.py

# 檢查語法
python3 -m py_compile _code/lambdaCalculus.py
```

### 6.3 目錄結構

```bash
# 列出所有 Markdown 檔案
ls *.md

# 列出程式碼目錄
ls _code/

# 計算行數
wc -l *.md
```

---

## 七、常見問題與解決

### 7.1 AI 忘記上下文

**現象**：AI 在長對話中忘記已完成的工作

**解決**：
1. 定期提供進度摘要
2. 使用 system prompt 記錄狀態
3. 明確指出下一步

### 7.2 編輯衝突

**現象**：檔案被多次修改後出現不一致

**解決**：
1. 使用 `read` 工具重新讀取檔案
2. 使用 `replaceAll` 確保一致性
3. 完成後立即驗證

### 7.3 特殊字元問題

**現象**：中文或特殊符號在某些工具中無法正確處理

**解決**：
1. 使用 Python 處理字串
2. 避免使用 heredoc 處理複雜內容
3. 直接使用 write 工具

---

## 八、最佳實踐總結

1. **分層建構**：先結構、後內容、最後除錯
2. **明確命名**：一致的命名慣例便於維護
3. **自動化測試**：每個程式檔案都要有 test()
4. **連結檢查**：修改後立即驗證所有引用
5. **進度摘要**：讓 AI 隨時知道專案狀態
6. **替代方案**：遇到限制時準備繞過方案

---

## 結語

AI 輔助編輯是一種新型態的協作模式。AI 擅長快速生成初稿、處理重複性任務、提供建議；但需要人類編輯把關品質、維護一致性、引導方向。掌握這些技巧，能讓 AI 輔助編輯的效率大幅提升。

---

*本文為《AI 程式人雜誌》編輯技巧記錄*
