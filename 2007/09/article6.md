# 語意網與 RDF：知識表示

## 概述

語意網（Semantic Web）是資訊網路的願景，旨在讓機器能夠理解和處理網路上的知識。RDF（Resource Description Framework）是語意網的基礎資料模型，用於表示網路資源的資訊。

## RDF 的核心概念

### 三元組模型

```python
"""
語意網與 RDF 概念展示
展示知識表示的基礎
"""

def demo():
    print("=" * 50)
    print("語意網與 RDF 概念展示")
    print("=" * 50)

    print("\n--- RDF 三元組 ---")
    print("""
RDF 使用主語-謂語-受語（Subject-Predicate-Object）三元組：

範例：
  <張三> <住在> <台北>
  <張三> <是> <工程師>
  <台北> <位於> <台灣>

相當於：
  Subject   Predicate   Object
  張三       住在        台北
  張三       是          工程師
  台北       位於        台灣
""")

    print("\n--- RDF 序列化格式 ---")
    formats = """
# Turtle 格式
@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:ZhangSan ex:name "張三" ;
            ex:occupation "工程師" ;
            ex:livesIn ex:Taipei .

ex:Taipei ex:locatedIn ex:Taiwan .

# XML 格式
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
         xmlns:ex="http://example.org/">
  <rdf:Description rdf:about="http://example.org/ZhangSan">
    <ex:name>張三</ex:name>
    <ex:occupation>工程師</ex:occupation>
  </rdf:Description>
</rdf:RDF>
"""
    print(formats)

    print("\n--- 本體與語意網堆疊 ---")
    stack = [
        ("URI/IRI", "資源識別符"),
        ("RDF", "陳述知識的三元組"),
        ("RDFS", "類別和屬性的定義"),
        ("OWL", "本體語言，豐富的語義"),
        ("SPARQL", "RDF 查詢語言"),
        ("RIF", "規則交換格式"),
        ("OWL-S", "Web 服務描述"),
    ]
    for layer, desc in stack:
        print(f"  {layer}: {desc}")

    print("\n--- SPARQL 查詢範例 ---")
    sparql = """
PREFIX ex: <http://example.org/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?person ?city
WHERE {
  ?person ex:livesIn ?city .
  ?city ex:locatedIn ex:Taiwan .
}
"""
    print(sparql)

    print("\n--- 應用場景 ---")
    applications = [
        "連結資料（Linked Data）",
        "知識圖譜",
        "語意搜尋",
        "智慧代理人",
        "科學資料共享",
    ]
    for app in applications:
        print(f"  - {app}")

    print("\n" + "=" * 50)
    print("語意網概念展示完成")

if __name__ == "__main__":
    demo()