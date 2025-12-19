#!/usr/bin/env python3
"""Debug script to test Ollama backend issues."""

def test_ollama_endpoints():
    """Test different Ollama endpoints to identify the issue."""
    import requests


    # Test 1: Check if /api/generate works
    try:
        response = requests.post("http://localhost:11434/api/generate",
                               json={
                                   "model": "qwen3:0.6b",
                                   "prompt": "Hello! How are you?",
                                   "stream": False,
                                   "options": {
                                       "temperature": 0.7,
                                       "num_predict": 100
                                   }
                               },
                               timeout=10)
        if response.status_code == 200:
            response.json()
        else:
            pass
    except Exception:
        pass

    # Test 2: Check if /api/chat works (we know this works)
    try:
        response = requests.post("http://localhost:11434/api/chat",
                               json={
                                   "model": "qwen3:0.6b",
                                   "messages": [
                                       {"role": "user", "content": "Hello! How are you?"}
                                   ],
                                   "stream": False
                               },
                               timeout=10)
        if response.status_code == 200:
            response.json()
        else:
            pass
    except Exception:
        pass

    # Test 3: Test with default model "llama3"
    try:
        response = requests.post("http://localhost:11434/api/chat",
                               json={
                                   "model": "llama3",
                                   "messages": [
                                       {"role": "user", "content": "Hello!"}
                                   ],
                                   "stream": False
                               },
                               timeout=10)
        if response.status_code == 200:
            response.json()
        else:
            pass
    except Exception:
        pass

def test_adaptivemind_backend():
    """Test the AdaptiveMind backend directly."""
    try:
        from adaptivemind_core.llm.ollama import OllamaBackend

        # Test with default config
        backend = OllamaBackend(
            host="http://127.0.0.1:11434",
            model="llama3",  # Default model
            timeout=30.0
        )


        if backend.is_available():

            # Test generate method
            from adaptivemind_core.llm.base import GenerationRequest

            request = GenerationRequest(
                messages=[{"role": "user", "content": "Hello!"}],
                persona="generalist",
                context="Hello!",
                temperature=0.7,
                max_tokens=100
            )

            backend.generate(request)
        else:
            pass

    except Exception:
        import traceback
        traceback.print_exc()

def main():
    test_ollama_endpoints()
    test_adaptivemind_backend()

if __name__ == "__main__":
    main()
