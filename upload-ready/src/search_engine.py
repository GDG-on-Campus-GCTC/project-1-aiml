# Use absolute imports
from encoders.clip_encoder import ClipEncoder
from storage.vector_store import VectorStore

class SearchEngine:
    def __init__(self):
        self.encoder = ClipEncoder()
        self.store = VectorStore()
    
    def index_image(self, image, metadata):
        """Index an image with metadata"""
        embedding = self.encoder.encode_image(image)
        doc_id = self.store.add(embedding, metadata)
        return doc_id
    
    def search(self, query_text, top_k=5):
        """Search for images using text query"""
        query_embedding = self.encoder.encode_text(query_text)
        results = self.store.search(query_embedding, top_k=top_k)
        
        # Format results with metadata
        formatted_results = []
        for doc_id, score in results:
            result = {
                "doc_id": doc_id,
                "score": float(score),
                "metadata": self.store.metadata[doc_id]
            }
            formatted_results.append(result)
        
        return formatted_results
