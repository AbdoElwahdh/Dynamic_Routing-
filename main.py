# main.py
import time
import json # Import the json library
from router.router import route_query
from utils.display import print_results

# Part C: Prepare 10 sample queries of varying complexity
TEST_QUERIES = [
    # 1. Simple factual question
    "what is the capital of France?",
    # 2. Simple list question
    "list three primary colors",
    # 3. Slightly more complex 'how to'
    "how to tie a shoelace?",
    # 4. Medium complexity - requires some description
    "who is Albert Einstein?",
    # 5. Medium complexity - definition
    "define photosynthesis",
    # 6. Advanced - requires comparison
    "compare Python and JavaScript for web development",
    # 7. Advanced - requires analysis and opinion
    "analyze the main themes in the movie Inception",
    # 8. Advanced - requires deep explanation
    "explain the theory of relativity in simple terms",
    # 9. Simple factual question (to test cache)
    "what is the capital of France?",
    # 10. Medium-Advanced - requires historical context
    "what is the significance of the Magna Carta in legal history?",
]

def main():
    """
    Main function to run the dynamic routing system with test queries.
    """
    start_time_total = time.time()
    all_results = [] # List to store results from all queries

    for i, query in enumerate(TEST_QUERIES):
        print(f"\n==================== Query {i+1}/{len(TEST_QUERIES)} ====================")
        print(f'Query: "{query}"')

        start_time_query = time.time()
        result = route_query(query)
        end_time_query = time.time()

        execution_time = end_time_query - start_time_query
        
        # Add execution time to the result dictionary
        result['execution_time'] = round(execution_time, 2)
        
        # Store the complete result
        all_results.append(result)

        print_results(result)

    end_time_total = time.time()
    total_execution_time = end_time_total - start_time_total

    print("\n==================================================")
    print(f"Total execution time for all queries: {total_execution_time:.2f} seconds")
    print("==================================================")

    # --- NEW: Save results to a log file for the evaluator ---
    with open("evaluation_log.json", "w") as f:
        json.dump(all_results, f, indent=4)
    print("\nEvaluation log saved to 'evaluation_log.json'")


if __name__ == "__main__":
    main()
