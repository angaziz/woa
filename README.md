# 🤖 WOA (Working Assistant)

A personal document assistant that helps you find information in your local documents. Built with Clean Architecture principles, WOA provides a modular system for document processing and question answering. Originally developed for personal use, this tool is now available for anyone to leverage and customize.

## 📋 Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Local storage for document processing and vector database
- Basic understanding of document organization and folder structures

## ✨ Features

- 📚 **Document Processing**: Handles PDF, DOCX, and TXT files processing from local folders
- 🏷️ **Folder-Based Tagging**: Tags documents based on their folder structure
- 🔍 **Semantic Search**: Retrieves relevant document chunks using embeddings
- 💡 **Question Answering**: Provides answers based on document context using GPT-4
- 🔄 **Modular Components**: Interchangeable LLM, Vector Store, and Parser implementations
- 🏗️ **Clean Architecture**: Structured for maintainability and testability

## 🚀 Getting Started

See our comprehensive [Usage Guide](docs/guide.md) for detailed instructions on:

- Setting up your environment
- Organizing your documents
- Processing documents
- Asking questions
- Configuration options
- Troubleshooting

## 🛠️ Tech Stack

- Python 3.x
- LangChain
- ChromaDB
- OpenAI (embeddings & LLM)
- Unstructured.io

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
