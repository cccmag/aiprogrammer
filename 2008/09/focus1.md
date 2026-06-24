# 分散式版本控制的興起

## 集中式版本控制的限制

### CVS 和 SVN

```python
# 集中式模型
centralized_model = {
    'server': '唯一真實來源',
    'network': '必需才能操作',
    'failure': '單點故障',
    'branch': '昂貴且繁瑣'
}
```

### 問題

1. **網路依賴**：需要網路連線才能提交或更新
2. **單點故障**：伺服器故障時無法工作
3. **分支昂貴**：建立分支需要複製整個倉庫
4. **速度慢**：每次操作都需要網路傳輸

## 分散式版本控制的優點

### 每個客戶端都是完整的倉庫

```python
# 分散式模型
distributed_model = {
    '每個克隆': '完整的倉庫副本',
    '離線操作': '可獨立工作',
    '快速分支': '本地分支無成本',
    '無單點故障': '對等網路'
}
```

### 常見 DVCS

| 系統 | 開發者 | 特點 |
|------|--------|------|
| Git | Linus Torvalds | 速度最快 |
| Mercurial | Matt Mackall | 簡單易用 |
| Bazaar | Canonical | 彈性設計 |
| Darcs | David Roundy | 理論優雅 |

## Git 的起源

### 為何需要新系統？

```python
# BitKeeper 的限制
bitkeeper_issues = [
    '專有軟體',
    '許可變更',
    '不能自由使用'
]
```

### Git 的設計目標

```python
git_design_goals = {
    '速度': '比 Mercurial 更快',
    '簡單設計': '易於理解和擴展',
    '非線性開發': '強大的分支合併能力',
    '完全分散': '每個克隆都是完整的',
    '大型專案': '支援 Linux 核心等級'
}
```

## 與 SVN 的比較

| 特性 | Git | SVN |
|------|-----|-----|
| 類型 | 分散式 | 集中式 |
| 克隆 | 完整倉庫 | 僅工作副本 |
| 離線操作 | 完全支援 | 有限支援 |
| 分支 | 快速本地 | 較慢 |
| 合併 | 強大 | 複雜 |
| 學習曲線 | 較陡 | 較平緩 |

## 結論

分散式版本控制解決了集中式系統的諸多限制。Git 的速度和分支能力使其成為大型開源專案的首選。

---

**延伸閱讀**

- [Git 核心概念與架構](focus2.md)
- [GitHub 與社交程式設計](focus3.md)
- [Git+vs+SVN](https://www.google.com/search?q=Git+vs+SVN+distributed+version+control)