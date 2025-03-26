#!/usr/bin/env python3
"""
Main entry point for the document-based smart assistant.
Provides a simple CLI interface to ask questions about documents.
"""

import sys
from typing import List, Optional

from domain.models.query import Query
from application.qa_service import QAService
from infrastructure.embedding.openai_embedder import OpenAIEmbeddingGenerator
from infrastructure.vector.chroma_store import ChromaVectorStore
from infrastructure.llm.openai_chat import OpenAIChat
from infrastructure.config import EMBEDDING_MODEL, TOP_K_RESULTS


def setup_dependencies() -> QAService:
    """Set up and wire all components needed for the QA system."""
    print("Initializing components...")
    
    # Create infrastructure implementations
    embedder = OpenAIEmbeddingGenerator(model=EMBEDDING_MODEL)
    print(f"✓ Embedding generator initialized (using {EMBEDDING_MODEL})")
    
    vector_store = ChromaVectorStore(collection_name="documents")
    print("✓ Vector store initialized")
    
    llm = OpenAIChat()
    print("✓ Language model initialized")
    
    # Create the application service
    qa_service = QAService(
        llm=llm,
        vector_store=vector_store,
        embedder=embedder
    )
    print("✓ QA service initialized")
    
    return qa_service


def parse_tags(tags_input: str) -> Optional[List[str]]:
    """Parse comma-separated tags input into a list of tags."""
    if not tags_input or tags_input.strip() == "":
        return None
    
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    return tags if tags else None


def main():
    """Main entry point for the CLI application."""
    print("\n🤖 Document Assistant CLI")
    print("=" * 40)
    
    try:
        # Set up all dependencies
        qa_service = setup_dependencies()
        
        print("\nReady to answer questions! Type 'exit' or press Ctrl+C to quit.\n")
        
        while True:
            # Get user question
            question = input("\n❓ Question: ").strip()
            if question.lower() in ["exit", "quit", "q"]:
                print("\nGoodbye! 👋")
                break
            
            if not question:
                print("Please enter a question or type 'exit' to quit.")
                continue
            
            # Get optional tags
            tags_input = input("🏷️  Tags (optional, comma-separated): ").strip()
            tags = parse_tags(tags_input)
            
            # Create query object
            query = Query(
                text=question,
                tags=tags,
                top_k=TOP_K_RESULTS
            )
            
            print("\n🔍 Searching for relevant information...")
            
            try:
                # Get answer from QA service
                answer = qa_service.ask(query)
                
                # Print the answer
                print("\n📝 Answer:")
                print("-" * 40)
                print(answer)
                print("-" * 40)
            except Exception as e:
                print(f"\n❌ Error getting answer: {str(e)}")
    
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 