# Agent 經濟的治理（2026-2029）

## 為何需要治理？

Agent 經濟如果缺乏治理，會出現市場失靈：壟斷、欺詐、資訊不對稱。去中心化自治組織（DAO）是 Agent 治理的主要形式。

## 治理層級

| 層級 | 決策內容 | 投票主體 |
|------|----------|----------|
| 協定層 | 共識規則、手續費 | 代幣持有者 |
| 市場層 | 服務標準、仲介規則 | Agent 營運者 |
| 應用層 | 特定 Agent 社群規則 | Agent 本身 |

## 治理模式

### 1. 代幣投票（Token-based）

最簡單的治理模式，一幣一票。但容易導致富豪統治（plutocracy）。

### 2. 聲譽投票（Reputation-based）

根據 Agent 的聲譽加權投票，聲譽越高權重越大。但聲譽系統本身需要信任。

### 3. 二次投票（Quadratic Voting）

成本 = (票數)²，讓小規模參與者的意見也能被聽見：

```python
class QuadraticVoting:
    def __init__(self):
        self.votes = {}

    def cast(self, voter, proposal, voice_credits):
        cost = voice_credits ** 2
        if voter.balance >= cost:
            voter.balance -= cost
            if proposal not in self.votes:
                self.votes[proposal] = 0
            self.votes[proposal] += voice_credits
            return True
        return False

dao = QuadraticVoting()
voters = [Agent("A", 100, []), Agent("B", 10, []), Agent("C", 5, [])]
dao.cast(voters[0], "提高手續費", 5)  # 花費 25
dao.cast(voters[1], "提高手續費", 3)  # 花費 9
dao.cast(voters[2], "降低手續費", 2)  # 花費 4
print(f"支持提高手續費票數: {dao.votes.get('提高手續費', 0)}")
print(f"支持降低手續費票數: {dao.votes.get('降低手續費', 0)}")
```

## 人類在治理中的角色

即使經濟參與者主要是 Agent，人類仍需扮演：

- **緊急暫停**：在系統異常時暫停合約
- **憲法性原則**：定義不可更改的基本規則
- **升級決策**：重大協定升級需要人類共識

## 治理攻擊與防禦

治理攻擊包括收買投票權、提案洪水、閃電貸投票等。防禦方法包括時間鎖、投票激勵、和反合謀機制。

## 參考資料

- [DAO 治理模型比較](https://www.google.com/search?q=DAO+governance+models+comparison)
- [二次投票理論](https://www.google.com/search?q=quadratic+voting+mechanism+design)
- [閃電貸治理攻擊](https://www.google.com/search?q=flash+loan+governance+attack)
