from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai

import sys
import os
sys.path.append(os.path.abspath(".."))
import config

# Load environment variables
load_dotenv()


@dataclass
class ModelInfo:
    """Information about a model"""
    name: str
    supports_thinking: bool
    max_tokens: int

class GeminiModels:
    """Manages all Gemini model operations"""
    
    def __init__(self):
        self._validate_api_key()
        self.client = self._create_client()
        self.models = self._setup_models()
    
    def _validate_api_key(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
    
    def _create_client(self):
        return genai.Client(api_key=self.api_key)
    
    def _setup_models(self):
        return {
            "G-Flash": ModelInfo(name=config.SIMPLE_MODEL, supports_thinking=False, max_tokens=2048),
            "G-Flash-8g": ModelInfo(name=config.MEDIUM_MODEL, supports_thinking=False, max_tokens=4096),
            "G-pro": ModelInfo(name=config.ADVANCED_MODEL, supports_thinking=True, max_tokens=8192)
        }
    
    def _get_model_info(self, model_level: str):
        if model_level not in self.models:
            raise ValueError(f"Unknown model level: {model_level}")
        return self.models[model_level]
    
    def _validate_thinking_mode(self, model_info: ModelInfo, use_thinking: bool):
        if use_thinking and not model_info.supports_thinking:
            raise ValueError(f"{model_info.name} does not support thinking mode")
    
    def generate(self, prompt: str, model_level: str = "G-Flash"):
        model_info = self._get_model_info(model_level)
        
        response = self.client.models.generate_content(
            model=model_info.name,
            contents=prompt
        )
        
        return response.text
    
    def generate_with_thinking(self, prompt: str, model_level: str = "G-pro"):
        model_info = self._get_model_info(model_level)
        
        response = self.client.models.generate_content(
            model=model_info.name,
            contents=prompt
        )
        
        return response.text
    
    def list_models(self):
        result = []
        for level, info in self.models.items():
            model_dict = {
                "level": level,
                "name": info.name
            }
            result.append(model_dict)
        return result
    
    def Print_all_available_Gemini_models(self) -> None:
        models = self.client.models.list()
        print("Available Gemini models:")
        for model in models:
            print("-", model.name)


def run_tests():
    gemini = GeminiModels()
    print("=== Running Tests ===")

    # Test Print_all_available_Gemini_models
    # print("\n[0] Testing list_models:")
    # gemini.Print_all_available_Gemini_models()
    
    # Test list_models
    print("\n[1] Testing list_models:")
    models = gemini.list_models()
    for m in models:
        print(f"- {m['level']}: {m['name']}")

    # Test generate
    print("\n[3] Testing generate:")
    prompts = {
        "G-Flash": "Tell me a quick fun fact",
        "G-Flash-8g": "Summarize the importance of data science in 3 sentences",
        "G-pro": "Write a short poem about the future of AI"
    }
    for level, prompt in prompts.items():
        response = gemini.generate(prompt, level)
        print(f"- {level} prompt: {prompt}")
        print(f"  response: {response}")

    # Test generate_with_thinking (advanced only)
    print("\n[4] Testing generate_with_thinking:")
    response = gemini.generate_with_thinking("Explain the difference between supervised and unsupervised learning")
    print(f"- advanced thinking response: {response}")

    print("\n=== Tests Completed ===")



if __name__ == "__main__":
    run_tests()