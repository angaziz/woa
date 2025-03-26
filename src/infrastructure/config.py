import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from the root project directory
load_dotenv()

# === OpenAI Config ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")

# === Chroma Config ===
CHROMA_DB_DIR = os.getenv("CHROMA_DB_DIR", ".chroma/")

# === Data Paths ===
RAW_DATA_PATH = Path(".data/raw")
PROCESSED_DATA_PATH = Path(".data/processed")

# === Other Configs ===
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))