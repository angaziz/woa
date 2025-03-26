# Architecture Overview

WOA is built following Clean Architecture principles, with clear separation of concerns and dependency inversion. This document outlines the architectural decisions and component organization.

## Core Principles

- **Dependency Rule**: Dependencies point inward, with the domain layer at the center
- **Separation of Concerns**: Each layer has a specific responsibility
- **Interface Segregation**: Components communicate through well-defined interfaces
- **Dependency Injection**: Dependencies are injected rather than created internally

## Layer Structure

### 1. Domain Layer (`src/domain/`)

- Contains business logic and core entities
- Defines interfaces for external dependencies
- No dependencies on external frameworks or libraries
- Key components:
  - Models (Document, Chunk, Query)
  - Interfaces (DocumentParser, VectorStore, LLMClient, EmbeddingGenerator)

### 2. Application Layer (`src/application/`)

- Orchestrates the flow of data and domain objects
- Implements use cases
- Depends only on the domain layer
- Key components:
  - IngestionService
  - QAService

### 3. Infrastructure Layer (`src/infrastructure/`)

- Implements interfaces defined in the domain layer
- Handles external concerns (file system, APIs, databases)
- Contains all framework-specific code
- Key components:
  - OpenAI implementations (OpenAIEmbeddingGenerator, OpenAIChat)
  - ChromaVectorStore
  - Document parsers
  - Configuration management

## Component Dependencies

```
Domain Layer
    ↑
Application Layer
    ↑
Infrastructure Layer
```

## Key Design Decisions

1. **Modularity**

   - All major components are interface-based
   - Easy to swap implementations (e.g., different LLM providers)
   - Testing facilitated through interface mocking

2. **Configuration**

   - Environment-based configuration
   - Sensible defaults with override capability
   - Clear separation of configuration from code

3. **Error Handling**

   - Domain-specific exceptions
   - Clear error boundaries between layers
   - Graceful degradation where appropriate

4. **Data Flow**
   - Unidirectional data flow
   - Clear ownership of data at each layer
   - Immutable domain objects where possible

## Future Considerations

- Scalability through modular design
- Potential for distributed processing
- Integration with additional document types
- Enhanced metadata handling
- Performance optimizations

# 🧠 Smart Assistant Architecture

This project is a modular document-based AI assistant built using Python, following **Onion / Clean Architecture** principles. It ingests documents from disk, chunks and embeds them, stores them in a vector database, and uses an LLM to answer user questions based on semantic search results.

---

## 🏗️ Layers Overview

**1. Domain Layer**

- Core models (`Document`, `Chunk`, `Query`, etc.)
- Abstract interfaces (aka ports): `EmbeddingGenerator`, `VectorStore`, `LLMClient`, `DocumentParser`
- No external dependencies

**2. Application Layer**

- Contains business logic and orchestrates use cases
- Example services: `IngestionService`, `QAService`
- Depends on domain interfaces

**3. Infrastructure Layer**

- Implements external integrations:
  - OpenAI for embeddings and LLM
  - Chroma for vector storage
  - Unstructured.io for file parsing
- These classes implement domain interfaces

**4. Interface Layer (UI)**

- Textual CLI interface (for chatting only, in Phase 1)
- Future: REST API or web UI can be added here

---

## 📦 Project Structure

```
src/
├── domain/
│ ├── models/ # Document, Chunk, Query, etc.
│ └── ports/ # EmbeddingGenerator, VectorStore, etc.
│
├── application/
│ ├── ingestion_service.py # Handles file-to-vector flow
│ ├── qa_service.py # Handles question → answer flow
│ └── tagging_service.py
│
├── infrastructure/
│ ├── embedding/ # OpenAI embedder
│ ├── vector/ # Chroma vector store
│ ├── llm/ # OpenAI chat implementation
│ ├── parser/ # Unstructured parser
│ └── config.py # Loads .env and constants
│
├── ui/
│ └── cli/ # Textual-based CLI interface
│
├── main.py # Chat runner
└── ingest_documents.py # Separate entry for ingestion
```

---

## 📂 Data Directories

```
data/
├── raw/ # Drop input files here (recursive scan supported)
├── processed/ # Optional: processed metadata, logs, etc.
```

You can simulate document tags via subdirectories (e.g., `.data/raw/hr/handbook.pdf` → tag: `hr`).

---

## 🔁 Swappable Interfaces (Ports)

Located in `domain/ports/`, these allow you to swap implementations without changing business logic.

| Interface          | Description                                 |
| ------------------ | ------------------------------------------- |
| EmbeddingGenerator | Converts text into embeddings               |
| VectorStore        | Stores and retrieves vectorized chunks      |
| LLMClient          | Generates answers using context chunks      |
| DocumentParser     | Extracts clean text from various file types |

---

## 🚀 Execution Flow

1. `ingest_documents.py`:
   - Parses and chunks documents
   - Embeds and stores them in Chroma
2. `main.py`:
   - Accepts a user question via CLI
   - Embeds query, retrieves top matches
   - Sends to LLM with context and returns the answer

---

## 🔒 Environment

Set secrets in `.env`:

```env
OPENAI_API_KEY=your-key-here
CHROMA_DB_PATH=chroma/
```
