# 為什麼 Git 勝過 SVN？

## 前言

在版本控制領域，Git 和 SVN 是兩個最被廣泛使用的系統。本文探討為什麼 Git 逐漸成為主流選擇。

---

## 分散式 vs 集中式

### SVN 的運作方式

 SVN 是集中式版本控制系統，所有歷史記錄儲存在中央伺服器。

**優點：**
- 管理簡單，權限控制集中
- 適合需要嚴格權限管理的企業

**缺點：**
- 必須連線才能操作
- 中央伺服器當機影響整個團隊
- 單點故障風險

### Git 的運作方式

Git 是分散式系統，每個克隆都是完整的倉庫。

**優點：**
- 離線可正常工作
- 完整的本地歷史
- 沒有單點故障

**缺點：**
- 學習曲線較陡
- 初期需要更多磁碟空間

---

## 效能比較

### 分支操作

Git 建立分支只是建立指標，幾乎零成本：

```bash
# Git
git branch new-feature    # 瞬間完成
git checkout new-feature  # 瞬間完成

# SVN
svn copy trunk branches/new-feature  # 需要複製資料
```

### 歷史查詢

```bash
# Git - 本地完成
git log --oneline -10

# SVN - 需要網路
svn log -l 10
```

---

## 合併能力

Git 的三路合併演算法比 SVN 的互動式合併更強大：

```bash
# Git 合併
git merge feature-branch

# SVN 合併
svn merge -r 1000:HEAD branches/feature
```

### 衝突標記

Git 的衝突標記更清晰：

```markdown
<<<<<<< HEAD
 Ours changes
=======
 Theirs changes
>>>>>>> feature-branch
```

---

## 社群與生態

### GitHub 的影響

GitHub 的崛起離不開 Git 的技術優勢：

- 豐富的開源專案
- 完善的 Pull Request 功能
- 強大的社群互動

[搜尋 GitHub vs SVN comparison](https://www.google.com/search?q=GitHub+vs+SVN+comparison)

---

## 遷移策略

從 SVN 遷移到 Git：

```bash
# 使用 git-svn
git svn clone http://svn.example.com/repo -T trunk -b branches -t tags

# 或者使用 svn2git
git svn2git http://svn.example.com/repo
```

---

## 結論

雖然 SVN 在某些企業場景仍有優勢，但 Git 的分散式特性、效能優勢和強大的社群支援，使其成為現代軟體開發的首選。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Git 官方網站](https://git-scm.com/)
- [Atlassian Git 教學](https://www.google.com/search?q=Atlassian+Git+tutorials)