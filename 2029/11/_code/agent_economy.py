"""
Agent 經濟模擬器 — Agent 市場、交易、聲譽系統
"""
import math
import random
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AgentService:
    name: str
    price: float
    quality: float  # 0-1
    provider: str

@dataclass
class Transaction:
    buyer: str
    seller: str
    service: str
    amount: float
    rating: int  # 1-5

class AgentMarketplace:
    def __init__(self):
        self.services: list[AgentService] = []
        self.transactions: list[Transaction] = []
        self.reputations: dict[str, float] = {}
    def list_service(self, svc: AgentService):
        self.services.append(svc)
        self.reputations.setdefault(svc.provider, 1.0)
    def search(self, query: str, max_price: float = 100) -> list[AgentService]:
        return [s for s in self.services if s.price <= max_price]
    def transact(self, buyer: str, seller: str, service: str, amount: float) -> Transaction:
        rating = random.randint(1, 5)
        tx = Transaction(buyer, seller, service, amount, rating)
        self.transactions.append(tx)
        delta = (rating - 3) / 10
        self.reputations[seller] = max(0, min(1, self.reputations.get(seller, 0.5) + delta))
        return tx
    def agent_value(self, agent_id: str) -> float:
        rep = self.reputations.get(agent_id, 0.5)
        return rep * 1000

def demo():
    print("=== Agent Economy Simulator ===\n")
    market = AgentMarketplace()
    market.list_service(AgentService("code_review", 5.0, 0.9, "CodeBot"))
    market.list_service(AgentService("data_analysis", 10.0, 0.85, "DataBot"))
    market.list_service(AgentService("translation", 3.0, 0.95, "TransBot"))
    print("  Available services:")
    for s in market.services:
        print(f"    {s.name}: ${s.price} (quality: {s.quality}) by {s.provider}")
    tx = market.transact("User1", "CodeBot", "code_review", 5.0)
    print(f"\n  Transaction: {tx.buyer} → {tx.seller} for {tx.service} (${tx.amount}, rating: {tx.rating})")
    print(f"  CodeBot reputation: {market.reputations['CodeBot']:.2f}")
    print(f"  CodeBot value: ${market.agent_value('CodeBot'):.0f}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
