from abc import ABC, abstractmethod
from typing import List

class LLMClient(ABC):
    @abstractmethod
    def answer(self, question: str, context_chunks: List[str]) -> str:
        pass