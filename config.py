import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model names
SIMPLE_MODEL = "gemini-2.5-flash"
MEDIUM_MODEL = "gemini-1.5-flash-8b"
ADVANCED_MODEL = "gemini-2.5-pro"

# Routing thresholds
MAX_SIMPLE_LENGTH = 50  # Characters
MAX_MEDIUM_LENGTH = 200  # Characters

# Keywords that indicate complexity
COMPLEX_KEYWORDS = [
    "explain", "analyze", "compare", "contrast", "evaluate",
    "synthesize", "critique", "interpret", "discuss", "theorize"
]

SIMPLE_KEYWORDS = [
    "what", "when", "where", "who", "how", "define", "list"
]

# Cache settings
CACHE_ENABLED = True

# Fallback settings
FALLBACK_ENABLED = True
MAX_RETRIES = 2