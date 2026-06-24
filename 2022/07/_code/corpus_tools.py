#!/usr/bin/env python3
"""Corpus Tools — scrape, clean, tokenize, dedup"""

import re
from collections import Counter

def mock_scrape(url):
    return f"""
<html><head><title>Test Page</title></head><body>
<h1>Hello World</h1>
<p>This is a <b>test</b> page for corpus tools.</p>
<p>Contact: info@example.com</p>
<p>Visit https://example.com for more info.</p>
<script>alert('hi');</script>
<style>.cls{{}}</style>
</body></html>
"""

def strip_html(html):
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html = re.sub(r'<[^>]+>', '', html)
    return html

def clean_text(text):
    text = re.sub(r'https?://\S+', '<URL>', text)
    text = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '<EMAIL>', text)
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s<>,\.!?;:\-]', '', text)
    return text.lower()

def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def dedup(items):
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

def demo():
    print("=== Corpus Tools Demo ===\n")

    print("1. Simulate web scraping")
    html = mock_scrape("https://example.com/test")
    print(f"   Fetched {len(html)} bytes from mock URL\n")

    print("2. Strip HTML tags")
    text = strip_html(html)
    print(f"   Raw text ({len(text)} chars): {text[:120]}...\n")

    print("3. Clean text")
    cleaned = clean_text(text)
    print(f"   Cleaned ({len(cleaned)} chars): {cleaned[:200]}...\n")

    print("4. Tokenize")
    tokens = tokenize(cleaned)
    print(f"   Tokens ({len(tokens)}): {tokens[:20]}...\n")

    print("5. Word frequency")
    freq = Counter(tokens).most_common(10)
    for word, count in freq:
        print(f"   {word}: {count}")

    print("\n6. Deduplicate tokens")
    unique = dedup(tokens)
    print(f"   Unique tokens: {len(unique)} (from {len(tokens)} total)\n")

    texts = [
        "hello world",
        "hello world",
        "foo bar",
        "hello world",
        "baz qux",
    ]
    print(f"7. Dedup example: {dedup(texts)}")

if __name__ == "__main__":
    demo()
