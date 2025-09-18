from .rules import classify_query
from .cache import Cache
from config import SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL, \
     FALLBACK_ENABLED, MAX_RETRIES

cache = Cache()


def RouteQuery(query, use_cache=True):
    """
    Main routing function that:
    1. Checks cache if enabled
    2. Classifies the query
    3. Routes to appropriate model
    4. Handles fallback if needed
    """
    # Check cache first
    if use_cache and cache.is_enabled():
        cached_response = cache.get(query)
        if cached_response:
            return {
                "query": query,
                "route": "cache",
                "response": cached_response,
                "cached": True
            }

    # Classify the query
    complexity = classify_query(query)

    # Route based on complexity
    if complexity == "simple":
        model = SIMPLE_MODEL
    elif complexity == "medium":
        model = MEDIUM_MODEL
    else:  # advanced
        model = ADVANCED_MODEL

    # Try to get response with potential fallback
    response, final_model = get_response_with_fallback(
        query, model, complexity)

    # Cache the response
    if use_cache and cache.is_enabled():
        cache.set(query, response)

    return {
        "query": query,
        "route": f"{complexity} -> {final_model}",
        "response": response,
        "cached": False
    }


def get_response_with_fallback(query, initial_model, initial_complexity, retries=0):
    """
    Get response with fallback logic in case of errors or unsatisfactory
     responses
    """
    try:
        response = None  # call and use model here

        # Simple validation - if response is too short or indicates confusion,
        #  try fallback
        if ("I don't know" in response or "I'm not sure" in response) and \
           FALLBACK_ENABLED and retries < MAX_RETRIES:

            # Upgrade to a more powerful model
            if initial_complexity == "simple":
                return get_response_with_fallback(
                    query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(
                    query, ADVANCED_MODEL, "advanced", retries + 1)

        return response, initial_model

    except Exception as e:
        # If there's an API error, try fallback
        if FALLBACK_ENABLED and retries < MAX_RETRIES:
            print(f"Error with {initial_model}: {str(e)}. Trying fallback...")

            if initial_complexity == "simple":
                return get_response_with_fallback(
                    query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(
                    query, ADVANCED_MODEL, "advanced", retries + 1)

        # If all retries fail or fallback is disabled, raise the exception
        raise
