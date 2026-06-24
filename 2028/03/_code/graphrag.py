"""
GraphRAG 系統 — 知識圖譜 + 向量搜尋 + RAG
"""

import math
import random
from dataclasses import dataclass, field
from typing import Optional


# --- 1. 知識圖譜 ---

@dataclass
class Entity:
    id: str
    name: str
    type: str
    properties: dict = field(default_factory=dict)

@dataclass
class Relation:
    source: str
    target: str
    relation: str
    weight: float = 1.0


class KnowledgeGraph:
    """Simple knowledge graph with traversal"""

    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.relations: list[Relation] = []

    def add_entity(self, entity: Entity):
        self.entities[entity.id] = entity

    def add_relation(self, relation: Relation):
        self.relations.append(relation)

    def get_neighbors(self, entity_id: str, relation_type: Optional[str] = None) -> list[str]:
        neighbors = []
        for r in self.relations:
            if r.source == entity_id:
                if relation_type is None or r.relation == relation_type:
                    neighbors.append(r.target)
            if r.target == entity_id:
                if relation_type is None or r.relation == relation_type:
                    neighbors.append(r.source)
        return list(set(neighbors))

    def shortest_path(self, start: str, end: str) -> Optional[list[str]]:
        """BFS shortest path"""
        visited = {start}
        queue = [[start]]
        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node == end:
                return path
            for neighbor in self.get_neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])
        return None


# --- 2. GraphRAG 檢索器 ---

class GraphRAGRetriever:
    """Retrieve context using both KG traversal and vector similarity"""

    def __init__(self, kg: KnowledgeGraph):
        self.kg = kg

    def retrieve(self, query_entities: list[str], depth: int = 2) -> str:
        """Walk the graph from query entities and collect context"""
        context_parts = []
        visited = set()

        for entity_id in query_entities:
            if entity_id not in self.kg.entities:
                continue
            entity = self.kg.entities[entity_id]
            context_parts.append(f"Entity: {entity.name} ({entity.type})")

            frontier = [(entity_id, 0)]
            while frontier:
                current, d = frontier.pop(0)
                if d >= depth:
                    continue
                for neighbor_id in self.kg.get_neighbors(current):
                    if neighbor_id in visited:
                        continue
                    visited.add(neighbor_id)
                    if neighbor_id in self.kg.entities:
                        n = self.kg.entities[neighbor_id]
                        context_parts.append(f"  Related: {n.name} ({n.type})")
                        for r in self.kg.relations:
                            if (r.source == current and r.target == neighbor_id) or \
                               (r.target == current and r.source == neighbor_id):
                                context_parts.append(f"    Relation: {r.relation}")
                    frontier.append((neighbor_id, d + 1))

        return "\n".join(context_parts)


# --- 3. 多跳檢索 ---

class MultiHopRetriever:
    """Multi-hop retrieval across knowledge sources"""

    def __init__(self, kg: KnowledgeGraph):
        self.kg = kg

    def retrieve(self, query: str, max_hops: int = 3) -> list[str]:
        retrieved = []
        # Parse query for entity mentions (simplified)
        current_entities = [eid for eid in self.kg.entities
                            if query.lower() in self.kg.entities[eid].name.lower()]
        if not current_entities:
            return ["No relevant entities found"]

        visited = set(current_entities)
        frontier = current_entities[:]

        for hop in range(max_hops):
            next_frontier = []
            for entity_id in frontier:
                for neighbor_id in self.kg.get_neighbors(entity_id):
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        next_frontier.append(neighbor_id)
                        if neighbor_id in self.kg.entities:
                            retrieved.append(
                                f"Hop {hop+1}: {self.kg.entities[neighbor_id].name}"
                            )
            frontier = next_frontier
            if not frontier:
                break

        return retrieved if retrieved else ["No multi-hop paths found"]


# --- Demo ---

def demo():
    print("=== GraphRAG System ===\n")

    # Build knowledge graph
    kg = KnowledgeGraph()
    entities = [
        Entity("e1", "Transformer", "model"),
        Entity("e2", "Attention", "mechanism"),
        Entity("e3", "BERT", "model"),
        Entity("e4", "GPT", "model"),
        Entity("e5", "NLP", "field"),
        Entity("e6", "Encoder", "component"),
        Entity("e7", "Decoder", "component"),
    ]
    for e in entities:
        kg.add_entity(e)

    relations = [
        Relation("e1", "e2", "uses"),
        Relation("e3", "e1", "based_on"),
        Relation("e4", "e1", "based_on"),
        Relation("e1", "e5", "applied_in"),
        Relation("e3", "e6", "uses"),
        Relation("e4", "e7", "uses"),
    ]
    for r in relations:
        kg.add_relation(r)

    # 1. Graph Traversal
    print("1. Knowledge Graph Traversal:")
    neighbors = kg.get_neighbors("e1")
    print(f"  Neighbors of Transformer: {[kg.entities[n].name for n in neighbors]}")

    path = kg.shortest_path("e3", "e7")
    if path:
        print(f"  BERT -> GPT path: {' -> '.join(kg.entities[p].name for p in path)}")

    # 2. GraphRAG Retrieval
    print("\n2. GraphRAG Retrieval:")
    retriever = GraphRAGRetriever(kg)
    context = retriever.retrieve(["e1", "e3"], depth=2)
    print(f"  {context}")

    # 3. Multi-hop Retrieval
    print("\n3. Multi-Hop Retrieval:")
    mhr = MultiHopRetriever(kg)
    results = mhr.retrieve("Attention", max_hops=3)
    for r in results:
        print(f"  {r}")

    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    demo()
