#!/usr/bin/env python3
import os
import sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from search_engine import SearchEngine

def index_existing_images(image_dir, source_name="ec_notes.pdf"):
    """Index already processed images"""
    search_engine = SearchEngine()
    
    # Get all image files
    image_files = sorted([f for f in os.listdir(image_dir) 
                         if f.endswith(('.jpg', '.jpeg', '.png', '.bmp'))])
    
    print(f"Found {len(image_files)} images in {image_dir}")
    
    for i, img_file in enumerate(image_files):
        img_path = os.path.join(image_dir, img_file)
        try:
            img = Image.open(img_path)
            metadata = {
                "source": source_name,
                "page": i,
                "path": img_path,
                "filename": img_file
            }
            doc_id = search_engine.index_image(img, metadata)
            print(f"  Indexed {img_file}: ID={doc_id}")
        except Exception as e:
            print(f"  Failed to index {img_file}: {e}")
    
    print(f"\n✅ Total indexed: {len(image_files)} images")

if __name__ == "__main__":
    index_existing_images("data/ec_notes")
