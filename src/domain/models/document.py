from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Document:
    id: str
    name: str
    content: str
    path: str
    tags: List[str]

@dataclass
class Chunk:
    document_id: str
    content: str
    chunk_id: str
    metadata: Dict[str, str]