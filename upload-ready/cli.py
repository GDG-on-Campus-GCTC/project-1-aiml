#!/usr/bin/env python3
"""
CLI for Multimodal RAG System
"""

import argparse
import os
import sys
from PIL import Image
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import components
try:
    from config.settings import settings
    print("✅ Config loaded")
except Exception as e:
    print(f"❌ Config error: {e}")
    settings = None

try:
    from encoders.clip_encoder import ClipEncoder
    print("✅ CLIP encoder imported")
except Exception as e:
    print(f"❌ CLIP import error: {e}")

try:
    from processors.pdf_processor import PDFProcessor
    print("✅ PDF processor imported")
except Exception as e:
    print(f"❌ PDF processor error: {e}")

try:
    from storage.vector_store import VectorStore
    print("✅ Vector store imported")
except Exception as e:
    print(f"❌ Vector store error: {e}")

try:
    from search_engine import SearchEngine
    print("✅ Search engine imported")
except Exception as e:
    print(f"❌ Search engine error: {e}")

def test_system():
    """Test all system components"""
    print("🧪 Testing system components...")
    
    try:
        encoder = ClipEncoder()
        print("✅ CLIP encoder created")
        
        # Test image encoding
        img = Image.new('RGB', (224, 224), color='red')
        img_emb = encoder.encode_image(img)
        print(f"✅ CLIP encoding works: shape={img_emb.shape}")
        
        # Test text encoding
        text_emb = encoder.encode_text("test query")
        print(f"✅ Text encoding works: shape={text_emb.shape}")
    except Exception as e:
        print(f"❌ Encoding test failed: {e}")
    
    try:
        store = VectorStore()
        
        # Create a test embedding
        test_embedding = np.random.randn(512)  # 1D array of size 512
        
        # Test both add and add_document methods
        doc_id1 = store.add(test_embedding, {"test": "metadata1"})
        print(f"✅ Vector store add works: ID={doc_id1}")
        
        doc_id2 = store.add_document(test_embedding, {"test": "metadata2"})
        print(f"✅ Vector store add_document works: ID={doc_id2}")
        
        results = store.search(test_embedding, top_k=2)
        print(f"✅ Vector store search works: {len(results)} results")
        
        if results:
            for i, (doc_id, score) in enumerate(results):
                print(f"  Result {i+1}: ID={doc_id}, Score={score:.3f}")
    except Exception as e:
        print(f"❌ Vector store test failed: {e}")
    
    print("\n✅ All tests completed!")

def process_command(args):
    """Process PDF file"""
    print(f"Processing: {args.input}")
    
    # Create processor with DPI
    processor = PDFProcessor(dpi=args.dpi)
    pages = processor.extract_pages(args.input)
    
    output_dir = args.output
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extracted {len(pages)} pages")
    
    # Save pages as images
    for i, page in enumerate(pages):
        img_path = os.path.join(output_dir, f"page_{i:03d}.jpg")
        page['image'].save(img_path, "JPEG", quality=95)
        print(f"  Saved: {img_path}")
    
    if args.index:
        print("\nIndexing pages...")
        search_engine = SearchEngine()
        for i, page in enumerate(pages):
            metadata = {
                "source": args.input,
                "page": i,
                "path": os.path.join(output_dir, f"page_{i:03d}.jpg")
            }
            doc_id = search_engine.index_image(page['image'], metadata)
            print(f"  Indexed page {i}: ID={doc_id}")
        
        print(f"✅ Total pages indexed: {len(pages)}")

def search_command(args):
    """Search indexed documents"""
    print(f"🔍 Searching for: '{args.query}'")
    
    try:
        search_engine = SearchEngine()
        results = search_engine.search(args.query, top_k=args.top_k)
        
        print(f"Found {len(results)} results:")
        for i, result in enumerate(results):
            print(f"\n{i+1}. Score: {result['score']:.3f}")
            print(f"   Page: {result['metadata'].get('page', 'N/A')}")
            print(f"   Source: {result['metadata'].get('source', 'N/A')}")
            print(f"   Path: {result['metadata'].get('path', 'N/A')}")
    except Exception as e:
        print(f"❌ Search failed: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Multimodal RAG System for PDF notes",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Test system components")
    test_parser.set_defaults(func=lambda args: test_system())
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process PDF file")
    process_parser.add_argument("input", help="Input PDF file")
    process_parser.add_argument("--output", required=True, help="Output directory for images")
    process_parser.add_argument("--dpi", type=int, default=150, help="Image quality (default: 150)")
    process_parser.add_argument("--index", action="store_true", help="Index after processing")
    process_parser.set_defaults(func=process_command)
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search documents")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of results (default: 5)")
    search_parser.set_defaults(func=search_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == "__main__":
    main()
