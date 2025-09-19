## Dynamic Routing System

A clean, unified AI model routing system that automatically selects the appropriate model based on query complexity.

### Features
- Automatic query complexity classification
- Unified response format across all models
- Intelligent caching system
- Fallback mechanism for failed requests
- Clean, maintainable codebase

### Setup

1. **Create Virtual Environment**
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure API Key**
Create `.env` file with:
```
GEMINI_API_KEY=your_api_key_here
```

4. **Run Application**
```bash
python main.py
```

### Usage
- Type queries to get AI responses
- Type `evaluate` to run system evaluation
- Type `exit` to quit

### Project Structure
- `main.py` - Application entry point
- `config.py` - Configuration settings
- `router/` - Query routing logic
- `models/` - AI model implementations
- `evaluation/` - System evaluation tools
- `data/` - Cache and test data