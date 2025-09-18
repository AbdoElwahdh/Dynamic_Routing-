# main.py
from src.routers.router import RouteQuery

def main():
    print("🔹 Dynamic Routing System Demo 🔹")
    print("ُEnter your query (type 'exit' to quit):")

    while True:
        query = input("Query: ").strip()
        if query.lower() == "exit":
            print("👋")
            break

        result = RouteQuery(query)
        print("\n--- Result ---")
        print(f"Query: {result['query']}")
        print(f"Route: {result['route']}")
        print(f"Response: {result['response']}")
        print(f"From Cache: {result['cached']}")
        print("---------------\n")

if __name__ == "__main__":
    main()
