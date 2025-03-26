import json
import os
import uuid
from pathlib import Path
from typing import List, Dict, Set

from langchain.text_splitter import RecursiveCharacterTextSplitter

from domain.interfaces.document_parser import DocumentParser
from domain.interfaces.embedding_generator import EmbeddingGenerator
from domain.interfaces.vector_store import VectorStore
from domain.models.document import Chunk
from infrastructure.config import PROCESSED_DATA_PATH


class IngestionService:
    def __init__(
        self,
        parser: DocumentParser,
        embedder: EmbeddingGenerator,
        store: VectorStore,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        self.parser = parser
        self.embedder = embedder
        self.store = store
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.processed_files: Set[str] = set()
        self._load_processed_files()
    
    def run(self, directory_path: str) -> None:
        """
        Process all supported files in the directory and its subdirectories.
        
        Args:
            directory_path: Path to the directory containing documents to process
        """
        directory = Path(directory_path)
        
        # Ensure directory exists
        if not directory.exists() or not directory.is_dir():
            raise ValueError(f"Directory {directory_path} does not exist or is not a directory")
        
        # Walk through all files in the directory and subdirectories
        for file_path in self._get_supported_files(directory):
            # Skip if already processed
            if str(file_path) in self.processed_files:
                print(f"Skipping already processed file: {file_path}")
                continue
            
            try:
                print(f"Processing: {file_path}")
                
                # Parse document
                document = self.parser.parse(str(file_path))
                
                # Chunk document
                texts = self.text_splitter.split_text(document.content)
                
                # Create chunks with metadata
                chunks = []
                chunk_metadatas = []
                
                for i, text in enumerate(texts):
                    chunk_id = str(uuid.uuid4())
                    
                    # Create metadata for the chunk
                    metadata = {
                        "document_id": document.id,
                        "chunk_id": chunk_id,
                        "tags": ",".join(document.tags),  # Currently a single tag from parent dir, but supports multiple tags in future
                        "filename": document.name,
                        "path": document.path,
                        "chunk_index": i,
                        "content": text  # Include the text content in metadata
                    }
                    
                    # Create Chunk object for domain model (not used directly here but useful for other services)
                    chunk = Chunk(
                        document_id=document.id,
                        chunk_id=chunk_id,
                        content=text,
                        metadata=metadata
                    )
                    
                    chunks.append(chunk)
                    chunk_metadatas.append(metadata)
                
                # Generate embeddings for all chunks
                texts_to_embed = [chunk.content for chunk in chunks]
                embeddings = self.embedder.embed(texts_to_embed)
                
                # Store embeddings with metadata
                self.store.add_documents(embeddings, chunk_metadatas)
                
                # Mark file as processed
                self._mark_as_processed(str(file_path))
                print(f"Successfully processed: {file_path}")
                
            except Exception as e:
                print(f"Warning: Failed to process {file_path}: {str(e)}")
    
    def _get_supported_files(self, directory: Path) -> List[Path]:
        """Find all supported files in directory and subdirectories."""
        files = []
        for path in directory.rglob("*"):
            if path.is_file() and self._is_supported_file(path):
                files.append(path)
        return files
    
    def _is_supported_file(self, file_path: Path) -> bool:
        """Check if file is a supported document type."""
        supported_extensions = [".pdf", ".docx", ".txt"]
        return file_path.suffix.lower() in supported_extensions
    
    def _load_processed_files(self) -> None:
        """Load the list of processed files from JSON file."""
        processed_files_path = PROCESSED_DATA_PATH / "processed_files.json"
        
        # Create directory if it doesn't exist
        processed_files_path.parent.mkdir(parents=True, exist_ok=True)
        
        if processed_files_path.exists():
            try:
                with open(processed_files_path, "r") as f:
                    self.processed_files = set(json.load(f))
            except json.JSONDecodeError:
                print(f"Warning: Could not parse {processed_files_path}. Starting with empty list.")
                self.processed_files = set()
        else:
            self.processed_files = set()
    
    def _mark_as_processed(self, file_path: str) -> None:
        """Mark a file as processed by adding it to the list and saving to disk."""
        # Add to in-memory set
        self.processed_files.add(file_path)
        
        # Write to disk
        processed_files_path = PROCESSED_DATA_PATH / "processed_files.json"
        with open(processed_files_path, "w") as f:
            json.dump(list(self.processed_files), f, indent=2) 