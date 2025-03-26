#!/usr/bin/env python3
"""
Vector Store Inspector - A utility to inspect the contents of the Chroma vector database.

This script directly connects to the Chroma DB and displays information about stored vectors.
"""

import os
import sys
from pathlib import Path
from collections import Counter

# Add the src directory to the Python path to import from infrastructure
sys.path.append(str(Path(__file__).parent.parent.parent))

import chromadb
from chromadb.config import Settings

# Import configuration
from src.infrastructure.config import CHROMA_DB_DIR

# Try to import rich for pretty printing, fall back to standard printing if not available
try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    
    console = Console()
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    print("Note: Install 'rich' package for prettier output")


def truncate_text(text, max_length=100):
    """Truncate text to max_length and add ellipsis if needed."""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def format_metadata(metadata):
    """Format metadata for display."""
    if not metadata:
        return "No metadata"
    
    # Format each key-value pair
    formatted = []
    for key, value in metadata.items():
        # Skip content to avoid redundancy
        if key == "content":
            continue
        formatted.append(f"{key}: {value}")
    
    return ", ".join(formatted)


def calculate_statistics(collection):
    """Calculate statistics about the collection."""
    # Get all ids and metadata
    try:
        # Get all items (this could be slow for large collections)
        all_meta = collection.get(
            include=["metadatas"],
            limit=10000  # Set a reasonable limit to avoid memory issues
        )
        
        if not all_meta or not all_meta["metadatas"]:
            return {}
        
        # Extract statistics
        doc_ids = set()
        tags = Counter()
        chunks_per_doc = Counter()
        file_types = Counter()
        
        for metadata in all_meta["metadatas"]:
            if not metadata:
                continue
                
            # Document IDs
            doc_id = metadata.get("document_id", "unknown")
            doc_ids.add(doc_id)
            
            # Count chunks per document
            chunks_per_doc[doc_id] += 1
            
            # Tags
            tag_str = metadata.get("tags", "")
            if tag_str:
                for tag in tag_str.split(","):
                    if tag.strip():
                        tags[tag.strip()] += 1
            
            # File types
            filename = metadata.get("filename", "")
            if filename:
                ext = Path(filename).suffix
                if ext:
                    file_types[ext] += 1
        
        # Calculate statistics
        stats = {
            "total_vectors": len(all_meta["ids"]),
            "unique_documents": len(doc_ids),
            "unique_tags": len(tags),
            "top_tags": dict(tags.most_common(3)),
            "avg_chunks_per_doc": sum(chunks_per_doc.values()) / len(doc_ids) if doc_ids else 0,
            "max_chunks_in_doc": max(chunks_per_doc.values()) if chunks_per_doc else 0,
            "file_types": dict(file_types.most_common()),
        }
        
        return stats
    except Exception as e:
        print(f"Error calculating statistics: {str(e)}")
        return {}


def display_statistics(stats):
    """Display statistics in a formatted table."""
    if not stats:
        return
        
    if HAS_RICH:
        # Create a table for statistics
        table = Table(title="Collection Statistics", box=box.ROUNDED)
        table.add_column("Statistic", style="cyan")
        table.add_column("Value", style="green")
        
        # Add rows for each statistic
        table.add_row("Total Vectors", str(stats.get("total_vectors", 0)))
        table.add_row("Unique Documents", str(stats.get("unique_documents", 0)))
        table.add_row("Unique Tags", str(stats.get("unique_tags", 0)))
        
        # Top tags
        top_tags = stats.get("top_tags", {})
        if top_tags:
            tag_str = ", ".join([f"{tag} ({count})" for tag, count in top_tags.items()])
            table.add_row("Top Tags", tag_str)
        
        # Chunks per document
        table.add_row("Avg. Chunks per Document", f"{stats.get('avg_chunks_per_doc', 0):.2f}")
        table.add_row("Max Chunks in a Document", str(stats.get("max_chunks_in_doc", 0)))
        
        # File types
        file_types = stats.get("file_types", {})
        if file_types:
            file_type_str = ", ".join([f"{ext} ({count})" for ext, count in file_types.items()])
            table.add_row("File Types", file_type_str)
        
        console.print("\n")
        console.print(table)
    else:
        # Plain text output
        print("\nCollection Statistics:")
        print("-" * 80)
        print(f"Total Vectors: {stats.get('total_vectors', 0)}")
        print(f"Unique Documents: {stats.get('unique_documents', 0)}")
        print(f"Unique Tags: {stats.get('unique_tags', 0)}")
        
        # Top tags
        top_tags = stats.get("top_tags", {})
        if top_tags:
            tag_str = ", ".join([f"{tag} ({count})" for tag, count in top_tags.items()])
            print(f"Top Tags: {tag_str}")
        
        # Chunks per document
        print(f"Avg. Chunks per Document: {stats.get('avg_chunks_per_doc', 0):.2f}")
        print(f"Max Chunks in a Document: {stats.get('max_chunks_in_doc', 0)}")
        
        # File types
        file_types = stats.get("file_types", {})
        if file_types:
            file_type_str = ", ".join([f"{ext} ({count})" for ext, count in file_types.items()])
            print(f"File Types: {file_type_str}")
        print("-" * 80)


def main():
    """Connect to Chroma and display vector store contents."""
    try:
        # Print header
        if HAS_RICH:
            console.print("[bold blue]Chroma Vector Store Inspector[/bold blue]")
            console.print(f"DB Path: [green]{CHROMA_DB_DIR}[/green]")
        else:
            print("=== Chroma Vector Store Inspector ===")
            print(f"DB Path: {CHROMA_DB_DIR}")
        
        # Check if the DB directory exists
        if not Path(CHROMA_DB_DIR).exists():
            if HAS_RICH:
                console.print(f"[bold red]Error:[/bold red] Database directory does not exist at {CHROMA_DB_DIR}")
            else:
                print(f"Error: Database directory does not exist at {CHROMA_DB_DIR}")
            return
        
        # Connect to the Chroma client
        client = chromadb.PersistentClient(
            path=CHROMA_DB_DIR,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Get all collections - in Chroma v0.6.0+ this returns collection names not objects
        collection_names = client.list_collections()
        
        if not collection_names:
            if HAS_RICH:
                console.print("[yellow]No collections found in the database.[/yellow]")
            else:
                print("No collections found in the database.")
            return
        
        # Display collections
        if HAS_RICH:
            console.print(f"\nFound [bold]{len(collection_names)}[/bold] collection(s):")
            for i, name in enumerate(collection_names):
                # Get collection to get count
                coll = client.get_collection(name)
                console.print(f"{i+1}. [cyan]{name}[/cyan] (count: {coll.count()})")
        else:
            print(f"\nFound {len(collection_names)} collection(s):")
            for i, name in enumerate(collection_names):
                # Get collection to get count
                coll = client.get_collection(name)
                print(f"{i+1}. {name} (count: {coll.count()})")
        
        # Access the 'documents' collection
        try:
            collection = client.get_collection("documents")
            count = collection.count()
            
            if HAS_RICH:
                console.print(f"\n[bold green]Documents Collection:[/bold green] {count} vectors stored")
            else:
                print(f"\nDocuments Collection: {count} vectors stored")
            
            # If empty, exit
            if count == 0:
                if HAS_RICH:
                    console.print("[yellow]No documents stored in the collection yet.[/yellow]")
                else:
                    print("No documents stored in the collection yet.")
                return
            
            # Display statistics
            stats = calculate_statistics(collection)
            display_statistics(stats)
            
            # Get the first 5 items
            items = collection.peek(limit=5)
            
            if HAS_RICH:
                # Create a table for the results
                table = Table(show_header=True, box=box.ROUNDED)
                table.add_column("ID", style="cyan")
                table.add_column("Metadata", style="green")
                table.add_column("Content Preview", style="yellow")
                
                for i in range(len(items["ids"])):
                    item_id = items["ids"][i]
                    metadata = format_metadata(items["metadatas"][i]) if i < len(items["metadatas"]) else ""
                    content = truncate_text(items["documents"][i]) if i < len(items["documents"]) else ""
                    
                    table.add_row(item_id, metadata, content)
                
                console.print("\n[bold]First 5 document chunks:[/bold]")
                console.print(table)
            else:
                # Plain text output
                print("\nFirst 5 document chunks:")
                print("-" * 80)
                
                for i in range(len(items["ids"])):
                    print(f"ID: {items['ids'][i]}")
                    if i < len(items["metadatas"]):
                        print(f"Metadata: {format_metadata(items['metadatas'][i])}")
                    if i < len(items["documents"]):
                        print(f"Content: {truncate_text(items['documents'][i])}")
                    print("-" * 80)
            
        except ValueError:
            if HAS_RICH:
                console.print("[bold red]Error:[/bold red] 'documents' collection not found.")
            else:
                print("Error: 'documents' collection not found.")
    
    except Exception as e:
        if HAS_RICH:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
        else:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()