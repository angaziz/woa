# ✅ Smart Assistant – Task Breakdown

---

## 📍 PHASE 1 – Document Ingestion

### Interfaces (Ports)

- [ ] `EmbeddingGenerator` (e.g. OpenAI)
- [ ] `VectorStore` (e.g. Chroma)
- [ ] `DocumentParser` (e.g. Unstructured)

### Infrastructure Implementations

- [ ] `openai_embedder.py`
- [ ] `chroma_store.py`
- [ ] `unstructured_parser.py`

### Domain Models

- [ ] `Document` – filename, content, metadata
- [ ] `Chunk` – chunked content with metadata
- [ ] `Query` – user input + tags

### Application Logic

- [ ] `IngestionService.run(path)` – full ingest pipeline
  - Recursively scan `.data/raw`
  - Parse → Chunk → Embed → Store
  - Assign tags from folder name (e.g. `data/raw/hr/` → tag: hr)

### Entry Point

- [ ] `ingest_documents.py`
  - Wire parser, embedder, vector store
  - Call `IngestionService.run()`

---

## 📍 PHASE 2 – Chat with LLM

> Not yet started – for later milestone

- [ ] `LLMClient` interface
- [ ] `openai_chat.py` implementation
- [ ] `QAService.ask(query)`:
  - Embed query
  - Retrieve chunks
  - Call LLM
- [ ] Textual UI (`ui/cli/main.py`)
- [ ] `main.py` to wire chat

---

## 🛠️ Dev Extras

- [x] `.gitignore`
- [x] `.env`
- [x] `requirements.txt`
- [ ] `config.py` to load settings

---

## 🧪 Testing (future)

- [ ] Unit tests for services
- [ ] Integration tests for ingestion
- [ ] Mocking ports for isolation

---

📈 Roadmap
• Modular ingestion system
• LLM-powered QnA system (textualize)
• Add Confluence, email, or other doc sources
• Expandable to REST, web UI, other vector DBs or LLMs
