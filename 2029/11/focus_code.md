# 程式實作：Agent 經濟模擬器

## 簡介

本實作模擬 Agent 經濟生態，包括 Agent 服務市場、交易系統和聲譽機制。完整程式碼在 `_code/agent_economy.py`。

## 核心元件

### 1. Agent 服務市場

```python
market = AgentMarket()
market.register_service(AgentService("CodeReview", 0.05, 0.95, "Alice"))
```

### 2. 交易系統

```python
ledger = TransactionLedger()
tx = Transaction("Bob", "Alice", "CodeReview", 0.05, "completed")
ledger.record(tx)
```

### 3. 聲譽系統

```python
reputation = ReputationSystem()
score = reputation.calculate_score("Alice")
```

### 4. 經濟模擬

```python
sim = EconomySimulator(market, ledger, reputation)
results = sim.run(steps=100)
```

## 執行方式

```bash
cd _code
python3 agent_economy.py
```

## 延伸練習

1. **串接區塊鏈**：用智慧合約實作交易結算
2. **動態定價**：根據供需自動調整價格
3. **爭議仲裁**：加入去中心化仲裁機制
4. **跨市場互通**：多市場 Agent 流動
5. **視覺化儀表板**：即時顯示經濟指標
