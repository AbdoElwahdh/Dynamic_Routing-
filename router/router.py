from .rules import classify_query
from .cache import Cache
from models.models import get_model
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
        model_name = SIMPLE_MODEL
    elif complexity == "medium":
        model_name = MEDIUM_MODEL
    else:  # advanced
        model_name = ADVANCED_MODEL

    # Try to get response with potential fallback
    response, final_model = get_response_with_fallback(
        query, model_name, complexity)

    # Cache the response
    if use_cache and cache.is_enabled():
        cache.set(query, response)

    return {
        "query": query,
        "route": f"{complexity} -> {final_model}",
        "response": response,
        "cached": False
    }


def get_response_with_fallback(query, initial_model_name, initial_complexity, retries=0):
    """
    Get response with fallback logic in case of errors or unsatisfactory responses
    """
    try:
        # Get the model instance
        model = get_model(initial_model_name)
        
        # Call the model to generate response
        response = model.generate(query)

        # Check if response is too short or unclear
        if response and len(response) < 20 and \
           FALLBACK_ENABLED and retries < MAX_RETRIES:
            
            print(f"Response too short from {initial_model_name}, upgrading...")
            
            # Upgrade to a more powerful model
            if initial_complexity == "simple":
                return get_response_with_fallback(
                    query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(
                    query, ADVANCED_MODEL, "advanced", retries + 1)

        return response, initial_model_name

    except Exception as e:
        # If there's an API error, try fallback
        if FALLBACK_ENABLED and retries < MAX_RETRIES:
            print(f"Error with {initial_model_name}: {str(e)}. Trying fallback...")

            if initial_complexity == "simple":
                return get_response_with_fallback(
                    query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(
                    query, ADVANCED_MODEL, "advanced", retries + 1)

        # If all retries fail, raise the exception
        raise Exception(f"All models failed. Last error: {str(e)}")