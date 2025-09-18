import re
from config import MAX_SIMPLE_LENGTH, MAX_MEDIUM_LENGTH, \
    SIMPLE_KEYWORDS, COMPLEX_KEYWORDS


def classify_query(query):
    """
    Classify a query into simple, medium, or advanced based on:
    - Length
    - Keywords
    - Structural complexity
    """
    # Check length first
    query_length = len(query)

    if query_length <= MAX_SIMPLE_LENGTH:
        # Check if it's a simple factual question
        if is_simple_factual(query):
            return "simple"

    if query_length <= MAX_MEDIUM_LENGTH:
        # Check for complexity indicators
        if has_complex_keywords(query):
            return "advanced"
        elif has_simple_keywords(query):
            return "medium"
        else:
            return "medium"  # Default to medium for medium-length queries

    # Long queries are typically complex
    return "advanced"


def is_simple_factual(query):
    """Check if query is a simple factual question"""
    # Simple questions often start with what, when, where, who, how
    simple_pattern = r'^(what|when|where|who|how|is|are|can|do|does)\s+'
    return re.match(simple_pattern, query.lower()) is not None


def has_complex_keywords(query):
    """Check if query contains complex keywords"""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in COMPLEX_KEYWORDS)


def has_simple_keywords(query):
    """Check if query contains simple keywords"""
    query_lower = query.lower()
    return any(keyword in query_lower for keyword in SIMPLE_KEYWORDS)
