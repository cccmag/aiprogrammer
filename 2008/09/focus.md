# 本期焦點

## Git 與分散式版本控制 — 社交程式設計新時代

### 引言

2008 年是分散式版本控制系統（DVCS）蓬勃發展的一年。GitHub 的上線開創了社交程式設計的新模式。

本期雜誌將帶您深入了解 Git 的設計理念和分散式版本控制的優勢。

---

## 大綱

* [Git 程式實作](focus_code.md)
   - 基本命令
   - 分支操作
   - 遠端協作

1. [分散式版本控制的興起](focus1.md)
   - CVS/SVN 的限制
   - Git、Mercurial、Bazaar
   - 分散式優勢

2. [Git 核心概念與架構](focus2.md)
   - Blob、Tree、Commit
   - 物件儲存
   - 指標系統

3. [GitHub 與社交程式設計](focus3.md)
   - Fork 模式
   - Pull Request
   - 程式碼審查

4. [分支策略與工作流程](focus4.md)
   - Git Flow
   - GitHub Flow
   - 熱修補流程

5. [常用 Git 命令詳解](focus5.md)
   - init, clone, add, commit
   - branch, checkout, merge
   - push, pull, fetch

6. [Git 進階技巧](focus6.md)
   - Rebase
   - Stash
   - Bisect

7. [版本控制的未來](focus7.md)
   - GitHub Enterprise
   - 整合趨勢
   - 雲端化

---

## 濃縮回顧

### 集中式 vs 分散式

```
集中式（SVN）：
        ┌─────────┐
        │ Server  │ ← 單點故障
        │  (唯一) │
        └────┬────┘
             │ 網路
      ┌──────┼──────┐
      ↓      ↓      ↓
   Client  Client  Client

分散式（Git）：
   ┌───┐   ┌───┐   ┌───┐
   │Dev│   │Dev│   │Dev│
   └─┬─┘   └─┬─┘   └─┬─┘
     │       │       │
     └───┬───┘       │
         │         (可選) 共享
         └───────────┘
```

### Git 儲存模型

```
┌────────────────────────────────────┐
│            Git 物件                 │
├────────────────────────────────────┤
│                                    │
│   Commit ───→ Tree ──→ Blob (file) │
│     │              └──→ Blob       │
│     │                               │
│     └──→ Parent Commit              │
│                                    │
└────────────────────────────────────┘
```

### 基本工作流程

```bash
git init                    # 初始化
git add file.txt            # 暂存
git commit -m "message"     # 提交
git push origin main        # 推送
git pull origin main        # 拉取
git branch new-feature      # 建立分支
git checkout new-feature    # 切換分支
git merge new-feature       # 合併分支
```

---

## 結論與展望

Git 和 GitHub 改變了開發者協作的方式。分散式版本控制和社交程式設計將繼續影響軟體開發的未來。

---

## 延伸閱讀

- [分散式版本控制的興起](focus1.md)
- [GitHub 與社交程式設計](focus3.md)

---

*本期雜誌到此結束。感謝您的閱讀！*