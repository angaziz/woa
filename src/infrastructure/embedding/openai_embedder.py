from openai import OpenAI
from typing import List
from domain.interfaces.embedding_generator import EmbeddingGenerator
import os

class OpenAIEmbeddingGenerator(EmbeddingGenerator):
    def __init__(self, model: str = "text-embedding-3-small"):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [r.embedding for r in response.data]