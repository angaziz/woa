import chromadb
from chromadb.config import Settings
from typing import List, Dict
from pathlib import Path

from domain.interfaces.vector_store import VectorStore
from infrastructure.config import CHROMA_DB_DIR

class ChromaVectorStore(VectorStore):
    def __init__(self, collection_name: str = "documents"):
        """Initialize ChromaDB client and collection."""
        # Create directory if it doesn't exist
        db_path = Path(CHROMA_DB_DIR)
        db_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize client with persistent storage
        self.client = chromadb.PersistentClient(
            path=str(db_path),
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}  # Using cosine similarity
        )
    
    def add_documents(self, embeddings: List[List[float]], metadatas: List[Dict]):
        """
        Add document embeddings with metadata to the vector store.
        
        Args:
            embeddings: List of document embeddings
            metadatas: List of metadata dicts containing document_id, chunk_id, etc.
        """
        # Generate IDs from metadata (document_id + chunk_id)
        ids = [f"{m.get('document_id', '')}_{m.get('chunk_id', '')}" for m in metadatas]
        
        # Convert documents to strings for storage (required by ChromaDB)
        documents = [m.get('content', '') for m in metadatas]
        
        # Add to collection
        self.collection.upsert(
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        """
        Search for similar documents using query embedding.
        
        Args:
            query_embedding: Embedding of the query text
            top_k: Number of results to return
            
        Returns:
            List of dictionaries containing document metadata and similarity scores
        """
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["metadatas", "documents", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "metadata": results["metadatas"][0][i],
                "content": results["documents"][0][i],
                "score": 1.0 - results["distances"][0][i]  # Convert distance to similarity score
            })
            
        return formatted_results 