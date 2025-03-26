.PHONY: ingest view-store setup install help run qa

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup       - Create required directories and setup environment"
	@echo "  make install     - Install required dependencies"
	@echo "  make ingest      - Run the document ingestion process"
	@echo "  make view-store  - View the contents of the vector store"
	@echo "  make qa          - Start the question-answering system (CLI)"
	@echo "  make help        - Show this help message"

# Setup directories and environment
setup:
	mkdir -p data/raw
	mkdir -p data/processed
	[ -f .env ] || cp .env.example .env
	@echo "Setup complete. Don't forget to add your documents to data/raw/"

# Install dependencies
install:
	pip install -r requirements.txt
	pip install rich

# Run document ingestion
ingest:
	@echo "Starting document ingestion..."
	python src/ingest_documents.py

# View vector store
view-store:
	@echo "Viewing vector store contents..."
	python src/dev/view_vector_store.py

# Start QA system
qa:
	@echo "Starting question-answering system..."
	python src/main.py

# Clean up (if needed)
clean:
	rm -rf .chroma
	rm -f data/processed/processed_files.json
	@echo "Cleaned up vector store and processed files tracking" 