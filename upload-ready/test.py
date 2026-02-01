"""
Test if everything works
"""
print("Testing Multimodal RAG System...")

# Test 1: Import config
try:
    from config.settings import settings
    print("✅ Config loaded")
except Exception as e:
    print(f"❌ Config error: {e}")

# Test 2: Import CLIP encoder
try:
    from src.encoders.clip_encoder import ClipEncoder
    print("✅ CLIP encoder imported")
except Exception as e:
    print(f"❌ CLIP import error: {e}")

# Test 3: Test CLIP encoding
try:
    encoder = ClipEncoder()
    print("✅ CLIP encoder created")
    
    # Test with dummy image
    from PIL import Image
    img = Image.new('RGB', (100, 100), color='red')
    embedding = encoder.encode_image(img)
    print(f"✅ Image encoded: shape={embedding.shape}")
    
    # Test text encoding
    text_emb = encoder.encode_text("test")
    print(f"✅ Text encoded: shape={text_emb.shape}")
    
except Exception as e:
    print(f"❌ Encoding test failed: {e}")

print("\n🎉 Basic tests complete!")
