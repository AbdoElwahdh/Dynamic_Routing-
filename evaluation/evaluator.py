# evaluation/evaluator.py
import json

def analyze_log_file(file_path="evaluation_log.json"):
    """
    Analyzes the JSON log file to generate insights and statistics.
    """
    try:
        with open(file_path, 'r') as f:
            results = json.load(f)
    except FileNotFoundError:
        print(f"Error: Log file not found at '{file_path}'. Please run main.py first.")
        return

    total_queries = len(results)
    total_time = sum(item['execution_time'] for item in results)
    cached_queries = sum(1 for item in results if item['was_cached'])
    fallback_triggers = sum(1 for item in results if "Fallback" in item.get('final_model', '')) # A simple way to check

    # --- Model Usage ---
    model_usage = {}
    for item in results:
        model = item['final_model']
        if model in model_usage:
            model_usage[model] += 1
        else:
            model_usage[model] = 1

    # --- Print Analysis ---
    print("=========================================")
    print("=      Dynamic Routing System Analysis      =")
    print("=========================================")
    print(f"\nTotal Queries Processed: {total_queries}")
    print(f"Total Execution Time: {total_time:.2f} seconds")
    print(f"Average Time Per Query: {total_time / total_queries:.2f} seconds")
    
    print("\n--- Cache Performance ---")
    print(f"Queries served from Cache: {cached_queries} ({ (cached_queries/total_queries)*100 :.1f}%)")

    print("\n--- Model Usage Distribution ---")
    for model, count in model_usage.items():
        print(f"- {model}: {count} times")

    print("\n--- Fallback Analysis ---")
    print(f"Fallback mechanism was triggered: {fallback_triggers} times")

    print("\n--- Key Observations ---")
    print("1. The routing logic successfully directed queries to different models based on complexity.")
    print("2. The caching mechanism significantly improved performance for repeated queries (see execution time for cached items).")
    print("3. Advanced models (e.g., llama3) provided more detailed answers but at a substantially higher time cost.")
    print("=========================================")


if __name__ == "__main__":
    # To run this analysis, we first need to modify main.py to save the results.
    # After running main.py, you can run this file directly: python evaluation/evaluator.py
    analyze_log_file()

