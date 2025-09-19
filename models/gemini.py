# models/gemini.py

import os
from typing import Dict, List
from dataclasses import dataclass
from dotenv import load_dotenv
import google.generativeai as genai
from .base import BaseModel
from config import config

# Load environment variables
load_dotenv()

@dataclass
class ModelInfo:
    name: str
    supports_thinking: bool
    max_tokens: int

class GeminiModels(BaseModel):
    def __init__(self):
        # تم دمج التحقق والتهيئة في خطوة واحدة
        self._validate_and_configure_api_key()
        self.models = self._setup_models()
    
    def _validate_and_configure_api_key(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        # التهيئة الصحيحة لمفتاح الـ API
        genai.configure(api_key=api_key)
    
    def _setup_models(self):
        return {
            "simple": ModelInfo(name=config.SIMPLE_MODEL, supports_thinking=False, max_tokens=2048),
            "medium": ModelInfo(name=config.MEDIUM_MODEL, supports_thinking=False, max_tokens=4096),
            "advanced": ModelInfo(name=config.ADVANCED_MODEL, supports_thinking=True, max_tokens=8192)
        }
    
    def _get_model_info(self, model_level: str):
        if model_level not in self.models:
            raise ValueError(f"Unknown model level: {model_level}")
        return self.models[model_level]
    
    def generate(self, prompt: str, model_level: str):
        model_info = self._get_model_info(model_level)
        
        # إنشاء كائن النموذج بالطريقة الصحيحة
        model = genai.GenerativeModel(model_info.name)
        
        # استدعاء النموذج
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # التعامل مع أي أخطاء قد تحدث من الـ API
            print(f"Error from Gemini API: {e}")
            return f"API_ERROR: Could not get a response from {model_info.name}."
    
    def list_models(self) -> List[Dict[str, str]]:
        result = []
        for level, info in self.models.items():
            model_dict = {
                "level": level,
                "name": info.name
            }
            result.append(model_dict)
        return result
    
    def get_model_name(self, level: str) -> str:
        model_info = self._get_model_info(level)
        return model_info.name

