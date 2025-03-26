from abc import ABC, abstractmethod
from typing import List

class EmbeddingGenerator(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of texts."""
        pass