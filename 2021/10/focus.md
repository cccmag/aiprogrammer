# Python 測試與品質確保 — 主題介紹

## 為什麼測試如此重要？

軟體錯誤的代價隨著發現階段推遲而指數成長。開發早期發現問題，修復成本可能只有幾分鐘；而在產品部署後才發現，則可能造成數小時的損失。自動化測試是建立快速回饋循環的關鍵。

## Python 測試生態系統

Python 提供了豐富的測試工具選擇。pytest 以其简洁的語法和強大的外掛生態成為事實標準；unittest 作為標準庫提供了完整的物件導向測試框架；doctest 允許將測試寫在文件字串中，實現文件和測試一體化。

## 測試金字塔

一個健康的測試策略遵循測試金字塔原則：大量的單元測試（基礎）、适量的整合測試（中層）、少量的端對端測試（頂層）。不同層級的測試有不同目的和成本，需要合理分配資源。

## 靜態類型檢查

Python 3.5 引入的類型標註逐漸成熟，mypy、pyright 等工具使得靜態類型檢查成為可能。這不僅能提前發現錯誤，還能改善 IDE 支援和程式碼可讀性。

## CI/CD 與自動化

現代開發流程中，CI/CD 流水線是品質保障的最後防線。每次程式碼變更都會觸發自動化測試，確保新程式碼不會破壞既有功能。GitHub Actions、GitLab CI、Jenkins 等工具使這一切變得簡單。

## 本期導覽

[focus1](focus1.md) 介紹 pytest 核心概念與外掛生態。[focus2](focus2.md) 探討 doctest 的獨特價值。[focus3](focus3.md) 深入 unittest 框架。[focus4](focus4.md) 討論類型標註與 mypy。[focus5](focus5.md) 分析測試覆蓋率。[focus6](focus6.md) 展示 CI/CD 整合。[focus7](focus7.md) 涵蓋整合測試策略。

## 參考資源

- pytest 文件：https://www.google.com/search?q=pytest+documentation
- mypy 文件：https://www.google.com/search?q=mypy+documentation