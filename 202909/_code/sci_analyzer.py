"""
科學文獻分析工具 — 論文檢索、摘要提取、趨勢分析
"""
import math
import random
import re
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Paper:
    id: str
    title: str
    abstract: str
    year: int
    keywords: list[str] = field(default_factory=list)

class PaperRetriever:
    def __init__(self):
        self.papers: list[Paper] = []
    def add(self, paper: Paper): self.papers.append(paper)
    def search(self, query: str, k: int = 3) -> list[Paper]:
        scored = [(p, sum(1 for kw in p.keywords if kw.lower() in query.lower())) for p in self.papers]
        scored.sort(key=lambda x: -x[1])
        return [p for p, _ in scored[:k]]

class AbstractSummarizer:
    def summarize(self, abstract: str, max_sentences: int = 3) -> str:
        sentences = re.split(r'[.!?]+', abstract)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        return ". ".join(sentences[:max_sentences]) + "."

class TrendAnalyzer:
    def analyze(self, papers: list[Paper]) -> dict:
        kw_count = {}
        for p in papers:
            for kw in p.keywords:
                kw_count[kw] = kw_count.get(kw, 0) + 1
        top = sorted(kw_count.items(), key=lambda x: -x[1])[:5]
        years = [p.year for p in papers]
        return {"top_keywords": top, "year_range": f"{min(years)}-{max(years)}" if years else "N/A",
                "total_papers": len(papers)}

def demo():
    print("=== Scientific Literature Analysis ===\n")
    retriever = PaperRetriever()
    retriever.add(Paper("p1", "Transformer", "Attention mechanism for NLP", 2017, ["transformer", "attention", "nlp"]))
    retriever.add(Paper("p2", "GPT-3", "Language models are few-shot learners", 2020, ["gpt", "language model", "few-shot"]))
    retriever.add(Paper("p3", "AlphaFold", "Protein structure prediction", 2021, ["protein", "structure", "deep learning"]))
    summarizer = AbstractSummarizer()
    analyzer = TrendAnalyzer()
    results = retriever.search("transformer model")
    print("  Search results:")
    for p in results:
        print(f"  [{p.id}] {p.title} ({p.year})")
        print(f"    Summary: {summarizer.summarize(p.abstract)}")
    trend = analyzer.analyze(retriever.papers)
    print(f"\n  Trend: top keywords = {trend['top_keywords']}")
    print(f"  Period: {trend['year_range']}")
    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo()
