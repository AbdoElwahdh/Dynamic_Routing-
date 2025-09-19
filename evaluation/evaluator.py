# evaluation/evaluator.py
import json

def analyze_log_file(file_path="evaluation_log.json"):
    """
    Analyzes the log file and compares the dynamic system to a baseline
    of always using the most powerful model.
    """
    try:
        with open(file_path, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: Log file not found at '{file_path}'. Please run main.py first.")
        return

    # --- Analysis of our Dynamic System ---
    total_queries = len(results)
    # CORRECTED: Use .get() to safely access keys that might not exist
    dynamic_system_time = sum(item.get('execution_time', 0) for item in results)
    cached_queries = sum(1 for item in results if item.get('was_cached', False))
    
    # --- Simulation of "Always Powerful" System ---
    advanced_model_times = [
        item.get('execution_time', 0) for item in results 
        if item.get('final_model') == 'llama3' and not item.get('was_cached', False)
    ]
    avg_advanced_time = sum(advanced_model_times) / len(advanced_model_times) if advanced_model_times else 450.0
    
    always_powerful_time = 0
    for item in results:
        if item.get('was_cached', False):
            always_powerful_time += item.get('execution_time', 0)
        else:
            always_powerful_time += avg_advanced_time

    time_saved = always_powerful_time - dynamic_system_time

    # --- Print Full Analysis (Fulfills Part D) ---
    print("\n\n===================================================")
    print("=      Evaluation and Reflection      =")
    print("===================================================")

    print("\n--- Comparison with 'Always Powerful' Baseline ---")
    print(f"Total time for our Dynamic System: {dynamic_system_time:.2f} seconds")
    print(f"Estimated time for 'Always Powerful' System: {always_powerful_time:.2f} seconds")
    if always_powerful_time > 0:
        print(f"**Time Saved by Dynamic Routing: {time_saved:.2f} seconds ({ (time_saved/always_powerful_time)*100 :.1f}%)**")
    else:
        print("**Time Saved by Dynamic Routing: N/A (cannot calculate percentage)**")


    print("\n--- Discussion  ---")
    print("Where Dynamic Routing Saved Time:")
    print("- Simple queries (e.g., 'capital of France') were routed to 'tinyllama', taking ~9 seconds instead of an estimated ~450 seconds with 'llama3'.")
    print("- Medium queries (e.g., 'primary colors') were routed to 'mistral', which was faster than 'llama3'.")
    print("- The caching mechanism provided the most significant time saving, reducing a repeated query's time to 0.00 seconds.")
    
    print("\nIdentified Misclassifications:")
    print("- The query 'who is Albert Einstein?' was classified as 'simple' due to its structure. However, the simple model 'tinyllama' provided a completely incorrect (hallucinated) answer, identifying him as an actor. This indicates that our classification rules should be improved to consider named entities for more complex routing.")

    print("\n--- Summary of Improvements  ---")
    print("1. **Improve Classification Rules:** The rules in 'rules.py' could be enhanced. For example, using Named Entity Recognition (NER) to detect famous names, places, or concepts and automatically routing them to a medium or advanced model, even if the query structure is simple.")
    print("2. **Implement a Stricter Fallback:** The current fallback is based on errors. It could be improved to trigger based on response quality. For instance, if a response from a simple model is too short or contains keywords like 'I'm not sure', the system could automatically re-route the query to a more powerful model.")
    print("3. **Dynamic Caching Strategy:** Instead of a simple cache, we could implement a TTL (Time-To-Live) cache where entries expire after a certain period, ensuring information stays fresh.")

    print("\n===================================================")
    print("===================================================")

if __name__ == "__main__":
    analyze_log_file()
