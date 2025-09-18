# config.py

# --- Model Names (for Ollama) ---
# These must match the model names you have in Ollama
SIMPLE_MODEL = "tinyllama"
MEDIUM_MODEL = "mistral"
ADVANCED_MODEL = "llama3"

# --- Ollama API URL ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# --- Routing Thresholds & Keywords (No changes ) ---
MAX_SIMPLE_LENGTH = 60
MAX_MEDIUM_LENGTH = 250
COMPLEX_KEYWORDS = [
    "explain", "analyze", "compare", "contrast", "evaluate",
    "synthesize", "critique", "interpret", "discuss", "theorize", "in depth"
]
SIMPLE_KEYWORDS = [
    "what is", "when was", "where is", "who is", "how to", "define", "list"
]

# --- Cache & Fallback Settings (No changes) ---
CACHE_ENABLED = True
FALLBACK_ENABLED = True
MAX_RETRIES = 2
