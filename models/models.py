# models/models.py
import requests
import json
from config import SIMPLE_MODEL, MEDIUM_MODEL, ADVANCED_MODEL, OLLAMA_API_URL

def call_ollama_model(model_name: str, query: str) -> str:
    """
    Calls a model hosted by the local Ollama server.
    """
    try:
        print(f"--> Sending query to local Ollama model: {model_name}...")
        
        # Construct the payload for the Ollama API
        payload = {
            "model": model_name,
            "prompt": query,
            "stream": False  # We want the full response at once
        }
        
        # Send the request to the local server
        response = requests.post(OLLAMA_API_URL, json=payload)
        
        # Check for a successful response
        response.raise_for_status()
        
        # Parse the JSON response and extract the 'response' field
        response_data = response.json()
        
        print(f"--> Received response from {model_name}.")
        return response_data.get("response", "").strip()

    except requests.exceptions.ConnectionError:
        # This error happens if the Ollama server isn't running
        error_message = "OLLAMA_ERROR: Connection failed. Is the Ollama server running?"
        print(error_message)
        return error_message
    except Exception as e:
        # For any other errors
        error_message = f"OLLAMA_ERROR: An unexpected error occurred with model {model_name}: {e}"
        print(error_message)
        return error_message

# The Model Map now points to our Ollama calling function
MODEL_MAP = {
    SIMPLE_MODEL: lambda q: call_ollama_model(SIMPLE_MODEL, q),
    MEDIUM_MODEL: lambda q: call_ollama_model(MEDIUM_MODEL, q),
    ADVANCED_MODEL: lambda q: call_ollama_model(ADVANCED_MODEL, q),
}
