import numpy as np

class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.metadata = []
    
    def add(self, embedding, metadata):
        """Add embedding with metadata to store"""
        # Flatten any shape to 1D
        embedding_flat = embedding.flatten()
        self.embeddings.append(embedding_flat)
        self.metadata.append(metadata)
        return len(self.embeddings) - 1
    
    def add_document(self, embedding, metadata):
        """Alias for add method"""
        return self.add(embedding, metadata)
    
    def search(self, query_embedding, top_k=5):
        """Search for similar embeddings"""
        if not self.embeddings:
            return []
        
        # Flatten query embedding
        query_flat = query_embedding.flatten()
        
        similarities = []
        for i, emb in enumerate(self.embeddings):
            # Calculate cosine similarity
            norm_query = np.linalg.norm(query_flat)
            norm_emb = np.linalg.norm(emb)
            
            if norm_query > 0 and norm_emb > 0:
                sim = np.dot(query_flat, emb) / (norm_query * norm_emb)
            else:
                sim = 0.0
                
            similarities.append((i, sim))
        
        # Sort by similarity (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
