# router/router.py
from .rules import classify_query
from .cache import Cache
from models.models import MODEL_MAP # استيراد الـ MODEL_MAP من models.py
from config import SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL, FALLBACK_ENABLED, MAX_RETRIES

cache = Cache()

# تم تغيير اسم الدالة ليكون أوضح
def route_query(query, use_cache=True):
    """
    Main routing function that:
    1. Checks cache if enabled
    2. Classifies the query
    3. Routes to appropriate model
    4. Handles fallback if needed
    """
    # 1. التحقق من الكاش
    if use_cache and cache.enabled:
        cached_response = cache.get(query)
        if cached_response:
            print("--> Response found in cache!")
            return {
                "query": query,
                "route": "cache",
                "response": cached_response,
                "cached": True,
                "model": "N/A (Cached)"
            }

    # 2. تصنيف الاستعلام
    complexity = classify_query(query)

    # 3. اختيار النموذج بناءً على التصنيف
    if complexity == "simple":
        model_name = SIMPLE_MODEL
    elif complexity == "medium":
        model_name = MEDIUM_MODEL
    else:  # advanced
        model_name = ADVANCED_MODEL

    # 4. الحصول على الإجابة مع منطق الـ Fallback
    response, final_model = get_response_with_fallback(query, model_name, complexity)

    # 5. تخزين الإجابة في الكاش (إذا لم تكن خطأ)
    if use_cache and cache.enabled and "API_ERROR" not in response:
        cache.set(query, response)

    return {
        "query": query,
        "route": complexity,
        "response": response,
        "cached": False,
        "model": final_model
    }

def get_response_with_fallback(query, initial_model_name, initial_complexity, retries=0):
    """
    يستدعي النموذج المحدد ويتعامل مع منطق الـ Fallback.
    """
    current_model_name = initial_model_name
    
    try:
        # **هذا هو التعديل الجوهري**: استدعاء الدالة من الـ MODEL_MAP
        model_function = MODEL_MAP[current_model_name]
        
        print(f"--> Routing to: {current_model_name} (Level: {initial_complexity})")
        response = model_function(query)

        # التحقق من الإجابات غير المرضية لتفعيل الـ Fallback
        if ("I don't know" in response or "I'm not sure" in response or "API_ERROR" in response) and FALLBACK_ENABLED and retries < MAX_RETRIES:
            print(f"Unsatisfactory response from {current_model_name}. Attempting fallback...")
            
            # الترقية إلى نموذج أقوى
            if initial_complexity == "simple":
                return get_response_with_fallback(query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(query, ADVANCED_MODEL, "advanced", retries + 1)

        return response, current_model_name

    except Exception as e:
        print(f"An error occurred with {current_model_name}: {e}. Trying fallback...")
        if FALLBACK_ENABLED and retries < MAX_RETRIES:
            if initial_complexity == "simple":
                return get_response_with_fallback(query, MEDIUM_MODEL, "medium", retries + 1)
            elif initial_complexity == "medium":
                return get_response_with_fallback(query, ADVANCED_MODEL, "advanced", retries + 1)
        
        return f"Fallback failed. Last error with {current_model_name}: {e}", current_model_name
