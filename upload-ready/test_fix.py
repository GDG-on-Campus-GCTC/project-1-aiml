#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Test ClipEncoder
from encoders.clip_encoder import ClipEncoder
from PIL import Image

encoder = ClipEncoder()
img = Image.new('RGB', (224, 224), color='red')
img_emb = encoder.encode_image(img)
print(f"Image embedding shape: {img_emb.shape}")

text_emb = encoder.encode_text("test query")
print(f"Text embedding shape: {text_emb.shape}")

# Test VectorStore
from storage.vector_store import VectorStore
store = VectorStore()
doc_id = store.add(img_emb, {"test": "metadata"})
print(f"Added document ID: {doc_id}")

# Test SearchEngine
from search_engine import SearchEngine
search_engine = SearchEngine()
print("✅ All imports work!")
