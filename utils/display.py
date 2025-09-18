# utils/display.py

def print_results(result: dict):
    """
    Prints the routing results in a formatted way.
    """
    print("-" * 40)
    print(f"Route Taken:      {result['route']}")
    print(f"Final Model Used: {result['model']}")
    print(f"Was Cached:       {result['cached']}")
    print(f"Execution Time:   {result.get('execution_time', 0):.2f} seconds")
    print(f"Response:\n\"{result['response']}\"")
    print("-" * 40)
