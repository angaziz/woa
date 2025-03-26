#!/usr/bin/env python3
import os
import time
from pathlib import Path

# Import components
from infrastructure.parser.unstructured_parser import UnstructuredParser
from infrastructure.embedding.openai_embedder import OpenAIEmbeddingGenerator
from infrastructure.vector.chroma_store import ChromaVectorStore
from application.ingestion_service import IngestionService

# Import config
import infrastructure.config as config


def main():
    """
    Main function to run the document ingestion process.
    Instantiates all required components and runs the ingestion service.
    """
    print("Starting document ingestion process...")
    print(f"Processing documents from: {config.RAW_DATA_PATH}")
    
    # Ensure the raw data path exists
    if not config.RAW_DATA_PATH.exists():
        print(f"Error: Directory {config.RAW_DATA_PATH} does not exist.")
        print(f"Creating directory {config.RAW_DATA_PATH}...")
        config.RAW_DATA_PATH.mkdir(parents=True, exist_ok=True)
        print(f"Please add documents to {config.RAW_DATA_PATH} and run again.")
        return
    
    # Create component instances
    start_time = time.time()
    print("Initializing components...")
    
    parser = UnstructuredParser()
    print("✓ Document parser initialized")
    
    embedder = OpenAIEmbeddingGenerator(model=config.EMBEDDING_MODEL)
    print(f"✓ Embedding generator initialized (using {config.EMBEDDING_MODEL})")
    
    vector_store = ChromaVectorStore(collection_name="documents")
    print(f"✓ Vector store initialized (using ChromaDB at {config.CHROMA_DB_DIR})")
    
    # Create and run ingestion service
    ingestion_service = IngestionService(
        parser=parser,
        embedder=embedder,
        store=vector_store,
        chunk_size=1000,  # Can be customized or loaded from config
        chunk_overlap=200  # Can be customized or loaded from config
    )
    print("✓ Ingestion service initialized")
    print("Starting document processing...")
    
    # Run the ingestion process
    ingestion_service.run(str(config.RAW_DATA_PATH))
    
    # Print completion message with elapsed time
    elapsed_time = time.time() - start_time
    print(f"\nDocument ingestion completed in {elapsed_time:.2f} seconds")
    print(f"Processed documents have been marked in: {config.PROCESSED_DATA_PATH / 'processed_files.json'}")
    print(f"Embeddings stored in: {config.CHROMA_DB_DIR}")


if __name__ == "__main__":
    main() 