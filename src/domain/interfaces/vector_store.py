from abc import ABC, abstractmethod
from typing import List, Dict

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, embeddings: List[List[float]], metadatas: List[Dict]):
        pass

    @abstractmethod
    def search(self, query_embedding: List[float], top_k: int = 5) -> List[Dict]:
        pass