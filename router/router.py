from typing import Dict, Tuple, Optional
from rules import classify_query
from cache import Cache
from models.models import GeminiModels
from config import (
    SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL,
    FALLBACK_ENABLED, MAX_RETRIES
)


class QueryRouter:
    """Main class for routing queries to appropriate models"""
    
    def __init__(self):
        """Initialize router with cache and model instances"""
        self.cache = Cache()
        self.gemini = GeminiModels()
        self.model_mapping = self._create_model_mapping()
    
    def _create_model_mapping(self):
        """mapping between complexity levels : model names"""
        return {
            "simple": "G-Flash",
            "medium": "G-Flash-8g",
            "advanced": "G-pro"
        }
    
    def route_query(self, query: str, use_cache: bool = True):
        # 1: Check cache
        cached_result = self._check_cache(query, use_cache)
        if cached_result:
            return cached_result
        
        # 2: Classify query complexity
        complexity = classify_query(query)
        
        # 3: Get model level based on complexity
        model_level = self.model_mapping.get(complexity, "simple") ####################################################################################################################################################################################################################################################################################
        
        # 4: Generate response with fallback
        response, final_model = self._get_response_with_fallback(query, model_level, complexity)
        
        # 5: Cache the response
        self._cache_response(query, response, use_cache)
        
        # 6: Return formatted result
        return {
            "query": query,
            "route": f"{complexity} -> {final_model}",
            "response": response,
            "cached": False
        }
    
    def _check_cache(self, query: str, use_cache: bool) -> Optional[Dict[str, any]]:
        if not use_cache or not self.cache.is_enabled():
            return None
            
        cached_response = self.cache.get(query)
        if cached_response:
            return {
                "query": query,
                "route": "cache",
                "response": cached_response,
                "cached": True
            }
        return None
    
    def _cache_response(self, query: str, response: str, use_cache: bool):
        if use_cache and self.cache.is_enabled():
            self.cache.set(query, response)
    
    def _get_response_with_fallback(self, query: str, model_level: str, complexity: str, retries: int = 0):
        """Generate response with fallback logic"""
        try:
            # Generate response using the model
            response = self.gemini.generate(query, model_level)
            
            # Check if response quality is good
            if self._is_response_valid(response):
                return response, self._get_model_name(model_level)
            
            # Try fallback if response is poor
            if FALLBACK_ENABLED and retries < MAX_RETRIES:
                return self._try_fallback(query, model_level, complexity, retries)
            
            return response, self._get_model_name(model_level)
            
        except Exception as e:
            if FALLBACK_ENABLED and retries < MAX_RETRIES:
                print(f"Error with {model_level} model: {str(e)}. Trying fallback...")
                return self._try_fallback(query, model_level, complexity, retries)
            
            # If all retries fail, raise the exception
            raise Exception(f"All models failed. Last error: {str(e)}")
    
    def _is_response_valid(self, response: str):
        """Check if response meets quality standards"""
        # // todo
        return True
    
    def _try_fallback(self, query: str, current_level: str, complexity: str, retries: int):
        """Try upgrading to a more powerful model"""
        # Define upgrade path
        upgrade_map = {
            "simple": "medium",
            "medium": "advanced"
        }
        
        # Get next level
        next_level = upgrade_map.get(current_level)
        if not next_level:
            raise Exception(f"No fallback available for {current_level} model")
        
        print(f"Upgrading from {current_level} to {next_level} model...")
        
        # Recursive call with upgraded model
        return self._get_response_with_fallback(query, next_level, complexity, retries + 1)
    
    def _get_model_name(self, model_level: str):
        """Get actual model name from level"""
        model_names = {
            "simple": SIMPLE_MODEL,
            "medium": MEDIUM_MODEL,
            "advanced": ADVANCED_MODEL
        }
        return model_names.get(model_level, SIMPLE_MODEL)


if __name__ == "__main__":
    # Simple test
    router = QueryRouter()
    test_query = "What is the capital of France?"
    result = router.route_query(test_query)
    print(result)


# Main function for backward compatibility
def RouteQuery(query: str, use_cache: bool = True) -> Dict[str, any]:
    """
    Route query using global router instance
    
    Args:
        query: User query to process
        use_cache: Whether to use caching
        
    Returns:
        Dictionary with routing results
    """
    return router.route_query(query, use_cache)


# from .rules import classify_query
# from .cache import Cache
# from models.models import from models.models import GeminiModels

# from config import SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL, \
#      FALLBACK_ENABLED, MAX_RETRIES

# cache = Cache()


# def RouteQuery(query, use_cache=True):
#     """
#     Main routing function that:
#     1. Checks cache if enabled
#     2. Classifies the query
#     3. Routes to appropriate model
#     4. Handles fallback if needed
#     """
#     # Check cache first
#     if use_cache and cache.is_enabled():
#         cached_response = cache.get(query)
#         if cached_response:
#             return {
#                 "query": query,
#                 "route": "cache",
#                 "response": cached_response,
#                 "cached": True
#             }

#     # Classify the query
#     complexity = classify_query(query)

#     # Route based on complexity
#     if complexity == "simple":
#         model_name = SIMPLE_MODEL
#     elif complexity == "medium":
#         model_name = MEDIUM_MODEL
#     else:  # advanced
#         model_name = ADVANCED_MODEL

#     # Try to get response with potential fallback
#     response, final_model = get_response_with_fallback(
#         query, model_name, complexity)

#     # Cache the response
#     if use_cache and cache.is_enabled():
#         cache.set(query, response)

#     return {
#         "query": query,
#         "route": f"{complexity} -> {final_model}",
#         "response": response,
#         "cached": False
#     }


# def get_response_with_fallback(query, initial_model_name, initial_complexity, retries=0):
#     """
#     Get response with fallback logic in case of errors or unsatisfactory responses
#     """
#     try:
#         # Get the model instance
#         gemini = GeminiModels()
        
#         # Call the model to generate response
#         response = gemini.generate(query)

#         # Check if response is too short or unclear
#         if response and len(response) < 20 and FALLBACK_ENABLED and retries < MAX_RETRIES:
            
#             print(f"Response too short from {initial_model_name}, upgrading...")
            
#             # Upgrade to a more powerful model
#             if initial_complexity == "simple":
#                 return get_response_with_fallback(
#                     query, MEDIUM_MODEL, "medium", retries + 1)
#             elif initial_complexity == "medium":
#                 return get_response_with_fallback(
#                     query, ADVANCED_MODEL, "advanced", retries + 1)

#         return response, initial_model_name

#     except Exception as e:
#         # If there's an API error, try fallback
#         if FALLBACK_ENABLED and retries < MAX_RETRIES:
#             print(f"Error with {initial_model_name}: {str(e)}. Trying fallback...")

#             if initial_complexity == "simple":
#                 return get_response_with_fallback(
#                     query, MEDIUM_MODEL, "medium", retries + 1)
#             elif initial_complexity == "medium":
#                 return get_response_with_fallback(
#                     query, ADVANCED_MODEL, "advanced", retries + 1)

#         # If all retries fail, raise the exception
#         raise Exception(f"All models failed. Last error: {str(e)}")