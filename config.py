# model names:
simple_model = ""
medium_model = ""
advanced_model = ""

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
