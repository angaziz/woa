from abc import ABC, abstractmethod
from domain.models.document import Document
from typing import List

class DocumentParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> Document:
        pass