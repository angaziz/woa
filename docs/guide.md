# Usage Guide

This guide explains how to use WOA to process your documents and get answers to your questions.

## Quick Start

1. **Setup**

   ```bash
   # Clone and install
   git clone https://github.com/yourusername/woa.git
   cd woa
   make setup
   make install

   # Configure environment
   cp .env.example .env
   # Edit .env with your OpenAI API key and other settings
   ```

2. **Organize Your Documents**

   ```
   data/
   └── raw/
       ├── hr/
       │   ├── handbook.pdf
       │   └── policies.docx
       ├── tech/
       │   ├── architecture.md
       │   └── api-docs.pdf
       └── general/
           └── company-info.txt
   ```

3. **Process Documents**

   ```bash
   # Ingest all documents
   make ingest

   # View what's in the vector store
   make view-store
   ```

4. **Ask Questions**
   ```bash
   # Start the Q&A system
   make qa
   ```

## Document Organization

### Folder Structure

- Place your documents in `data/raw/`
- Use subdirectories to organize by category
- Subdirectory names become document tags
- Supported formats: PDF, DOCX, TXT

### Example Structure

```
data/raw/
├── hr/              # Tag: hr
│   ├── handbook.pdf
│   └── policies.docx
├── tech/            # Tag: tech
│   ├── architecture.md
│   └── api-docs.pdf
└── general/         # Tag: general
    └── company-info.txt
```

## Document Processing

### What Happens During Ingestion

1. Documents are scanned recursively from `data/raw/`
2. Each document is:
   - Parsed to extract text
   - Split into chunks
   - Converted to embeddings
   - Stored in the vector database
3. Tags are automatically assigned based on folder names

### Processing Options

- Chunk size: Configure in `.env` (default: 1000 tokens)
- Embedding model: Configure in `.env` (default: text-embedding-3-small)
- Vector store location: Configure in `.env` (default: `data/vector_store/`)

## Question Answering

### Using the Q&A System

1. Start the system: `make qa`
2. Enter your question when prompted
3. Optionally provide tags to filter results
4. Get your answer based on relevant document chunks

### Example Interaction

```
$ make qa
🤖 WOA - Working Assistant
----------------------------
Enter your question (or 'exit' to quit): What are our vacation policies?
Optional tags (comma-separated): hr

Searching for relevant information...
Found 3 relevant chunks.

Answer:
[Generated answer based on handbook.pdf and policies.docx]
```

### Tips for Better Answers

1. Be specific in your questions
2. Use relevant tags to narrow down the search
3. For complex topics, break down into smaller questions
4. Check the source documents if you need more context

## Configuration

### Environment Variables

Key settings in `.env`:

```env
# Required
OPENAI_API_KEY=your-key-here
CHROMA_DB_DIR=data/vector_store/

# Optional (with defaults)
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
TOP_K_RESULTS=3
```

### Customization Options

1. **Chunking**: Adjust `CHUNK_SIZE` in `.env`
2. **Model Selection**: Change `LLM_MODEL` and `EMBEDDING_MODEL`
3. **Search Results**: Modify `TOP_K_RESULTS`
4. **Response Style**: Adjust `LLM_TEMPERATURE`

## Troubleshooting

### Common Issues

1. **No Documents Found**

   - Check `data/raw/` directory exists
   - Verify file permissions
   - Ensure supported file formats

2. **API Errors**

   - Verify OpenAI API key
   - Check rate limits
   - Ensure internet connection

3. **Poor Answer Quality**
   - Try more specific questions
   - Use relevant tags
   - Check document quality
   - Adjust chunk size

### Getting Help

- Check the [Development Guide](development.md)
- Review [Architecture Overview](architecture.md)
- Open an issue on GitHub

## Best Practices

1. **Document Organization**

   - Use clear folder names
   - Keep related documents together
   - Use consistent naming conventions

2. **Question Asking**

   - Be specific and focused
   - Use appropriate tags
   - Break complex questions into parts

3. **Maintenance**
   - Regularly update documents
   - Monitor vector store size
   - Backup important documents
