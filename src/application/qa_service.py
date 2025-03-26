from typing import List

from domain.interfaces.llm_client import LLMClient
from domain.interfaces.vector_store import VectorStore
from domain.interfaces.embedding_generator import EmbeddingGenerator
from domain.models.query import Query


class QAService:
    """
    Question-answering service that orchestrates the retrieval and answering process.
    Follows the Onion Architecture pattern with all dependencies injected as abstractions.
    """
    
    def __init__(
        self,
        llm: LLMClient,
        vector_store: VectorStore,
        embedder: EmbeddingGenerator
    ):
        """
        Initialize the QA service with its dependencies.
        
        Args:
            llm: Language model client for generating answers
            vector_store: Vector database for storing and retrieving document chunks
            embedder: Embedding generator for converting text to vectors
        """
        self.llm = llm
        self.vector_store = vector_store
        self.embedder = embedder
    
    def ask(self, query: Query) -> str:
        """
        Process a query to generate an answer based on retrieved context.
        
        The flow:
        1. Generate embedding for query text
        2. Search vector store for relevant chunks
        3. Extract content from chunks
        4. Generate answer using LLM
        
        Args:
            query: The Query object containing the question and search parameters
            
        Returns:
            str: The answer to the question
        """
        # Step 1: Generate embedding for the query text
        query_embedding = self.embedder.embed([query.text])[0]
        
        # Step 2: Search for relevant chunks
        search_results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=query.top_k
        )
        
        # Step 3: Extract content from the retrieved chunks
        context_chunks = []
        for result in search_results:
            # The content could be in 'content' field of metadata or directly in result
            content = result.get("content", None)
            if content is None and "metadata" in result:
                content = result["metadata"].get("content", "")
            
            if content:
                context_chunks.append(content)
        
        # If no chunks were found, return a message
        if not context_chunks:
            return "I couldn't find any relevant information to answer your question."
        
        # Step 4: Generate answer using LLM
        answer = self.llm.answer(
            question=query.text,
            context_chunks=context_chunks
        )
        
        # Step 5: Return the answer
        return answer 