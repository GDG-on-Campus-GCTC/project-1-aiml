#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from search_engine import SearchEngine

# Create search engine
search_engine = SearchEngine()

# Test search
queries = [
    "electrical circuit",
    "resistor",
    "capacitor",
    "voltage",
    "current",
    "ohm's law",
    "diode",
    "transistor"
]

print("🔍 Testing search queries...")
for query in queries:
    print(f"\nQuery: '{query}'")
    results = search_engine.search(query, top_k=2)
    print(f"  Found {len(results)} results")
    for i, result in enumerate(results):
        print(f"  {i+1}. Score: {result['score']:.3f}, Page: {result['metadata'].get('page', 'N/A')}")
