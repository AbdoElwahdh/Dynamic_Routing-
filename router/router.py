# router/router.py
import time
from .rules import classify_query
from .cache import Cache
from models.models import call_ollama_model, SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL
from config import FALLBACK_ENABLED, MAX_RETRIES

cache = Cache()

def route_query(query, use_cache=True):
    """
    Main routing function that now correctly identifies and returns the final model name.
    """
    start_time = time.time()

    # 1. Check cache first
    if use_cache and cache.enabled:
        cached_response = cache.get(query)
        if cached_response:
            # If found in cache, we don't know the original model, which is fine.
            return {
                "query": query,
                "route": "cache",
                "response": cached_response,
                "cached": True,
                "execution_time": 0.0,
                "final_model": "Cached"
            }

    # 2. Classify the query
    complexity = classify_query(query)

    # 3. Determine the initial model to use based on complexity
    # THIS IS THE KEY CHANGE: We now get the *actual* model name (e.g., 'tinyllama')
    if complexity == "simple":
        initial_model_name = SIMPLE_MODEL
    elif complexity == "medium":
        initial_model_name = MEDIUM_MODEL
    else:  # advanced
        initial_model_name = ADVANCED_MODEL

    # 4. Try to get a response, with potential fallback
    response, final_model_used = get_response_with_fallback(query, initial_model_name, complexity)

    # 5. Cache the new response
    if use_cache and cache.enabled and "API_ERROR" not in response:
        cache.set(query, response)

    exec_time = time.time() - start_time

    # 6. Return the CORRECT data
    return {
        "query": query,
        "route": f"{complexity} -> {final_model_used}",
        "response": response,
        "cached": False,
        "execution_time": exec_time,
        "final_model": final_model_used # Now this is the correct name!
    }


def get_response_with_fallback(query, initial_model_name, initial_complexity, retries=0):
    """
    Gets a response from a model and handles fallback logic.
    Returns the response and the name of the model that ultimately provided it.
    """
    current_model_name = initial_model_name
    
    try:
        # Call the model
        response = call_ollama_model(current_model_name, query)

        # Simple validation: if response is empty or indicates an error, try fallback
        if (not response or "i'm not sure" in response.lower()) and FALLBACK_ENABLED and retries < MAX_RETRIES:
            # Fallback logic: upgrade to a more powerful model
            if initial_complexity == "simple":
                return get_response_with_fallback(query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(query, ADVANCED_MODEL, "advanced", retries + 1)
        
        # If successful, return the response and the name of the model that worked
        return response, current_model_name

    except Exception as e:
        error_message = f"API_ERROR: An error occurred with model {current_model_name}: {str(e)}"
        print(error_message) # Keep logging for debugging

        # If there's an error, try fallback
        if FALLBACK_ENABLED and retries < MAX_RETRIES:
            if initial_complexity == "simple":
                return get_response_with_fallback(query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(query, ADVANCED_MODEL, "advanced", retries + 1)

        # If all retries fail, return the error and the last model attempted
        return "I'm not sure", current_model_name