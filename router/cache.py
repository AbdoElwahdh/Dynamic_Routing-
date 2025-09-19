import time
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from config import config

class Cache:
    
    def __init__(self):
        self.enabled = config.CACHE_ENABLED
        self.cache_dir = os.path.join("data", "cache")
        self.cache_file = os.path.join(self.cache_dir, "query_cache.json")
        self.memory_cache = {}
        self._ensure_cache_dir()
        self._load_from_file()
    
    def _ensure_cache_dir(self) -> None:
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _load_from_file(self) -> None:
        if not self.enabled:
            return
        
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.memory_cache = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache file: {e}")
            self.memory_cache = {}
    
    def _save_to_file(self) -> None:
        if not self.enabled:
            return
        
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory_cache, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Warning: Could not save cache file: {e}")
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def get(self, query: str) -> Optional[Dict[str, Any]]:
        if not self.enabled:
            return None
        
        if query in self.memory_cache:
            entry = self.memory_cache[query]
            return {
                "response": entry["response"],
                "model": entry.get("model", "unknown"),
                "complexity": entry.get("complexity", "unknown"),
                "timestamp": entry.get("timestamp", 0)
            }
        
        return None
    
    def set(
        self, 
        query: str, 
        response: str, 
        model: str = "unknown", 
        complexity: str = "unknown"
    ) -> None:
        if not self.enabled:
            return
        
        self.memory_cache[query] = {
            "query": query,
            "response": response,
            "model": model,
            "complexity": complexity,
            "timestamp": time.time(),
            "date": datetime.now().isoformat(),
            "response_length": len(response)
        }
        
        self._save_to_file()
    
    def clear(self) -> None:
        self.memory_cache = {}
        if self.enabled and os.path.exists(self.cache_file):
            try:
                os.remove(self.cache_file)
            except Exception as e:
                print(f"Warning: Could not delete cache file: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        if not self.memory_cache:
            return {"total_entries": 0}
        
        total_entries = len(self.memory_cache)
        total_size = sum(len(entry["response"]) for entry in self.memory_cache.values())
        
        model_counts = {}
        complexity_counts = {}
        
        for entry in self.memory_cache.values():
            model = entry.get("model", "unknown")
            complexity = entry.get("complexity", "unknown")
            
            model_counts[model] = model_counts.get(model, 0) + 1
            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1
        
        return {
            "total_entries": total_entries,
            "total_size_chars": total_size,
            "by_model": model_counts,
            "by_complexity": complexity_counts,
            "cache_file": self.cache_file
        }
    
    def print_stats(self) -> None:
        stats = self.get_stats()
        print("=== Cache Statistics ===")
        print(f"Total Entries: {stats['total_entries']}")
        print(f"Total Size: {stats['total_size_chars']} characters")
        print(f"Cache File: {stats['cache_file']}")
        
        if stats['total_entries'] > 0:
            print("By Model:")
            for model, count in stats['by_model'].items():
                print(f"  {model}: {count}")
            
            print("By Complexity:")
            for complexity, count in stats['by_complexity'].items():
                print(f"  {complexity}: {count}")