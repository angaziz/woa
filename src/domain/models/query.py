from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Query:
    text: str
    tags: Optional[List[str]] = None
    top_k: int = 5