# Development Guide

This guide provides information for developers who want to contribute to or extend WOA.

## Development Setup

1. **Environment Setup**

   ```bash
   # Clone the repository
   git clone https://github.com/yourusername/woa.git
   cd woa

   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   make install
   ```

2. **Configuration**
   - Copy `.env.example` to `.env`
   - Set required environment variables:
     - `OPENAI_API_KEY`
     - `CHROMA_DB_DIR`
     - Other optional configurations

## Project Structure

```
woa/
├── src/
│   ├── domain/           # Core business logic and interfaces
│   ├── application/      # Use cases and orchestration
│   ├── infrastructure/   # External implementations
│   └── main.py          # Application entry point
├── docs/                # Documentation
├── tests/              # Test files
├── data/               # Data directories
│   ├── raw/           # Original documents
│   └── processed/     # Processed documents
├── Makefile           # Build and utility commands
└── requirements.txt   # Python dependencies
```

## Development Workflow

1. **Adding New Features**

   - Start with domain layer interfaces
   - Implement application layer logic
   - Add infrastructure implementations
   - Update tests
   - Document changes

2. **Testing**

   ```bash
   # Run tests
   make test

   # Run with coverage
   make test-coverage
   ```

3. **Code Style**
   - Follow PEP 8 guidelines
   - Use type hints
   - Document public interfaces
   - Keep functions focused and small

## Extending WOA

### Adding New Document Types

1. Create a new parser in `src/infrastructure/parsers/`
2. Implement the `DocumentParser` interface
3. Update the parser factory

### Adding New LLM Provider

1. Create new implementation in `src/infrastructure/llm/`
2. Implement the `LLMClient` interface
3. Update configuration handling

### Adding New Vector Store

1. Create new implementation in `src/infrastructure/vector_store/`
2. Implement the `VectorStore` interface
3. Update configuration handling

## Common Tasks

### Document Ingestion

```bash
# Ingest documents
make ingest

# View vector store contents
make view-store
```

### Question Answering

```bash
# Start the QA system
make qa
```

### Development Tools

```bash
# Clean build artifacts
make clean

# Update dependencies
make update-deps
```

## Troubleshooting

1. **Vector Store Issues**

   - Check ChromaDB directory permissions
   - Verify document ingestion success
   - Check vector store contents

2. **API Issues**

   - Verify API key configuration
   - Check rate limits
   - Validate API responses

3. **Performance Issues**
   - Monitor memory usage
   - Check chunk sizes
   - Verify embedding dimensions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Best Practices

1. **Code Organization**

   - Keep related code together
   - Use meaningful names
   - Document complex logic

2. **Error Handling**

   - Use domain-specific exceptions
   - Provide clear error messages
   - Handle edge cases

3. **Testing**

   - Write unit tests
   - Include integration tests
   - Maintain test coverage

4. **Documentation**
   - Update README
   - Document new features
   - Include examples
