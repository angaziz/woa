import uuid
from pathlib import Path
from typing import List

from unstructured.partition.auto import partition

from domain.interfaces.document_parser import DocumentParser
from domain.models.document import Document


class UnstructuredParser(DocumentParser):
    def parse(self, file_path: str) -> Document:
        """
        Parse a document file and extract its content using unstructured library.
        
        Args:
            file_path: Path to the document file (PDF, DOCX, TXT, etc.)
            
        Returns:
            Document: Document object with extracted content and metadata
        """
        # Convert to Path object for easier path manipulation
        path = Path(file_path)
        
        # Generate a unique ID for the document
        doc_id = str(uuid.uuid4())
        
        # Use filename without extension as document name
        name = path.stem
        
        # Extract tags from parent folder path
        tags = self._extract_tags_from_path(path)
        
        # Parse the document
        elements = partition(file_path)
        
        # Extract text content from elements
        content = "\n".join([str(element) for element in elements])
        
        # Create Document object
        document = Document(
            id=doc_id,
            name=name,
            content=content,
            path=str(path),
            tags=tags
        )
        
        return document
    
    def _extract_tags_from_path(self, path: Path) -> List[str]:
        """
        Extract tags from the parent directory structure.
        For example: .data/raw/hr/policy.pdf → tags: ["hr"]
        If the path is deeper, include all parent folders: 
        data/raw/hr/regional/policy.pdf → tags: ["hr", "hr-regional"]
        
        Args:
            path: Path object of the document
            
        Returns:
            List[str]: List of extracted tags
        """
        tags = []
        
        # Skip the first two parts (data/raw)
        parts = list(path.parts)[2:-1]  # exclude filename
        
        # Add each part as a tag
        for i, part in enumerate(parts):
            if i == 0:
                # Add the first level as a standalone tag
                tags.append(part)
            
            # Create composite tags for nested folders
            if i > 0:
                parent_tag = parts[0]
                for j in range(1, i + 1):
                    parent_tag += f"-{parts[j]}"
                tags.append(parent_tag)
        
        return tags 